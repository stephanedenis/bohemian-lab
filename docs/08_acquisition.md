# 📡 Acquisition des Données Empiriques

[← Retour au README](../README.md) · [← Contrôle et Asservissement](06_controle.md)

---

## Introduction

Ce document spécifie l'infrastructure d'acquisition des données
expérimentales — le pont entre le **protocole** (§4.2) et les
**fichiers de données** stockés dans `data/empirique/`.

La chaîne d'acquisition se décompose en 3 maillons :

```
  ESP32 embarqué          Script Python             Analyse
  (firmware/)             (010_acquisition.py)      (011_analyse_empirique.py)
       │                        │                        │
       │  Série/Wi-Fi           │  CSV brut              │  Résultats + figures
       ├────────────────────▶   ├───────────────────▶    ├──────────────────▶
       │  trames JSON           │  data/empirique/       │  data/empirique/
       │  @ 100 Hz              │  *_type_NNN.csv        │  *_resultats.json
       │                        │                        │  *_analyse_*.png
```

---

## 8.1 Architecture de la chaîne

### Flux de données

| Étape | Composant | Entrée | Sortie | Cadence |
|:---|:---|:---|:---|:---|
| 1 | ESP32 ADC | Capteurs analogiques | Trames JSON série | 100 Hz |
| 2 | ESP32 Wi-Fi | Trames internes | Topics MQTT | 1 Hz (télémétrie) |
| 3 | ESP32 SD | Trames internes | CSV local (backup) | 100 Hz |
| 4 | PC (010_acquisition.py) | Port série USB ou MQTT | CSV dans `data/empirique/` | 100 Hz |
| 5 | PC (011_analyse_empirique.py) | CSV brut | Résultats JSON + figures | Post-traitement |

### Redondance

Les données sont enregistrées **en double** :
- **Carte SD** de l'ESP32 (backup embarqué, 100 Hz)
- **PC** via port série ou Wi-Fi (acquisition principale, 100 Hz)

En cas de perte de connexion série, les données sont récupérables
sur la carte SD.

---

## 8.2 Protocole série ESP32 → PC

### Format des trames

L'ESP32 émet une ligne JSON par lecture à 100 Hz (10 ms) :

```json
{"t":1230,"psd":12.5,"P":3.12,"Pr":15.4,"lum":2048,"T":42.3,"I":285,"V":17.8,"dv":0.45,"dr":0.78,"mag":1,"st":"M"}
```

| Champ | Type | Unité | Description |
|:---|:---|:---|:---|
| `t` | int | ms | Timestamp (depuis boot ESP32) |
| `psd` | float | µrad | Position PSD (angle pendule) |
| `P` | float | mbar | Pression |
| `Pr` | float | mW | Puissance réfléchie |
| `lum` | int | mV | Luminosité plasma |
| `T` | float | °C | Température paroi |
| `I` | int | mA | Courant magnétron |
| `V` | float | V | Tension batterie |
| `dv` | float | 0–1 | Duty cycle vanne |
| `dr` | float | 0–1 | Duty cycle RF |
| `mag` | int | 0/1 | État commande magnétron |
| `st` | str | — | État machine (I/P/L/M/E/F) |

### Codes d'état machine

| Code | État | Description |
|:---|:---|:---|
| `I` | INIT | Initialisation, auto-test |
| `P` | POMPAGE | Pompe active, PID₃ |
| `L` | PLASMA | Magnétron ON, 3 PID actifs |
| `M` | MESURE | Acquisition de données (vanne fermée) |
| `E` | ERREUR | Anomalie, SSR OFF |
| `F` | FIN | Session terminée |

### Paramètres série

| Paramètre | Valeur |
|:---|:---|
| Baudrate | 115 200 bps |
| Data bits | 8 |
| Parité | Aucune |
| Stop bits | 1 |
| Encodage | UTF-8 |

Débit : ~120 octets/trame × 100 trames/s = **12 Ko/s** (confortable
pour 115 200 bps = 11,5 Ko/s utile, avec marge si on réduit à 50 Hz).

---

## 8.3 Format CSV des fichiers empiriques

### Nommage

```
AAAA-MM-JJ_HHhMM_type_NNN.csv
```

Voir [data/empirique/README.md](../data/empirique/README.md) pour le
détail des types d'essais et le format complet des colonnes.

### En-tête de métadonnées

