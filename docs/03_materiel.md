# ⚙️ Configuration Matérielle

[← Retour au README](../README.md) · [← Cadre Théorique](02_theorie.md)

---

## Introduction vulgarisée

Imaginez un petit cylindre en acier inoxydable — une chambre à vide de
laboratoire d'environ 25 cm de diamètre — suspendu à un fil, comme une
balançoire très sensible. À l'intérieur, un four micro-ondes démonté
(le magnétron) envoie ses ondes dans cette chambre contenant une fine
brume d'eau. Les micro-ondes transforment cette brume en **plasma** :
un gaz ionisé lumineux, comme un éclair miniature enfermé dans un bocal.

L'inox est conducteur : la chambre sert donc naturellement de **cage de
Faraday** — aucune radiation ne s'échappe. Le couvercle transparent en
acrylique est recouvert d'un grillage métallique pour compléter le
blindage. Tout est confiné dans un système compact et hermétique,
certifié pour le vide, et suffisamment léger (~ 5 kg) pour que le fil
de torsion détecte la moindre force — de l'ordre du millionième de
newton.

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
> Le baril de 205L reste toutefois utilisé comme **enceinte de
> confinement secondaire** pendant l'expérience (défense en profondeur :
> double cage de Faraday, rétention d'éclats, confinement des gaz).
> Voir la [section sécurité](05_securite.md#enceinte-de-confinement-secondaire-baril-de-205l).

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

où $x_{mn}$ est le $n$-ième zéro de $J_m$ (mode TM) ou de $J'_m$ (mode TE).

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

où $I$ est le moment d'inertie de la chambre autour de l'axe de torsion.

Pour la chambre inox (cylindre creux, masse $M \approx 5$ kg, rayon $R = 0{,}125$ m) :

$$I \approx M R^2 = 5 \times 0{,}125^2 \approx 0{,}078 \; \text{kg}\cdot\text{m}^2$$

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
un bras de levier $L = 0{,}125$ m (rayon de la chambre), et un fil
de tungstène ($\kappa = 5 \times 10^{-8}$ N·m/rad) :

$$\theta = \frac{F \cdot L}{\kappa} = \frac{3{,}3 \times 10^{-6} \times 0{,}125}{5 \times 10^{-8}} \approx 8{,}3 \; \text{rad}$$

Cette valeur est irréaliste, ce qui signifie qu'un fil aussi fin serait
trop sensible. En pratique, un fil plus rigide
($\kappa \sim 10^{-4}$ N·m/rad) donnerait :

$$\theta = \frac{3{,}3 \times 10^{-6} \times 0{,}125}{10^{-4}} \approx 4{,}1 \times 10^{-3} \; \text{rad} \approx 0{,}24°$$

Cet angle est mesurable par analyse vidéo ou par réflexion laser.
Notons que la masse réduite (~ 5 kg vs ~ 20 kg avec le baril) rend le
pendule **4× plus réactif** pour la même force.

### Alternative : Balance de torsion

Si la sensibilité du pendule simple est insuffisante, une **balance de
torsion** (type Cavendish) peut être utilisée, avec un fléau horizontal
portant des masses aux extrémités, suspendu par la fibre. Cette
configuration augmente le moment d'inertie et la stabilité.

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
> thermostat, mais appliqué à un plasma.

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
  │                 MICROCONTRÔLEUR (ESP32)               │
  │                                                      │
  │   ADC0 ← Jauge pression (Pirani)                     │
  │   ADC1 ← Photodiode (luminosité plasma)              │
  │   ADC2 ← Coupleur directionnel (P_réfléchie)          │
  │   ADC3 ← Thermocouple type K (via MAX31855)           │
  │                                                      │
  │   PWM0 → Électrovanne admission H₂O (via MOSFET)     │
  │   PWM1 → Duty cycle magnétron (via SSR / triac)      │
  │   GPIO → Relais pompe à vide                         │
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
  - timeout de communication (> 5 s sans battement de cœur).

### Protection RF du microcontrôleur

À proximité d'un magnétron 1 kW, le microcontrôleur doit être **blindé** :

- Boîtier métallique (aluminium ≥ 1 mm) avec passages de câbles via
  filtres feedthrough ou câbles blindés.
- Ferrites sur chaque ligne d'entrée/sortie.
- Alimentation isolée (convertisseur DC-DC isolé ou batterie).
- Placement **à l'extérieur de la chambre**, relié aux capteurs par câbles
  blindés traversant la cage de Faraday via des
  [feedthrough](https://en.wikipedia.org/wiki/Feedthrough) filtrés.

---

## Schéma d'ensemble

```
                ┌───────── Fil de torsion ─────────┐
                │                                   │
                ▼                                   │
╔═════════════════════════════════════════╗    Support fixe
║  BARIL 205L (confinement secondaire)   ║    (plafond)
║                                         ║
║  ┌─────────────────────────────────┐    ║
║  │  CHAMBRE INOX 3 GAL (Ø250×250)  │    ║
║  │                                  │    ║
║  │  ╔═══════════════════════════╗   │    ║
║  │  ║  Couvercle acrylique 3/4" ║   │    ║
║  │  ║  + grillage métallique    ║   │    ║
║  │  ║  (cage de Faraday)        ║   │    ║
║  │  ╚═══════════════════════════╝   │    ║
║  │  ┌─────────────────────────┐     │    ║
║  │  │    PLASMA  H₂O → H-OH   │     │    ║
║  │  │    (2–5 mbar, T_e~2 eV) │     │    ║
║  │  └────────────┬────────────┘     │    ║
║  │               │                  │    ║
║  │    Magnétron 2,45 GHz (1 kW)     │    ║
║  │    [Nixie IN-9] [Nixie IN-13]    │    ║
║  │    Joint silicone                │    ║
║  └────────┬────────────────┬────────┘    ║
║           │  câbles blindés │             ║
╚═══════════╪════════════════╪═════════════╝
            │                │
            ▼                ▼
┌─────────────────────────────────────────┐
│   MICROCONTRÔLEUR (ESP32)               │
│  ┌───────────────┐                      │
│  │ ADC: P, P_r,  │  PID → PWM          │
│  │ lum, T        │  vanne+RF           │
│  └───────────────┘                      │
│  Wi-Fi → Dashboard / SD log            │
└─────────────────────────────────────────┘
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
