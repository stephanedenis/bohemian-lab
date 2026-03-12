# 🔬 Bohemian Lab — Instructions pour l'Agent IA

## Identité du projet

**Bohemian Lab** est un laboratoire d'expérimentation en physique quantique piloté par un ingénieur indépendant.
Le projet explore la **mécanique bohmienne** (interprétation de de Broglie–Bohm)
à travers des simulations numériques et une expérience matérielle de propulsion
par guidage d'onde pilote dans un plasma de vapeur d'eau.

## Stack technique

| Couche | Outils |
|---|---|
| Langage | Python 3.11+ |
| Simulation quantique | **Qiskit** (IBM), **PennyLane** (Xanadu) |
| Calcul scientifique | NumPy, SciPy, SymPy |
| Visualisation | Matplotlib, Qiskit Visualization |
| Notebooks | Jupyter / JupyterLab |
| Environnement | venv (`.venv/`) |

## Structure du dépôt

```
bohemian-lab/
├── experiments/     # Scripts Python exécutables (un fichier par expérience)
│                    #   Convention : NNN_nom.py  (ex: 001_superposition.py)
├── notebooks/       # Jupyter Notebooks exploratoires
├── src/             # Modules Python réutilisables (viz, utils, etc.)
├── data/            # Données brutes et résultats (.npy, .csv, .json)
├── docs/            # Documentation, notes, schémas
├── requirements.txt # Dépendances pip
└── README.md        # Protocole expérimental principal
```

## Conventions de code

- **Langue** : le code, les commentaires, les docstrings et les messages de commit sont en **français**.
- **Style** : PEP 8, largeur max 88 colonnes (Black-compatible).
- **Docstrings** : Google-style, en français.
- **Typage** : annotations de type systématiques (Python 3.11+ syntax : `list[int]`, `tuple[float, …]`).
- **Imports** : stdlib → tiers → locaux, séparés par des lignes vides.
- **Expériences** :
  - Chaque fichier dans `experiments/` est un script autonome exécutable (`if __name__ == "__main__"`).
  - Nommage séquentiel : `NNN_nom_court.py`.
  - Docstring d'en-tête obligatoire décrivant l'objectif de l'expérience.
- **Modules `src/`** : ne contiennent que des fonctions et classes réutilisables, jamais de `__main__`.

## Contexte scientifique

L'agent doit maîtriser les concepts suivants pour aider efficacement :

1. **Interprétation de de Broglie–Bohm** : loi de guidage $\vec{v} = \nabla S / m$, potentiel quantique $Q = -\frac{\hbar^2}{2m}\frac{\nabla^2 R}{R}$.
2. **Circuits quantiques** : portes (H, X, Y, Z, CNOT, Rz, …), mesures, simulateurs.
3. **Qiskit** : `QuantumCircuit`, `AerSimulator`, `Statevector`, visualisation Bloch.
4. **PennyLane** : `qml.device`, `@qml.qnode`, différentiation automatique de circuits.
5. **Physique expérimentale** : micro-ondes 2,45 GHz, plasmas basse-pression, pendules de torsion, cavités RF.

## Règles de sécurité

- Ne **jamais** minimiser les risques électriques (4 000 V), RF ou d'implosion décrits dans le README.
- Toute suggestion liée au matériel doit rappeler les précautions de sécurité pertinentes.

## Comportement attendu de l'agent

- Privilégier les **explications physiques** accompagnées des équations ($\LaTeX$ inline).
- Proposer du code **exécutable immédiatement** dans l'environnement du projet.
- Quand un résultat numérique est produit (simulation), toujours proposer une **visualisation** (plot ou Bloch).
- Si une expérience échoue à l'import Qiskit, prévoir un **fallback PennyLane** (cf. modèle de `001_superposition.py`).
- Utiliser `src/viz.py` pour les visualisations réutilisables ; ne pas dupliquer le code.
- Écrire les résultats de données dans `data/` au format NumPy (`.npy`) ou CSV.

## Conventions de diagrammes

- **Tous les diagrammes** (coupes, P&ID, schémas de câblage, vues du dessus, flowcharts…) doivent être produits en **SVG** et placés dans `docs/img/`.
- Référencer les SVG en Markdown via `![légende](img/nom.svg)`.
- Un **fallback ASCII** est conservé en commentaire HTML (`<!-- Fallback ASCII … -->`) pour le rendu dans les terminaux et diffs Git, mais le SVG est l'image de référence.
- Les SVG doivent avoir un **fond blanc** (`<rect width="100%" height="100%" fill="white"/>` en premier élément enfant du `<svg>`) pour garantir la lisibilité sur GitHub, dans les previews Markdown et en impression.
- Les traits, textes et bordures utilisent `currentColor` ou des couleurs foncées explicites (ex. `#222`) pour conserver le contraste sur fond blanc.
- Ne **jamais** utiliser de diagramme ASCII seul sans SVG correspondant dans un document finalisé.
