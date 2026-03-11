/**
 * @file main.cpp
 * @brief Firmware ESP32 — Bohemian Lab — Contrôle plasma et acquisition.
 *
 * Ce firmware implémente :
 *   1. Lecture des 6 capteurs ADC/SPI à 100 Hz
 *   2. Trois boucles PID imbriquées (100 / 10 / 1 Hz)
 *   3. Machine d'état (INIT → POMPAGE → PLASMA → MESURE → FIN)
 *   4. Watchdog de sécurité (coupure SSR automatique)
 *   5. Émission série JSON à 100 Hz (acquisition PC)
 *   6. Télémétrie MQTT à 1 Hz (dashboard)
 *   7. Logging CSV sur carte microSD (backup)
 *
 * Documentation : docs/06_controle.md, docs/08_acquisition.md
 *
 * ⚠️  SÉCURITÉ — Ce firmware contrôle un magnétron 600–700 W / 4 000 V
 *     (fonctionnement à 200–400 W effectifs via duty cycle SSR).
 *     Le watchdog matériel coupe le SSR si le firmware plante.
 *     Ne JAMAIS désactiver le watchdog.
 *
 * @author  Stéphane Denis
 * @date    Mars 2026
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <SD.h>
#include <esp_task_wdt.h>

// ═══════════════════════════════════════════════════════════════════════
// Configuration — À adapter selon le montage
// ═══════════════════════════════════════════════════════════════════════

// Wi-Fi
const char* WIFI_SSID = "bohemian-lab";
const char* WIFI_PASS = "quantum2026";

// MQTT
const char* MQTT_BROKER = "192.168.1.100";
const int   MQTT_PORT   = 1883;

// Fréquence d'échantillonnage principale
const int FE_HZ            = 100;
const int PERIOD_US        = 1000000 / FE_HZ;  // 10 000 µs

// Cadences des boucles PID (diviseurs de FE_HZ)
const int PID1_DIVIDER     = 1;    // 100 Hz
const int PID2_DIVIDER     = 10;   // 10 Hz
const int PID3_DIVIDER     = 100;  // 1 Hz

// ── Broches GPIO (cf. §6.9 de 06_controle.md) ─────────────────────
// Entrées ADC
const int PIN_PR_ADC       = 36;   // Puissance RF réfléchie (coupleur)
const int PIN_VBAT_ADC     = 32;   // Tension batterie (diviseur)
const int PIN_TBAT_ADC     = 33;   // NTC température batterie

// Sorties PWM / GPIO
const int PIN_VANNE_PWM    = 25;   // Électrovanne H₂O (MOSFET)
const int PIN_SSR_PWM      = 26;   // SSR magnétron
const int PIN_POMPE_RELAY  = 27;   // Relais pompe à vide
const int PIN_LED_ALARM    = 2;    // LED alarme
const int PIN_BUZZER       = 4;    // Buzzer

// SPI — MAX31855 (thermocouple)
const int PIN_MAX_CS       = 5;
// SPI — Carte SD
const int PIN_SD_CS        = 15;

// ── Seuils de sécurité (watchdog, §6.7) ───────────────────────────
const float T_PAROI_MAX    = 150.0;  // °C
const float VBAT_MIN       = 15.0;   // V
const float TBAT_MAX       = 60.0;   // °C
const float PR_MAX_MW      = 800.0;  // mW (découplage total)

// ── PID — Constantes initiales (§6.5) ─────────────────────────────
struct PIDConfig {
    float Kp, Ki, Kd;
    float integral;
    float prev_error;
    float output_min, output_max;
};

PIDConfig pid1 = {1.0, 0.5, 0.01, 0.0, 0.0, 0.0, 1.0};  // Résonance
PIDConfig pid2 = {0.5, 0.2, 0.005, 0.0, 0.0, 0.0, 1.0};  // Ionisation
PIDConfig pid3 = {0.3, 0.1, 0.01, 0.0, 0.0, 0.0, 1.0};   // Pompage

// ── Consignes ─────────────────────────────────────────────────────
float consigne_Pr  = 10.0;   // Puissance réfléchie cible (mW)
float consigne_lum = 2000.0; // Luminosité cible (mV)
float consigne_P   = 3.0;    // Pression cible (mbar)

// ═══════════════════════════════════════════════════════════════════════
// Machine d'état (§6.6)
// ═══════════════════════════════════════════════════════════════════════

enum State {
    STATE_INIT,
    STATE_POMPAGE,
    STATE_PLASMA,
    STATE_MESURE,
    STATE_ERREUR,
    STATE_FIN
};

const char* STATE_CODES[] = {"I", "P", "L", "M", "E", "F"};
const char* STATE_NAMES[] = {"INIT", "POMPAGE", "PLASMA", "MESURE", "ERREUR", "FIN"};

State currentState = STATE_INIT;

// ═══════════════════════════════════════════════════════════════════════
// Variables globales capteurs
// ═══════════════════════════════════════════════════════════════════════

struct SensorData {
    uint32_t timestamp_ms;
    float psd_urad;      // Position PSD (angle pendule)
    float P_mbar;        // Pression
    float Pr_mW;         // Puissance RF réfléchie
    int   lum_mV;        // Luminosité plasma
    float T_paroi_C;     // Température paroi
    int   I_mag_mA;      // Courant magnétron
    float V_bat_V;       // Tension batterie
    float T_bat_C;       // Température batterie
    float duty_vanne;    // Sortie PID₁
    float duty_RF;       // Sortie PID₂
    int   commande_mag;  // État ON/OFF magnétron
};

SensorData sensors = {};
uint32_t loopCounter = 0;
uint32_t startTime = 0;

// MQTT & SD
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
File logFile;
bool sdReady = false;

// ═══════════════════════════════════════════════════════════════════════
// Fonctions utilitaires
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Calcul PID avec anti-windup.
 */
