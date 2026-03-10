# ⚙️ Configuration Matérielle

[← Retour au README](../README.md) · [← Cadre Théorique](02_theorie.md)

---

## Inventaire du kit — Statut des composants

> 💡 **En termes simples** — Ce tableau liste toutes les pièces du
> montage, comme la liste de courses d'un kit IKEA. Les ✅ sont
> déjà dans l'atelier ; les 🔶 restent à se procurer. Rien ici n'est
> exotique : la plupart des composants viennent de la quincaillerie,
> d'un micro-ondes de récupération ou d'Amazon.

| # | Composant | Statut | Notes |
|:--|:---|:---|:---|
| 1 | Magnétron 2,45 GHz (1 kW, récupéré d'un micro-ondes) | 🔶 À récupérer | Inclut transfo HT + condensateur + diode |
| 2 | Chambre à vide inox 3 gal (⌀250×250 mm, 0–29 inHg) | 🔶 À acheter | Avec couvercle acrylique 3/4" et joint silicone |
| 3 | 8× tubes Nixie IN-13 | ✅ **En stock** | Disponibles |
| 4 | Batterie Makita 18V Li-ion (BL1850B, 5 Ah) | 🔶 À acheter | Ou BL1860B (6 Ah) ; prévoir 2 batteries |
| 5 | Onduleur 120V AC sinus pur (≥ 1200 W) | 🔶 À acheter | < 1,5 kg, entrée 18V DC |
| 6 | ESP32 (DevKitC ou similaire) | 🔶 À acheter | ~ 5 € ; boîtier alu blindé requis |
| 7 | Baril 205L (acier, récupéré) | 🔶 À trouver | Avec couvercle amovible |
| 8 | Fil de torsion (acier ou tungstène, ⌀ 0,1–0,2 mm) | 🔶 À acheter | Longueur ~ 0,5–1 m |
| 9 | Fléau (tige alu ou inox, ⌀ 10–15 mm, L = 400 mm) | 🔶 À fabriquer | Support chambre + contrepoids |
| 10 | Contrepoids (~ 10 kg, ajustable) | 🔶 À fabriquer | Masse + vis de réglage fin |
| 11 | Pompe à vide (palettes ou membrane, ≥ 10 L/min) | 🔶 À acheter | Occasion acceptable |
| 12 | Vanne à boisseau sphérique DN10 (quart de tour) | 🔶 À acheter | Inox ou laiton, vide-compatible |
| 13 | Grillage métallique (maille < 12 mm) | 🔶 À acheter | Pour la cage de Faraday (couvercle) |
| 14 | Laser diode (< 5 mW, classe 3R) | 🔶 À acheter | Pour mesure angulaire PSD |
| 15 | PSD (Position Sensitive Detector) | 🔶 À acheter | Ou barrette de photodiodes |
| 16 | Capteurs : jauge Pirani, coupleur directionnel, photodiode BPW34, thermocouple K + MAX31855, ADS1115 | 🔶 À acheter | Kit capteurs ESP32 |
| 17 | SSR (relais statique) + MOSFET pour électrovanne | 🔶 À acheter | Commande magnétron |
| 18 | Caméras Wi-Fi (2–3) | 🔶 À acheter | Internes + externes |
| 19 | Miroir plan (~ 20×20 mm) | 🔶 À acheter | Collé sur le fléau |
| 20 | Résistances ballast, shunts, connectique, ruban cuivre | 🔶 À acheter | Consommables |

> **Composant confirmé** : les **8 tubes Nixie IN-13** sont disponibles.
> C'est un élément critique car ces tubes sont de production soviétique
> discontinuée — il est difficile de s'en procurer.

---

## Introduction vulgarisée

Imaginez un petit cylindre en acier inoxydable — une chambre à vide
d'environ 25 cm de diamètre — suspendu à un fil **en plein air**, comme
une balançoire très sensible. À l'intérieur, un four micro-ondes démonté
(le magnétron) envoie ses ondes dans cette chambre contenant une fine
brume d'eau. Les micro-ondes transforment cette brume en **plasma** :
un gaz ionisé lumineux, comme un éclair miniature enfermé dans un bocal.

L'inox est conducteur : la chambre sert donc naturellement de **cage de
Faraday** — aucune radiation ne s'échappe. Le couvercle transparent en
acrylique est recouvert d'un grillage métallique pour compléter le
blindage. L'ensemble est suspendu par un fil de torsion **à l'intérieur
d'un baril métallique de 205 litres**, qui le protège du vent, du soleil
et de toute perturbation extérieure. Le baril est posé au sol et ne
bouge pas — c'est la référence fixe. Si le plasma « pousse » d'un côté,
la chambre tourne imperceptiblement dans le baril, et on le mesure par
réflexion laser à travers un petit hublot.

---

## 3.1 Source RF — Magnétron

> 💡 **En termes simples** — Un magnétron, c'est le composant qui
> chauffe vos plats dans un four micro-ondes. Il transforme
> l'électricité en ondes radio à 2,45 GHz. Ici, au lieu de cuire
> un bol de soupe, on l'utilise pour ioniser de la vapeur d'eau —
> exactement la même pièce, recyclée d'un four de cuisine.
> *(Inventé en 1940 par Boot & Randall [1] pour le radar militaire.)*

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
mécanique de la chambre $f = 1/T_0$. Ce mode permet :

- D'amplifier le mouvement du pendule par **résonance mécanique**.
- De distinguer l'effet de poussée de l'effet thermique (le chauffage est
  continu, la poussée est pulsée et corrélée).
- De réduire la puissance thermique moyenne déposée.

---

## 3.2 Enceinte intégrée — Chambre à vide inox

> 💡 **Simplification majeure** — L'architecture initiale prévoyait un
> baril de 205L comme cage de Faraday externe + une chambre à plasma
> séparée. La chambre à vide en inox décrite ci-dessous **cumule les
> trois fonctions** (cage de Faraday, chambre à vide, masse oscillante).
> Le baril de 205L sert d'**enceinte du pendule de torsion** : la
> chambre est suspendue par un fil à l'intérieur du baril, qui repose
> au sol comme référentiel fixe. Le baril cumule ainsi 5 fonctions :
> protection contre le vent, stabilité thermique, double cage de
> Faraday, rétention d'éclats et confinement des gaz (défense en
> profondeur). Voir la [section pendule](#36-mesure--pendule-de-torsion)
> et la [section sécurité](05_securite.md#enceinte-de-confinement-secondaire-baril-de-205l).

### Fonction

La chambre inox remplit **trois fonctions simultanées** :

1. **Chambre à vide et cavité RF** — Confine le plasma et sert de
   cavité résonante pour les micro-ondes.
2. **Cage de Faraday** — L'inox est conducteur ($\sigma \approx 1{,}4 \times 10^6$ S/m) ;
   les parois métalliques + le couvercle acrylique recouvert de grillage
   confinent le rayonnement RF.
3. **Masse oscillante** — Suspendue au fil de torsion, c'est l'élément
   mobile dont on mesure le déplacement.

### Spécifications

| Paramètre | Valeur |
|:---|:---|
| Type | Chambre à vide de laboratoire |
| Volume | 3 gallons US (≈ 11,4 litres) |
| Matériau | Acier inoxydable |
| Diamètre intérieur | 250 mm |
| Hauteur intérieure | 250 mm |
| Couvercle | Acrylique (PMMA), épaisseur 3/4" (19 mm) |
| Joint d'étanchéité | Silicone |
| Certification vide | 0 à 29 inHg (≈ 0 à 982 mbar de dépression) |
| Pression résiduelle min. | ~ 18 mbar (vide limite à 29 inHg) |
| Masse estimée (vide) | ~ 5 kg |

> **Note :** 29 inHg correspond à une pression absolue d'environ
> $1\,013 - 982 = 31$ mbar. Pour atteindre le régime optimal de
> 2–5 mbar, une pompe à vide plus performante (pompe à palettes) sera
> nécessaire. La certification à 29 inHg garantit toutefois la tenue
> mécanique sous vide partiel.

### Efficacité de blindage RF

L'atténuation $A$ d'une cage de Faraday en inox à 2,45 GHz :

L'épaisseur de peau dans l'inox ($\sigma \approx 1{,}4 \times 10^6$ S/m) :

$$\delta = \sqrt{\frac{1}{\pi f \mu_0 \sigma}} = \sqrt{\frac{1}{\pi \times 2{,}45 \times 10^9 \times 4\pi \times 10^{-7} \times 1{,}4 \times 10^6}} \approx 8{,}6 \; \mu\text{m}$$

Pour une paroi d'inox typique (~ 2 mm) :

$$A \approx 20 \log_{10}\left(\frac{2\,000}{8{,}6}\right) \approx 47 \; \text{dB}$$

Soit un facteur $\sim 50\,000$ en puissance — blindage excellent.

### Complétion de la cage de Faraday (couvercle)

Le couvercle en acrylique est transparent aux micro-ondes. Pour fermer
la cage de Faraday :

- **Grillage métallique** (cuivre ou inox) plaqué sur la face extérieure
  du couvercle. Maille < $\lambda/10 = 12$ mm.
- **Contact galvanique** entre le grillage et la bride inox de la chambre
  (ruban de cuivre conducteur, pinces, ou vis).
- Le grillage est suffisamment ouvert pour permettre l'observation
  visuelle du plasma et le passage de la lumière vers la photodiode.
- L'ensemble (acrylique + grillage) remplace la transmission directe
  par une cavité entièrement blindée.

### Avantages par rapport au baril de 205L

| Critère | Baril 205L (ancien) | Chambre inox 3 gal (actuel) |
|:---|:---|:---|
| Masse | ~ 20 kg | ~ 5 kg |
| Volume | 205 L | 11,4 L |
| Sensibilité pendule | Faible (masse élevée → $\theta$ petit) | **4× meilleure** (masse réduite) |
| Certification vide | Aucune (bricolage) | 0–29 inHg (industrielle) |
| Cage de Faraday | Native (acier) | Native (inox) + grillage couvercle |
| Encombrement | Volumineux | Compact (25 × 25 cm) |
| Complexité | Chambre séparée à l'intérieur | Tout intégré |

---

## 3.3 Cavité RF et modes de résonance

> 💡 **En termes simples** — Imaginez un tambour : frappez-le, et il
> vibre selon des motifs précis (les « modes »). Ici, la chambre inox
> est le tambour et les micro-ondes sont le son. Parmi les dizaines
> de motifs possibles, un seul — le mode TM₃₁₀ — vibre pile à
> 2,45 GHz, la fréquence de notre magnétron. C'est une coïncidence
> heureuse des dimensions de la chambre. Les formules ci-dessous
> calculent tous ces motifs (Pozar [2], chap. 6).

### Dimensions de la cavité

La chambre inox sert directement de **cavité résonante** pour les
micro-ondes. Ses dimensions :

- Rayon : $a = 125$ mm
- Hauteur : $d = 250$ mm
- Parois : inox (conductivité finie → pertes ohmiques modérées)
- Couvercle : acrylique 19 mm (partiellement transparent aux RF →
  recouvert de grillage pour le confinement)

### Modes de résonance

Les modes de résonance d'une cavité cylindrique sont les modes
$\text{TM}_{mnp}$ et $\text{TE}_{mnp}$. La fréquence de résonance est :

$$f_{mnp} = \frac{c}{2\pi} \sqrt{\left(\frac{x_{mn}}{a}\right)^2 + \left(\frac{p\pi}{d}\right)^2}$$

où $x_{mn}$ est le $n$-ième zéro de $J_m$ (mode TM) ou de $J'_m$
(mode TE) — voir Pozar [2], §6.3 pour la dérivation complète, et
Jackson [7], chap. 8 pour le traitement en électrodynamique classique.

### Calcul pour $a = 125$ mm, $d = 250$ mm

| Mode | $x_{mn}$ | $f$ (GHz) | Compatible 2,45 GHz ? |
|:---|:---|:---|:---|
| TM$_{010}$ | 2,405 | $\frac{c \times 2{,}405}{2\pi \times 0{,}125} = 0{,}918$ | Non (trop bas) |
| TM$_{110}$ | 3,832 | $\frac{c \times 3{,}832}{2\pi \times 0{,}125} = 1{,}46$ | Non |
| TE$_{111}$ | 1,841 | $\frac{c}{2\pi}\sqrt{(1{,}841/0{,}125)^2 + (\pi/0{,}25)^2} = 1{,}17$ | Non |
| TM$_{011}$ | 2,405 | $\frac{c}{2\pi}\sqrt{(2{,}405/0{,}125)^2 + (\pi/0{,}25)^2} = 1{,}14$ | Non |
| TM$_{210}$ | 5,136 | 1,96 | Non |
| TE$_{211}$ | 3,054 | 1,32 | Non |
| TM$_{310}$ | 6,380 | **2,44** | **✔ Excellent !** |
| TE$_{011}$ | 3,832 | 1,62 | Non |
| TM$_{020}$ | 5,520 | 2,11 | Non (proche) |
| TE$_{311}$ | 4,201 | 1,78 | Non |
| TM$_{410}$ | 7,588 | 2,90 | Non |
| TE$_{411}$ | 5,318 | 2,19 | Non (proche) |
| TM$_{120}$ | 7,016 | **2,68** | Proche |
| TE$_{112}$ | 1,841 | 1,46 | Non |
| TM$_{320}$ | 8,417 | 3,22 | Non |
| TE$_{012}$ | 3,832 | 2,17 | Non (proche) |
| TE$_{511}$ | 6,416 | **2,62** | Proche |

**Résultat clé** : le mode **TM$_{310}$** à **2,44 GHz** est quasi
parfaitement accordé à la fréquence du magnétron (2,45 GHz). C'est
une coïncidence favorable des dimensions de la chambre.

D'autres modes (TM$_{020}$ à 2,11 GHz, TM$_{120}$ à 2,68 GHz,
TE$_{511}$ à 2,62 GHz) sont proches et pourraient être excités
par la largeur spectrale du magnétron ($\Delta f \sim 50$ MHz),
créant un champ multimode complexe — favorable à l'inhémogénéité
de la distribution de champ, et donc au gradient de phase recherché.

### Couplage du magnétron

Le magnétron est couplé à la cavité par une **antenne** (sonde
capacitive) ou un **iris** (ouverture dans la paroi) positionné pour
exciter préférentiellement le mode TM$_{310}$. La position optimale
est au maximum du champ électrique de ce mode.

### Disposition interne de la chambre

La chambre inox regroupe **tous les composants actifs** de l'expérience.
Voici l'agencement interne, vu en coupe :

```
    ╔═══════════════════════════════════╗ ← Couvercle acrylique 3/4"
    ║  Grillage Faraday (maille <12mm) ║     + grillage
    ╚═══════════════════════════════════╝
    ┌───────────────────────────────────┐
    │  8× Nixie IN-13                  │ ← Paroi interne (octogone)
    │  (montés verticalement sur la    │
    │   paroi, espacés de 45°)         │
    │                                  │
    │  ┌────────────────────────────┐  │
    │  │  PLASMA  H₂O              │  │ ← Volume central (~11 L)
    │  │  2–5 mbar                 │  │
    │  │                           │  │
    │  └────────────────────────────┘  │
    │                                  │
    │  Magnétron (sonde ou iris)  ──→  │ ← Couplé à la paroi (~30°)
    │  Jauge Pirani               ──→  │ ← Feedthrough paroi
    │  Coupleur directionnel      ──→  │ ← Entre magnétron et cavité
    │  Photodiode BPW34           ──→  │ ← Face au plasma
    │  Thermocouple K             ──→  │ ← Collé paroi extérieure
    │                                  │
    │  Vanne DN10 (quart de tour) ──→  │ ← Pompage + injection H₂O
    └───── ── ── ── ── ── ── ── ──────┘
            Joint silicone
```

L'**alimentation embarquée** (batterie, onduleur, ESP32) est montée
**à l'extérieur de la chambre**, solidaire du fléau. Elle n'est pas
dans le volume sous vide — seuls les câbles capteurs et le câble HT
du magnétron traversent la paroi via des feedthroughs étanches.

---

## 3.4 Médium — Plasma de vapeur d'eau

> 💡 **En termes simples** — Un plasma, c'est un gaz tellement
> chauffé (ou électrifié) que ses atomes perdent des électrons.
> C'est le « quatrième état de la matière » — après solide, liquide,
> gaz. Les néons dans la rue, les éclairs, le Soleil : tous des
> plasmas. Ici, on ionise de la vapeur d'eau à l'aide des
> micro-ondes, un peu comme un orage miniature dans une boîte.
> Le plasma obtenu modifie la vitesse des ondes qui le traversent
> (Chen [5], Lieberman & Lichtenberg [6]).

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

## 3.5 Capteurs — Tubes Nixie linéaires (8× IN-13)

### Principe de fonctionnement

Les tubes Nixie **linéaires** (IN-9 et IN-13) sont des tubes à décharge
gazeuse dont la colonne lumineuse a une **longueur proportionnelle au
courant** qui les traverse :

- **IN-9** : longueur de colonne 0–30 mm pour 0–10 mA.
- **IN-13** : longueur de colonne 0–100 mm pour 0–5 mA (plus long,
  meilleure résolution spatiale).

Ils sont remplis de néon avec un peu de mercure (effet Penning) et
fonctionnent à ~ 120–140 V DC. Alimentés par le 120 V AC de
l'onduleur embarqué via un redresseur/résistance ballast simple.

### Utilisation comme capteurs de plasma

Les tubes Nixie sont utilisés de manière non conventionnelle :

- Placés **à l'intérieur de la chambre** (sur la paroi interne),
  ils agissent comme des **capteurs de rayonnement RF** — le champ
  électromagnétique modifie le courant de décharge dans le tube.
- La longueur de la colonne lumineuse donne une **indication visuelle
  directe** du flux RF en ce point.
- En disposant **8 tubes IN-13** autour de la chambre, on obtient une
  **cartographie octogonale** du gradient de champ / densité plasma.

### Disposition des 8 IN-13 — Cartographie du gradient

Les 8 tubes sont montés **verticalement** sur la paroi intérieure de
la chambre, espacés de **45°** (octogone régulier) :

```
            Vue du dessus — Chambre inox (⌀ 250 mm)

                      N₁ (0°)
                    ╱        ╲
               N₈ (315°)   N₂ (45°)
              │                    │
        N₇ (270°)   ┌──────┐  N₃ (90°)
              │     │magnét│     │
               N₆ (225°)   N₄ (135°)
                    ╲        ╱
                      N₅ (180°)

            Nₖ = tube IN-13 n° k
            Le magnétron est couplé à ~ 30° du N₁
```

Cette disposition permet de mesurer :

| Mesure | Méthode |
|:---|:---|
| **Symétrie du champ** | Comparer les 8 colonnes lumineuses : si toutes égales → champ homogène ; si gradient → asymétrie |
| **Direction du gradient** | Le tube le plus long indique la région de plus forte densité $n_e$ |
| **Intensité du gradient** | $\Delta L = L_{\max} - L_{\min}$ proportionnel à $\nabla n_e$ |
| **Confirmation de l'asymétrie** | Corrélation entre la direction du gradient Nixie et la direction de la force mesurée au pendule |

> 💡 **C'est la mesure la plus critique** — Si on observe une force au
> pendule sans asymétrie visible sur les Nixie, c'est probablement un
> artefact. Si l'asymétrie Nixie corrèle spatialement avec la force,
> c'est un indice fort du gradient de phase.

### Lecture des Nixie par l'ESP32

Chaque tube IN-13 est alimenté en série avec une **résistance ballast**
de précision (± 1 %). Le courant $I_k$ dans chaque tube est mesuré par
l'ESP32 via un shunt de 10 Ω (→ signal 0–50 mV pour 0–5 mA, amplifié
par un INA219 ou un ADS1115). Les 8 courants sont loggés en CSV
et transmis en Wi-Fi.

