# 🔌 Firmware ESP32 — Contrôle et Acquisition

Firmware PlatformIO pour l'ESP32 embarqué sur le pendule de torsion.

## Structure

```
firmware/
├── platformio.ini          # Configuration PlatformIO
├── README.md               # Ce fichier
└── src/
    └── main.cpp            # Firmware principal
```

## Fonctionnalités

- **Lecture capteurs** à 100 Hz : PSD, pression, puissance RF réfléchie,
  luminosité, température, courant magnétron, batterie
- **3 boucles PID** imbriquées (100 / 10 / 1 Hz) — voir §6.5
- **Machine d'état** (INIT → POMPAGE → PLASMA → MESURE → FIN) — voir §6.6
- **Watchdog de sécurité** — coupure SSR automatique — voir §6.7
- **Communication** :
  - Port série USB : trames JSON à 100 Hz (acquisition PC)
  - Wi-Fi MQTT : télémétrie à 1 Hz (dashboard)
  - Carte microSD : logging CSV local (backup)

## Compilation et flash

```bash
# Installer PlatformIO (si pas déjà fait)
pip install platformio

# Compiler
cd firmware/
pio run

# Flasher l'ESP32
pio run --target upload

# Moniteur série
pio device monitor --baud 115200
```

## Configuration

Modifier les constantes dans `src/main.cpp` :

| Constante | Défaut | Description |
|:---|:---|:---|
| `WIFI_SSID` | `"bohemian-lab"` | Réseau Wi-Fi |
| `WIFI_PASS` | `"quantum2026"` | Mot de passe Wi-Fi |
| `MQTT_BROKER` | `"192.168.1.100"` | Adresse du broker MQTT |
| `FE_HZ` | `100` | Fréquence d'échantillonnage |
| `T_PAROI_MAX` | `150.0` | Seuil sécurité température (°C) |

## Pinout ESP32

Voir [docs/06_controle.md §6.9](../docs/06_controle.md) pour le
schéma complet des connexions.

## Documentation associée

- [§6 Contrôle et Asservissement](../docs/06_controle.md)
- [§8 Acquisition des Données](../docs/08_acquisition.md)
- [§5 Notes de Sécurité](../docs/05_securite.md)