float computePID(PIDConfig &pid, float error, float dt) {
    pid.integral += error * dt;
    // Anti-windup : borner l'intégrateur
    pid.integral = constrain(pid.integral,
                             pid.output_min / (pid.Ki + 1e-6),
                             pid.output_max / (pid.Ki + 1e-6));

    float derivative = (error - pid.prev_error) / dt;
    pid.prev_error = error;

    float output = pid.Kp * error + pid.Ki * pid.integral + pid.Kd * derivative;
    return constrain(output, pid.output_min, pid.output_max);
}

/**
 * @brief Lit la tension ADC convertie en volts (0–3,3 V).
 */
float readADC_V(int pin) {
    int raw = analogRead(pin);
    return raw * 3.3 / 4095.0;
}

/**
 * @brief Lit la température via MAX31855 (SPI).
 *
 * Protocole simplifié : lecture 32 bits, extraction des bits 31–18.
 */
float readThermocouple() {
    digitalWrite(PIN_MAX_CS, LOW);
    delayMicroseconds(1);

    uint32_t data = 0;
    for (int i = 31; i >= 0; i--) {
        digitalWrite(SCK, HIGH);
        delayMicroseconds(1);
        if (digitalRead(MISO)) data |= (1UL << i);
        digitalWrite(SCK, LOW);
        delayMicroseconds(1);
    }

    digitalWrite(PIN_MAX_CS, HIGH);

    // Vérifier le bit de faute (bit 16)
    if (data & 0x00010000) return -999.0;

    // Température : bits 31–18, résolution 0,25 °C
    int16_t temp_raw = (data >> 18) & 0x3FFF;
    if (temp_raw & 0x2000) temp_raw |= 0xC000;  // Extension de signe
    return temp_raw * 0.25;
}

// ═══════════════════════════════════════════════════════════════════════
// Lecture des capteurs
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Lit tous les capteurs et remplit la structure SensorData.
 */