Les lignes commençant par `#` contiennent les métadonnées de la session
(date, type d'essai, paramètres du pendule, conditions initiales).
Elles sont ignorées par `pandas.read_csv(comment='#')`.

### Colonnes

12 colonnes à 100 Hz. Voir le détail dans
[data/empirique/README.md](../data/empirique/README.md#colonnes-de-données).

---

## 8.4 Procédure d'acquisition

### Pré-requis

1. ESP32 alimenté et firmware flashé (`firmware/`)
2. PC connecté en USB ou sur le même réseau Wi-Fi
3. Dépendances Python installées : `pyserial` (série) ou
   `paho-mqtt` (Wi-Fi)

### Lancement

```bash
# Mode série (recommandé — fiable, faible latence)
python experiments/010_acquisition.py --port /dev/ttyUSB0 --type test_principal

# Mode MQTT (Wi-Fi — si le câble série n'est pas possible)
python experiments/010_acquisition.py --mqtt --broker 192.168.1.100 --type test_principal
```

### Déroulement

1. Le script ouvre la connexion (série ou MQTT).
2. Il demande les métadonnées interactivement (opérateur, notes) ou
   les prend en arguments de ligne de commande.
3. Il attend le premier `{"st":"M"}` (état MESURE) pour commencer
   l'écriture CSV.
4. Chaque trame JSON est parsée et convertie en ligne CSV.
5. Un compteur temps réel affiche le nombre de lignes, la durée,
   et le dernier angle $\theta$.
6. L'acquisition s'arrête sur :
   - `Ctrl+C` (arrêt manuel)
   - État `F` (FIN) reçu de l'ESP32
   - Durée maximale atteinte (`--duree`)

### Fichier de sortie

Le fichier CSV est écrit dans `data/empirique/` avec le nommage
automatique. Un message de confirmation affiche le chemin et la
taille du fichier.

---

## 8.5 Analyse post-acquisition

Le script `experiments/011_analyse_empirique.py` applique le
**même pipeline** que la simulation 006 (filtrage → corrélation →
extraction force → SNR) mais sur les **données réelles** :

```bash
python experiments/011_analyse_empirique.py data/empirique/2026-04-15_14h30_test_principal_001.csv
```

### Sorties

| Fichier | Contenu |
|:---|:---|
| `*_resultats.json` | $\eta$, SNR, corrélation, force nette, critères |
| `*_analyse_signal.png` | Signal brut + filtré + commande |
| `*_analyse_fft.png` | Spectre FFT + pic à $f_0$ |
| `*_analyse_correlation.png` | $C(\tau)$ avec pic annoté |
| `*_analyse_eta.png` | Comparaison $\eta$ mesuré vs prédiction théorique |

### Comparaison théorie vs mesure

L'analyse compare automatiquement les résultats mesurés aux
prédictions des simulations :

| Grandeur | Prédiction (simulations) | Source |
|:---|:---|:---|
| $F_{\text{rad}}$ | $P/c = 3{,}3\;\mu\text{N}$ pour 1 kW | Calcul analytique |
| $\theta_{\text{max}}$ | $\sim 1050\;\mu\text{rad}$ en résonance | 006_analyse_signal.py |
| SNR | $\sim 12$ pour $F = 3{,}3\;\mu\text{N}$ | 006_analyse_signal.py |
| $\eta_H$ | $\sim 0{,}57 \times \eta_{\text{total}}$ | 009_plasma_3d.py |
| IC 90 % de $\eta$ | $[0{,}6 \;;\; 1{,}5]$ | 008_sensibilite_eta.py |

---

## 8.6 Campagne d'essais complète

Une session expérimentale complète (§4.2) produit les fichiers
suivants dans `data/empirique/` :

```
2026-04-15_14h30_calibration_001.csv          ← Étape 2
2026-04-15_14h45_reference_vide_001.csv       ← Étape 3.1
2026-04-15_15h00_reference_fantome_001.csv    ← Étape 3.2
2026-04-15_15h15_test_principal_001.csv       ← Étape 4
2026-04-15_15h40_test_principal_002.csv       ← Étape 4 (répét.)
2026-04-15_16h05_test_principal_003.csv       ← Étape 4 (répét.)
2026-04-15_16h30_test_principal_004.csv       ← Étape 4 (répét.)
2026-04-15_16h55_test_principal_005.csv       ← Étape 4 (répét.)
2026-04-15_17h20_controle_inversion_001.csv   ← Étape 5.1
2026-04-15_17h45_controle_argon_001.csv       ← Étape 5.2
2026-04-15_18h10_controle_vide_001.csv        ← Étape 5.3
2026-04-15_18h10_resultats.json               ← Analyse globale
```

### Rapport de campagne

Le script `011_analyse_empirique.py` en mode campagne (`--campagne`)
traite tous les fichiers d'une session et produit :

1. Un **tableau comparatif** des η pour chaque essai
2. Un **test de reproductibilité** (écart-type sur les 5 essais)
3. La **vérification des critères de succès** (§4.4)
4. Un rapport texte et un graphique récapitulatif

---

## Références

1. **§4.2 Procédure de test** — [docs/04_protocole.md](04_protocole.md)
2. **§6.8 Communication et télémétrie** — [docs/06_controle.md](06_controle.md)
3. **006_analyse_signal.py** — Pipeline d'analyse sur données synthétiques
4. **data/empirique/README.md** — Format détaillé des fichiers CSV

---

[← Contrôle et Asservissement](06_controle.md) · [Retour au README →](../README.md)
