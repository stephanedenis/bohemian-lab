# Objectifs Scientifiques

[← Retour au README](../README.md)

---

## Introduction vulgarisée

Imaginez que vous souffliez dans un sifflet : l'air vibre, et cette vibration crée
un son qui se propage dans une direction. Maintenant, imaginez que ce « souffle » soit
une onde électromagnétique (comme celles de votre four micro-ondes) et que le
« sifflet » soit un nuage de plasma — un gaz ionisé qui brille comme un petit éclair.

En manipulant la façon dont l'onde se propage à travers ce plasma, on cherche à
détecter si une **force mécanique anomale** — au-delà de la pression de radiation
classique — apparaît dans un système totalement fermé. La **mécanique bohmienne**
(une interprétation de la physique quantique où les particules suivent de vraies
trajectoires guidées par une « onde pilote ») prédit l'existence d'une telle force.
Mais d'autres interprétations — et le principe classique d'action/réaction —
prédisent une force nette **nulle**. L'expérience tranche.

---

## Intuition fondatrice — de la double fente à la cavité plasma

> 💡 **En termes simples** — Dans l'expérience de la
> [double fente](https://fr.wikipedia.org/wiki/Fentes_de_Young), un
> photon passe « par les deux fentes à la fois » (du point de vue de
> l'onde) et crée des franges d'interférence de l'autre côté. Dans
> l'interprétation de Bohm, le photon passe par **une seule** fente,
> mais le potentiel quantique $Q$ — créé par l'interférence des deux
> ondes — le **dévie systématiquement** vers les franges claires.
>
> L'idée fondatrice de cette expérience est de reproduire cet effet
> **à l'intérieur d'une cavité** : le plasma joue le rôle d'une
> « fente variable » qui replie la fonction d'onde sur elle-même,
> forçant une déviation nette du flux de photons. Et cette déviation
> — une force — est formellement identique à ce que produirait une
> **courbure de l'espace-temps**.

### La double fente vue par Bohm

Dans la double fente classique, l'onde pilote $\psi$ passe par les deux
ouvertures et interfère au-delà. Le potentiel quantique résultant :

$$Q = -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R}$$

possède une structure spatiale très riche : des **crêtes** (aux
inter-franges sombres, où $R \to 0$ et $\nabla^2 R / R$ diverge) et
des **vallées** (aux franges brillantes). Les trajectoires bohmiennes
sont canalisées par ces vallées — comme de l'eau dans des rigoles.

Le point crucial : la déviation est **systématique et déterministe**.
Les particules passant par la fente du haut sont **toujours** courbées
vers le haut ; celles du bas, vers le bas. Il n'y a pas de croisement
(propriété de non-croisement des trajectoires bohmiennes en 2D). Le
potentiel quantique impose un **aiguillage** — pas un hasard.

> 📐 **Simulation** — Le script
> [004_trajectoires_bohm.py](../experiments/004_trajectoires_bohm.py)
> visualise ces trajectoires bohmiennes dans le scénario double fente.

### La cavité plasma comme « double fente repliée »

L'intuition fondatrice est la suivante : dans une cavité RF, une onde
stationnaire est un **système de fentes replié sur lui-même**. Les
nœuds du champ EM jouent le rôle des parois opaques entre les fentes ;
les ventres jouent le rôle des ouvertures. Le mode TM₃₁₀ (3 nœuds
azimutaux) crée effectivement **6 « fentes » en anneau** dans la
cavité.

Le plasma introduit l'**asymétrie** absente de la double fente
classique. Il modifie l'indice de réfraction de façon inhomogène :
plus dense d'un côté (près du magnétron) que de l'autre. L'effet est
de **déformer les fentes** — certaines deviennent plus étroites
(plasma opaque, $n_e > n_{e,c}$), d'autres restent ouvertes (plasma
sous-critique). L'interférence résultante n'est plus symétrique :