Alternativement, une **caméra Wi-Fi** embarquée peut photographier les
8 tubes simultanément pour une lecture visuelle directe.

---

## 3.6 Mesure — Pendule de torsion

> 💡 **En termes simples** — La chambre à vide est suspendue par un fil
> très fin à l'intérieur du baril de 205L, comme une marionnette dans
> un théâtre. Le baril est posé au sol et ne bouge pas : c'est le
> « décor fixe ». Si le plasma pousse la chambre ne serait-ce qu'un
> millionième de newton, le fil se tord légèrement. Un petit miroir
> collé sur la chambre réfléchit un rayon laser vers un détecteur,
> et on mesure le déplacement avec une précision extrême — le tout
> protégé du vent et des vibrations par le baril.

### Architecture — Chambre décentrée sur fléau

Le baril de 205L (⌀ 580 mm × 880 mm de haut) sert d'**enceinte du
pendule**. La chambre inox (⌀ 250 × 250 mm) est montée **décentrée**
par rapport à l'axe de torsion, sur un **fléau horizontal** (type
balance de Cavendish). Un contrepoids équilibre la masse.

#### Pourquoi décentrer la chambre ?

La grandeur mesurée par un pendule de torsion est le **couple** :

$$\tau = F \times d$$

où $F$ est la force produite par le plasma et $d$ est la distance
entre la ligne d'action de $F$ et l'axe de rotation (bras de levier).

