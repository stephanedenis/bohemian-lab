# 📐 Cadre Théorique

[← Retour au README](../README.md) · [← Objectifs](01_objectifs.md)

---

## Introduction vulgarisée

La physique quantique standard nous dit qu'une particule — un électron, un
photon — n'existe pas en un point précis avant d'être mesurée. Elle est décrite
par une « fonction d'onde » qui donne seulement la **probabilité** de la trouver
ici ou là. C'est la vision dite de **[Copenhague](https://fr.wikipedia.org/wiki/Interpr%C3%A9tation_de_Copenhague)**, adoptée par la plupart des
physiciens depuis les années 1920.

Mais il existe une autre lecture, proposée par **[Louis de Broglie](https://fr.wikipedia.org/wiki/Louis_de_Broglie)** en 1927 puis
redécouverte par **[David Bohm](https://fr.wikipedia.org/wiki/David_Bohm)** en 1952 : la particule a toujours une position
réelle et une trajectoire bien définie. Elle est simplement **guidée** par une
onde — « l'onde pilote » — un peu comme un surfeur porté par une vague. Cette
onde pilote est exactement la fonction d'onde $\psi$ de la mécanique quantique
standard, mais elle joue un rôle physique concret : elle dicte la vitesse et
la direction de la particule.

Ce qui rend cette théorie fascinante pour notre expérience, c'est qu'elle prédit
l'existence d'un **potentiel quantique** $Q$ — une sorte de « terrain invisible »
qui dépend de la forme de l'onde et qui peut exercer une force sur les particules.
Contrairement aux forces classiques, cette force ne diminue pas avec la distance
et peut être très sensible à la géométrie du milieu traversé.

Notre expérience cherche à exploiter cet effet : en façonnant la forme de l'onde
pilote (via un plasma inhomogène), on espère créer un gradient de potentiel
quantique qui produirait une force mécanique mesurable.

---

## 2.1 L'interprétation de de Broglie–Bohm

> 💡 **En termes simples** — En physique quantique classique, on renonce à
> dire où se trouve une particule : on ne donne que des probabilités.
> La théorie de de Broglie–Bohm dit le contraire : la particule **est**
> quelque part, elle a un chemin précis, mais ce chemin est dicté par
> une onde qui la guide — exactement comme un bouchon de liège suit
> le courant d'une rivière. L'onde est partout, le bouchon est à un
> seul endroit.

### Historique

- **1924** — [Louis de Broglie](https://fr.wikipedia.org/wiki/Louis_de_Broglie) propose dans sa [thèse de doctorat](https://fr.wikipedia.org/wiki/Th%C3%A8se_de_doctorat_de_Louis_de_Broglie) l'hypothèse
  de l'[onde de matière](https://fr.wikipedia.org/wiki/Dualit%C3%A9_onde-corpuscule) : toute particule est associée à une onde de longueur
  $\lambda = h/p$ ([relation de de Broglie](https://fr.wikipedia.org/wiki/Hypoth%C3%A8se_de_De_Broglie)).

- **1927** — Au [Congrès Solvay](https://fr.wikipedia.org/wiki/Congr%C3%A8s_Solvay), de Broglie présente sa **[théorie de l'onde
  pilote](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_l%27onde_pilote)** (*théorie de la double solution*) : la particule est un point
  singulier guidé par une onde réelle. La théorie est critiquée par [Pauli](https://fr.wikipedia.org/wiki/Wolfgang_Pauli)
  et éclipsée par l'[interprétation de Copenhague](https://fr.wikipedia.org/wiki/Interpr%C3%A9tation_de_Copenhague) ([Bohr](https://fr.wikipedia.org/wiki/Niels_Bohr), [Heisenberg](https://fr.wikipedia.org/wiki/Werner_Heisenberg), [Born](https://fr.wikipedia.org/wiki/Max_Born)).

- **1952** — [David Bohm](https://fr.wikipedia.org/wiki/David_Bohm), alors au Brésil, redécouvre et complète la théorie
  dans deux articles fondateurs publiés dans *[Physical Review](https://fr.wikipedia.org/wiki/Physical_Review)*. Il montre
  que la mécanique quantique peut être reformulée comme une théorie
  déterministe à [variables cachées](https://fr.wikipedia.org/wiki/Variable_cach%C3%A9e_(physique_quantique)), reproduisant toutes les prédictions
  expérimentales de la mécanique quantique standard.

- **1964–1987** — [John Stewart Bell](https://fr.wikipedia.org/wiki/John_Stewart_Bell), profondément influencé par Bohm,
  développe son célèbre [théorème](https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_de_Bell) ([inégalités de Bell](https://fr.wikipedia.org/wiki/In%C3%A9galit%C3%A9s_de_Bell)) et plaide
  publiquement pour la théorie de Bohm comme « la meilleure formulation
  disponible de la mécanique quantique non-relativiste ».

### Postulats fondamentaux

La théorie repose sur deux éléments :

1. **La fonction d'onde** $\psi(\mathbf{r}, t)$ évolue selon l'[équation de
   Schrödinger](https://fr.wikipedia.org/wiki/%C3%89quation_de_Schr%C3%B6dinger) habituelle :

$$i\hbar \frac{\partial \psi}{\partial t} = -\frac{\hbar^2}{2m}\nabla^2\psi + V\psi$$

2. **L'équation de guidage** dicte la vitesse de la particule :

$$\frac{d\mathbf{Q}}{dt} = \frac{\hbar}{m} \text{Im}\left(\frac{\nabla\psi}{\psi}\right)$$

La particule a toujours une position définie $\mathbf{Q}(t)$. La fonction
d'onde n'est pas un simple outil de calcul : c'est un **champ physique réel**
qui pilote la particule.

---

## 2.2 La Loi de Guidage — Dérivation complète

> 💡 **En termes simples** — Une onde, c'est deux informations : sa
> **hauteur** (l'amplitude $R$ : « à quel point elle est forte ») et son
> **rythme** (la phase $S$ : « où elle en est dans son cycle »). Pensez à
> une vague sur la mer : la hauteur dit si la vague est grosse, la phase
> dit si on est sur la crête ou dans le creux.
>
> La loi de guidage dit simplement : *la particule se déplace dans la
> direction où la phase change le plus vite*. Si la phase varie plus vite
> à droite qu'à gauche, la particule va à droite. C'est comme une bille
> qui roule dans la direction de la plus grande pente.
>
> L'équation de Hamilton-Jacobi, quant à elle, est l'équivalent classique
> (avant la physique quantique) de la description du mouvement par la phase.
> C'est la même équation qu'utilisait Newton, mais avec un terme en plus :
> le potentiel quantique $Q$.

### Décomposition polaire

On écrit la fonction d'onde sous forme polaire :

$$\psi(\mathbf{r}, t) = R(\mathbf{r}, t) \; e^{i S(\mathbf{r}, t) / \hbar}$$

où :
- $R(\mathbf{r}, t) \geq 0$ est l'**amplitude** de l'onde,
- $S(\mathbf{r}, t) \in \mathbb{R}$ est la **phase** de l'onde.

La densité de probabilité est $\rho = |\psi|^2 = R^2$.

### Obtention de la vitesse de guidage

En substituant la forme polaire dans l'équation de Schrödinger et en séparant
parties réelle et imaginaire, on obtient deux équations couplées :

**Partie imaginaire** — Équation de continuité :

$$\frac{\partial R^2}{\partial t} + \nabla \cdot \left(R^2 \frac{\nabla S}{m}\right) = 0$$

Cette équation exprime la conservation de la probabilité et identifie
naturellement le champ de vitesse :

$$\boxed{\vec{v} = \frac{\nabla S}{m}}$$

C'est la **loi de guidage** : la vitesse de la particule est proportionnelle
au gradient de la phase de la fonction d'onde.

**Partie réelle** — Équation de [Hamilton-Jacobi](https://fr.wikipedia.org/wiki/%C3%89quation_de_Hamilton-Jacobi) modifiée :

$$\frac{\partial S}{\partial t} + \frac{(\nabla S)^2}{2m} + V + Q = 0$$

où apparaît le terme supplémentaire $Q$, le **potentiel quantique**.

### Équivalence avec la forme standard

Pour un système de $N$ particules, l'équation de guidage se généralise :

$$\frac{d\mathbf{Q}_k}{dt} = \frac{\hbar}{m_k} \text{Im}\left(\frac{\nabla_k \psi}{\psi}\right) \bigg|_{\mathbf{q} = \mathbf{Q}(t)}$$

Cette forme est directement calculable à partir de $\psi$ sans passer par
la décomposition polaire.

---

## 2.3 Le Potentiel Quantique

> 💡 **En termes simples** — Imaginez un terrain vallonné invisible.
> Une bille posée dessus roule vers les creux et évite les bosses —
> c'est ce que fait un « potentiel » en physique. Le potentiel quantique
> $Q$ est un terrain de ce type, mais avec des propriétés étranges :
>
> - **Il ne dépend pas de la force de l'onde**, seulement de sa forme.
>   Une toute petite ondulation bien courbée crée un terrain aussi pentu
>   qu'une grosse vague. C'est comme si la forme des collines comptait
>   plus que leur taille.
> - **Il « sait » ce qui se passe partout en même temps** (non-localité).
>   Modifier l'onde à gauche change instantanément le terrain à droite.
>   C'est l'origine de l'intrication quantique.
> - **Il disparaît dans le monde macroscopique** : quand les objets sont
>   gros, le terrain s'aplatit et on retrouve la physique de Newton.
>
> La force que notre expérience cherche à mesurer est simplement :
> « la bille dévale la pente du terrain quantique ».

### Définition

Le potentiel quantique est défini par :

$$\boxed{Q = -\frac{\hbar^2}{2m} \frac{\nabla^2 R}{R}}$$

### Propriétés remarquables

1. **Insensibilité à l'intensité** — $Q$ dépend de la *forme* de $R$
   (via $\nabla^2 R / R$), pas de son amplitude absolue. Multiplier $R$
   par une constante ne change pas $Q$. Cela signifie que le potentiel
   quantique peut être très grand même là où l'onde est très faible.

2. **Non-localité** — $Q$ dépend de la forme globale de $\psi$ dans
   tout l'espace. Il encode des corrélations à distance (intrication)
   sans signal supraluminique, conformément au [théorème de Bell](https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_de_Bell).

3. **Pas d'analogue classique** — Dans la limite classique ($\hbar \to 0$),
   $Q \to 0$ et on retrouve l'[équation de Hamilton-Jacobi](https://fr.wikipedia.org/wiki/%C3%89quation_de_Hamilton-Jacobi) classique.
   Le potentiel quantique est donc la signature spécifiquement quantique
   de la dynamique.

4. **Force quantique** — La force exercée par le potentiel quantique est :

$$\mathbf{F}_Q = -\nabla Q$$

C'est cette force que l'expérience Bohemian Lab cherche à détecter.

### Interprétation géométrique

[Holland](https://en.wikipedia.org/wiki/Peter_R._Holland) (1993) propose une analogie : le potentiel quantique joue un rôle
similaire à la courbure de l'espace-temps en [relativité générale](https://fr.wikipedia.org/wiki/Relativit%C3%A9_g%C3%A9n%C3%A9rale). Il
modifie les trajectoires des particules non pas en exerçant une force
au sens newtonien, mais en « déformant » l'espace de configuration dans
lequel les particules se déplacent.

---

## 2.4 Application aux photons RF

> 💡 **En termes simples** — La théorie de Bohm a été écrite pour des
> particules qui ont une masse (électrons, atomes…). Les photons, eux,
> n'ont pas de masse — ils sont de la lumière pure. On ne peut donc pas
> appliquer la formule directement.
>
> Mais l'idée-clé se transpose : dans un milieu comme un plasma, la
> lumière ne voyage pas à la même vitesse partout. Là où le plasma est
> plus dense, la lumière ralentit et change de direction — exactement
> comme un rayon lumineux dévie en entrant dans l'eau (c'est la
> **réfraction**). L'**indice de réfraction** mesure cet effet.
>
> Si le plasma est plus dense d'un côté que de l'autre, la lumière est
> déviée préférentiellement dans une direction. C'est cet « aiguillage »
> asymétrique qui, dans notre expérience, pourrait créer la poussée.
>
> Un point crucial : la fréquence naturelle de vibration de notre plasma
> (~ 1-9 GHz) est très proche de la fréquence du magnétron (2,45 GHz).
> C'est comme accorder un instrument de musique : quand les deux
> fréquences se rapprochent, l'interaction est maximale.

### Le problème de la masse

La formule standard $\vec{v} = \nabla S / m$ suppose une particule massive.
Pour les photons ($m = 0$), le guidage se reformule via la dynamique de
champ. L'analogie pertinente est la suivante :

- L'onde électromagnétique dans la cavité joue le rôle de $\psi$.
- Le [vecteur de Poynting](https://fr.wikipedia.org/wiki/Vecteur_de_Poynting) $\vec{\mathcal{S}} = \vec{E} \times \vec{H}$
  joue le rôle du courant de probabilité.
- Le flux d'énergie est « guidé » par le gradient de phase de l'onde.

Dans un milieu plasma avec un indice de réfraction $n(\mathbf{r})$ :

$$n(\mathbf{r}) = \sqrt{1 - \frac{\omega_p^2(\mathbf{r})}{\omega^2}}$$

la phase accumulée sur un trajet est :

$$S = \int n(\mathbf{r}) \, \frac{\omega}{c} \, d\ell$$

Un gradient de $n$ crée un gradient de $S$, et donc une déviation du flux
d'énergie (analogue au guidage bohmien).

### Fréquence plasma

La pulsation plasma est :

$$\omega_p = \sqrt{\frac{n_e \, e^2}{\varepsilon_0 \, m_e}}$$

Pour un plasma de vapeur d'eau typique ($n_e \sim 10^{16} - 10^{18} \; \text{m}^{-3}$) :

$$f_p = \frac{\omega_p}{2\pi} \approx 0{,}9 - 9 \; \text{GHz}$$

Ceci est du même ordre de grandeur que la fréquence du magnétron
($f = 2{,}45$ GHz), ce qui place le système dans un régime où le plasma
interagit fortement avec l'onde — condition idéale pour maximiser le
gradient de phase.

---

## 2.5 Force de Poussée Totale

> 💡 **En termes simples** — On sait depuis Maxwell (1873) que la lumière
> exerce une pression quand elle frappe un objet : c'est la **pression de
> radiation**. C'est elle qui pousse les queues des comètes à l'opposé du
> Soleil. Mais cette force est minuscule : pour 1 000 watts (la puissance
> d'un four micro-ondes), elle vaut environ 3 millionièmes de newton — le
> poids d'un grain de poussière.
>
> Notre expérience mesure la force totale exercée. Si on trouve **plus**
> que ces 3,3 µN, l'excès ne peut pas venir de la pression de radiation
> classique. C'est cet excès qui serait la signature de la force
> bohmienne — la « poussée du terrain quantique ».

### Expression théorique

La force mesurée est la somme de deux contributions :

$$\boxed{F_{\text{totale}} = \underbrace{\frac{P_{\text{abs}}}{c}}_{\text{pression de radiation}} + \underbrace{\int \rho \, (-\nabla Q) \, dV}_{\text{force bohmienne}}}$$

### Estimation de la composante classique

Pour une puissance absorbée $P_{\text{abs}} = 1\,000$ W :

$$F_{\text{rad}} = \frac{P_{\text{abs}}}{c} = \frac{1\,000}{3 \times 10^8} \approx 3{,}3 \; \mu\text{N}$$

Cette force est extrêmement faible (comparable au poids d'un grain de
poussière). Tout excès mesuré par rapport à cette valeur serait attribuable
à la composante bohmienne $\int \rho (-\nabla Q) \, dV$.

### Signature expérimentale attendue

- **Corrélation temporelle** : la force doit apparaître et disparaître
  synchroniquement avec le plasma.
- **Directionnalité** : la force doit être orientée selon l'axe du
  gradient de densité plasma.
- **Non-réversibilité par rotation** : rotation de 180° du dispositif
  interne → inversion de la direction de la force (et non annulation).

---

## 2.6 Lien avec le formalisme quantique computationnel

> 💡 **En termes simples** — Avant de construire l'expérience physique, on
> la « joue » sur ordinateur. Pour cela, on utilise le langage des
> **circuits quantiques** — une façon de représenter des opérations
> quantiques comme des briques qu'on assemble, un peu comme un circuit
> électronique mais pour l'information quantique.
>
> La **sphère de Bloch** est simplement un globe 3D : chaque point sur
> la surface représente un état possible du qubit (le « bit » quantique).
> Le pôle Nord = état 0, le pôle Sud = état 1, et tous les points entre
> les deux = superpositions. Tourner autour de l'axe vertical, c'est
> changer la phase — exactement le $S$ de notre théorie. Monter ou
> descendre, c'est changer l'amplitude $R$. On retrouve les mêmes
> deux ingrédients que dans la loi de guidage.

Les simulations numériques du projet (dossier `experiments/`) utilisent
**[Qiskit](https://fr.wikipedia.org/wiki/Qiskit)** et **[PennyLane](https://en.wikipedia.org/wiki/PennyLane_(software))** pour modéliser des aspects du guidage bohmien
dans un cadre de [circuits quantiques](https://fr.wikipedia.org/wiki/Circuit_quantique) :

- **Superposition** → modélise l'onde pilote (amplitude et phase).
- **Portes de phase** ($R_z$, $P$) → simulent l'accumulation de phase
  dans le plasma.
- **Intrication** (CNOT) → explore les corrélations non-locales du
  potentiel quantique.
- **Mesure** → simule l'effondrement de la fonction d'onde et la
  sélection de trajectoire bohmienne.

La visualisation sur la **[sphère de Bloch](https://fr.wikipedia.org/wiki/Sph%C3%A8re_de_Bloch)** permet de suivre l'évolution
de la phase et de l'amplitude du qubit, en analogie directe avec le
rapport $S/R$ de la décomposition polaire.

---

## Références

### Articles fondateurs

1. **[de Broglie, L.](https://fr.wikipedia.org/wiki/Louis_de_Broglie)** (1924). *Recherches sur la théorie des quanta*.
   Thèse de doctorat, Faculté des Sciences de Paris.
   [Texte intégral (Gallica)](https://gallica.bnf.fr/ark:/12148/bpt6k62461489)

2. **de Broglie, L.** (1928). « La nouvelle dynamique des quanta ».
   *Électrons et Photons : Rapports et Discussions du Cinquième Conseil
   de Physique*, Solvay, pp. 105–132.

3. **[Bohm, D.](https://fr.wikipedia.org/wiki/David_Bohm)** (1952a). « A Suggested Interpretation of the Quantum
   Theory in Terms of "Hidden" Variables, I ». *Physical Review*, 85(2),
   166–179.
   [doi:10.1103/PhysRev.85.166](https://doi.org/10.1103/PhysRev.85.166)

4. **Bohm, D.** (1952b). « A Suggested Interpretation of the Quantum
   Theory in Terms of "Hidden" Variables, II ». *Physical Review*, 85(2),
   180–193.
   [doi:10.1103/PhysRev.85.180](https://doi.org/10.1103/PhysRev.85.180)

### Ouvrages de référence

5. **[Holland, P. R.](https://en.wikipedia.org/wiki/Peter_R._Holland)** (1993). *The Quantum Theory of Motion: An Account
   of the de Broglie–Bohm Causal Interpretation of Quantum Mechanics*.
   Cambridge University Press. ISBN 978-0-521-48543-2.

6. **[Bell, J. S.](https://fr.wikipedia.org/wiki/John_Stewart_Bell)** (1987). *Speakable and Unspeakable in Quantum Mechanics*.
   Cambridge University Press. ISBN 978-0-521-36869-8.

7. **[Bohm, D.](https://fr.wikipedia.org/wiki/David_Bohm) & [Hiley, B. J.](https://en.wikipedia.org/wiki/Basil_Hiley)** (1993). *The Undivided Universe: An
   Ontological Interpretation of Quantum Theory*. Routledge.
   ISBN 978-0-415-06588-7.

### Articles contemporains

8. **[Dürr, D.](https://en.wikipedia.org/wiki/Detlef_D%C3%BCrr), [Goldstein, S.](https://en.wikipedia.org/wiki/Sheldon_Goldstein) & Zanghì, N.** (1992). « Quantum Equilibrium
   and the Origin of Absolute Uncertainty ». *Journal of Statistical
   Physics*, 67, 843–907.
   [doi:10.1007/BF01049004](https://doi.org/10.1007/BF01049004)

9. **[Dürr, D.](https://en.wikipedia.org/wiki/Detlef_D%C3%BCrr) & Teufel, S.** (2009). *Bohmian Mechanics: The Physics and
   Mathematics of Quantum Theory*. Springer. ISBN 978-3-540-89343-1.

10. **Goldstein, S.** (2021). « Bohmian Mechanics ». In *Stanford
    Encyclopedia of Philosophy*.
    [plato.stanford.edu/entries/qm-bohm](https://plato.stanford.edu/entries/qm-bohm/)

### Physique des plasmas

11. **Chen, F. F.** (2016). *Introduction to Plasma Physics and Controlled
    Fusion*. 3ᵉ édition, Springer. ISBN 978-3-319-22308-7.

12. **Lieberman, M. A. & Lichtenberg, A. J.** (2005). *Principles of
    Plasma Discharges and Materials Processing*. 2ᵉ édition, Wiley.
    ISBN 978-0-471-72001-0.

---

[← Objectifs](01_objectifs.md) · [Section suivante : Configuration Matérielle →](03_materiel.md)
