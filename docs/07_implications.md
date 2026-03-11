# 🌌 Implications d'un Résultat Positif

[← Retour au README](../README.md) · [← Protocole de validation](04_protocole.md)

---

## Introduction

> 💡 **En termes simples** — Si le pendule de torsion détecte une force
> reproductible dans la chambre fermée, et que cette force résiste à
> tous les tests de contrôle (inversion 180°, gaz noble, vide sans
> plasma), alors quelque chose de **fondamentalement inattendu** se passe.
> La physique classique dit que c'est impossible. La mécanique quantique
> standard aussi. Seule l'interprétation de Bohm, dans un régime très
> particulier (non-équilibre quantique), le permettrait.
>
> Cette page explore ce qui découlerait d'une telle observation —
> non pas comme une certitude, mais comme un exercice de pensée rigoureux
> sur les conséquences physiques, technologiques et épistémologiques.

⚠️ **Avertissement** — Un résultat positif devrait être traité avec une
**extrême prudence**. L'histoire de la physique regorge de faux positifs
(EmDrive, fusion froide, neutrinos supraluminiques). Avant toute
interprétation, la priorité absolue serait la **réplication indépendante**
par d'autres laboratoires, avec des instruments et des protocoles
différents. Les implications discutées ci-dessous ne deviendraient
pertinentes qu'après un tel processus de validation.

---

## 1. Implications Fondamentales

### 1.1 Violation du théorème du centre de masse

La physique classique impose que les forces internes à un système fermé
s'annulent par paires ([3ᵉ loi de Newton](https://fr.wikipedia.org/wiki/Lois_du_mouvement_de_Newton#Troisi%C3%A8me_loi_de_Newton)).
La force nette sur le centre de masse est :

$$\vec{F}_{\text{nette}} = \frac{d\vec{p}_{\text{total}}}{dt} = 0 \quad \text{(système isolé)}$$

Une force anomale détectée dans la chambre fermée — sans éjection de
masse ni échange de quantité de mouvement avec l'extérieur — impliquerait
que **la 3ᵉ loi de Newton n'est pas universelle** dans les systèmes
quantiques hors-équilibre. Ce serait l'observation la plus disruptive en
mécanique depuis 1687.

### 1.2 Preuve expérimentale du non-équilibre quantique

La mécanique bohmienne (dBB) est construite pour être empiriquement
équivalente à la MQ standard **tant que** la distribution de probabilité
des particules satisfait l'**équilibre quantique** :

$$\rho(\mathbf{r}, t) = |\psi(\mathbf{r}, t)|^2$$

Valentini (1991, 2002) a montré que si $\rho \neq |\psi|^2$ (régime de
**non-équilibre quantique**), les prédictions de dBB **divergent** de
celles de la MQ standard. Les conséquences théoriques incluraient :

| Propriété | Équilibre quantique ($\rho = |\psi|^2$) | Non-équilibre ($\rho \neq |\psi|^2$) |
|:---|:---|:---|
| Inégalités de Bell | Violées (comme la MQ standard) | Violées **davantage** |
| Incertitude de Heisenberg | $\Delta x \cdot \Delta p \geq \hbar/2$ | Peut être **violée** |
| Signaux supraluminiques | Impossibles (localité des signaux) | **Possibles** en principe |
| Force en système fermé | $F = 0$ | $F \neq 0$ possible |

Un résultat positif constituerait la **première preuve expérimentale**
du non-équilibre quantique — un état de la matière jamais observé, prédit
uniquement dans le cadre de dBB.

> 📝 **Analogie thermodynamique** — Le non-équilibre quantique est à la
> mécanique quantique ce que le non-équilibre thermodynamique est à la
> thermodynamique statistique. Un plasma est notoirement hors-équilibre
> thermodynamique ($T_e \gg T_g$) ; l'hypothèse spéculative est qu'il
> pourrait aussi être hors-équilibre *quantique*.

### 1.3 Statut ontologique de l'onde pilote

Dans l'interprétation de Copenhague, la fonction d'onde $\psi$ est un
outil de calcul — elle n'a pas de réalité physique indépendante. Dans
dBB, $\psi$ est un **champ physique réel** qui guide les particules.

Si $\psi$ peut exercer une force mécanique nette (via $-\nabla Q$) sans
subir de réaction, cela confirmerait que l'onde pilote est une entité
physique d'un genre nouveau — un champ qui **agit sans être agi**. Ce
serait la première observation d'une causalité à sens unique en physique
fondamentale, avec des implications profondes pour :

