# 🔬 Bohemian Lab

**Laboratoire d'expérimentation en physique quantique**
*Propulsion par guidage d'onde pilote (de Broglie–Bohm)*

**Auteur :** Stéphane Denis, Expérimentateur Indépendant
**Date :** Mars 2026

---

## L'objectif en une phrase

> **Peut-on créer une force nette à l'intérieur d'une boîte fermée
> — sans rien éjecter ?**

La physique classique dit non. La mécanique quantique standard aussi.
L'interprétation de **de Broglie–Bohm** dit : *peut-être, si le
gradient quantique est asymétrique*. Cette expérience le **teste**.

---

## Pourquoi c'est important

![Résultat nul vs positif — dans les deux cas, le résultat est publiable](docs/img/resultats_dual.svg)

<!-- Fallback texte si le SVG ne s'affiche pas :
     • Résultat nul → borne supérieure publiable, contrainte pour la communauté
     • Résultat positif → violation 3ᵉ loi Newton, propulsion sans éjection -->

L'expérience ne *présuppose* pas un résultat positif :
elle le met à l'épreuve.

> 📖 L'analyse complète des implications est dans
> **[Implications d'un résultat positif](docs/07_implications.md)**.

---

## Comment ça marche — en 60 secondes

### 🌊 L'analogie de la vague

Imaginez une piscine fermée avec une machine à vagues à une extrémité.
Les vagues rebondissent contre les murs, créant des **interférences** —
des zones calmes et des zones agitées. Normalement, la piscine ne bouge
pas : les forces se compensent de tous les côtés.

Maintenant, placez un **obstacle asymétrique** dans la piscine — un
rocher en pente douce d'un côté et abrupt de l'autre. Les vagues sont
déviées : elles « poussent » plus fort d'un côté que de l'autre.

Dans notre expérience :
- La **piscine** → une chambre à vide en acier inoxydable
- Les **vagues** → des micro-ondes à 2,45 GHz (identiques à un four de cuisine)
- Le **rocher asymétrique** → un **plasma** de vapeur d'eau, plus dense
  d'un côté que de l'autre

![Schéma de l'expérience — chambre plasma, pendule de torsion, gradient asymétrique](docs/img/schema_experience.svg)

<!-- Fallback : Magnétron (700 W, 2,45 GHz) → ondes RF → plasma H₂O asymétrique
     dans chambre inox ⌀250mm, sur pendule de torsion dans baril 205 L. -->

### 🔬 La physique derrière

La **mécanique de de Broglie–Bohm** (1927/1952) prédit que chaque
photon suit une trajectoire **réelle**, guidée par une « onde pilote ».
Cette onde crée un **potentiel quantique** :

$$Q = -\frac{\hbar^2}{2m}\frac{\nabla^2 R}{R}$$

Si le plasma rend ce potentiel **asymétrique** ($\nabla Q \neq 0$),
une force nette apparaît — même à l'intérieur d'une boîte fermée.
C'est exactement ce que le pendule de torsion cherche à mesurer.

> 📖 L'analogie complète (double fente → cavité plasma → espace-temps
> courbe) est développée dans **[Objectifs Scientifiques](docs/01_objectifs.md)**.
> Le cadre mathématique est dans **[Cadre théorique](docs/02_theorie.md)**.

---

## Ce qu'on trouve dans ce dépôt

| Dossier | Contenu |
|:--------|:--------|
| [experiments/](experiments/) | **9 simulations** Python autonomes (Qiskit / PennyLane / NumPy) + **2 scripts d'acquisition/analyse empirique** |
| [notebooks/](notebooks/) | Notebooks Jupyter exploratoires |
| [src/](src/) | Modules Python réutilisables (visualisation, utilitaires) |
| [firmware/](firmware/) | Firmware ESP32 (PlatformIO) — lecture capteurs, PID plasma, émission série/MQTT |
| [data/](data/) | Résultats organisés en sous-dossiers : [`simulations/`](data/simulations/) (~40 fichiers `.png`, `.csv`, `.npy`, `.npz`) et [`empirique/`](data/empirique/) (données d'acquisition terrain) |
| [docs/](docs/) | 8 documents de référence : objectifs, théorie, matériel, protocole, sécurité, contrôle PID, implications, acquisition |

---

## Objectifs scientifiques

| # | Objectif | Ce qu'on mesure |
|:--|:---------|:----------------|
| 1 | **Force anomale en système fermé** | Existe-t-il une force au-delà de la pression de radiation classique ($P/c$) dans une chambre scellée ? Résultat positif ou nul → publiable. |
| 2 | **Gradient de phase asymétrique** | Comment un plasma inhomogène dévie les photons micro-ondes (comme un prisme courbe la lumière). Cartographié par les 8 tubes Nixie IN-13. |
| 3 | **Potentiel quantique mesurable** | Le potentiel quantique $Q = -\frac{\hbar^2}{2m}\frac{\nabla^2 R}{R}$ peut-il produire un effet mécanique ($F_Q = -\nabla Q$) détectable au pendule ? |

> 📖 **[Objectifs — documentation détaillée →](docs/01_objectifs.md)** —
> vulgarisation complète, analogie double fente → cavité → espace-temps,
> précédent EmDrive, critères de succès.

---

## 2. Cadre Théorique

### 2.1 La Loi de Guidage
Selon l'interprétation de de Broglie–Bohm (1927 / 1952), la particule possède une trajectoire réelle dictée par la phase $S$ de la fonction d'onde $\psi = R \, e^{iS/\hbar}$ :
$$\vec{v} = \frac{\nabla S}{m}$$
Pour un photon RF dans un plasma, le guidage s'exprime via le vecteur de Poynting, influencé par le gradient de l'indice de réfraction $n = \sqrt{1 - \omega_p^2/\omega^2}$.

### 2.2 Le Potentiel Quantique ($Q$)
La force « exotique » est générée par le potentiel quantique, qui dépend de la *forme* de l'amplitude $R$ — pas de son intensité absolue :
$$Q = -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R}$$
L'objectif est de créer un $\nabla Q$ asymétrique via un plasma inhomogène pour induire une force mécanique $F_Q = -\nabla Q$.

> 📐 **Modèle 3D** — Le [modèle plasma 3D](experiments/009_plasma_3d.py) montre que $\nabla Q$ possède une composante **verticale** dominante (ratio H/V ≈ 0,69, angle d'élévation ≈ −55°), due à la position du magnétron au sommet de la cavité. Seule la composante horizontale est mesurable par le pendule de torsion.

### 2.3 Force de Poussée Totale
La force mesurée sur le pivot est la résultante de la pression de radiation classique et de la contribution bohmienne :
$$F_{\text{totale}} = \frac{P_{\text{abs}}}{c} + \int \rho (-\nabla Q) \, dV$$

> � **3D** — L'intégrale volumique $\int \rho(-\nabla Q)\,dV$ est un vecteur 3D. La simulation [009_plasma_3d.py](experiments/009_plasma_3d.py) décompose cette force en composantes horizontale et verticale et montre que le pendule de torsion ne capte que $\sim 41\%$ de la force totale ($\cos 55° \approx 0{,}57$). Voir les résultats dans [data/simulations/009_decomposition_force.png](data/simulations/009_decomposition_force.png).

> �📖 **[Cadre théorique — documentation détaillée →](docs/02_theorie.md)** — historique, dérivation complète, application aux photons, références.

---

## 3. Configuration Matérielle

| Composant | Description Technique | Rôle |
| :--- | :--- | :--- |
| **Source** | 2× Magnétrons LG 2M213-01TAG (~700 W, 2,45 GHz, rendement ~ 65 %), un seul actif à la fois, fonctionnement à **200–400 W** via duty cycle SSR | Générateur de l'onde pilote (mode pulsé à $f = 1/T_0$), commutation A/B pour contrôle de la direction du gradient |
| **Enceinte / Chambre** | Chambre à vide inox 3 gal (Ø250×250 mm, 0–29 inHg) + couvercle acrylique 3/4" + grillage | Cage de Faraday, cavité RF, système isolé |
| **Enceinte pendule** | Baril de 205 L (acier, posé au sol) | Enceinte du pendule, double Faraday, rétention éclats, coupe-vent |
| **Médium** | Vapeur d'eau sous vide (1–5 mbar) → Plasma H-OH | Modulateur de phase non-linéaire |
| **Capteur** | 8× tubes Nixie IN-13 (octogone intérieur à la chambre) | Cartographie du gradient de densité plasma |
| **Mesure** | Balance de torsion sur fléau (Cavendish, $d = 200$ mm) + laser/PSD | Détection de la force de réaction |
| **Alimentation** | Batterie Li-ion Makita 18V (5 Ah) + onduleur 120V sinus pur | Alimentation embarquée — zéro câble |
| **Pompage** | Pompe à vide (palettes ou membrane) + vanne d'isolement DN10 | Cycle pump-seal-disconnect |
| **Protection RF** | Firmware soft-start SSR (rampe duty 3 % → 43 %) — magnétron consommable (~15 $) | Protection amorçage sans masse ajoutée. [§14](docs/14_adaptation_rf.md) |
| **Contrôle** | ESP32 embarqué + capteurs + Wi-Fi (PID, logging, télémétrie) | Homéostasie plasma autonome |
| **Observation** | Caméras sans fil (Wi-Fi) — fixes + mobiles | Vérification indépendante |

> 📖 **[Configuration matérielle — documentation détaillée →](docs/03_materiel.md)** — magnétron, blindage, modes de cavité, plasma, pendule.

---

## 4. Protocole de Validation et Objections

### 4.1 Élimination des biais (Faux positifs)
* **Vent Ionique :** Neutralisé par le confinement hermétique sous vide. Contrôle : test avec gaz noble (argon).
* **Effet Thermique :** Réduit par des tirs RF pulsés (séparation fréquentielle signal/thermique). Contrôle : charge fantôme (eau liquide).
* **Forces Électromagnétiques :** Contrôle par inversion à 180° du dispositif interne + blindage mu-métal.

### 4.2 Procédure de test
1. Mise sous vide de la chambre et injection capillaire de vapeur d'eau (1–5 mbar).
2. Calibration du pendule : détermination de la période de résonance $T_0$ et de la constante de torsion $\kappa$.
3. Activation pulsée du magnétron ($f = 1/T_0$) pour amplifier le mouvement par résonance mécanique.
4. Mesure du déplacement angulaire par **réflexion laser + PSD** (photodétecteur linéaire) à l'intérieur du baril. Corrélation croisée avec le signal de commande (objectif : SNR > 3).
5. Tests de contrôle : inversion 180°, gaz noble, vide sans plasma.

> 📖 **[Protocole de validation — documentation détaillée →](docs/04_protocole.md)** — analyse de données, critères de succès, objections anticipées.

---

## 5. Notes de Sécurité

* **Risque RF :** Vérification de l'étanchéité de la chambre avant chaque session (fuites < 5 mW/cm² selon ICNIRP / IEEE C95.1). Double confinement par le baril de 205L.
* **Haute Tension :** Isolation du transformateur (4 000 V / 300 mA). **Danger de mort.** Toujours décharger le condensateur avant intervention (énergie résiduelle ~ 8 J).
* **Implosion :** Couvercle acrylique 3/4" (19 mm), chambre certifiée 29 inHg. Grillage de protection + baril de confinement (rétention d'éclats).
* **Urgences : 911.**
* **Gaz :** Expérience en extérieur (ventilation naturelle). Se positionner dos au vent lors de l'ouverture du baril.
* **Météo :** Pas de pluie, pas d'orage. Le pendule est protégé du vent par le baril.
* **Règle absolue :** Toujours travailler **à deux personnes**.

> ⚠️ **[Notes de sécurité — documentation détaillée →](docs/05_securite.md)** — Normes, calculs, checklist pré-expérience. Lecture obligatoire avant toute manipulation.

---

## � Simulations Numériques

Le dossier `experiments/` contient les scripts de simulation autonomes
(un fichier par expérience, exécutable directement) :

| # | Expérience | Description |
|:--|:-----------|:------------|
| 001 | [001_superposition.py](experiments/001_superposition.py) | Superposition quantique — circuit Hadamard, sphère de Bloch |
| 002 | [002_modes_cavite.py](experiments/002_modes_cavite.py) | Modes de résonance TM/TE de la cavité cylindrique |
| 003 | [003_profil_plasma.py](experiments/003_profil_plasma.py) | Profil plasma 2D — densité $n_e(r,\theta)$, potentiel quantique $Q$, force $F_Q$ |
| 004 | [004_trajectoires_bohm.py](experiments/004_trajectoires_bohm.py) | Trajectoires bohmiennes — intégration de $\vec{v} = \nabla S / m$ |
| 005 | [005_phase_circuit.py](experiments/005_phase_circuit.py) | Circuits quantiques et accumulation de phase — portes $R_z$, interféromètre, gradient 8 qubits |
| 006 | [006_analyse_signal.py](experiments/006_analyse_signal.py) | Analyse de signal — corrélation croisée, filtrage, extraction SNR |
| 007 | [007_dynamique_pid.py](experiments/007_dynamique_pid.py) | Dynamique du plasma et boucles PID — simulation ODE couplée, auto-tuning |
| 008 | [008_sensibilite_eta.py](experiments/008_sensibilite_eta.py) | Analyse Monte-Carlo de sensibilité sur $\eta$ et estimation des faux positifs |
| **009** | [**009_plasma_3d.py**](experiments/009_plasma_3d.py) | **Modèle 3D complet** — $n_e(r,\theta,z)$, champ EM multimode, force bohmienne 3D, décomposition H/V |

### 🔧 Scripts d'acquisition et d'analyse empirique

| # | Script | Description |
|:--|:-------|:------------|
| 010 | [010_acquisition.py](experiments/010_acquisition.py) | **Acquisition terrain** — lecture ESP32 (série/MQTT), écriture CSV dans `data/empirique/`, horodatage, métadonnées |
| 011 | [011_analyse_empirique.py](experiments/011_analyse_empirique.py) | **Analyse empirique** — filtrage, corrélation croisée, extraction de force, calcul $\eta$, comparaison théorie, mode campagne |

> 📊 Les résultats de simulation sont dans `data/simulations/` — préfixés par
> le numéro de l'expérience (ex. `data/simulations/009_*.png`, `data/simulations/009_*.csv`).
> Les données empiriques sont enregistrées dans `data/empirique/` par le script 010.

---

## �📖 Documentation Détaillée

| # | Section | Fichier |
|:--|:--------|:--------|
| 1 | Objectifs Scientifiques | [docs/01_objectifs.md](docs/01_objectifs.md) |
| 2 | Cadre Théorique | [docs/02_theorie.md](docs/02_theorie.md) |
| 3 | Configuration Matérielle | [docs/03_materiel.md](docs/03_materiel.md) |
| 4 | Protocole de Validation | [docs/04_protocole.md](docs/04_protocole.md) |
| 5 | Notes de Sécurité | [docs/05_securite.md](docs/05_securite.md) |
| 6 | Contrôle et Asservissement | [docs/06_controle.md](docs/06_controle.md) |
| 7 | Implications d'un Résultat Positif | [docs/07_implications.md](docs/07_implications.md) |
| 8 | Chaîne d'Acquisition Empirique | [docs/08_acquisition.md](docs/08_acquisition.md) |
| 9 | Hypothèse Inverter | [docs/09_hypothese_inverter.md](docs/09_hypothese_inverter.md) |
| 10 | Capteur Spectral AS7343 | [docs/10_capteur_spectral.md](docs/10_capteur_spectral.md) |
| 11 | Pistes d'Optimisation Plasma | [docs/11_pistes_optimisation.md](docs/11_pistes_optimisation.md) |
| 12 | Contrôle de la Vapeur d'Eau | [docs/12_controle_vapeur.md](docs/12_controle_vapeur.md) |
| 13 | Justification du Médium | [docs/13_justification_medium.md](docs/13_justification_medium.md) |
| **14** | **Adaptation RF et Amorçage** | **[docs/14_adaptation_rf.md](docs/14_adaptation_rf.md)** |
