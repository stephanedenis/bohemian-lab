# 🎨 Palette des composants — Conventions SVG

> **Référence unique** pour tous les schémas dans `docs/img/`.
> En cas de nouveau diagramme, utiliser ces couleurs exactes.

## Composants physiques

| Composant | fill | stroke | text | Aperçu |
|---|---|---|---|---|
| **Magnétron** | `#ef4444` | `#b91c1c` | `white` / `#fecaca` | 🟥 rouge |
| **Contrepoids** | `#fecaca` | `#dc2626` | `#991b1b` | 🩷 rouge clair |
| **Chambre inox** | `#f1f5f9` | `#475569` | `#475569` | ⬜ gris neutre |
| **Plateau porteur** | `#78716c` | `#44403c` | `#44403c` | ⬛ stone |
| **Barre transversale** | `#78716c` | `#44403c` | `#44403c` | ⬛ stone |
| **Fil de torsion** | `#a16207` | `#854d0e` | `#854d0e` | 🟫 ambre |
| **Miroir** | `#fbbf24` | `#a16207` | `#a16207` | 🟨 or |
| **Tige rigide** | `#57534e` | `#44403c` | `#44403c` | ⬛ stone foncé |
| **Baril 205L** | `#fafaf9` | `#57534e` | `#57534e` | ⬜ stone clair |

## Capteurs & actuateurs

| Composant | fill | stroke | text | Aperçu |
|---|---|---|---|---|
| **Laser** | `#10b981` | `#047857` | `white` | 🟢 émeraude |
| **PSD** | `#10b981` | `#047857` | `white` | 🟢 émeraude |
| **Nixie IN-13** | `#ff6b2b` | `#cc4400` | `white` | 🟧 néon orange |
| **Coupleur directionnel** | `#fef3c7` | `#f59e0b` | `#92400e` | 🟨 ambre clair |
| **Thermocouple K** | `#ccfbf1` | `#14b8a6` | `#0f766e` | 🩵 teal |
| **Jauge Pirani** | `#fefce8` | `#ca8a04` | `#92400e` | 🟨 jaune |
| **Caméra Wi-Fi** | `#dbeafe` | `#3b82f6` | `#1d4ed8` | 🟦 bleu |
| **AS7343 (spectral)** | `#fae8ff` | `#a855f7` | `#7c3aed` | 🟪 violet clair |

| **Vanne DN10** | `#94a3b8` | `#334155` | `white` | 🩶 slate |

## Infrastructure

| Composant | fill | stroke | text | Aperçu |
|---|---|---|---|---|
| **ESP32 / MCU** | `#eef2ff` | `#4f46e5` | `#3730a3` | 🟪 indigo |
| **Grillage Faraday** | `#e2e8f0` | `#475569` | `#334155` | ⬜ gris grille |
| **Couvercle acrylique** | `#e0f2fe` | `#0284c7` | `#0c4a6e` | 🩵 sky |
| **Joint silicone** | `#fdba74` | `#ea580c` | — | 🟧 orange clair |
| **Plasma H₂O** | gradient violet | `#a855f7` | `#7c3aed` | 🟣 violet |

## Règles générales

1. **Opacité** : par défaut `1.0`. Utiliser `0.25` uniquement pour les éléments fantômes (ex : contrepoids en arrière-plan).
2. **Formes** : la forme peut varier selon la vue (cercle en plan, ellipse en élévation) — mais les **couleurs** restent identiques.
3. **Symbole magnétron** : cercle avec 6 cavités + cathode centrale (`<g id="magnetron">`). En vue de côté, utiliser une ellipse avec cavités alignées horizontalement.
4. **Polices** : `'Segoe UI', Arial, sans-serif`, taille `11` par défaut.
5. **Fond** : toujours `#ffffff` (blanc).
6. **Labels** : texte `font-weight="bold"` pour le nom du composant, poids normal pour les détails.
7. **Laser / PSD** : vert émeraude `#10b981` — bien distinct du néon orange des Nixie `#ff6b2b`.