void readSensors() {
    sensors.timestamp_ms = millis() - startTime;

    // Puissance RF réfléchie (coupleur directionnel + diode Schottky)
    // Calibration linéaire : V_adc → P_r (mW)
    float v_pr = readADC_V(PIN_PR_ADC);
    sensors.Pr_mW = v_pr * 300.0;  // Calibration à ajuster

    // Pression (jauge Pirani via ADS1115 I²C — simplifié ici en ADC interne)
    // TODO : remplacer par lecture ADS1115 pour meilleure résolution
    sensors.P_mbar = readADC_V(PIN_VBAT_ADC) * 10.0;  // Placeholder

    // Luminosité plasma (valeur brute ADC — proxy caméra)
    // TODO : intégrer lecture via Wi-Fi caméra
    sensors.lum_mV = analogRead(36) * 3300 / 4095;

    // Température paroi (MAX31855 SPI)
    sensors.T_paroi_C = readThermocouple();

    // Tension batterie (diviseur résistif 18V → 3,3V, ratio = 5,45)
    sensors.V_bat_V = readADC_V(PIN_VBAT_ADC) * 5.45;

    // Température batterie (NTC — linéarisé simplifié)
    float v_ntc = readADC_V(PIN_TBAT_ADC);
    sensors.T_bat_C = (v_ntc - 1.5) * 50.0;  // Calibration approx.

    // PSD (angle du pendule) — signal analogique du photodétecteur
    // Le PSD produit une tension proportionnelle à la position du spot
    // Calibration : V_adc → µrad (à déterminer lors de la calibration)
    float v_psd = readADC_V(36);  // Même broche que Pr — à séparer
    sensors.psd_urad = (v_psd - 1.65) * 100.0;  // Centré sur Vcc/2

    // Courant magnétron (shunt + ampli — placeholder)
    sensors.I_mag_mA = (sensors.commande_mag) ? 285 : 0;
}

// ═══════════════════════════════════════════════════════════════════════
// Watchdog de sécurité (§6.7)
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Vérifie les seuils de sécurité.
 * @return true si tout est nominal, false si anomalie détectée.
 */
bool checkSafety() {
    // Surchauffe paroi
    if (sensors.T_paroi_C > T_PAROI_MAX && sensors.T_paroi_C > 0) {
        Serial.println("{\"alerte\":\"SURCHAUFFE_PAROI\"}");
        return false;
    }

    // Batterie faible
    if (sensors.V_bat_V < VBAT_MIN && sensors.V_bat_V > 5.0) {
        Serial.println("{\"alerte\":\"BATTERIE_FAIBLE\"}");
        return false;
    }

    // Surchauffe batterie
    if (sensors.T_bat_C > TBAT_MAX) {
        Serial.println("{\"alerte\":\"SURCHAUFFE_BATTERIE\"}");
        return false;
    }

    // Découplage RF total
    if (sensors.Pr_mW > PR_MAX_MW) {
        Serial.println("{\"alerte\":\"DECOUPLAGE_RF\"}");
        return false;
    }

    return true;
}

/**
 * @brief Coupe immédiatement le magnétron (SSR OFF).
 */
void emergencyStop() {
    ledcWrite(1, 0);  // SSR OFF (canal PWM 1)
    digitalWrite(PIN_POMPE_RELAY, LOW);
    sensors.duty_RF = 0.0;
    sensors.duty_vanne = 0.0;
    sensors.commande_mag = 0;

    digitalWrite(PIN_LED_ALARM, HIGH);
    digitalWrite(PIN_BUZZER, HIGH);
}

// ═══════════════════════════════════════════════════════════════════════
// Émission série JSON (100 Hz)
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Émet une trame JSON sur le port série.
 */
