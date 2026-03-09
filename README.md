# 🔬 Bohemian Lab

**Expérimentations en physique quantique** 

# Protocole Expérimental : Propulsion par Guidage d'Onde Pilote (Bohm)

**Auteur :** Expérimentateur Indépendant
**Date :** Mars 2026
**Sujet :** Étude de la force de réaction issue de la manipulation d'un potentiel quantique via un plasma de vapeur d'eau en cavité RF.

---

## 1. Objectifs Scientifiques
1. **Démontrer** l'existence d'une force de poussée dans un système fermé (baril de 205L).
2. **Quantifier** l'influence d'un gradient de phase asymétrique sur la trajectoire des photons RF (2,45 GHz).
3. **Valider** l'interaction entre le potentiel quantique de Bohm et un plasma de vapeur d'eau sous vide.

---

## 2. Cadre Théorique

### 2.1 La Loi de Guidage
Selon l'interprétation de de Broglie-Bohm, la particule possède une trajectoire réelle dictée par la phase $S$ de la fonction d'onde $\psi$ :
$$\vec{v} = \frac{\nabla S}{m}$$
Pour un photon, le guidage s'exprime par la direction du vecteur de propagation, influencé par le gradient de phase imposé par le milieu (plasma).

### 2.2 Le Potentiel Quantique ($Q$)
La force "exotique" est générée par le potentiel quantique, qui dépend de l'amplitude $R$ de l'onde :
$$Q = -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R}$$
L'objectif de l'expérience est de créer un $\nabla Q$ asymétrique pour induire une force mécanique $F_Q = -\nabla Q$.

### 2.3 Force de Poussée Totale
La force mesurée sur le pivot est la résultante de la pression de radiation et de l'effet de guidage :
$$F_{totale} = \frac{P_{abs}}{c} + \int \rho (-\nabla Q) \, dV$$

---

## 3. Configuration Matérielle

| Composant | Description Technique | Rôle |
| :--- | :--- | :--- |
| **Source** | Magnétron de 1000W (2,45 GHz) | Générateur de l'onde pilote |
| **Enceinte** | Baril de 205L (Métal) | Cage de Faraday et système isolé |
| **Chambre** | Cylindre métal + Couvercle Plexiglas | Confinement du vide et du plasma |
| **Médium** | Vapeur d'eau (Plasma H-OH) | Modulateur de phase non-linéaire |
| **Capteur** | Tubes Nixie linéaires (IN-9/13) | Visualisation du flux et gradient |
| **Mesure** | Pendule de torsion / Balance | Détection de la force de réaction |

---

## 4. Protocole de Validation et Objections

### 4.1 Élimination des biais (Faux positifs)
* **Vent Ionique :** Neutralisé par le confinement hermétique de la chambre à vide.
* **Effet Thermique :** Réduit par des tirs RF pulsés et l'absorption des ondes par une masse d'eau (charge fantôme).
* **Forces Électromagnétiques :** Vérifiées par inversion à 180° du dispositif interne.

### 4.2 Procédure de test
1. Mise sous vide de la chambre et injection capillaire de vapeur d'eau.
2. Détermination de la période de résonance du baril $T_0$.
3. Activation pulsée du magnétron ($f = 1/T_0$) pour amplifier le mouvement.
4. Analyse vidéo du déplacement du bras de torsion synchronisé avec l'allumage du plasma.

---

## 5. Notes de Sécurité
* **Risque RF :** Vérification de l'étanchéité du baril (fuites < 5mW/cm²).
* **Haute Tension :** Isolation du transformateur (4000V). Danger de mort.
* **Implosion :** Vérification de l'épaisseur du Plexiglas sous vide (min. 15mm).
* **Gaz :** Ventilation obligatoire pour évacuer l'ozone et les NOx produits par le plasma.

---
*Document généré pour assistance à l'expérimentation de physique non-conventionnelle.*