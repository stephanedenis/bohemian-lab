# 🌈 Capteur Spectral — AS7343

[← Retour au README](../README.md) · [← Contrôle et Asservissement](06_controle.md)

---

## Résumé exécutif

Le diagnostic du plasma H₂O nécessite une **mesure spectrale embarquée**
pour alimenter les boucles PID en proxy de $n_e$ et $T_e$. Après
évaluation systématique de la gamme ams-OSRAM (AS7262, AS7263, AS7341,
AS7343) et d'alternatives (AH-300, Hamamatsu C12880MA), le capteur
retenu est :

$$\boxed{\textbf{AS7343} \;\text{— 14 canaux multi-spectraux, 380–1000 nm, I²C}}$$

**Un seul capteur suffit.** L'AS7343 couvre les deux raies critiques
(Hβ 486 nm, Hα 656 nm) avec un gain allant jusqu'à 2048× — adapté
aux émissions faibles d'un plasma basse-pression. L'ajout d'un
capteur UV (AS7331) n'est pas nécessaire en Phase 1.

---

## 1. Pourquoi un capteur spectral ?

### 1.1 Limite de la caméra Wi-Fi

La caméra Wi-Fi (PID₂ actuel, §6.5.2) fournit un proxy de $n_e^2$
via la luminosité globale — mais elle est **spectralement aveugle** :
elle ne distingue pas Hα de Hβ, ni OH· d'une contamination N₂.

Pour un contrôle PID fin du plasma, on a besoin de :

| Grandeur physique | Méthode | Raie(s) requise(s) |
|:---|:---|:---|
| Densité électronique $n_e$ | Intensité absolue de Hβ (Stark) | **Hβ 486,1 nm** |
| Température électronique $T_e$ | Ratio de raies Boltzmann | **Hα/Hβ** (656/486 nm) |
| Qualité du plasma (dissociation) | Présence de OH· | OH· 309 nm (UV) |
| Oxygène atomique | Intensité O I | O I 777 nm (NIR) |

Un capteur multi-spectral avec des canaux **centrés sur ces
longueurs d'onde** fournit ces informations en temps réel,
directement sur le bus I²C de l'ESP32.

### 1.2 Principe : mesures relatives, pas absolues

Pour le PID, seules les **variations relatives** d'intensité comptent :
- $I(\text{Hβ})$ augmente → $n_e$ augmente → réduire $P_{\text{RF}}$
- $I(\text{Hα}) / I(\text{Hβ})$ augmente → $T_e$ augmente →
  ajuster pression