- Le **problème de la mesure** en mécanique quantique,
- Le débat sur le **réalisme** vs. l'**instrumentalisme** en philosophie
  de la physique,
- La nature de l'**intrication** et de la **non-localité**.

### 1.4 Conservation de l'énergie et de la quantité de mouvement

Si une force $F_Q \neq 0$ apparaît dans un système fermé, **d'où vient
la quantité de mouvement ?**

Dans le cadre dBB, la réponse est que la quantité de mouvement est
stockée dans le **champ** $\psi$ lui-même. L'onde pilote porte une
quantité de mouvement distribuée dans tout l'espace de configuration :

$$\vec{p}_\psi = \int \rho \, \nabla S \, dV$$

Si $\rho \neq |\psi|^2$, le bilan de quantité de mouvement entre
particules et champ ne s'équilibre plus — le champ peut « injecter » de
la quantité de mouvement dans la matière sans contrepartie mécanique
locale. L'énergie totale (particule + champ) reste conservée, mais le
transfert de quantité de mouvement échappe au cadre newtonien.

C'est un point théoriquement délicat qui nécessiterait des développements
mathématiques rigoureux. Holland (1993, chap. 12) et Bohm & Hiley
(1993, chap. 6) discutent les bilans d'énergie en dBB.

---

## 2. Implications Technologiques

### 2.1 Propulsion sans éjection de masse

L'implication la plus immédiate — et la plus spectaculaire — serait la
possibilité d'une **propulsion sans propergol**. Contrairement à une
fusée qui obéit à l'[équation de Tsiolkovski](https://fr.wikipedia.org/wiki/%C3%89quation_de_Tsiolkovski) :

$$\Delta v = v_e \ln\frac{m_0}{m_f}$$

où la masse finale $m_f$ diminue à mesure que le carburant est éjecté,
un propulseur bohmien utiliserait uniquement de l'énergie électrique
pour maintenir le plasma et le champ RF. La masse du véhicule resterait
**constante**.

| Paramètre | Fusée chimique | Propulsion ionique | Propulseur bohmien (hypothétique) |
|:---|:---|:---|:---|
| Éjection de masse | Oui (gaz brûlés) | Oui (ions) | **Non** |
| $I_{sp}$ (s) | 300–450 | 1 500–10 000 | **∞** (pas d'éjection) |
| Poussée typique | kN–MN | mN–N | µN–mN (à valider) |
| Énergie requise | Chimique | Électrique (solaire/nucléaire) | Électrique |
| Limite fondamentale | Masse de propergol | Masse de propergol (réduite) | Puissance électrique |

> ⚠️ **Ordre de grandeur** — Avec 1 kW et un facteur d'efficacité
> bohmien $\eta \sim 1$, la force serait de l'ordre de $P/c \approx
> 3{,}3\;\mu$N. Pour une application spatiale utile, il faudrait
> soit augmenter massivement la puissance, soit découvrir un facteur
> d'amplification ($\eta \gg 1$) — deux possibilités hautement
> spéculatives à ce stade.

### 2.2 Applications spatiales

Même une poussée modeste (µN) pourrait transformer l'ingénierie spatiale
si elle ne nécessite aucun propergol :

- **Maintien de station** pour satellites géostationnaires — fin de vie
  actuellement limitée par l'épuisement du carburant.
- **Compensation de traînée** en orbite basse — les satellites LEO
  subissent une traînée résiduelle atmosphérique ; une poussée continue
  sans consommation de masse prolongerait indéfiniment leur durée de vie.
- **Missions interstellaires précurseurs** — Un $\Delta v$ continu,
  même minuscule, accumule une vitesse considérable sur des décennies.
  Pour une sonde de 10 kg avec une poussée de 100 µN :

$$a = \frac{F}{m} = \frac{100 \times 10^{-6}}{10} = 10^{-5} \; \text{m/s}^2$$

$$v(t) = at \implies v(1\;\text{an}) \approx 315 \; \text{m/s} \implies v(30\;\text{ans}) \approx 9{,}5 \; \text{km/s}$$

Modeste par rapport aux 17 km/s de Voyager 1, mais **sans limite de
carburant** — la sonde accélère tant que l'énergie est fournie.

### 2.3 Production d'énergie ?

> ⚠️ **Attention** — Ce paragraphe est hautement spéculatif.

Si le potentiel quantique peut transférer de la quantité de mouvement à
la matière, le bilan énergétique doit être examiné avec soin. La
puissance mécanique extraite serait :

$$P_{\text{méc}} = F_Q \cdot v$$

Pour $F_Q = 10\;\mu$N et $v = 1$ m/s : $P_{\text{méc}} = 10\;\mu$W —
négligeable devant les 1 kW injectés ($\eta_{\text{conversion}} \sim
10^{-8}$). Il n'y a **aucune** indication de violation de la conservation
de l'énergie. Le dispositif est un **consommateur** d'énergie (et un
consommateur extraordinairement inefficace), pas un producteur.

---

## 3. Implications Épistémologiques

### 3.1 Discriminer les interprétations de la MQ

Depuis 1927, les physiciens débattent : la mécanique quantique
est-elle **complète** (Copenhague), ou faut-il des « variables cachées »
pour la compléter (Bohm) ? Bell (1964) a montré que certaines théories à
variables cachées sont exclues par l'expérience (variables cachées
**locales**), mais la théorie de Bohm — qui est **non-locale** — est
compatible avec toutes les observations existantes.