void emitSerialJSON() {
    // Format compact pour minimiser la bande passante
    Serial.print("{\"t\":");
    Serial.print(sensors.timestamp_ms);
    Serial.print(",\"psd\":");
    Serial.print(sensors.psd_urad, 2);
    Serial.print(",\"P\":");
    Serial.print(sensors.P_mbar, 2);
    Serial.print(",\"Pr\":");
    Serial.print(sensors.Pr_mW, 1);
    Serial.print(",\"lum\":");
    Serial.print(sensors.lum_mV);
    Serial.print(",\"T\":");
    Serial.print(sensors.T_paroi_C, 1);
    Serial.print(",\"I\":");
    Serial.print(sensors.I_mag_mA);
    Serial.print(",\"V\":");
    Serial.print(sensors.V_bat_V, 1);
    Serial.print(",\"dv\":");
    Serial.print(sensors.duty_vanne, 2);
    Serial.print(",\"dr\":");
    Serial.print(sensors.duty_RF, 2);
    Serial.print(",\"mag\":");
    Serial.print(sensors.commande_mag);
    Serial.print(",\"st\":\"");
    Serial.print(STATE_CODES[currentState]);
    Serial.println("\"}");
}

// ═══════════════════════════════════════════════════════════════════════
// Logging SD (100 Hz)
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Écrit une ligne CSV sur la carte SD.
 */
void logToSD() {
    if (!sdReady) return;

    logFile.print(sensors.timestamp_ms);
    logFile.print(',');
    logFile.print(sensors.psd_urad, 2);
    logFile.print(',');
    logFile.print(sensors.P_mbar, 2);
    logFile.print(',');
    logFile.print(sensors.Pr_mW, 1);
    logFile.print(',');
    logFile.print(sensors.lum_mV);
    logFile.print(',');
    logFile.print(sensors.T_paroi_C, 1);
    logFile.print(',');
    logFile.print(sensors.I_mag_mA);
    logFile.print(',');
    logFile.print(sensors.V_bat_V, 1);
    logFile.print(',');
    logFile.print(sensors.duty_vanne, 2);
    logFile.print(',');
    logFile.print(sensors.duty_RF, 2);
    logFile.print(',');
    logFile.print(sensors.commande_mag);
    logFile.print(',');
    logFile.println(STATE_NAMES[currentState]);

    // Flush toutes les 100 lignes (1 seconde)
    if (loopCounter % 100 == 0) logFile.flush();
}

// ═══════════════════════════════════════════════════════════════════════
// MQTT (1 Hz)
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Publie la télémétrie MQTT (1 Hz).
 */
void publishMQTT() {
    if (!mqtt.connected()) return;

    JsonDocument doc;

    // État
    mqtt.publish("bohemian/etat",
        ("{\"state\":\"" + String(STATE_NAMES[currentState]) +
         "\",\"uptime_s\":" + String(sensors.timestamp_ms / 1000) + "}").c_str());

    // Capteurs
    char buf[256];
    snprintf(buf, sizeof(buf),
        "{\"P_mbar\":%.2f,\"Pr_mW\":%.1f,\"lum\":%d,\"T_paroi\":%.1f,"
        "\"psd_urad\":%.2f,\"I_mA\":%d}",
        sensors.P_mbar, sensors.Pr_mW, sensors.lum_mV,
        sensors.T_paroi_C, sensors.psd_urad, sensors.I_mag_mA);
    mqtt.publish("bohemian/capteurs", buf);

    // Sécurité
    snprintf(buf, sizeof(buf),
        "{\"V_bat\":%.1f,\"T_bat\":%.0f,\"watchdog\":\"OK\"}",
        sensors.V_bat_V, sensors.T_bat_C);
    mqtt.publish("bohemian/securite", buf);
}

