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

---

[← Retour au README](../README.md) · [Section suivante : Cadre Théorique →](02_theorie.md)