- Double fente symétrique → diffraction symétrique → force nette = 0
- « Fentes » asymétriques (plasma) → diffraction asymétrique → $\nabla Q \neq 0$ → **force nette**

C'est le « repliement » de la fonction d'onde : l'onde qui rebondit
dans la cavité interfère avec elle-même des milliers de fois
(facteur $Q$), accumulant une asymétrie de phase à chaque passage
à travers le plasma.

### Équivalence formelle avec la courbure espace-temps

Holland (1993, chap. 12) a montré que l'équation de Hamilton-Jacobi
bohmienne :

$$\frac{\partial S}{\partial t} + \frac{(\nabla S)^2}{2m} + V + Q = 0$$

est formellement identique à l'équation des
[géodésiques](https://fr.wikipedia.org/wiki/G%C3%A9od%C3%A9sique)
dans un espace-temps dont la métrique serait modifiée par $Q$. Le
potentiel quantique ne « pousse » pas les particules au sens newtonien
— il **déforme la géométrie** dans laquelle elles se déplacent.

La comparaison terme à terme :

| Relativité générale | Mécanique bohmienne |
|:---|:---|
| Métrique $g_{\mu\nu}$ | Potentiel quantique $Q$ |
| Courbure de Ricci $R_{\mu\nu}$ | $\nabla^2 R / R$ (courbure de l'amplitude) |
| Masse-énergie $T_{\mu\nu}$ courbe l'espace | Forme de $\psi$ courbe les trajectoires |
| Géodésique : ligne droite dans l'espace courbe | Trajectoire bohmienne : « ligne droite » dans l'espace déformé par $Q$ |
| Force gravitationnelle $F_g = -\nabla \Phi$ | Force quantique $F_Q = -\nabla Q$ |

En relativité générale, la masse-énergie **courbe** l'espace-temps et
les objets suivent les géodésiques de cet espace courbé — ce qu'on
interprète comme la « gravité ». Dans dBB, la fonction d'onde $\psi$
**courbe** l'espace de configuration via $Q$ et les particules suivent
les « géodésiques » de cet espace déformé — ce qu'on interprète comme
la « force quantique ».

Le plasma asymétrique joue donc le rôle d'une **distribution de
masse-énergie** qui courbe l'espace effectif. Détecter une force dans
la chambre fermée, c'est détecter une **distorsion géométrique
artificielle** — un « champ gravitationnel » d'origine quantique.

> ⚠️ **Limites de l'analogie** — L'équivalence est **formelle**, pas
> physique. $Q$ vit dans l'espace de configuration ($3N$ dimensions
> pour $N$ particules), pas dans l'espace-temps 4D de la RG. Il ne
> s'agit pas de « créer de la gravité » au sens d'Einstein, mais de
> créer un effet mécanique qui, du point de vue de la particule guidée,
> est **indistinguable** d'une courbure géométrique. La distinction
> deviendrait cruciale pour toute tentative de théorie unifiée
> Bohm + RG (voir Hiley, 2010 ; Shojai & Shojai, 2004).

### Résumé conceptuel

| Double fente | Cavité plasma | Espace-temps courbe |
|:---|:---|:---|
| 2 ouvertures | Modes TM (6 « fentes ») | Distribution de masse |
| Interférence | Onde stationnaire + plasma | Courbure métrique |
| $Q$ structuré | $\nabla Q$ asymétrique | Champ gravitationnel |
| Déviation des trajectoires | Force nette sur la chambre fermée | Déviation des géodésiques |

Cette chaîne conceptuelle — de Young (1801) à Bohm (1952) à la cavité
plasma (2026) — est le fil conducteur de l'expérience. La double fente
montre que $Q$ **peut** dévier des trajectoires. La cavité plasma tente
de transformer cette déviation en **force macroscopique mesurable** en
repliant et en asymétrisant la fonction d'onde.

---

## Objectif 1 — Contraindre expérimentalement la force anomale en système fermé

> 💡 **En termes simples** — Imaginez une boîte fermée posée sur une
> table. À l'intérieur, quelqu'un pousse contre les murs. La boîte
> ne bouge pas, parce que pousser le mur de gauche revient à pousser
> le mur de droite dans l'autre sens : les forces s'annulent. C'est la
> [3ᵉ loi de Newton](https://fr.wikipedia.org/wiki/Lois_du_mouvement_de_Newton#Troisi%C3%A8me_loi_de_Newton).
> L'expérience vise à mesurer si une exception à cette règle existe
> lorsqu'un plasma est guidé par une onde électromagnétique en cavité.
> Le résultat — positif ou nul — est scientifiquement informatif.

### Énoncé

Mesurer si une **force anomale** (au-delà de la pression de radiation
classique) existe dans un système fermé (chambre à vide inox de 3 gallons)
**sans éjection de masse ni échange mécanique avec l'extérieur**, et
établir une **borne supérieure** sur cette force.

### Contexte physique

La conservation de la quantité de mouvement dans un système isolé est un
principe fondamental de la mécanique classique (3ᵉ loi de Newton). Dans un
système fermé rigide, les forces internes s'annulent par paires :

- Le magnétron émet des photons → recule vers la gauche.
- Les photons frappent la paroi droite → la poussent vers la droite.
- Mais le magnétron est **fixé** à la chambre → les deux forces s'annulent.

Le **théorème du centre de masse** impose que $\vec{F}_{\text{nette}} = 0$
si aucune quantité de mouvement n'est échangée avec l'extérieur — y compris
la pression de radiation classique $P/c$, puisque la source (magnétron) est
interne.

Dans le cadre bohmien, la force additionnelle provient du **potentiel quantique**
$Q$, qui n'a pas d'analogue classique :

$$F_Q = -\nabla Q = -\nabla \left( -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R} \right)$$

L'asymétrie structurelle de dBB est ici cruciale : l'onde pilote $\psi$ guide
les particules ($\vec{v} = \nabla S / m$), mais les particules **n'exercent
pas de réaction** sur $\psi$ (qui évolue selon Schrödinger indépendamment).
Si $-\nabla Q$ exerce une force sur le plasma, et que cette force n'a pas de
réaction mécanique sur un objet physique, le théorème du centre de masse
serait violé.

> ⚠️ **Avertissement épistémologique** — La mécanique bohmienne est
> construite pour être **empiriquement équivalente** à la mécanique
> quantique standard (Bohm, 1952 ; Holland, 1993, chap. 3). Cela
> signifie que si la MQ standard prédit $F = 0$ dans un système fermé,
> dBB devrait prédire la même chose — sauf si le système se trouve
> dans un régime de **non-équilibre quantique** ($\rho \neq |\psi|^2$),
> une condition spéculative théorisée par Valentini (1991, 2002).
>
> Le plasma hors-équilibre thermodynamique est un candidat intéressant
> (mais non garanti) pour explorer cette faille. L'expérience ne
> *présuppose* pas un résultat positif : elle le **teste**.

> 📝 **Précédent : l'EmDrive** — L'[EmDrive](https://en.wikipedia.org/wiki/EmDrive)
> (Shawyer, 2001) est une cavité RF fermée qui prétendait produire une
> poussée nette. Après 15 ans de tests (NASA Eagleworks, Université de
> Dresde), toutes les mesures positives ont été attribuées à des
> **artefacts thermiques** (dilatation, courants de convection, forces
> de Lorentz sur les câbles). Les tests les plus soignés (Dresde, 2021)
> ont donné un résultat **nul**.
>
> Notre motivation théorique est différente (dBB + plasma vs. cavité
> asymétrique vide), mais ce précédent illustre la difficulté des
> mesures de micro-force en cavité RF et la fréquence des faux positifs.
> Le protocole de Bohemian Lab intègre les leçons de l'EmDrive :
> autonomie sur pendule (pas de câbles rigides), baril isolant, tests
> de baseline et rotation 180°.

### Critère de succès

L'expérience a **deux issues scientifiquement valides** :

| Issue | Observation | Conclusion |
|:---|:---|:---|
| **Résultat positif** | Force reproductible corrélée au plasma, non explicable par les artefacts connus (vent ionique, effets thermiques, forces EM résiduelles), et significativement supérieure au bruit | Anomalie nécessitant une explication théorique (non-équilibre quantique ?) |
| **Résultat nul** | Aucune force détectable au-delà du bruit du pendule | Borne supérieure publiable : « dans une cavité RF plasma à $n_{e,c}$, aucune force anomale > $X\;\mu$N n'a été détectée » — contrainte expérimentale sur les théories alternatives |

Dans les deux cas, la corrélation temporelle avec l'activation du magnétron
et le test de rotation 180° restent les contrôles clés.

### Pertinence

Un résultat **positif** ouvrirait un champ d'investigation fondamental
sur les transferts de quantité de mouvement médiés par le potentiel
quantique. Un résultat **nul** fournirait une contrainte expérimentale
rigoureuse dans un régime (cavité RF + plasma) rarement testé
— les deux contribuent à la littérature scientifique.

---

## Objectif 2 — Quantifier le gradient de phase asymétrique

> 💡 **En termes simples** — Quand la lumière traverse un verre inégalement
> épais (comme un prisme), elle dévie. Pourquoi ? Parce qu'un côté du
> verre « ralentit » la lumière plus que l'autre. Notre plasma joue le
> rôle du prisme : si un côté est plus dense en électrons, l'onde
> micro-onde y voyage plus lentement, ce qui crée un « gradient de phase ».
> Dans la théorie de Bohm, ce gradient dicte la direction de la force.
> Les 8 tubes Nixie IN-13 servent de carte du gradient : en mode
> **passif** (broches à la masse, pas d'alimentation), le néon brille
> spontanément sous le champ RF — plus la lueur est intense, plus le
> champ EM local est fort.

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
la chambre (espacés de 45°), fonctionnent en **mode passif** : broches
court-circuitées à la paroi inox (mise à la masse), aucune alimentation
extérieure. Le néon s'ionise spontanément sous le champ RF et la brillance
de chaque tube indique l'intensité du champ EM local. La lecture se fait
par **caméra Wi-Fi** embarquée (analyse d'image).

La corrélation entre la direction de l'asymétrie Nixie et la
direction de la force détectée au pendule est le test clé de l'Objectif 2
(voir la [matrice décisionnelle](04_protocole.md#46-attentes-concrètes--confirmer-ou-infirmer-lhypothèse)).

> 📐 **Circuit quantique** — Le script [005_phase_circuit.py](../experiments/005_phase_circuit.py)
> simule l'accumulation de phase $S = \int n \cdot (\omega/c) \, d\ell$
> par des portes $R_z$ et modélise le gradient sur 8 qubits (analogie
> directe avec les 8 Nixie IN-13).

> 📐 **Modèle 3D** — La simulation [009_plasma_3d.py](../experiments/009_plasma_3d.py)
> prédit que la direction de $-\nabla Q$ a un angle d'élévation de
> ≈ −55° (composante verticale dominante). La corrélation Nixie
> n'est sensible qu'à la **projection horizontale** du gradient. Voir
> [data/009_decomposition_force.png](../data/009_decomposition_force.png).

---

## Objectif 3 — Valider l'interaction potentiel quantique / plasma

> 💡 **En termes simples** — La physique classique prédit qu'un faisceau
> de lumière de 1 kW venant de **l'extérieur** peut pousser un objet
> avec une force de ~ 3,3 µN (micro-newtons) — le poids d'un grain de
> poussière. C'est la
> [pression de radiation](https://fr.wikipedia.org/wiki/Pression_de_radiation),
> démontrée expérimentalement par [Lebedev](https://fr.wikipedia.org/wiki/Piotr_Lebedev)
> en 1901. Dans notre cas, la source (magnétron) est **interne** au
> système fermé, donc la force nette classique devrait être **nulle**.
> Toute force détectée constituerait une anomalie.

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

> 📐 **Modèle 2D** — Le script [003_profil_plasma.py](../experiments/003_profil_plasma.py)
> calcule cette intégrale en 2D ($r,\theta$) pour un plasma asymétrique
> et obtient $F_Q \sim$ quelques µN, du même ordre que $P_{\text{abs}}/c$.

> 📐 **3D** — Cette intégrale volumique est un **vecteur 3D**. La simulation
> [009_plasma_3d.py](../experiments/009_plasma_3d.py) la décompose en
> composantes horizontale/verticale sur 384 000 points de grille
> ($N_{xy}=80, N_z=60$). Résultats :
> [data/009_forces_3d.csv](../data/009_forces_3d.csv).

### Bilan de quantité de mouvement en système fermé

**Note importante** : la pression de radiation classique $P_{\text{abs}}/c$
ne s'applique comme force nette que si la source de photons est
**extérieure** au système. Ici, le magnétron est fixé à la chambre :
le recul du magnétron annule exactement la pression sur la paroi opposée
(théorème du centre de masse). La force nette classique attendue est donc
**zéro**, pas $3{,}3\;\mu$N.

Cela renforce l'intérêt de l'expérience : toute force mesurable au-delà
du bruit est **entièrement anomale**, sans baseline classique à soustraire.

### Défi expérimental

Le pendule de torsion doit être suffisamment sensible pour détecter des
forces de l'ordre du micro-newton. La sensibilité de l'instrument
(constante de torsion $\kappa$, longueur du bras, résolution du PSD)
définit la borne supérieure atteignable.

> 📐 **Composante mesurable** — Le pendule de torsion ne détecte que
> la composante **horizontale** de la force. Le [modèle 3D](../experiments/009_plasma_3d.py)
> montre que le ratio $F_H/F_V \approx 0{,}69$ : la force verticale
> représente ≈ 59 % de la force totale et échappe entièrement à la
> mesure. La borne supérieure mesurée doit donc être interprétée
> comme une borne sur $F_H$ seulement, pas sur $F_{\text{totale}}$.

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

9. **Valentini, A.** (1991). « Signal-locality, uncertainty, and the
   subquantum H-theorem ». *Physics Letters A*, 156(1–2), 5–11.
   (Non-équilibre quantique : conditions où dBB prédit des résultats
   différents de la MQ standard.)

10. **Valentini, A.** (2002). « Signal-locality in hidden-variables
    theories ». *Physics Letters A*, 297(5–6), 273–278.
    (Formalisation du régime $\rho \neq |\psi|^2$.)

11. **Tajmar, M. et al.** (2021). « The SpaceDrive Project — Thrust
    Balance Development and New Measurements of the Mach-Effect and
    EmDrive Thrusters ». *Acta Astronautica*, 187, 224–237.
    (Tests de l'EmDrive à l'Université de Dresde — résultat nul après
    correction des artefacts thermiques.)

12. **Young, T.** (1804). « Experiments and Calculations Relative to
    Physical Optics ». *Philosophical Transactions of the Royal Society*,
    94, 1–16. (Expérience de la double fente.)

13. **Shojai, A. & Shojai, F.** (2004). « Constraint algebra and
    equations of motion in the Bohmian interpretation of quantum
    gravity ». *Classical and Quantum Gravity*, 21(1), 1–9.
    [doi:10.1088/0264-9381/21/1/001](https://doi.org/10.1088/0264-9381/21/1/001)

14. **Hiley, B. J.** (2010). « Process, Distinction, Groupoids and
    Clifford Algebras: an Alternative View of the Quantum Formalism ».
    *New Structures for Physics*, Lecture Notes in Physics 813, Springer,
    pp. 705–752.
    [doi:10.1007/978-3-642-12821-9_12](https://doi.org/10.1007/978-3-642-12821-9_12)

---

[← Retour au README](../README.md) · [Section suivante : Cadre Théorique →](02_theorie.md)
