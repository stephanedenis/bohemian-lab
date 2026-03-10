# Bohemian Lab

Expérimentations en physique quantique : Propulsion par Guidage d'Onde Pilote (Bohm)

**Auteur :** Stéphane Denis, Expérimentateur Indépendant

**Date :** Mars 2026

**Sujet :** Étude de la force de réaction issue de la manipulation d'un potentiel quantique via un plasma de vapeur d'eau en cavité RF.

---

## 1. Objectifs Scientifiques

1. **Démontrer** l'existence d'une force de poussée macroscopique dans un système fermé (chambre à vide inox 3 gallons), sans éjection de masse ni échange avec l'extérieur.
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
| **Enceinte / Chambre** | Chambre à vide inox 3 gal (Ø250×250 mm, 0–29 inHg) + couvercle acrylique 3/4" + grillage | Cage de Faraday, cavité RF, système isolé |
| **Enceinte pendule** | Baril de 205 L (acier, posé au sol) | Enceinte du pendule, double Faraday, rétention éclats, coupe-vent |
| **Médium** | Vapeur d'eau sous vide (1–5 mbar) → Plasma H-OH | Modulateur de phase non-linéaire |
| **Capteur** | 8× tubes Nixie IN-13 (octogone intérieur à la chambre) | Cartographie du gradient de densité plasma |
| **Mesure** | Balance de torsion sur fléau (Cavendish, $d = 200$ mm) + laser/PSD | Détection de la force de réaction |
| **Alimentation** | Batterie Li-ion Makita 18V (5 Ah) + onduleur 120V sinus pur | Alimentation embarquée — zéro câble |
| **Pompage** | Pompe à vide (palettes ou membrane) + vanne d'isolement DN10 | Cycle pump-seal-disconnect |
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

## 📖 Documentation Détaillée

| # | Section | Fichier |
|:--|:--------|:--------|
| 1 | Objectifs Scientifiques | [docs/01_objectifs.md](docs/01_objectifs.md) |
| 2 | Cadre Théorique | [docs/02_theorie.md](docs/02_theorie.md) |
| 3 | Configuration Matérielle | [docs/03_materiel.md](docs/03_materiel.md) |
| 4 | Protocole de Validation | [docs/04_protocole.md](docs/04_protocole.md) |
| 5 | Notes de Sécurité | [docs/05_securite.md](docs/05_securite.md) |
