# ⚙️ Configuration Matérielle

[← Retour au README](../README.md) · [← Cadre Théorique](02_theorie.md)

---

## Introduction vulgarisée

Imaginez un gros baril métallique — le genre qu'on utilise pour stocker de
l'huile — posé en équilibre sur un fil, comme une balançoire très sensible.
À l'intérieur, on installe un four micro-ondes démonté (le magnétron) qui
envoie ses ondes dans un petit cylindre métallique fermé contenant une fine
brume d'eau. Les micro-ondes sont si intenses qu'elles transforment cette brume
en **plasma** : un gaz où les molécules d'eau sont brisées et ionisées, créant
un petit nuage lumineux — comme un éclair miniature enfermé dans un bocal.

Le baril métallique sert de **cage de Faraday** : aucune radiation ne s'échappe.
Tout est confiné. Et le fil de torsion sur lequel repose le baril est si
sensible qu'il peut détecter une force de l'ordre du millionième de newton —
comparable au poids d'un grain de poussière. Si le plasma « pousse » d'un côté,
le baril tourne imperceptiblement, et on le mesure.

---

## 3.1 Source RF — Magnétron

### Principe de fonctionnement

Un **magnétron à cavité** est un tube à vide qui convertit l'énergie
électrique en ondes micro-ondes. Son fonctionnement repose sur l'interaction
entre un faisceau d'électrons et un ensemble de cavités résonantes :

1. Un **cathode chauffée** (filament) émet des électrons par effet
   thermoïonique.
2. Une **haute tension** (≈ 4 000 V) entre la cathode et l'anode
   accélère les électrons radialement.
3. Un **champ magnétique permanent** (aimant) force les électrons à
   suivre des trajectoires courbes (cycloïdales).
4. Les électrons passent devant les ouvertures des **cavités résonantes**
   creusées dans l'anode, y induisant des oscillations électromagnétiques
   à la fréquence de résonance.
5. Un **couplage par antenne** extrait l'énergie micro-onde des cavités
   vers un guide d'onde.

### Spécifications techniques

| Paramètre | Valeur |
|:---|:---|
| Fréquence | 2,45 GHz (λ = 12,24 cm) |
| Puissance RF | ~ 1 000 W (nominale) |
| Puissance électrique | ~ 1 500 W (entrée) |
| Rendement | ~ 65 % |
| Tension d'anode | ~ 4 000 V DC |
| Courant d'anode | ~ 300 mA |
| Champ magnétique | ~ 0,1 T (aimants permanents) |

### Fréquence de 2,45 GHz

Cette fréquence est choisie car :

- C'est une **bande ISM** (Industriel, Scientifique, Médical) — pas de
  licence requise.
- La longueur d'onde ($\lambda = c/f = 12{,}24$ cm) est compatible avec
  les dimensions de la chambre à plasma.
- La fréquence plasma de la vapeur d'eau ionisée ($f_p \sim 1-9$ GHz)
  chevauche cette fréquence, permettant une **interaction forte** onde-plasma.

### Mode de fonctionnement pulsé

Le magnétron est activé en mode **pulsé** à la fréquence de résonance
mécanique du baril $f = 1/T_0$. Ce mode permet :

- D'amplifier le mouvement du pendule par **résonance mécanique**.
- De distinguer l'effet de poussée de l'effet thermique (le chauffage est
  continu, la poussée est pulsée et corrélée).
- De réduire la puissance thermique moyenne déposée.

---

## 3.2 Enceinte — Baril de 205 litres

### Fonction

Le baril remplit trois fonctions simultanées :

1. **Cage de Faraday** — Confine le rayonnement RF à l'intérieur.
   Aucune fuite significative (< 5 mW/cm² requis par les normes).
2. **Système isolé** — Pour démontrer une force dans un système fermé,
   il ne doit y avoir aucun échange de matière avec l'extérieur.
3. **Masse oscillante** — Le baril suspendu au fil de torsion est
   l'élément mobile dont on mesure le déplacement.

### Spécifications

| Paramètre | Valeur |
|:---|:---|
| Volume | 205 litres |
| Matériau | Acier doux (épaisseur ≈ 1 mm) |
| Masse à vide | ~ 20 kg |
| Conductivité | Suffisante pour l'effet de cage de Faraday |
| Étanchéité RF | Joints conducteurs aux ouvertures |

### Efficacité de blindage

L'atténuation $A$ d'une cage de Faraday en acier à 2,45 GHz est
très élevée. Pour une paroi conductrice d'épaisseur $t$ :

$$A \approx 20 \log_{10}\left(\frac{t}{\delta}\right) \quad [\text{dB}]$$

où $\delta$ est l'épaisseur de peau :

$$\delta = \sqrt{\frac{2}{\omega \mu \sigma}} = \sqrt{\frac{1}{\pi f \mu_0 \sigma}}$$

Pour l'acier à 2,45 GHz ($\sigma \approx 6 \times 10^6$ S/m) :

$$\delta \approx 4 \; \mu\text{m}$$

