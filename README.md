# Bohemian Lab

Expérimentations en physique quantique : Propulsion par Guidage d'Onde Pilote (Bohm)

**Auteur :** Stéphane Denis, Expérimentateur Indépendant

**Date :** Mars 2026

**Sujet :** Étude de la force de réaction issue de la manipulation d'un potentiel quantique via un plasma de vapeur d'eau en cavité RF.

---

## 1. Objectifs Scientifiques

1. **Démontrer** l'existence d'une force de poussée macroscopique dans un système fermé (baril de 205L), sans éjection de masse ni échange avec l'extérieur.
2. **Quantifier** l'influence d'un gradient de phase asymétrique sur la trajectoire des photons RF (2,45 GHz) traversant un milieu plasma inhomogène.
3. **Valider** expérimentalement l'interaction entre le potentiel quantique de Bohm ($Q = -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R}$) et un plasma de vapeur d'eau sous vide, en mesurant un éventuel excès de force au-delà de la pression de radiation classique ($F_{\text{rad}} = P/c \approx 3{,}3 \; \mu\text{N}$ pour 1 kW).

> 📖 **[Objectifs — documentation détaillée →](docs/01_objectifs.md)**

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

### 2.3 Force de Poussée Totale
La force mesurée sur le pivot est la résultante de la pression de radiation classique et de la contribution bohmienne :
$$F_{\text{totale}} = \frac{P_{\text{abs}}}{c} + \int \rho (-\nabla Q) \, dV$$

> 📖 **[Cadre théorique — documentation détaillée →](docs/02_theorie.md)** — historique, dérivation complète, application aux photons, références.

---

## 3. Configuration Matérielle

| Composant | Description Technique | Rôle |
| :--- | :--- | :--- |
| **Source** | Magnétron à cavité de 1 000 W (2,45 GHz, rendement ~ 65 %) | Générateur de l'onde pilote (mode pulsé à $f = 1/T_0$) |
| **Enceinte** | Baril de 205 L (acier, atténuation > 40 dB) | Cage de Faraday et système isolé |
| **Chambre** | Cylindre métal + Couvercle Plexiglas (≥ 15 mm) | Confinement du vide et du plasma |
| **Médium** | Vapeur d'eau sous vide (1–5 mbar) → Plasma H-OH | Modulateur de phase non-linéaire |
| **Capteur** | Tubes Nixie linéaires (IN-9 / IN-13) | Cartographie du flux RF et du gradient |
| **Mesure** | Pendule de torsion (calibré par $\kappa = 4\pi^2 I / T_0^2$) | Détection de la force de réaction |
| **Contrôle** | Microcontrôleur ESP32 + capteurs (pression, $P_r$, lumière, temp.) | Homéostasie plasma (boucle PID) |

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
4. Analyse vidéo du déplacement du bras de torsion, corrélation croisée avec le signal de commande (objectif : SNR > 3).
5. Tests de contrôle : inversion 180°, gaz noble, vide sans plasma.

> 📖 **[Protocole de validation — documentation détaillée →](docs/04_protocole.md)** — analyse de données, critères de succès, objections anticipées.

---

## 5. Notes de Sécurité

* **Risque RF :** Vérification de l'étanchéité du baril avant chaque session (fuites < 5 mW/cm² selon ICNIRP / IEEE C95.1).
* **Haute Tension :** Isolation du transformateur (4 000 V / 300 mA). **Danger de mort.** Toujours décharger le condensateur avant intervention (énergie résiduelle ~ 8 J).
* **Implosion :** Épaisseur du Plexiglas ≥ 15 mm (facteur de sécurité ×3). Grillage de protection devant le hublot.
* **Gaz :** Ventilation mécanique obligatoire pour évacuer l'ozone (O₃, VLEP 0,1 ppm) et les NOₓ produits par le plasma.
* **Règle absolue :** Toujours travailler **à deux personnes**.

> ⚠️ **[Notes de sécurité — documentation détaillée →](docs/05_securite.md)** — Normes, calculs, checklist pré-expérience. Lecture obligatoire avant toute manipulation.

---

## 📖 Documentation Détaillée

| # | Section | Fichier |
|:--|:--------|:--------|
| 1 | Objectifs Scientifiques | [docs/01_objectifs.md](docs/01_objectifs.md) |
| 2 | Cadre Théorique | [docs/02_theorie.md](docs/02_theorie.md) |
| 3 | Configuration Matérielle | [docs/03_materiel.md](docs/03_materiel.md) |
| 4 | Protocole de Validation | [docs/04_protocole.md](docs/04_protocole.md) |
| 5 | Notes de Sécurité | [docs/05_securite.md](docs/05_securite.md) |
