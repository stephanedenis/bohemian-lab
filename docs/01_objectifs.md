# Objectifs Scientifiques

[← Retour au README](../README.md)

---

## Introduction vulgarisée

Imaginez que vous souffliez dans un sifflet : l'air vibre, et cette vibration crée
un son qui se propage dans une direction. Maintenant, imaginez que ce « souffle » soit
une onde électromagnétique (comme celles de votre four micro-ondes) et que le
« sifflet » soit un nuage de plasma — un gaz ionisé qui brille comme un petit éclair.

En manipulant la façon dont l'onde
se propage à travers ce plasma, on espère créer une **poussée mécanique** — une force
qui déplacerait physiquement l'appareil. C'est un peu comme si la lumière pouvait
« pousser » la boîte dans laquelle elle est enfermée, non pas seulement par la
classique pression de radiation (effet connu et minuscule), mais grâce à un effet
prédit par la **mécanique bohmienne** — une interprétation de la physique quantique
où les particules suivent de vraies trajectoires guidées par une « onde pilote ».

---

## Objectif 1 — Démontrer une force de poussée en système fermé

> 💡 **En termes simples** — Imaginez une boîte fermée posée sur une
> table. À l'intérieur, quelqu'un pousse contre les murs. La boîte
> ne bouge pas, parce que pousser le mur de gauche revient à pousser
> le mur de droite dans l'autre sens : les forces s'annulent. C'est la
> [3ᵉ loi de Newton](https://fr.wikipedia.org/wiki/Lois_du_mouvement_de_Newton#Troisi%C3%A8me_loi_de_Newton).
> Si notre boîte (la chambre) bouge quand même, c'est qu'il se passe
> quelque chose de **très inhabituel** à l'intérieur — quelque chose
> que la physique classique ne prédit pas.

### Énoncé

Démontrer l'existence d'une force de poussée macroscopique dans un système
fermé (chambre à vide inox de 3 gallons), c'est-à-dire **sans éjection
de masse ni échange avec l'extérieur**.

### Contexte physique

La conservation de la quantité de mouvement dans un système isolé est un
principe fondamental de la mécanique classique (3ᵉ loi de Newton). Toute
force mesurée dans un système fermé sans éjection de matière constituerait
une anomalie exigeant une explication théorique nouvelle.

Dans le cadre bohmien, la force additionnelle provient du **potentiel quantique**
$Q$, qui n'a pas d'analogue classique. Le potentiel quantique peut produire
un transfert de quantité de mouvement entre le champ et la matière qui n'est
pas entièrement capturé par la pression de radiation standard :

$$F_Q = -\nabla Q = -\nabla \left( -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R} \right)$$

