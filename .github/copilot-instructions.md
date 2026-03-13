# 🔬 Bohemian Lab — Instructions pour l'Agent IA

## Identité du projet

**Bohemian Lab** est un laboratoire d'expérimentation en physique quantique piloté par un ingénieur indépendant.
Le projet explore la **mécanique bohmienne** (interprétation de de Broglie–Bohm)
à travers des simulations numériques et une expérience matérielle de propulsion
par guidage d'onde pilote dans un plasma de vapeur d'eau.

## Stack technique

| Couche | Outils |
|---|---|
| **Simulations quantiques** | Python 3.11+, Qiskit (IBM), PennyLane (Xanadu) |
| **Calcul scientifique** | NumPy, SciPy, SymPy |
| **Visualisation** | Matplotlib, JupyterLab, Qiskit Visualization |
| **Firmware / Hardware** | C/C++ (C++11/14), ESP32 (Arduino Core via PlatformIO), FreeRTOS |
| **Capteurs (I²C / SPI)** | AS7343 + AS7331 (Spectral), ADS1115 + ZJ-52T (Vide), MAX31855 (Température) |
| **Télémétrie** | WiFi, MQTT, carte SD |

## Structure du dépôt

```
bohemian-lab/
├── experiments/     # Scripts Python exécutables (un fichier par expérience)
│                    #   Convention : NNN_nom.py  (ex: 001_superposition.py)
├── firmware/        # Code embarqué ESP32 (PlatformIO)
│   ├── src/         # Main et tâches FreeRTOS (.cpp)
│   └── platformio.ini # Configuration matérielle et dépendances
├── notebooks/       # Jupyter Notebooks exploratoires
├── src/             # Modules Python réutilisables (viz, utils, etc.)
├── data/            # Données brutes et résultats (.npy, .csv, .json)
├── docs/            # Documentation technique et physique détaillée
├── requirements.txt # Dépendances pip (Python)
└── README.md        # Protocole expérimental principal
```

## Conventions de code

**Règle générale :**
- **Langue** : le code, les commentaires, les docstrings et les messages de commit sont en **français** ou en anglais technique selon le standard du langage.
- Les interfaces utilisateurs, les logs séries et la documentation restent en français.

**Python (Simulation & Data) :**
- **Style** : PEP 8, largeur max 88 colonnes (Black-compatible).
- **Docstrings** : Google-style, en français.
- **Typage** : annotations de type systématiques (Python 3.11+ syntax : `list[int]`, `tuple[float, …]`).
- **Expériences** : Chaque fichier dans `experiments/` est un script autonome (`if __name__ == "__main__"`).

**C++ / Firmware (ESP32) :**
- **Architecture** : Utiliser **FreeRTOS** (`xTaskCreate`, `vTaskDelay`, `xQueueSend`).
- Ne **jamais** utiliser la fonction bloquante `delay()` dans les boucles principales.
- Organiser le code en séparant les tâches de manière logique (Acquisition I²C, Contrôle PID, Communication MQTT).
- Gérer explicitement les échecs de communication capteur (bus I²C défaillant) sans faire crasher l'OS complet.

## Contexte scientifique

L'agent doit maîtriser les concepts suivants pour aider efficacement :

1. **La Théorie de de Broglie–Bohm** : loi de guidage $\vec{v} = \nabla S / m$, violant potentiellement le théorème d'action-réaction en état de **non-équilibre quantique**.
2. **Physique des plasmas** : Coupure résonante 2,45 GHz à $n_{e,c} \approx 7,4 \times 10^{16} \, \text{m}^{-3}$, créant la "falaise d'indice de réfraction" ($n \to 0$).
3. **Contrôle temps réel** : La nécessité absolue d'asservir la pression de vapeur d'eau et le magnétron via des boucles PID stabilisant l'émission optique (ratios H$\alpha$/H$\beta$ et présence de OH·).
4. **Qiskit & PennyLane** : `QuantumCircuit`, `AerSimulator`, différentiation automatique pour l'émulation du phénomène.

## Règles de sécurité

- Ne **jamais** minimiser les risques électriques (4 000 V), RF (micro-ondes) ou d'implosion associés aux protocoles.
- Toute suggestion liée au matériel (câblage relai, firmware de puissance) doit appeler à des précautions de conception logicielle (Fail-safe, Watchdog).

## Comportement attendu de l'agent

- Quand le contexte est "Python", agir comme un chercheur en physique : proposer des explications basées sur $\LaTeX$ et des graphiques.
- Quand le contexte est `firmware/` ou "C++", agir comme un Ingénieur en Système Embarqué : optimiser les cycles I²C, respecter les timings FreeRTOS, et garantir la robustesse temporelle des boucles PID.
- Tous les diagrammes doivent être gérés en SVG (dans `docs/img/`) et inclus en tant qu'images, avec de simples fallbacks ASCII en commentaires HTML.