Une paroi de 1 mm offre donc $A \approx 20 \log_{10}(1000/4) \approx 48$ dB
d'atténuation, soit un facteur $\sim 60\,000$ en puissance.

---

## 3.3 Chambre à Plasma

### Construction

La chambre est un **cylindre métallique** (cuivre ou aluminium) dont une
extrémité est fermée par un **couvercle en Plexiglas** (polyméthacrylate
de méthyle, PMMA) :

- Le cylindre métallique sert de **cavité RF** — ses dimensions sont
  choisies pour supporter un ou plusieurs modes de résonance proches
  de 2,45 GHz.
- Le Plexiglas est **transparent aux micro-ondes** partiellement et
  transparent optiquement, permettant l'observation visuelle du plasma.
- L'ensemble est **hermétique** pour maintenir le vide.

### Modes de résonance

Les modes de résonance d'une cavité cylindrique sont les modes
$\text{TM}_{mnp}$ et $\text{TE}_{mnp}$. La fréquence de résonance est :

$$f_{mnp} = \frac{c}{2\pi\sqrt{\mu_r \varepsilon_r}} \sqrt{\left(\frac{x_{mn}}{a}\right)^2 + \left(\frac{p\pi}{d}\right)^2}$$

où $a$ est le rayon, $d$ la longueur, et $x_{mn}$ est le $n$-ième zéro de
la fonction de Bessel $J_m$ (mode TM) ou de sa dérivée $J'_m$ (mode TE).

Le dimensionnement vise à placer un mode fondamental proche de 2,45 GHz
pour maximiser le couplage avec le magnétron.

---

## 3.4 Médium — Plasma de vapeur d'eau

### Formation du plasma

La vapeur d'eau est injectée à basse pression (~ 1–10 mbar) dans la
chambre. Le champ micro-onde à 2,45 GHz initie l'ionisation par
**claquage** :

1. Les électrons libres résiduels sont accélérés par le champ RF.
2. Ils acquièrent assez d'énergie pour ioniser les molécules d'eau
   par collision : $\text{H}_2\text{O} + e^- \to \text{H}_2\text{O}^+ + 2e^-$
3. Avalanche électronique → formation du plasma.

### Composition chimique

Le plasma de vapeur d'eau contient un mélange complexe d'espèces :

| Espèce | Type | Rôle |
|:---|:---|:---|
| $e^-$ | Électrons libres | Porteurs du courant, modifient $n_e$ |
| $\text{H}_2\text{O}^+$ | Ion moléculaire | Ion primaire |
| $\text{OH}$ | Radical hydroxyle | Espèce réactive dominante |
| $\text{H}$ | Hydrogène atomique | Produit de dissociation |
| $\text{O}$ | Oxygène atomique | Produit de dissociation |
| $\text{H}_2$ | Hydrogène moléculaire | Recombinaison |
| $\text{O}_3$ | Ozone | Sous-produit (⚠️ toxique) |

### Rôle physique dans l'expérience

Le plasma agit comme un **modulateur de phase non-linéaire** :

- Sa densité électronique $n_e$ modifie l'indice de réfraction :
  $n = \sqrt{1 - \omega_p^2 / \omega^2}$
