# 📊 Données de simulation

Ce dossier contient les résultats produits par les scripts de simulation
numérique (`experiments/005_*` à `009_*`).

## Convention de nommage

```
NNN_description.extension
```

- `NNN` : numéro de l'expérience (005–009)
- Formats : `.csv`, `.png`, `.npy`, `.npz`

## Contenu

| Préfixe | Expérience | Fichiers |
|:---|:---|:---|
| `005_*` | Circuits de phase quantique | Balayage phase, corrélations Bell, gradient Nixie |
| `006_*` | Analyse de signal (synthétique) | Signal pendule, FFT, corrélation croisée, scan SNR |
| `007_*` | Dynamique PID | Réponse temporelle, scan Kp, comparaison tuning |
| `008_*` | Sensibilité Monte-Carlo | Distribution η, budget d'erreur, forces parasites |
| `009_*` | Modèle plasma 3D | Coupes, isosurfaces, décomposition force H/V |

## Régénération

Chaque fichier peut être régénéré en exécutant le script correspondant :

```bash
cd bohemian-lab
python experiments/006_analyse_signal.py
# → produit data/simulations/006_*.png, data/simulations/006_*.csv
```