Pas besoin de calibration spectrophotométrique absolue. Un capteur
à **filtres interférentiels** (comme l'AS7343) suffit — on n'a
pas besoin d'un spectromètre à réseau.

---

## 2. Évaluation de la gamme ams-OSRAM

### 2.1 Candidats évalués

| Capteur | Canaux | Plage (nm) | FWHM | Gain max | I²C | Statut | Prix |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **AS7262** | 6 VIS | 430–670 | 40 nm | 64× | 0x49 | ⚠️ NRND | ~16 $ |
| **AS7263** | 6 NIR | 610–870 | 20 nm | 64× | 0x49 | ⚠️ NRND | ~23 $ |
| **AS7341** | 11 (8 spectral) | 350–1000 | ~30 nm | 512× | 0x39 | ✅ Actif | ~16 $ |
| **AS7343** | 14 (11 spectral) | 380–1000 | ~25 nm | **2048×** | 0x39 | ✅ Actif | ~22 $ |

> **NRND** = *Not Recommended for New Design*. L'AS7262 et l'AS7263
> sont en fin de vie — pas de garantie d'approvisionnement à long terme.

### 2.2 Grille d'évaluation vs. raies plasma

La qualité de la couverture dépend de la **proximité** entre les
canaux du capteur et les raies d'émission du plasma H₂O :

#### Hβ — 486,1 nm (★★★ — proxy $n_e$, critique)

| Capteur | Canaux proches | Meilleur écart | Verdict |
|:---|:---|:---|:---|
| AS7262 | 500 nm | +14 nm | ⚠️ Marginal |
| AS7263 | — | hors plage | ❌ |
| AS7341 | F3=480 nm | −6 nm | ✅ Bon |
| **AS7343** | **F3=475 + F4=515** | **−11 / +29** | ✅ **Encadré** |

#### Hα — 656,3 nm (★★★ — ratio $T_e$, critique)

| Capteur | Canaux proches | Meilleur écart | Verdict |
|:---|:---|:---|:---|
| AS7262 | 650, 670 nm | −6 / +14 nm | ✅ Bon |
| AS7263 | 680 nm | +24 nm | ⚠️ Marginal |
| AS7341 | F7=630, F8=680 | −26 / +24 | ⚠️ Large |
| **AS7343** | **F6=640 + F7=690** | **−16 / +34** | ✅ **Encadré** |

#### O I — 777,2 nm (★★☆ — oxygène atomique)

| Capteur | Canaux proches | Meilleur écart | Verdict |
|:---|:---|:---|:---|
| AS7262 | — | hors plage | ❌ |
| AS7263 | 810 nm | +33 nm | ⚠️ Loin |
| AS7341 | NIR=910 nm | +133 nm | ❌ Trop loin |
| **AS7343** | **F8=745 + NIR=855** | **−32 / +78** | ⚠️ **Queue FWHM F8** |

#### OH· — 306–309 nm (★★☆ — dissociation H₂O)

| Capteur | Couverture | Verdict |
|:---|:---|:---|
| AS7262 | Hors plage (début 430 nm) | ❌ |
| AS7263 | Hors plage (début 610 nm) | ❌ |
| AS7341 | Limite basse ~350 nm, pas de canal dédié | ❌ |
| **AS7343** | Limite basse ~380 nm | ❌ **Hors plage** |

> 💡 **OH· n'est pas bloquant** — La présence de OH· est déjà
> confirmée **visuellement** par la couleur cyan du plasma (caméra
> Wi-Fi). Pour le PID, les ratios Hα/Hβ suffisent. En Phase 2, un
> capteur UV dédié (AS7331, ~8 $, I²C 0x74) pourra être ajouté si
> un diagnostic quantitatif de OH· est souhaité.

### 2.3 Tableau de synthèse

| Critère | AS7262 | AS7263 | AS7341 | **AS7343** |
|:---|:---|:---|:---|:---|
| Hβ (486 nm) | ⚠️ | ❌ | ✅ | ✅✅ |
| Hα (656 nm) | ✅ | ⚠️ | ⚠️ | ✅✅ |
| O I (777 nm) | ❌ | ⚠️ | ❌ | ⚠️ |
| OH· (309 nm) | ❌ | ❌ | ❌ | ❌ |
| Gain max | 64× | 64× | 512× | **2048×** |
| Statut produit | NRND | NRND | Actif | **Actif** |
| Nb canaux utiles | 3/6 | 1/6 | 5/8 | **8/11** |
| Adresse I²C | 0x49 | 0x49 ⚠️ | 0x39 | **0x39** |
| **Score global** | ⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

> ⚠️ AS7262 et AS7263 partagent l'adresse I²C 0x49 — impossible de
> les utiliser ensemble sur le même bus sans multiplexeur.

---

## 3. Solution retenue : AS7343 seul

### 3.1 Fiche technique

| Paramètre | Valeur |
|:---|:---|
| **Modèle** | ams-OSRAM AS7343 |
| **Breakout** | SparkFun SEN-23220 (Qwiic) |
| **Prix** | ~22 $ US |
| **Canaux spectraux** | 11 (F1–F8 + FZ + FY + FXL) |
| **Canaux auxiliaires** | Clear, NIR, Flicker |
| **Plage spectrale** | 380–1000 nm |
| **FWHM typique** | ~25 nm |
| **Gain programmable** | 0,5× à **2048×** (log₂, 13 paliers) |
| **ADC** | 16 bits par canal |
| **Temps d'intégration** | 2,78 µs – 182 ms (programmable) |
| **Interface** | I²C, adresse **0x39** |
| **Tension** | 1,8 V (régulateur sur le breakout Qwiic) |
| **Courant** | ~210 µA (actif), ~350 µA (veille) |
| **Boîtier** | LGA 3,1 × 2,0 × 1,0 mm |
| **LED intégrée** | Driver programmable 4–258 mA |
| **AutoSmux** | 3 cycles pour lire les 14 canaux |

### 3.2 Carte des canaux

L'AS7343 utilise une matrice de photodiodes 5×5 avec des filtres
interférentiels déposés en couche mince. Les 14 canaux sont lus
en **3 cycles AutoSmux** de 6 canaux chacun :

| Cycle | Canal | λ centre (nm) | Couleur | Usage plasma |
|:---|:---|:---|:---|:---|
| 1 | **F1** | 405 | Violet | Continuum UV-VIS |
| 1 | **F2** | 425 | Bleu profond | — |
| 1 | **FZ** | 450 | Bleu | Pied de Hβ |
| 1 | F3 | 475 | Bleu ciel | **← Hβ 486 (−11 nm)** ★★★ |
| 1 | F4 | 515 | Cyan | Hβ épaule droite |
| 1 | Clear | — | Large bande | Référence de normalisation |
| 2 | **F5** | 550 | Vert étroit | — |
| 2 | **FY** | 555 | Vert large | — |
| 2 | **FXL** | 600 | Orange | Continuum |
| 2 | F6 | 640 | Rouge-orange | **← Hα 656 (−16 nm)** ★★★ |
| 2 | F7 | 690 | Rouge | Hα épaule droite |
| 2 | NIR | 855 | Proche IR | O I 777 (indirect) |
| 3 | **F8** | 745 | Rouge profond | **← O I 777 (−32 nm)** ★★☆ |
| 3 | Flicker | — | — | Détection scintillement |

> 💡 **Avantage des canaux « auxiliaires »** — FZ (450), FY (555) et
> FXL (600) n'étaient pas présents sur l'AS7341. Ils permettent une
> **interpolation spectrale** plus fine entre les canaux principaux,
> améliorant la soustraction du continuum Bremsstrahlung.

### 3.3 Extraction des grandeurs physiques

#### Proxy de $n_e$ — Intensité Hβ

$$\hat{n}_e \;\propto\; I(\text{F3}_{475}) - \underbrace{\frac{I(\text{FZ}_{450}) + I(\text{F4}_{515})}{2}}_{\text{continuum interpolé}}$$

La soustraction du continuum (moyenne des canaux adjacents) isole
la contribution de la raie Hβ. Le gain 2048× de l'AS7343 permet
de détecter cette raie même dans un plasma faiblement ionisé
($n_e \sim 10^{16}$ m⁻³).

#### Proxy de $T_e$ — Ratio Hα/Hβ (méthode de Boltzmann)

$$\frac{I(\text{H}\alpha)}{I(\text{H}\beta)} = \frac{g_3 A_{32} \lambda_\beta}{g_4 A_{42} \lambda_\alpha} \exp\!\left(-\frac{E_3 - E_4}{k_B T_e}\right)$$

En pratique, le ratio des canaux corrigés :

$$R = \frac{I(\text{F6}_{640}) + I(\text{F7}_{690}) - 2 \cdot I(\text{FXL}_{600})}{I(\text{F3}_{475}) - \text{continuum Hβ}}$$

est un proxy monotone de $T_e$. Pas besoin de calibration absolue
pour le PID — seules les variations de $R$ comptent.

#### Indicateur O I — Oxygène atomique

$$\hat{I}_{\text{O\,I}} \;\propto\; I(\text{F8}_{745})$$

Le canal F8 (745 nm) capte la **queue** de la raie O I 777 nm via
son FWHM (~25 nm). C'est un indicateur qualitatif, pas quantitatif.
Suffisant pour détecter une variation de la dissociation de H₂O.

### 3.4 Pourquoi l'AS7331 (UV) n'est pas nécessaire

| Argument | Détail |
|:---|:---|
| OH· n'est pas dans le PID | Les boucles PID (§6.5) utilisent $P_r$, luminosité et $T_{\text{paroi}}$ — pas OH· |
| Détection qualitative par caméra | La couleur cyan du plasma (caméra Wi-Fi) confirme la présence de OH· |
| Hα/Hβ suffisent pour $T_e$ | Le ratio de Boltzmann donne $T_e$ sans raie UV |
| Coût et complexité | Un seul capteur = un seul driver, une seule adresse I²C, un seul budget courant |
| Phase 2 optionnelle | Si un diagnostic UV quantitatif est souhaité plus tard, l'AS7331 (I²C 0x74) s'ajoute sans conflit |

---

## 4. Intégration matérielle

### 4.1 Placement physique

Le capteur doit **voir le plasma** à travers le grillage Faraday et
le couvercle acrylique. Deux options :

| Position | Avantages | Inconvénients |
|:---|:---|:---|
| **Au-dessus du grillage** (recommandé) | Hors cage Faraday, pas d'EMI RF, accès facile | Signal atténué par le grillage (maille < 12 mm, transmission ~70 % dans le visible) |
| Sur la paroi interne | Signal direct, pas d'atténuation | Exposé aux RF (2,45 GHz), blindage difficile |

**Recommandation** : monter le breakout SparkFun Qwiic **au-dessus du
grillage Faraday**, à côté de la caméra Wi-Fi, orienté
vers le bas (photodiode face au plasma). Le grillage atténue le signal
d'un facteur ~1,4× — compensé par le gain 2048× du capteur.

### 4.2 Bus I²C — Intégration ESP32

Le breakout SparkFun Qwiic utilise le connecteur standardisé Qwiic
(JST SH 4 broches) :

| Broche Qwiic | Signal | ESP32 |
|:---|:---|:---|
| Noir | GND | GND |
| Rouge | 3.3V | 3.3V |
| Bleu | SDA | GPIO21 |
| Jaune | SCL | GPIO22 |

L'AS7343 utilise l'adresse I²C **0x39** — pas de conflit avec les
périphériques existants :

| Périphérique | Bus | Adresse |
|:---|:---|:---|
| ADS1115 (ADC Pirani) | I²C | 0x48 |
| **AS7343** (spectral) | **I²C** | **0x39** |
| MAX31855 (thermocouple) | SPI | CS=GPIO5 |
| Carte SD | SPI | CS=GPIO15 |

### 4.3 Architecture firmware — Tâche FreeRTOS

La lecture de l'AS7343 nécessite **3 cycles AutoSmux** séquentiels
pour obtenir les 14 canaux. Chaque cycle comprend :
1. Configuration du multiplexeur (registre SMUX)
2. Démarrage de l'intégration
3. Attente du temps d'intégration (2,78 µs – 182 ms)
4. Lecture des 6 registres 16 bits

**Cadence cible** : 10 Hz (compatible avec PID₂, §6.5.2).

Avec un temps d'intégration de 30 ms par cycle :
$3 \times 30 = 90$ ms par lecture complète → **~11 Hz** réalisable.

```
┌─────────────────────────────────────────────────┐
│  Tâche FreeRTOS : spectral_task (priorité 2)     │
│  Cadence : 10 Hz (100 ms)                        │
│                                                   │
│  1. Cycle AutoSmux 1 → F1, F2, FZ, F3, F4, Clear │
│  2. Cycle AutoSmux 2 → F5, FY, FXL, F6, F7, NIR  │
│  3. Cycle AutoSmux 3 → F8, Flicker                │
│  4. Calculer proxy_ne (Hβ corrigé)                │
│  5. Calculer ratio_Te (Hα/Hβ)                     │
│  6. Publier vers PID₂ (queue FreeRTOS)            │
│  7. Logger sur SD (colonnes spectrales)            │
└─────────────────────────────────────────────────┘
```

### 4.4 Colonnes CSV additionnelles

Le fichier de logging SD (§6.8) est étendu avec les colonnes
spectrales :

```csv
...,F1_405,F2_425,FZ_450,F3_475,F4_515,F5_550,FY_555,FXL_600,F6_640,F7_690,F8_745,NIR_855,Clear,proxy_ne,ratio_Te,...
```

### 4.5 Topics MQTT additionnels

| Topic | Payload | Cadence |
|:---|:---|:---|
| `bohemian/spectral` | `{"F3":1234,"F6":567,"F7":890,"proxy_ne":42.1,"ratio_Te":3.14}` | 1 Hz |
| `bohemian/spectral/brut` | Tous les 14 canaux (JSON) | 0,1 Hz |

---

## 5. Impact sur les boucles PID

### 5.1 PID₂ amélioré — De la luminosité au spectre

La boucle PID₂ actuelle (§6.5.2) utilise la luminosité globale de
la caméra comme proxy de $n_e^2$. Avec l'AS7343, on peut remplacer
ce proxy par une mesure **spectralement résolue** :

| Aspect | PID₂ actuel (caméra) | PID₂ amélioré (AS7343) |
|:---|:---|:---|
| Entrée | Luminosité RGB globale | **Intensité Hβ corrigée** |
| Proxy de | $n_e^2$ (recombinaison) | **$n_e$ (émission Balmer)** |
| Spécificité | Capte tout (plasma + parasites) | **Sélectif** (raie Hβ isolée) |
| Cadence | 10 Hz (framerate caméra) | 10 Hz (AutoSmux 3 cycles) |
| Immunité RF | Bonne (caméra au-dessus du grillage) | **Excellente** (I²C blindé) |

### 5.2 Nouvelle boucle PID₄ — Contrôle de $T_e$ (optionnelle)

Le ratio Hα/Hβ ouvre la possibilité d'une **4ᵉ boucle PID**
dédiée au contrôle de la température électronique :

| Paramètre | Valeur |
|:---|:---|
| Entrée | Ratio $R = I(\text{Hα}) / I(\text{Hβ})$ |
| Consigne | $R_0$ (calibré empiriquement) |
| Sortie | $u_4(t)$ → duty cycle magnétron (ajustement fin) |
| Cadence | 1–5 Hz |
| Priorité | Inférieure à PID₁ et PID₂ |

> 💡 Cette boucle est **optionnelle** — elle n'est pertinente que si
> le régime de plasma est suffisamment stable pour que le ratio Hα/Hβ
> soit significatif. En Phase 1, PID₁ + PID₂ (avec AS7343 comme
> entrée) suffisent.

---

## 6. Capteurs éliminés — Justification

### 6.1 AH-300 (Environmental Sensors Co.)

Malgré un marketing attractif (« spectromètre portable »), l'AH-300
est un **luxmètre à LED** : son capteur est un BH1750 (photodiode
silicium large bande) sans résolution spectrale. Aucun canal
sélectif pour Hα, Hβ ou OH·. **Éliminé.**

### 6.2 Hamamatsu C12880MA

Vrai micro-spectromètre à réseau (340–850 nm, 15 nm de résolution) :
excellent en théorie, mais **inadapté** au contexte embarqué :

| Critère | C12880MA | AS7343 |
|:---|:---|:---|
| Prix | ~280 $ | **22 $** |
| Interface | Analogique (circuit de lecture dédié) | **I²C** (Qwiic) |
| Taille | 20 × 12 × 10 mm + PCB | **3 × 2 × 1 mm** (breakout 25 × 25 mm) |
| Résolution | 15 nm (288 pixels) | 25 nm (14 canaux) |
| Sensibilité plasma | Excellente | Bonne (gain 2048×) |

Le C12880MA est surdimensionné pour un contrôle PID où seules 3–4
raies comptent. Réservé aux laboratoires de spectroscopie.

### 6.3 AS7262 et AS7263

- **AS7262** : 6 canaux VIS (430–670 nm), FWHM 40 nm, gain max 64×.
  Couvre Hα (650/670 nm) mais pas Hβ (500 nm est à +14 nm, FWHM
  trop large). **NRND.** Éliminé.
- **AS7263** : 6 canaux NIR (610–870 nm), FWHM 20 nm, gain max 64×.
  Ne couvre ni Hβ ni Hα correctement. **NRND.** Éliminé.
- **Conflit I²C** : les deux partagent l'adresse 0x49 — impossible
  de les combiner sans multiplexeur.

### 6.4 AS7341

Le prédécesseur de l'AS7343 — bon capteur, mais surpassé :

| Critère | AS7341 | AS7343 | Avantage |
|:---|:---|:---|:---|
| Canaux spectraux | 8 | **11** | +3 canaux en zones critiques |
| Gain max | 512× | **2048×** | 4× plus sensible |
| Canal le plus proche de Hα | F7=630 / F8=680 | **F6=640 / F7=690** | Meilleur encadrement |
| Canal le plus proche de O I | NIR=910 nm (−133 nm) | **F8=745 nm (−32 nm)** | Beaucoup plus proche |
| Canaux intermédiaires | — | FZ=450, FY=555, FXL=600 | Soustraction continuum |
| Prix | ~16 $ | ~22 $ | +6 $ |

Pour +6 $, l'AS7343 offre une couverture spectrale nettement
supérieure et un gain 4× plus élevé. Le surcoût est marginal.

---

## 7. Approvisionnement

| Fournisseur | Référence | Prix | Stock | Lien |
|:---|:---|:---|:---|:---|
| **SparkFun** | SEN-23220 (Qwiic AS7343) | **21,95 $ US** | En stock | [sparkfun.com](https://www.sparkfun.com/sparkfun-spectral-sensor-breakout-as7343-qwiic.html) |
| Adafruit | Breakout AS7343 | ~22 $ US | Annoncé (2026) | [adafruit.com](https://www.adafruit.com) |
| Mouser/DigiKey | AS7343 (composant nu) | ~8–10 $ US | En stock | Pour intégration PCB custom |

> 💡 Le breakout SparkFun Qwiic est recommandé pour le prototypage :
> connecteur Qwiic standardisé (JST SH 4 broches), régulateur de
> tension intégré, résistances de pull-up I²C, et librairie Arduino
> disponible. En Phase 2, un PCB custom pourra intégrer le composant
> nu (3 × 2 mm) directement sur la carte capteur de l'ESP32.

---

## 8. Bibliothèque Arduino / ESP32

SparkFun fournit une librairie Arduino complète :

| Ressource | Lien |
|:---|:---|
| Librairie Arduino | [github.com/sparkfun/SparkFun_AS7343_Arduino_Library](https://github.com/sparkfun/SparkFun_AS7343_Arduino_Library) |
| Hookup Guide | [docs.sparkfun.com](https://docs.sparkfun.com/SparkFun_Qwiic_Spectral_Sensor_AS7343/) |
| Datasheet AS7343 | ams-OSRAM (NDA requis pour le document complet) |

### Exemple d'utilisation (ESP32 / Arduino)

```cpp
#include <SparkFun_AS7343.h>

SparkFun_AS7343 capteurSpectral;

void setup() {
    Wire.begin();
    capteurSpectral.begin();
    capteurSpectral.setGain(AS7343_GAIN_256X);  // Gain adapté au plasma
    capteurSpectral.setATIME(29);               // ~83 ms d'intégration
    capteurSpectral.setASTEP(999);              // pas de 2,78 µs × 1000
}

void loop() {
    // Lecture des 14 canaux (3 cycles AutoSmux)
    if (capteurSpectral.readAllChannels()) {
        uint16_t hBeta  = capteurSpectral.getF3();   // 475 nm → Hβ
        uint16_t hAlpha = capteurSpectral.getF6();   // 640 nm → Hα (gauche)
        uint16_t hAlpha2 = capteurSpectral.getF7();  // 690 nm → Hα (droite)
        uint16_t continuum = capteurSpectral.getFXL(); // 600 nm

        // Proxy nₑ : intensité Hβ corrigée du continuum
        float proxy_ne = (float)hBeta
                       - 0.5f * (capteurSpectral.getFZ() + capteurSpectral.getF4());

        // Ratio Hα/Hβ → proxy Tₑ
        float hAlphaMoy = 0.5f * (hAlpha + hAlpha2) - continuum;
        float ratio_Te = (proxy_ne > 10) ? hAlphaMoy / proxy_ne : 0.0f;
    }
    delay(100);  // 10 Hz
}
```

---

## 9. Récapitulatif de la solution

```
                    ┌──────────────────────┐
                    │   AS7343 (SparkFun)   │
                    │   14 canaux           │
                    │   I²C 0x39            │
                    │   Gain 2048×          │
                    │   ~22 $               │
                    └────────┬─────────────┘
                             │ I²C (SDA/SCL)
                    ┌────────▼─────────────┐
                    │      ESP32            │
                    │  ┌─────────────────┐  │
                    │  │ spectral_task   │  │
                    │  │ 10 Hz           │  │
                    │  │ proxy_ne (Hβ)   │──┼──→ PID₂ (ionisation)
                    │  │ ratio_Te (Hα/β) │──┼──→ PID₄ (optionnel)
                    │  │ indicateur O I  │──┼──→ Logger SD + MQTT
                    │  └─────────────────┘  │
                    └───────────────────────┘
```

| Élément | Valeur |
|:---|:---|
| **Capteur unique** | AS7343 (SparkFun SEN-23220) |
| **Prix total** | **~22 $ US** |
| **Raies couvertes** | Hβ (486 nm) ✅, Hα (656 nm) ✅, O I (777 nm) ⚠️ partiel |
| **Raies non couvertes** | OH· (309 nm) — diagnostic visuel par caméra |
| **Bus** | I²C 0x39 (Qwiic, câble 4 fils) |
| **Gain** | 2048× — adapté aux émissions faibles |
| **Cadence** | 10 Hz (3 cycles AutoSmux × 30 ms) |
| **Masse** | < 5 g (breakout Qwiic) |
| **Évolution Phase 2** | + AS7331 (UV, 0x74, ~8 $) si diagnostic OH· quantitatif souhaité |

---

## Références

1. **ams-OSRAM** (2024). *AS7343 — 14-Channel Multi-Spectral Sensor*.
   Datasheet. [ams-osram.com](https://ams-osram.com/products/sensor-solutions/spectral-sensors/ams-as7343)

2. **SparkFun Electronics** (2025). *SparkFun Spectral Sensor Breakout —
   AS7343 (Qwiic)*. SEN-23220.
   [sparkfun.com](https://www.sparkfun.com/sparkfun-spectral-sensor-breakout-as7343-qwiic.html)

3. **SparkFun** (2025). *SparkFun AS7343 Arduino Library*.
   [github.com/sparkfun/SparkFun_AS7343_Arduino_Library](https://github.com/sparkfun/SparkFun_AS7343_Arduino_Library)

4. **Kramida, A. *et al.*** (2024). *NIST Atomic Spectra Database*
   (version 5.12). NIST.
   [nist.gov/pml/atomic-spectra-database](https://www.nist.gov/pml/atomic-spectra-database)
   (Raies Balmer : Hα 656,28 nm, Hβ 486,13 nm. O I 777,19 nm.)

5. **Bruggeman, P. J. *et al.*** (2014). « Gas temperature determination
   from rotational lines in non-equilibrium plasmas ». *Plasma Sources
   Sci. Technol.*, 23(2), 023001.
   [doi:10.1088/0963-0252/23/2/023001](https://doi.org/10.1088/0963-0252/23/2/023001)

6. **Griem, H. R.** (1997). *Principles of Plasma Spectroscopy*.
   Cambridge University Press. ISBN 978-0-521-61941-7.
   (Chapitre 5 : diagnostic spectroscopique par ratios de raies Balmer.)

---

[← Contrôle et Asservissement](06_controle.md) · [Retour au README →](../README.md)