- Si la distribution de $n_e$ est **inhomogène** (plus dense d'un côté),
  l'onde accumule une phase différente selon sa trajectoire.
- Ce gradient de phase est l'analogue du $\nabla S$ de la mécanique
  bohmienne.

---

## 3.5 Capteurs — Tubes Nixie linéaires

### Principe de fonctionnement

Les tubes Nixie **linéaires** (IN-9 et IN-13) sont des tubes à décharge
gazeuse dont la colonne lumineuse a une **longueur proportionnelle au
courant** qui les traverse :

- **IN-9** : longueur de colonne 0–30 mm pour 0–10 mA.
- **IN-13** : longueur de colonne 0–100 mm pour 0–5 mA.

Ils sont remplis de néon avec un peu de mercure (effet Penning) et
fonctionnent à ~ 120–140 V DC.

### Utilisation comme capteurs de plasma

Les tubes Nixie sont utilisés de manière non conventionnelle :

- Placés à proximité de la chambre, ils agissent comme des **capteurs
  de rayonnement RF** — le champ électromagnétique modifie le courant
  de décharge dans le tube.
- La longueur de la colonne lumineuse donne une **indication visuelle
  du flux RF** en ce point.
- En disposant plusieurs tubes autour de la chambre, on obtient une
  **cartographie** du gradient de champ / densité plasma.

---

## 3.6 Mesure — Pendule de torsion

### Principe physique

Le pendule de torsion est un instrument de mesure de force extrêmement
sensible, utilisé depuis Coulomb (1785) et Cavendish (1798).

Un objet (ici le baril) est suspendu à un fil (**fibre de torsion**).
Lorsqu'une force tangentielle $F$ est appliquée à une distance $L$ de
l'axe de rotation, le fil se tord d'un angle $\theta$ :

$$\tau = F \cdot L = \kappa \cdot \theta$$

d'où :

$$\boxed{\theta = \frac{F \cdot L}{\kappa}}$$

où $\kappa$ est la **constante de torsion** du fil (N·m/rad).

### Calibration par oscillation libre

La constante de torsion se détermine par la mesure de la période
d'oscillation libre $T_0$ :

$$T_0 = 2\pi \sqrt{\frac{I}{\kappa}} \quad \Longrightarrow \quad \kappa = \frac{4\pi^2 I}{T_0^2}$$

où $I$ est le moment d'inertie du baril autour de l'axe de torsion.

Pour un cylindre creux de masse $M$, rayon $R$ :

$$I \approx M R^2$$

### Sensibilité

La sensibilité du pendule dépend de la **faiblesse** de $\kappa$.
Plus le fil est fin et long, plus $\kappa$ est petit, plus l'angle
$\theta$ est grand pour une force donnée.

Pour un fil métallique de rayon $r$, longueur $\ell$, module de
cisaillement $G$ :

$$\kappa = \frac{\pi G r^4}{2 \ell}$$

| Matériau | $G$ (GPa) | $r$ (mm) | $\ell$ (m) | $\kappa$ (N·m/rad) |
|:---|:---|:---|:---|:---|
| Tungstène | 161 | 0,05 | 1,0 | $5 \times 10^{-8}$ |
| Acier | 79 | 0,1 | 1,0 | $1,2 \times 10^{-6}$ |
| Cuivre-Béryllium | 50 | 0,05 | 1,0 | $3 \times 10^{-8}$ |

### Estimation de la résolution

Pour une force $F = 3{,}3 \; \mu\text{N}$ (pression de radiation),
un bras de levier $L = 0{,}3$ m, et un fil de tungstène
($\kappa = 5 \times 10^{-8}$ N·m/rad) :

$$\theta = \frac{F \cdot L}{\kappa} = \frac{3{,}3 \times 10^{-6} \times 0{,}3}{5 \times 10^{-8}} \approx 20 \; \text{rad}$$

Cette valeur est irréaliste, ce qui signifie qu'un fil aussi fin serait
trop sensible pour cette application. En pratique, un fil plus rigide
($\kappa \sim 10^{-4}$ N·m/rad) donnerait :

$$\theta \approx 10^{-2} \; \text{rad} \approx 0{,}6°$$

Cet angle est mesurable par analyse vidéo ou par réflexion laser.

### Alternative : Balance de torsion

Si la sensibilité du pendule simple est insuffisante, une **balance de
torsion** (type Cavendish) peut être utilisée, avec un fléau horizontal
portant des masses aux extrémités, suspendu par la fibre. Cette
configuration augmente le moment d'inertie et la stabilité.

---

## Schéma d'ensemble

```
                    ┌─────── Fil de torsion ───────┐
                    │                               │
                    ▼                               │
    ┌───────────────────────────────┐    Support fixe
    │         BARIL 205L            │    (plafond)
    │  ┌─────────────────────┐     │
    │  │   CHAMBRE À PLASMA  │     │
    │  │  ┌───────────────┐  │     │
    │  │  │   PLASMA      │  │     │
    │  │  │   H₂O → H-OH  │  │     │
    │  │  └───────┬───────┘  │     │
    │  │          │          │     │
    │  │   Magnétron 2,45GHz │     │
    │  └─────────────────────┘     │
    │                               │
    │  [Nixie IN-9] [Nixie IN-13]  │
    └───────────────────────────────┘
```

---

## Références

1. **Boot, H. A. H. & Randall, J. T.** (1976). « Historical Notes on
   the Cavity Magnetron ». *IEEE Transactions on Electron Devices*, 23(7),
   724–729.
   [doi:10.1109/T-ED.1976.18476](https://doi.org/10.1109/T-ED.1976.18476)

2. **Pozar, D. M.** (2012). *Microwave Engineering*. 4ᵉ édition, Wiley.
   ISBN 978-0-470-63155-3.

3. **Cavendish, H.** (1798). « Experiments to Determine the Density of
   the Earth ». *Philosophical Transactions of the Royal Society*, 88,
   469–526.
   [doi:10.1098/rstl.1798.0022](https://doi.org/10.1098/rstl.1798.0022)

4. **Coulomb, C. A.** (1785). « Premier mémoire sur l'électricité et le
   magnétisme ». *Mémoires de l'Académie Royale des Sciences*, pp. 569–577.

5. **Chen, F. F.** (2016). *Introduction to Plasma Physics and Controlled
   Fusion*. 3ᵉ édition, Springer. ISBN 978-3-319-22308-7.

6. **Lieberman, M. A. & Lichtenberg, A. J.** (2005). *Principles of
   Plasma Discharges and Materials Processing*. 2ᵉ édition, Wiley.
   ISBN 978-0-471-72001-0.

7. **Jackson, J. D.** (1999). *Classical Electrodynamics*. 3ᵉ édition,
   Wiley. ISBN 978-0-471-30932-1.
   (Chapitre 8 : cavités résonantes.)

---

[← Cadre Théorique](02_theorie.md) · [Section suivante : Protocole de Validation →](04_protocole.md)