> ⚠️ **Ce n'est pas une fusée** — Le mécanisme de poussée ici est
> fondamentalement différent d'un moteur à réaction. Dans une fusée,
> des gaz brûlés **s'échappent** (système ouvert) et la fusée recule
> par réaction (3ᵉ loi de Newton). Ici, **rien ne sort** : le plasma
> reste enfermé dans la chambre hermtique.
>
> La force provient du **gradient du potentiel quantique** $\nabla Q$
> dans le plasma. Le $Q$ est maximal près du magnétron (champ intense,
> gradient de $n_e$ abrupt, forte courbure de $R$) et la force
> $F = -\nabla Q$ pousse la chambre vers la zone de plus faible $Q$
> — c'est-à-dire **à l'opposé du magnétron**.
>
> L'analogie correcte est la **pression de radiation** : un photon
> qui frappe un miroir le pousse *sans s'échapper*. De même, l'onde
> micro-onde interagit avec le gradient de plasma et exerce une
> poussée sur la paroi — dans un système totalement fermé.
> Voir le [diagramme de torsion](03_materiel.md#schéma-de-lexpérience-de-torsion)
> pour la géométrie détaillée.

### Critère de succès

Un déplacement reproductible du pendule de torsion, corrélé temporellement
avec l'activation du magnétron, et **non explicable** par les artefacts connus
(vent ionique, effets thermiques, forces EM résiduelles).

### Pertinence

Si une telle force était confirmée, elle ouvrirait un champ d'investigation
fondamental sur les transferts de quantité de mouvement médiés par le
potentiel quantique — indépendamment de toute application.

---

## Objectif 2 — Quantifier le gradient de phase asymétrique

> 💡 **En termes simples** — Quand la lumière traverse un verre inégalement
> épais (comme un prisme), elle dévie. Pourquoi ? Parce qu'un côté du
> verre « ralentit » la lumière plus que l'autre. Notre plasma joue le
> rôle du prisme : si un côté est plus dense en électrons, l'onde
> micro-onde y voyage plus lentement, ce qui crée un « gradient de phase ».
> Dans la théorie de Bohm, ce gradient dicte la direction de la force.
> Les 8 tubes Nixie IN-13 servent de carte du gradient : plus la colonne
> lumineuse est longue, plus le plasma est dense à cet endroit.

### Énoncé

Quantifier l'influence d'un **gradient de phase asymétrique** sur la
trajectoire des photons RF à 2,45 GHz traversant un milieu plasma.

### Contexte physique

Dans la théorie de de Broglie–Bohm, la vitesse d'une particule est dictée
par le gradient de la phase $S$ de la fonction d'onde :

$$\vec{v} = \frac{\nabla S}{m}$$

Un plasma de vapeur d'eau est un milieu **dispersif et non-linéaire** : son
indice de réfraction dépend de la densité électronique locale, ce qui
modifie la phase de l'onde qui le traverse. En créant une distribution
spatiale inhomogène du plasma — plus dense d'un côté que de l'autre — on
impose un $\nabla S$ asymétrique.

L'indice de réfraction d'un plasma non-magnétisé est :

$$n = \sqrt{1 - \frac{\omega_p^2}{\omega^2}}$$

où $\omega_p = \sqrt{n_e e^2 / (\varepsilon_0 m_e)}$ est la pulsation plasma.
Un gradient de densité électronique $n_e$ produit donc un gradient d'indice,
et par conséquent un gradient de phase.

### Méthode de mesure

Les **8 tubes Nixie IN-13**, disposés en octogone sur la paroi interne de
la chambre (espacés de 45°), servent de capteurs visuels de la luminosité
du plasma, fournissant une cartographie angulaire du gradient de densité
$n_e$. La corrélation entre la direction de l'asymétrie Nixie et la
direction de la force détectée au pendule est le test clé de l'Objectif 2
(voir la [matrice décisionnelle](04_protocole.md#46-attentes-concrètes--confirmer-ou-infirmer-lhypothèse)).

---

## Objectif 3 — Valider l'interaction potentiel quantique / plasma

> 💡 **En termes simples** — La physique classique prédit qu'un faisceau
> de lumière de 1 kW peut pousser un objet avec une force de ~ 3,3 µN
> (micro-newtons) — le poids d'un grain de poussière. C'est la
> [pression de radiation](https://fr.wikipedia.org/wiki/Pression_de_radiation),
> démontrée expérimentalement par [Lebedev](https://fr.wikipedia.org/wiki/Piotr_Lebedev)
> en 1901. Si on mesure une force **supérieure** à cette valeur,
> l'excédent ne peut pas être expliqué par la physique classique.
> C'est précisément ce que prédit le potentiel quantique de Bohm.

### Énoncé

Valider expérimentalement que l'interaction entre le **potentiel quantique
de Bohm** et un **plasma de vapeur d'eau** sous vide peut produire un effet
mécanique mesurable.

### Contexte physique

Le potentiel quantique $Q$ dépend de l'amplitude $R$ de la fonction d'onde
($\psi = R \, e^{i S / \hbar}$). Dans un plasma, les processus de
diffusion, d'absorption et d'émission stimulée modifient l'amplitude $R$
de manière spatialement inhomogène. Selon l'équation de Bohm :

$$Q = -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R}$$

Une modification locale de $R$ (par exemple via un nœud de densité
électronique) crée un $\nabla Q$ non nul, et donc une force sur les
entités guidées.

La force totale mesurable est la somme de la pression de radiation
classique et de la contribution bohmienne :

$$F_{\text{totale}} = \frac{P_{\text{abs}}}{c} + \int \rho \, (-\nabla Q) \, dV$$

### Défi expérimental

La pression de radiation classique pour 1 kW absorbé est de l'ordre de :

$$F_{\text{rad}} = \frac{P}{c} = \frac{1000}{3 \times 10^8} \approx 3{,}3 \; \mu\text{N}$$

Le pendule de torsion doit donc être suffisamment sensible pour détecter
des forces de cet ordre de grandeur, et toute composante supérieure serait
attribuable à l'effet de guidage bohmien.

---

## Références

1. **Bohm, D.** (1952). « A Suggested Interpretation of the Quantum Theory
   in Terms of "Hidden" Variables, I & II ». *Physical Review*, 85(2),
   166–179 & 180–193.
   [doi:10.1103/PhysRev.85.166](https://doi.org/10.1103/PhysRev.85.166)

2. **Holland, P. R.** (1993). *The Quantum Theory of Motion: An Account
   of the de Broglie–Bohm Causal Interpretation of Quantum Mechanics*.
   Cambridge University Press.
   ISBN 978-0-521-48543-2.

3. **Bell, J. S.** (1987). *Speakable and Unspeakable in Quantum Mechanics*.
   Cambridge University Press.
   ISBN 978-0-521-36869-8.

4. **de Broglie, L.** (1928). « La nouvelle dynamique des quanta ».
   *Électrons et Photons : Rapports et Discussions du Cinquième Conseil
   de Physique*, Solvay, pp. 105–132.

5. **Dürr, D., Goldstein, S. & Zanghì, N.** (1992). « Quantum Equilibrium
   and the Origin of Absolute Uncertainty ». *Journal of Statistical
   Physics*, 67, 843–907.
   [doi:10.1007/BF01049004](https://doi.org/10.1007/BF01049004)

6. **Maxwell, J. C.** (1873). *A Treatise on Electricity and Magnetism*.
   Clarendon Press, Oxford.
   (Prédiction théorique de la pression de radiation.)

7. **Lebedev, P.** (1901). « Experimental Examination of Light Pressure ».
   *Annalen der Physik*, 311(11), 433–458.
   [doi:10.1002/andp.19013111102](https://doi.org/10.1002/andp.19013111102)
   (Première confirmation expérimentale de $F = P/c$.)

8. **Chen, F. F.** (2016). *Introduction to Plasma Physics and Controlled
   Fusion*. 3ᵉ édition, Springer. ISBN 978-3-319-22308-7.
   (Indice de réfraction du plasma, pulsation plasma $\omega_p$.)

---

[← Retour au README](../README.md) · [Section suivante : Cadre Théorique →](02_theorie.md)