| Configuration | Bras de levier $d$ | Couple $\tau$ pour $F = 3{,}3~\mu$N |
|:---|:---|:---|
| Chambre centrée | $R_{\text{chambre}} \approx 0{,}125$ m (force tangentielle requise) | $4{,}1 \times 10^{-7}$ N·m |
| Chambre décentrée (fléau 200 mm) | $d = 0{,}20$ m | $6{,}6 \times 10^{-7}$ N·m |

Mais l'avantage principal n'est pas le facteur 1,6× — c'est que :

1. **Toute force nette** (quelle que soit sa direction dans le plan
   horizontal) produit un couple si la chambre est hors axe. Avec
   la chambre centrée, seule la composante tangentielle contribue.
2. **L'inversion à 180°** est triviale : faire pivoter le fléau de
   180° change le signe du couple → test de contrôle immédiat.
3. **Le fléau amplifie le moment d'inertie** $I$, ce qui augmente
   $T_0$ et éloigne la fréquence de résonance du bruit (avantage
   signal/bruit en basse fréquence).

> 💡 **Analogie** — C'est exactement le principe de la
> [balance de Cavendish](https://fr.wikipedia.org/wiki/Exp%C3%A9rience_de_Cavendish)
> (1798) qui a permis de « peser la Terre ». Cavendish a mesuré des
> forces gravitationnelles de l'ordre du nano-newton grâce à un fléau
> de 1,8 m. Notre fléau de 0,4 m mesure des micro-newtons — mille
> fois plus gros.

#### Géométrie du fléau

```
    Vue du dessus — Baril de 205L (⌀ 580 mm)

                    ┌─ Fil de torsion
                    │  (axe de rotation)
                    ▼
    ┌───────────────●───────────────┐
    │               │               │
    │   ┌───────┐   │   ┌───────┐   │
    │   │Chambre│   │   │Contre-│   │
    │   │ inox  │   │   │ poids │   │
    │   │⌀250mm │   │   │       │   │
    │   └───────┘   │   └───────┘   │
    │    ← 200 →    │    ← 200 →    │
    │      mm       │      mm       │
    └───────────────┴───────────────┘
                  Fléau
              (tige rigide)
```

| Paramètre | Valeur |
|:---|:---|
| Longueur du fléau | 400 mm (200 mm de chaque côté de l'axe) |
| Bras de levier chambre | $d = 200$ mm |
| Masse chambre (assemblage complet) | ~ 10 kg |
| Masse contrepoids | ~ 10 kg (ajustable) |
| Matériau fléau | Tige en aluminium ou inox, ⌀ 10–15 mm |

Le fléau doit être **parfaitement équilibré** : le centre de masse
total de l'assemblage (chambre + fléau + contrepoids) doit être
exactement **sur l'axe de torsion**. Un déséquilibre résiduel crée
un couple gravitationnel parasite.

Équilibrage : ajuster la position du contrepoids sur le fléau par
une vis de réglage fin (± 1 mm). Critère : le système au repos doit
rester stable quelle que soit l'orientation du fléau.

### Table d'architecture

| Élément | Position |
|:---|:---|
| Fil de torsion | Ancré au **couvercle du baril** (seul lien mécanique) |
| Fléau horizontal | Suspendu au fil, **traverse le baril** horizontalement |
| Chambre inox + alimentation embarquée | **Décentrée** à 200 mm de l'axe (côté A du fléau) |
| Contrepoids (~ 10 kg) | **Côté B** du fléau, à 200 mm de l'axe |
| 8× Nixie IN-13 | **Intérieur** de la chambre (octogone sur la paroi) |
| Miroir de mesure | Collé **sur le fléau**, près de l'axe (face au hublot) |
| Laser + PSD | Fixés à la **paroi interne du baril** (référentiel fixe) |
| Baril de 205L | **Posé au sol** (référentiel fixe) |
| Pompe à vide | **Externe**, déconnectée pendant la mesure |
| Caméras Wi-Fi | Internes (hublot) et externes (mobiles) |

Le baril offre un environnement **calme et confiné** :

- **Pas de vent** — perturbation n° 1 en extérieur, totalement éliminée.
- **Stabilité thermique** — l'inertie du baril en acier tamponne les
  variations de température ambiante.
- **Atmosphère interne contrôlée** — l'air piégé dans le baril (entre
  la chambre et les parois) est immobile.

### Mesure angulaire par réflexion laser

La rotation de la chambre est mesurée par un système optique interne :

1. Un **miroir plan** est collé sur la paroi de la chambre.
2. Un **laser diode** (< 5 mW, classe 3R) est fixé à la paroi du baril,
   dirigé vers le miroir.
3. Le faisceau réfléchi frappe un **photodétecteur linéaire** (PSD
   ou barrette de photodiodes) monté sur la paroi opposée du baril.
4. Le déplacement du spot sur le détecteur est proportionnel à
   l'angle de rotation $\theta$ :

$$\Delta x = 2 D \cdot \theta$$

où $D$ est la distance miroir–détecteur (~ 0,3 m dans le baril).
Pour $\theta = 0{,}24°= 4{,}1 \times 10^{-3}$ rad :

$$\Delta x = 2 \times 0{,}3 \times 4{,}1 \times 10^{-3} \approx 2{,}5 \; \text{mm}$$

Ce déplacement est facilement mesurable par un PSD
([Position Sensitive Detector](https://en.wikipedia.org/wiki/Position_sensitive_device))
avec une résolution de ~ 1 µm.

Un petit **hublot en verre** (⌀ 20–30 mm) percé dans la paroi du baril
permet aussi l'observation visuelle ou vidéo du miroir si nécessaire.

### Découplage mécanique — Alimentation embarquée

> 💡 **Simplification radicale** — Plutôt que de gérer des câbles
> souples entre la partie fixe (baril) et la partie mobile (chambre),
> **toute l'alimentation électrique est embarquée** sur l'assemblage
> suspendu. Résultat : **zéro câble** entre le baril et la chambre.
> Le seul lien physique est le fil de torsion. Le système est
> véritablement isolé.

#### Architecture électrique embarquée

L'assemblage suspendu au fil de torsion comprend :

| Composant | Masse (kg) | Rôle |
|:---|:---|:---|
| Chambre inox 3 gal | ~ 5,0 | Cavité RF, vide, cage de Faraday |
| Batterie Li-ion 18V Makita (BL1850B, 5 Ah) | 0,63 | Source d'énergie |
| Onduleur 120 V AC (300–600 W) | ~ 1,0 | Conversion DC→AC |
| Transformateur HT + magnétron | ~ 3,5 | Inclus dans la chambre |
| ESP32 (boîtier blindé) | < 0,1 | Contrôle PID + télémétrie Wi-Fi |
| Capteurs (Pirani, coupleur, photodiode, thermo.) | < 0,2 | Asservissement |
| **Total assemblage suspendu** | **~ 10,4** | |

#### Bilan énergétique

La batterie Makita BL1850B offre 18 V × 5 Ah = **90 Wh**.

| Mode | Puissance moy. | Autonomie |
|:---|:---|:---|
| Magnétron continu (1 kW sortie, ~1,2 kW entrée AC) | 1 400 W (pertes onduleur) | **~ 4 min** |
| Magnétron pulsé 50 % duty ($f = 1/T_0$) | ~ 700 W | **~ 8 min** |
| Magnétron pulsé 25 % duty | ~ 350 W | **~ 15 min** |
| Veille (ESP32 + capteurs, magnétron off) | ~ 5 W | **~ 18 h** |

Pour une session de mesure de 20 cycles à $T_0 \sim 20$ s :
$ 20 \times 20 = 400$ s ≈ **7 min** de fonctionnement pulsé → une batterie
5 Ah suffit en mode 50 % duty.

> **Astuce** : utiliser **deux batteries en parallèle** (via adaptateur
> double Makita) pour doubler l'autonomie à ~15 min en mode 50 %.
> Les batteries 6 Ah (BL1860B, 108 Wh) offrent encore plus de marge.

#### Onduleur 120 V

L'onduleur convertit le 18 V DC de la batterie en 120 V AC 60 Hz
pour alimenter le transformateur HT du magnétron.

| Critère | Exigence |
|:---|:---|
| Puissance nominale | ≥ 1 200 W (crête magnétron) |
| Forme d'onde | **Sinusoïdale pure** (recommandé pour le transfo HT) |
| Masse | < 1,5 kg (embarqué sur le pendule) |
| Rendement | > 85 % |

> ⚠️ **Sécurité** — L'onduleur produit du 120 V AC et le transformateur
> génère **4 000 V DC**. L'ESP32 embarqué doit pouvoir **couper le SSR
> du magnétron** en cas d'anomalie, même sans connexion Wi-Fi (watchdog
> autonome). La batterie doit être protégée contre les courts-circuits
> (BMS intégré dans les batteries Makita).

#### Avantages du tout-embarqué

| Critère | Architecture câblée (ancien) | Tout embarqué (actuel) |
|:---|:---|:---|
| Câbles fixe→mobile | HT + capteurs en boucle pendante | **Aucun** |
| Couple parasite $\kappa_{\text{câbles}}$ | ~ $10^{-5}$ N·m/rad (~10 % de $\kappa$) | **0** |
| Système fermé | Partiellement (câbles traversent) | **Totalement** |
| Complexité calibration | Mesurer $\kappa_{\text{total}}$ in situ | $\kappa = \kappa_{\text{fil}}$ uniquement |
| Masse suspendue | ~ 5 kg | ~ 10 kg (recalcul $I$ nécessaire) |

#### Nouveau moment d'inertie (configuration fléau)

Avec le fléau, le moment d'inertie est dominé par les deux masses
(chambre + contrepoids) aux extrémités :

$$I = M_{\text{chambre}} \, d^2 + M_{\text{contrepoids}} \, d^2 = 2 M d^2$$

Pour $M \approx 10$ kg et $d = 0{,}20$ m :

$$I \approx 2 \times 10 \times 0{,}20^2 = 0{,}80 \; \text{kg}\cdot\text{m}^2$$

La période d'oscillation libre :

$$T_0 = 2\pi \sqrt{\frac{I}{\kappa}} = 2\pi \sqrt{\frac{0{,}80}{10^{-4}}} \approx 562 \; \text{s} \approx 9{,}4 \; \text{min}$$

C'est long mais très avantageux :
- La fréquence de pulsation est basse ($f_0 \approx 1{,}8$ mHz).
- C'est **loin** des fréquences de bruit sismique (> 1 Hz) et de
  vibration mécanique (> 0,1 Hz) → **rapport S/B excellent**.
- Le bilan énergétique est favorable : en mode pulsé 50 %, la
  batterie 5 Ah suffit pour~ 1 cycle complet ($T_0 \approx$ 9 min,
  magnétron actif ~ 4,5 min → 85 Wh requis ≈ 90 Wh dispo).
- Pour accumuler 5+ cycles, utiliser deux batteries (180 Wh) ou
  réduire le duty cycle.

#### Connexion unique restante : la pompe à vide

La pompe reste **externe et fixe** (trop lourde pour être embarquée).
Elle est connectée uniquement pendant la phase de préparation, puis
déconnectée via la **vanne d'isolement** (quart de tour, DN10) montée
sur la chambre.

| Phase | Pompe | Tuyau | Chambre |
|:---|:---|:---|:---|
| 1. Pompage + injection | Active | Connecté | **Bridée** |
| 2. Fermeture vanne | Arrêtée | Connecté | Bridée |
| 3. Déconnexion tuyau | Off | **Déconnecté** | **Libre** |
| 4. Amortissement (~30 min) | Off | Aucun | Libre (repos) |
| 5. Mesure | Off | Aucun | Libre |

> **Tenue du vide** — À 2–5 mbar, un débit de fuite de $10^{-3}$
> mbar·L/s donne une remontée de ~ 0,005 mbar/min dans 11,4 L
> — négligeable sur une session de 15 min.

#### Caméras de surveillance

Plusieurs **caméras sans fil** (Wi-Fi) sont placées à divers points :

| Caméra | Position | Vue |
|:---|:---|:---|
| Caméra 1 (fixe) | Hublot du baril | Miroir de mesure / confirmations PSD |
| Caméra 2 (fixe) | Extérieur, plongée | Vue d'ensemble du baril |
| Caméra 3 (mobile, optionnel) | Trépied, angle variable | Gros plan, détails |

Les caméras fournissent une **vérification indépendante** du signal PSD
et documentent chaque session pour une validation ultérieure.

#### Checklist de découplage

- [ ] Vanne d'isolement fermée et tuyau de pompe déconnecté
- [ ] Batterie chargée (vérifier indicateur LED Makita)
- [ ] Onduleur et ESP32 sous tension (vérifier Wi-Fi)
- [ ] Chambre libre de tourner sans frottement ni butoir
- [ ] Aucun câble entre le baril et la chambre
- [ ] Caméras sans fil en marche

---

### Principe physique

Le pendule de torsion est un instrument de mesure de force extrêmement
sensible, utilisé depuis Coulomb (1785) et Cavendish (1798).

Un objet (ici la chambre à vide) est suspendu à un fil (**fibre de torsion**).
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

où $I$ est le moment d'inertie de l'assemblage suspendu autour de l'axe
de torsion.

Pour la configuration fléau (chambre + contrepoids, chacun à $d = 0{,}20$ m
de l'axe, masse $M \approx 10$ kg chacun) :

$$I \approx 2 M d^2 = 2 \times 10 \times 0{,}20^2 = 0{,}80 \; \text{kg}\cdot\text{m}^2$$

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
un bras de levier $L = 0{,}20$ m (distance chambre–axe sur le fléau),
et un fil de tungstène ($\kappa = 5 \times 10^{-8}$ N·m/rad) :

$$\theta = \frac{F \cdot L}{\kappa} = \frac{3{,}3 \times 10^{-6} \times 0{,}20}{5 \times 10^{-8}} \approx 13{,}2 \; \text{rad}$$

Cette valeur est irréaliste, ce qui signifie qu'un fil aussi fin serait
trop sensible. En pratique, un fil plus rigide
($\kappa \sim 10^{-4}$ N·m/rad) donnerait :

$$\theta = \frac{3{,}3 \times 10^{-6} \times 0{,}20}{10^{-4}} \approx 6{,}6 \times 10^{-3} \; \text{rad} \approx 0{,}38°$$

Cet angle correspond à un déplacement du spot laser de $\Delta x \approx
4{,}0$ mm sur le PSD (voir ci-dessus) — largement mesurable.

> **Note** — La configuration fléau augmente le moment d'inertie
> ($I = 0{,}80$ vs $0{,}225$ kg·m²), ce qui allonge la période $T_0$
> (9 min vs 5 min), mais **augmente aussi le bras de levier** de 0,15
> à 0,20 m. La sensibilité statique $\theta = FL/\kappa$ est donc
> **améliorée de 33 %** par rapport à la chambre centrée.

### Résumé comparatif : centrée vs fléau

| Critère | Chambre centrée | Fléau (d = 200 mm) |
|:---|:---|:---|
| Bras de levier | ~ 0,125 m (tangentiel seulement) | **0,20 m (toute direction)** |
| Sensibilité statique ($\theta$) | 0,24° pour 3,3 µN | **0,38°** (+60 %) |
| Moment d'inertie | 0,225 kg·m² | 0,80 kg·m² |
| Période $T_0$ | ~ 5 min | ~ 9 min |
| Inversion 180° | Complexe (retourner la chambre) | **Trivial** (pivoter le fléau) |
| Équilibrage | Automatique (centré) | Ajustement contrepoids requis |
| Encombrement dans le baril | Compact | Plus serré (fléau 400 mm vs ⌀ 580 mm) |

> **Verdict** — La configuration fléau est **nettement supérieure** pour
> la sensibilité et les tests de contrôle. L'encombrement est gérable :
> le fléau de 400 mm tient dans le baril de ⌀ 580 mm avec 90 mm de
> dégagement de chaque côté.

---

## 3.7 Contrôle — Microcontrôleur

> 💡 **En termes simples** — Le plasma est capricieux : si on le laisse
> sans surveillance, il dérive hors des conditions idéales en quelques
> fractions de seconde. C'est comme essayer de maintenir la température
> d'une douche en jouant avec le robinet — sauf qu'ici le « robinet »
> c'est la pression de gaz et la puissance micro-ondes, et la « douche »
> c'est un plasma à 30 000 °C.
>
> On confie donc cette tâche à un petit ordinateur embarqué (un
> [microcontrôleur](https://fr.wikipedia.org/wiki/Microcontr%C3%B4leur))
> qui mesure en permanence l'état du plasma et ajuste les paramètres
> pour le garder au point de résonance. C'est le même principe qu'un
> thermostat, mais appliqué à un plasma. Le microcontrôleur est
> **embarqué directement sur l'assemblage suspendu**, alimenté par
> la batterie Makita et communiquant par **Wi-Fi** — aucun câble
> vers l'extérieur.

### Choix du microcontrôleur

| Critère | Exigence | Candidat : [ESP32](https://fr.wikipedia.org/wiki/ESP32) |
|:---|:---|:---|
| ADC | ≥ 4 canaux, ≥ 12 bits, ≥ 1 kHz | 18 canaux, 12 bits, SAR ~ 1 kHz ✔ |
| PWM | ≥ 2 sorties, résolution ≥ 10 bits | 16 canaux LEDC, 16 bits ✔ |
| Wi-Fi / BLE | Télémétrie temps réel | Intégré ✔ |
| GPIO | Relais pompe, sécurité | 34 GPIO ✔ |
| Coût | Accessible | ~ 5 € ✔ |
| Blindage RF | Survie à proximité du magnétron | Boîtier métallique obligatoire ⚠️ |

**Alternative** : un [Arduino](https://fr.wikipedia.org/wiki/Arduino) Nano
suffit si la télémétrie sans fil n'est pas requise. Pour du temps réel
strict, un [STM32](https://en.wikipedia.org/wiki/STM32) (ARM Cortex-M4)
offre un ADC plus rapide (1 MHz) et un DMA matériel.

### Architecture de la boucle

```
  ┌────────────────────────────────────────────────────┐
  │       MICROCONTRÔLEUR (ESP32) — EMBARQUÉ            │
  │       Alimentation : batterie Makita 18V → DC-DC 5V │
  │                                                      │
  │   ADC0 ← Jauge pression (Pirani)                     │
  │   ADC1 ← Photodiode (luminosité plasma)              │
  │   ADC2 ← Coupleur directionnel (P_réfléchie)          │
  │   ADC3 ← Thermocouple type K (via MAX31855)           │
  │   ADC4 ← Tension batterie (diviseur résistif)         │
  │   ADC5 ← NTC température batterie / onduleur          │
  │                                                      │
  │   PWM0 → Électrovanne admission H₂O (via MOSFET)     │
  │   PWM1 → Duty cycle magnétron (via SSR / triac)      │
  │   GPIO → LED/Buzzer alarme sécurité                  │
  │                                                      │
  │   Wi-Fi → Dashboard temps réel (MQTT / WebSocket)    │
  │   SD    → Logging CSV (horodatage + tous canaux)     │
  └────────────────────────────────────────────────────┘
```

### Capteurs — Détail

#### Pression (jauge Pirani)

La [jauge Pirani](https://fr.wikipedia.org/wiki/Jauge_de_Pirani) mesure
la pression par la variation de conductivité thermique du gaz. Plage
typique : 10⁻³ à 100 mbar — parfaitement adaptée au régime 2–5 mbar.
Sortie analogique 0–10 V (diviseur résistif pour le 3,3 V de l'ESP32).

#### Puissance RF réfléchie (coupleur directionnel)

Un [coupleur directionnel](https://fr.wikipedia.org/wiki/Coupleur_directif)
inséré entre le magnétron et la chambre prélève une fraction (~ −20 dB)
de l'onde réfléchie. Après détection par diode Schottky, le signal DC
est proportionnel à $P_r$.

**C'est le signal-clé** de l'asservissement : à la résonance
($f_p = 2{,}45$ GHz), le couplage plasma-onde est maximal et $P_r$ est
minimal. Toute dérive de $n_e$ hors de $n_{e,c}$ augmente $P_r$ →
le contrôleur corrige.

#### Luminosité plasma (photodiode)

Une photodiode (BPW34 ou similaire) placée face au couvercle acrylique
mesure l'intensité lumineuse de la recombinaison radiative, qui est
proportionnelle à $n_e^2$. C'est un proxy redondant de la densité
électronique.

#### Température (thermocouple)

Thermocouple type K collé sur la paroi extérieure de la chambre,
lu via un convertisseur [MAX31855](https://www.analog.com/en/products/max31855.html)
(interface SPI, résolution 0,25 °C). Permet de détecter une dérive
thermique et de couper le magnétron si $T_{\text{paroi}} > T_{\text{max}}$
(sécurité).

### Actionneurs

#### Électrovanne d'admission

Électrovanne proportionnelle (ou tout-ou-rien commandée en PWM basse
fréquence, ~ 1 Hz) sur la ligne d'injection de vapeur d'eau. Le duty
cycle contrôle le débit moyen $\dot{m}$ et donc la pression $P$ :

$$\frac{dP}{dt} = \frac{1}{V}(\dot{m}_{\text{in}} - S_p \cdot P)$$

où $V$ est le volume de la chambre et $S_p$ la vitesse de pompage.
Le PID ajuste $\dot{m}_{\text{in}}$ pour stabiliser $P$ à la consigne.

#### Modulation de puissance RF

Le magnétron est commandé par un [relais statique (SSR)](https://fr.wikipedia.org/wiki/Relais_statique)
à passage par zéro sur le transformateur HT. Le duty cycle (période
~ 100 ms) contrôle la puissance moyenne délivrée et donc $T_e$.

### Firmware et logging

- **Boucle PID** : cadencée à 100 Hz (période 10 ms), priorité temps
  réel (tâche FreeRTOS dédiée sur l'ESP32).
- **Logging** : écriture sur carte SD au format CSV avec horodatage
  (colonnes : `timestamp_ms, P_mbar, P_refl_mW, lum_plasma_mV,
  T_paroi_C, duty_vanne, duty_RF, erreur_PID`).
- **Télémétrie** : publication MQTT à 1 Hz vers un dashboard
  (Grafana, Node-RED, ou simple page web ESP32).
- **Sécurité firmware** : watchdog matériel, coupure automatique
  du magnétron si :
  - $P_r > P_{r,\text{max}}$ (découplage total → onde non absorbée),
  - $T_{\text{paroi}} > 150$ °C,
  - perte du signal de pression (capteur déconnecté),
  - $V_{\text{bat}} < 15$ V (seuil de surdécharge batterie Li-ion),
  - $T_{\text{batterie}} > 60$ °C ou $T_{\text{onduleur}} > 80$ °C,
  - timeout de communication (> 5 s sans battement de cœur).

### Protection RF du microcontrôleur

À proximité d'un magnétron 1 kW, le microcontrôleur doit être **blindé** :

- Boîtier métallique (aluminium ≥ 1 mm) avec passages de câbles via
  filtres feedthrough ou câbles blindés.
- Ferrites sur chaque ligne d'entrée/sortie.
- Alimentation depuis la batterie Makita (via régulateur DC-DC 18 V → 5 V).
- Placement **sur l'assemblage suspendu**, à l'extérieur de la chambre
  mais à l'intérieur du baril. Communication **exclusivement par
  Wi-Fi** — aucun câble vers le baril ou l'extérieur.

---

## Schéma d'ensemble

### Vue en coupe (élévation)

```
╔══════════════════════════════════════════════════════════╗
║  BARIL 205L (posé au sol — référentiel fixe)             ║
║  ⌀ 580 mm × 880 mm                                      ║
║                                                          ║
║  ┄┄┄┄┄┄┄┄┄┄┄ couvercle du baril ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  ║
║                      │                                   ║
║              Fil de torsion                              ║
║              (seul lien mécanique)                       ║
║                      │                                   ║
║  ┌───────────────────●───────────────────┐               ║
║  │     ← 200 mm →    │    ← 200 mm →    │               ║
║  │                  FLÉAU                │               ║
║  │                    │                  │               ║
║  │  ┌─────────────┐   │  ┌───────────┐   │               ║
║  │  │ CHAMBRE INOX│   │  │CONTREPOIDS│   │               ║
║  │  │ 3 gal       │   │  │  ~ 10 kg  │   │               ║
║  │  │ ⌀250×250 mm │   │  │           │   │               ║
║  │  │             │  [M]  └───────────┘   │               ║
║  │  │  ┌────────┐ │   │                   │               ║
║  │  │  │ PLASMA │ │   │ [M] = Miroir      │               ║
║  │  │  │  H₂O   │ │   │  (sur le fléau,   │               ║
║  │  │  │ 2-5mbar│ │   │   près de l'axe)  │               ║
║  │  │  └────────┘ │   │                   │               ║
║  │  │  8× IN-13   │   │                   │               ║
║  │  │  (octogone) │   │                   │               ║
║  │  │  Magnétron  │   │                   │               ║
║  │  │  Vanne DN10 │   │                   │               ║
║  │  │  🔋 Batterie│   │                   │               ║
║  │  │  ⚡ Onduleur │   │                   │               ║
║  │  │  🖥 ESP32   │   │                   │               ║
║  │  └─────────────┘   │                   │               ║
║  └────────────────────┴───────────────────┘               ║
║                                                          ║
║  ┌──────────────────────────────────────────┐            ║
║  │  Laser ──→ [Miroir] ──→ PSD              │            ║
║  │  (fixés à la paroi interne du baril)     │            ║
║  └──────────────────────────────────────────┘            ║
║                                                          ║
║  📷 Caméra Wi-Fi (hublot)                                ║
╚══════════════════════════════════════════════════════════╝

    Extérieur du baril :
    ┌──────────────────────────────┐
    │  Pompe à vide (déconnectée   │
    │  pendant la mesure)          │
    ├──────────────────────────────┤
    │  📱 Dashboard Wi-Fi          │
    │  📷 Caméras mobiles Wi-Fi    │
    └──────────────────────────────┘
```

### Vue du dessus (plan d'implantation)

```
    ┌─────────────────── Baril ⌀ 580 mm ──────────────────┐
    │                                                      │
    │                        ●                             │
    │                  fil de torsion                      │
    │                        │                             │
    │        CÔTÉ A          │         CÔTÉ B              │
    │    ┌───────────┐  ─────┼─────  ┌──────────┐          │
    │    │  Chambre  │  fléau│       │Contrepoid│          │
    │    │   inox    │  400mm│       │  ~ 10 kg │          │
    │    │  ⌀ 250    │       │       └──────────┘          │
    │    │           │   [M] │                             │
    │    │  N₁  N₂   │  miroir                             │
    │    │N₈    N₃  │       │                             │
    │    │  ⊕mag    │      Laser──→[M]──→PSD              │
    │    │N₇    N₄  │       │     (sur paroi du baril)    │
    │    │  N₆  N₅   │       │                             │
    │    │           │       │                             │
    │    └───────────┘       │                             │
    │                        │                             │
    │         90 mm          │        90 mm                │
    │      dégagement        │     dégagement              │
    │                                                      │
    └──────────────────────────────────────────────────────┘

    Légende : Nₖ = tube IN-13 (k = 1..8, espacés de 45°)
              ⊕ = position du couplage magnétron
              ● = axe du fil de torsion
              [M] = miroir (sur le fléau, près de l'axe)
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

8. **IN-13** — Fiche technique du tube Nixie bargraph soviétique.
   Plage de courant 0–5 mA, longueur de colonne 0–100 mm, tension
   d'amorçage ~ 140 V DC. Original : *OKB Gazotron*, URSS.
   [tube-tester.com/IN-13](http://www.tube-tester.com/sites/nixie/dat_arch/IN-13_datasheet.pdf)

9. **Makita BL1850B** — Batterie Li-ion 18 V / 5,0 Ah (90 Wh). BMS
   intégré (surcharge, surdécharge, surintensité, surtempérature).
   Fiche produit : [makita.ca](https://www.makita.ca/productdetail/BL1850B)

10. **Young, W. C. & Budynas, R. G.** (2002). *Roark's Formulas for
    Stress and Strain*. 7ᵉ édition, McGraw-Hill.
    ISBN 978-0-07-072542-3.
    (Constante de torsion d'un fil cylindrique : $\kappa = \pi G r^4 / 2L$.)

---

[← Cadre Théorique](02_theorie.md) · [Section suivante : Protocole de Validation →](04_protocole.md)