Le problème : dBB et Copenhague donnent les **mêmes prédictions
mesurables** dans toutes les expériences connues. Elles sont
*empiriquement indistinguables* — ce qui rend le débat philosophique
plutôt que scientifique.

Un résultat positif dans notre expérience **briserait cette
dégénérescence**. Il identifierait un régime (plasma hors-équilibre en
cavité RF) où les deux interprétations donnent des prédictions
**différentes** — faisant de dBB une théorie **testable et falsifiable**,
et non plus une simple reformulation.

### 3.2 Le rôle des expériences « improbables »

L'histoire de la physique montre que les avancées fondamentales viennent
souvent d'expériences que le consensus jugeait inutiles ou impossibles :

| Expérience | Prédiction du consensus | Résultat réel |
|:---|:---|:---|
| Michelson-Morley (1887) | Détection du vent d'éther | **Nul** → relativité restreinte |
| Expérience d'Aspect (1982) | Respect des inégalités de Bell (réalisme local) | **Violation** → non-localité quantique |
| Détection des ondes gravitationnelles (LIGO, 2015) | Signal trop faible pour être détecté | **Détection** → astronomie gravitationnelle |

Dans chaque cas, le résultat « improbable » a restructuré la physique.
Notre expérience se situe dans cette tradition : le résultat le plus
probable est **nul** (ce qui est scientifiquement valide comme borne
supérieure), mais le résultat positif, s'il survenait, serait
transformateur.

### 3.3 Falsifiabilité et réplication

Un résultat positif ne serait **pas** suffisant en soi. La démarche
scientifique exigerait :

1. **Réplication interne** — Reproduire le résultat >30 fois avec des
   conditions variées (pression, puissance, géométrie).