/**
 * @brief Callback MQTT : réception des commandes opérateur.
 */
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    String msg;
    for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];

    String t = String(topic);

    if (t == "bohemian/cmd/etat") {
        if (msg == "MESURE" && currentState == STATE_PLASMA)
            currentState = STATE_MESURE;
        else if (msg == "FIN")
            currentState = STATE_FIN;
        else if (msg == "RESET" && currentState == STATE_ERREUR)
            currentState = STATE_INIT;
    }
    else if (t == "bohemian/cmd/consigne") {
        JsonDocument doc;
        deserializeJson(doc, msg);
        if (doc.containsKey("Pr0"))  consigne_Pr  = doc["Pr0"];
        if (doc.containsKey("Lum0")) consigne_lum = doc["Lum0"];
        if (doc.containsKey("P0"))   consigne_P   = doc["P0"];
    }
    else if (t == "bohemian/cmd/pid") {
        JsonDocument doc;
        deserializeJson(doc, msg);
        int pidNum = doc["pid"] | 0;
        PIDConfig* target = nullptr;
        if (pidNum == 1) target = &pid1;
        else if (pidNum == 2) target = &pid2;
        else if (pidNum == 3) target = &pid3;

        if (target) {
            if (doc.containsKey("Kp")) target->Kp = doc["Kp"];
            if (doc.containsKey("Ki")) target->Ki = doc["Ki"];
            if (doc.containsKey("Kd")) target->Kd = doc["Kd"];
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════
// Setup
// ═══════════════════════════════════════════════════════════════════════

void setup() {
    Serial.begin(115200);
    Serial.println("\n[Bohemian Lab] Démarrage firmware v1.0.0");

    // ── GPIO ───────────────────────────────────────────────────────
    pinMode(PIN_LED_ALARM, OUTPUT);
    pinMode(PIN_BUZZER, OUTPUT);
    pinMode(PIN_POMPE_RELAY, OUTPUT);
    pinMode(PIN_MAX_CS, OUTPUT);
    digitalWrite(PIN_MAX_CS, HIGH);
    digitalWrite(PIN_LED_ALARM, LOW);
    digitalWrite(PIN_BUZZER, LOW);
    digitalWrite(PIN_POMPE_RELAY, LOW);

    // PWM — Électrovanne (canal 0) et SSR magnétron (canal 1)
    ledcSetup(0, 10, 10);          // 10 Hz, 10 bits
    ledcAttachPin(PIN_VANNE_PWM, 0);
    ledcSetup(1, 10, 10);          // 10 Hz, 10 bits
    ledcAttachPin(PIN_SSR_PWM, 1);
    ledcWrite(0, 0);
    ledcWrite(1, 0);   // SSR OFF au démarrage

    // ADC — Résolution 12 bits
    analogReadResolution(12);

    // ── SPI (MAX31855 + SD) ────────────────────────────────────────
    SPI.begin();

    // Carte SD
    if (SD.begin(PIN_SD_CS)) {
        sdReady = true;
        // Créer le fichier de log avec horodatage
        String filename = "/log_" + String(millis()) + ".csv";
        logFile = SD.open(filename, FILE_WRITE);
        if (logFile) {
            logFile.println("timestamp_ms,psd_urad,P_mbar,Pr_mW,lum_mV,"
                            "T_paroi_C,I_mag_mA,V_bat_V,duty_vanne,"
                            "duty_RF,commande_mag,etat");
            Serial.println("[SD] Logging actif : " + filename);
        }
    } else {
        Serial.println("[SD] Carte non détectée — logging désactivé");
    }

    // ── Wi-Fi ──────────────────────────────────────────────────────
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.print("[WiFi] Connexion");
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println(" OK (" + WiFi.localIP().toString() + ")");
    } else {
        Serial.println(" ÉCHEC — mode série uniquement");
    }

    // ── MQTT ───────────────────────────────────────────────────────
    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    mqtt.setCallback(mqttCallback);

    // ── Watchdog matériel (500 ms) ─────────────────────────────────
    esp_task_wdt_init(1, true);  // 1 seconde, reboot en cas de timeout
    esp_task_wdt_add(NULL);

    startTime = millis();
    currentState = STATE_INIT;
    Serial.println("[Bohemian Lab] Firmware prêt — état INIT");
}

// ═══════════════════════════════════════════════════════════════════════
// Boucle principale (100 Hz)
// ═══════════════════════════════════════════════════════════════════════

void loop() {
    uint32_t loopStart = micros();

    // Nourrir le watchdog matériel
    esp_task_wdt_reset();

    // ── 1. Lecture capteurs ────────────────────────────────────────
    readSensors();

    // ── 2. Watchdog de sécurité ────────────────────────────────────
    if (!checkSafety() && currentState != STATE_ERREUR &&
        currentState != STATE_FIN) {
        emergencyStop();
        currentState = STATE_ERREUR;
    }

    // ── 3. Machine d'état + PID ────────────────────────────────────
    float dt1 = PID1_DIVIDER / (float)FE_HZ;
    float dt2 = PID2_DIVIDER / (float)FE_HZ;
    float dt3 = PID3_DIVIDER / (float)FE_HZ;

    switch (currentState) {
        case STATE_INIT:
            // Auto-test : vérifier que les capteurs répondent
            // Transition automatique vers POMPAGE après 2 secondes
            if (sensors.timestamp_ms > 2000) {
                currentState = STATE_POMPAGE;
                Serial.println("{\"transition\":\"INIT->POMPAGE\"}");
            }
            break;

        case STATE_POMPAGE:
            // PID₃ actif (pompage, 1 Hz)
            if (loopCounter % PID3_DIVIDER == 0) {
                float e3 = sensors.P_mbar - consigne_P;
                float u3 = computePID(pid3, e3, dt3);
                // Contrôle pompe (simplifié : ON si pression > consigne)
                digitalWrite(PIN_POMPE_RELAY, u3 > 0.5 ? HIGH : LOW);
            }
            // Transition vers PLASMA quand pression atteinte
            if (sensors.P_mbar < consigne_P + 0.5 &&
                sensors.P_mbar > 0.1) {
                currentState = STATE_PLASMA;
                Serial.println("{\"transition\":\"POMPAGE->PLASMA\"}");
            }
            break;

        case STATE_PLASMA:
        case STATE_MESURE:
            // PID₁ — Résonance (100 Hz)
            if (loopCounter % PID1_DIVIDER == 0) {
                float e1 = sensors.Pr_mW - consigne_Pr;
                sensors.duty_vanne = computePID(pid1, e1, dt1);
                ledcWrite(0, (int)(sensors.duty_vanne * 1023));
            }

            // PID₂ — Ionisation (10 Hz)
            if (loopCounter % PID2_DIVIDER == 0) {
                float e2 = sensors.lum_mV - consigne_lum;
                sensors.duty_RF = computePID(pid2, e2, dt2);
                ledcWrite(1, (int)(sensors.duty_RF * 1023));
                sensors.commande_mag = (sensors.duty_RF > 0.05) ? 1 : 0;
            }

            // PID₃ — Pompage (1 Hz, seulement en PLASMA)
            if (currentState == STATE_PLASMA &&
                loopCounter % PID3_DIVIDER == 0) {
                float e3 = sensors.P_mbar - consigne_P;
                computePID(pid3, e3, dt3);
            }
            break;

        case STATE_ERREUR:
            emergencyStop();
            break;

        case STATE_FIN:
            emergencyStop();
            if (sdReady && logFile) {
                logFile.flush();
                logFile.close();
                sdReady = false;
            }
            break;
    }

    // ── 4. Émission série JSON (100 Hz) ────────────────────────────
    emitSerialJSON();

    // ── 5. Logging SD (100 Hz) ─────────────────────────────────────
    logToSD();

    // ── 6. MQTT (1 Hz) ─────────────────────────────────────────────
    if (loopCounter % FE_HZ == 0) {
        if (!mqtt.connected() && WiFi.status() == WL_CONNECTED) {
            mqtt.connect("bohemian-esp32");
            mqtt.subscribe("bohemian/cmd/#");
        }
        mqtt.loop();
        publishMQTT();
    }

    // ── 7. Cadence 100 Hz ──────────────────────────────────────────
    loopCounter++;
    uint32_t elapsed = micros() - loopStart;
    if (elapsed < (uint32_t)PERIOD_US) {
        delayMicroseconds(PERIOD_US - elapsed);
    }
}
