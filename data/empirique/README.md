# 🧪 Données empiriques

Ce dossier reçoit les mesures expérimentales du pendule de torsion,
acquises via l'ESP32 embarqué et le script `experiments/010_acquisition.py`.

## Convention de nommage

```
AAAA-MM-JJ_HHhMM_type_NNN.csv
```

- `AAAA-MM-JJ_HHhMM` : horodatage de début de session
- `type` : catégorie de l'essai
- `NNN` : numéro séquentiel de l'essai dans la session

### Types d'essais

| Type | Description | Référence protocole |
|:---|:---|:---|
| `calibration` | Calibration pendule (§4.2, étape 2) | Période $T_0$, constante $\kappa$ |
| `reference_vide` | Mesure à vide — bruit de fond (§4.2, étape 3.1) | Magnétron OFF, 10 min |
| `reference_fantome` | Charge fantôme — artefact thermique (§4.2, étape 3.2) | Eau liquide, magnétron pulsé |
| `test_principal` | Test plasma H₂O (§4.2, étape 4) | Vapeur d'eau, magnétron pulsé |
| `controle_inversion` | Inversion 180° (§4.2, étape 5.1) | Même test, dispositif retourné |
| `controle_argon` | Gaz noble (§4.2, étape 5.2) | Argon, même pression |
| `controle_vide` | Sans plasma (§4.2, étape 5.3) | $P < 0{,}01$ mbar |

### Exemple

```
2026-04-15_14h30_calibration_001.csv
2026-04-15_14h45_reference_vide_001.csv
2026-04-15_15h00_reference_fantome_001.csv
2026-04-15_15h15_test_principal_001.csv
2026-04-15_15h40_test_principal_002.csv
2026-04-15_16h05_controle_inversion_001.csv
```

## Format CSV

Fréquence d'échantillonnage : **100 Hz** (10 ms entre lignes).

### En-tête de métadonnées (lignes commençant par `#`)

```csv
# bohemian-lab — données empiriques
# date: 2026-04-15T14:30:00
# type: test_principal
# essai: 001
# operateur: S. Denis
# pression_initiale_mbar: 3.1
# T0_s: 444.3
# kappa_Nm_rad: 1.02e-05
# L_bras_m: 0.200
# duree_s: 600
# fe_Hz: 100
# firmware_version: 1.0.0
# notes: Première session extérieure, vent < 5 km/h
```

### Colonnes de données

| # | Colonne | Unité | Source | Description |
|:--|:---|:---|:---|:---|
| 1 | `timestamp_ms` | ms | Timer ESP32 | Temps depuis début acquisition |
| 2 | `psd_urad` | µrad | PSD (laser) | Déplacement angulaire du pendule |
| 3 | `P_mbar` | mbar | Jauge Pirani | Pression chambre |
| 4 | `Pr_mW` | mW | Coupleur dir. | Puissance RF réfléchie |
| 5 | `lum_mV` | mV | Caméra | Luminosité plasma (proxy $n_e^2$) |
| 6 | `T_paroi_C` | °C | MAX31855 | Température paroi chambre |
| 7 | `I_mag_mA` | mA | Shunt courant | Courant magnétron |
| 8 | `V_bat_V` | V | Diviseur résistif | Tension batterie |
| 9 | `duty_vanne` | 0–1 | PID₁ sortie | Duty cycle électrovanne |
| 10 | `duty_RF` | 0–1 | PID₂ sortie | Duty cycle SSR magnétron |
| 11 | `commande_mag` | 0/1 | Séquenceur | État ON/OFF du magnétron (pulsation) |
| 12 | `etat` | texte | Machine d'état | `MESURE`, `PLASMA`, etc. |

### Exemple de données

```csv
timestamp_ms,psd_urad,P_mbar,Pr_mW,lum_mV,T_paroi_C,I_mag_mA,V_bat_V,duty_vanne,duty_RF,commande_mag,etat
0,0.12,3.12,15.4,2048,22.3,0,17.8,0.00,0.00,0,MESURE
10,0.15,3.12,15.3,2052,22.3,0,17.8,0.00,0.00,0,MESURE
20,0.18,3.11,14.8,2180,22.4,285,17.7,0.45,0.78,1,MESURE
```

## Fichier de résultats — Analyse post-traitement

Le script `experiments/011_analyse_empirique.py` produit en sortie :

```
AAAA-MM-JJ_HHhMM_resultats.json
```

Contenu :

```json
{
  "date": "2026-04-15T14:30:00",
  "type": "test_principal",
  "T0_mesure_s": 443.8,
  "theta_max_urad": 58.3,
  "force_extraite_uN": 2.95,
  "force_fantome_uN": 0.42,
  "force_nette_uN": 2.53,
  "eta": 0.77,
  "snr": 8.4,
  "correlation_pic": 0.87,
  "criteres_succes": {
    "snr_gt_3": true,
    "correlation_gt_0.8": true,
    "inversion_coherente": null,
    "fantome_lt_0.3": true
  }
}
```

## Analyse

Voir `experiments/011_analyse_empirique.py` pour le pipeline complet
(filtrage → corrélation → extraction force → calcul η → comparaison théorie).