2. **Publication préliminaire** — Mettre en ligne le protocole complet,
   les données brutes et le code d'analyse (ce dépôt Git) sur une
   plateforme de prépublication ([arXiv](https://arxiv.org/)).
3. **Réplication indépendante** — Au moins deux laboratoires indépendants
   doivent reproduire le résultat avec leurs propres instruments.
4. **Revue par les pairs** — Soumission à une revue à comité de lecture
   (*Physical Review Letters*, *New Journal of Physics*).
5. **Recherche systématique d'artefacts** — Chaque source possible de
   faux positif doit être éliminée individuellement :
   - Effets thermiques (dilatation, convection résiduelle),
   - Couplage électromagnétique (courants de Foucault, forces de Lorentz),
   - Dégazage et vent ionique résiduel,
   - Vibrations mécaniques (sismiques, acoustiques),
   - Biais de l'expérimentateur (double aveugle automatisé).

> 📝 **Leçon de l'EmDrive** — L'EmDrive de Shawyer a fait l'objet
> de 15 ans de revendications avant que des tests rigoureux (Dresde,
> 2021) ne démontrent un résultat **nul**. La différence avec notre
> approche : (a) nous publions le protocole et le code en Open Source
> **avant** toute revendication, (b) le dispositif est conçu pour
> être reproductible à faible coût (~ 500 $ CAD en pièces), et
> (c) nous ne présumons aucun résultat.

---

## 4. Feuille de Route Post-Résultat

### Phase 1 — Confirmation (0–6 mois)

| Étape | Détail |
|:---|:---|
| Réplication interne | >30 tirs, variation de $P$, $n_e$, géométrie |
| Tests d'artefacts systématiques | Charge fantôme (eau), gaz noble (argon), vide seul |
| Rotation 180° | Vérification de l'inversion de direction |
| Analyse statistique | SNR, intervalle de confiance, test d'hypothèse |
| Publication du dataset | Données brutes + code d'analyse sur GitHub/Zenodo |

### Phase 2 — Publication (6–12 mois)

| Étape | Détail |
|:---|:---|
| Prépublication | arXiv (quant-ph ou physics.plasm-ph) |
| Soumission | *New Journal of Physics* (accès ouvert) |
| Conférences | Présentation à QMDO (Quantum Mechanics: De Broglie–Bohm) |
| Appel à réplication | Mise à disposition du plan mécanique 3D (STEP/STL) |

### Phase 3 — Exploration (12–36 mois)

| Étape | Détail |
|:---|:---|
| Scaling | Augmentation de puissance (2 kW, 5 kW) — loi $F_Q(P)$ |
| Variation du médium | Argon, azote, mélange H₂O/Ar — rôle de la chimie |
| Géométrie de cavité | Modes TE vs TM, cavités elliptiques, cornets |
| Balance de poussée | Remplacement du pendule par une balance micropoustre (nN) |
| Collaboration académique | Partenariat avec un laboratoire de physique des plasmas |

---

## 5. Et si le Résultat est Nul ?

Un résultat nul n'est **pas un échec** — c'est une **mesure**. Il
fournit une borne supérieure publiable :

> *« Dans une cavité cylindrique RF ($a = 125$ mm, $d = 250$ mm) excitée
> à 2,45 GHz (1 kW) contenant un plasma de vapeur d'eau
> ($n_e \sim 7 \times 10^{16}$ m$^{-3}$, $P \approx 3$ mbar), aucune
> force anomale supérieure à $X\;\mu$N n'a été détectée (IC 95 %) sur
> un système fermé monté sur pendule de torsion. »*

Cette borne contraint :
- Les modèles de non-équilibre quantique (Valentini),
- Les théories alternatives de propulsion en cavité RF,
- Le paramètre d'efficacité bohmien $\eta$ (voir
  [008_sensibilite_eta.py](../experiments/008_sensibilite_eta.py)).

Dans le régime testé, elle confirmerait que **l'équivalence empirique
entre dBB et la MQ standard est respectée** — un résultat important
mais attendu.

---

## Références

1. **Valentini, A.** (1991). « Signal-locality, uncertainty, and the
   subquantum H-theorem ». *Physics Letters A*, 156(1–2), 5–11.

2. **Valentini, A.** (2002). « Signal-locality in hidden-variables
   theories ». *Physics Letters A*, 297(5–6), 273–278.

3. **Valentini, A.** (2010). « Inflationary Cosmology as a Probe of
   Primordial Quantum Mechanics ». *Physical Review D*, 82(6), 063513.
   [doi:10.1103/PhysRevD.82.063513](https://doi.org/10.1103/PhysRevD.82.063513)

4. **Holland, P. R.** (1993). *The Quantum Theory of Motion*. Cambridge
   University Press. Chapitres 6, 12, 15.

5. **Bohm, D. & Hiley, B. J.** (1993). *The Undivided Universe*.
   Routledge. Chapitres 3, 6.

6. **Tajmar, M. et al.** (2021). « The SpaceDrive Project — Thrust
   Balance Development and New Measurements of the Mach-Effect and
   EmDrive Thrusters ». *Acta Astronautica*, 187, 224–237.

7. **Tsiolkovsky, K.** (1903). « The Exploration of Cosmic Space by
   Means of Reaction Devices ». *The Science Review*, 5.

8. **Colin, S. & Struyve, W.** (2007). « Quantum non-equilibrium and
   relaxation to quantum equilibrium for a class of de Broglie–Bohm-type
   theories ». *New Journal of Physics*, 9, 306.
   [doi:10.1088/1367-2630/9/9/306](https://doi.org/10.1088/1367-2630/9/9/306)

---

[← Protocole de validation](04_protocole.md) · [← Retour au README](../README.md)
