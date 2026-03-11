# 🔬 Hypothèse : Four micro-ondes *inverter* comme source de pièces

[← Retour au README](../README.md) · [← Configuration matérielle](03_materiel.md)

---

## Résumé exécutif

L'architecture actuelle du Bohemian Lab repose sur un schéma
**classique** de micro-ondes domestique :

$$
\underbrace{\text{Batterie 18V}}_{\text{DC}}
\;\xrightarrow{\text{onduleur}}\;
\underbrace{120\text{V AC}}_{\text{60 Hz}}
\;\xrightarrow{\text{SSR}}\;
\underbrace{\text{MOT}}_{\substack{\text{transfo HT} \\ \sim 2{,}5\text{ kg}}}
\;\xrightarrow{\text{Villard}}\;
\underbrace{-4\text{ kV DC}}_{\text{anode}}
\;\rightarrow\;
\text{Magnétron}
$$

Les **fours inverter** (Panasonic, LG NeoChef, Samsung) remplacent le
MOT + doubleur par un **convertisseur haute fréquence** (SMPS 20–50 kHz)
qui produit directement la haute tension. Cette note explore les
avantages, risques et implications pour le projet.

---

## 1. Architecture d'un four inverter

### 1.1 Chaîne de puissance

```
Secteur 120V AC
     │
     ▼
┌──────────┐
│ Pont de   │ ← Redresseur + filtre (condensateur bus DC)
│ diodes    │
└──────────┘
     │  ~170 V DC (bus)
     ▼
┌──────────────┐
│ Onduleur      │ ← IGBT demi-pont (2× IGBT 600-900V)
│ HF 20-50 kHz │    piloté par MCU dédié (contrôle PFC + PWM)
└──────────────┘
     │  AC haute fréquence
     ▼
┌──────────────┐
│ Transfo HF    │ ← Ferrite (noyau E+E), beaucoup plus léger
│ (ferrite)     │    que le MOT laminé 50 Hz
└──────────────┘
     │  ~2100 V AC crête (sec.)
     ▼
┌──────────────┐
│ Doubleur HV   │ ← Diode HV + condensateur HV
│ ou pont        │    (identique au classique, ou pont complet)
└──────────────┘
     │  ~4000 V DC
     ▼
   Magnétron
```

### 1.2 Différences clés vs. MOT classique

| Caractéristique | MOT (classique) | Inverter (SMPS) |
|:---|:---|:---|
| Fréquence de fonctionnement | 60 Hz (secteur) | 20–50 kHz |
| Masse du transformateur | **2,5–3,5 kg** (tôles fer-silicium) | **0,3–0,8 kg** (ferrite) |
| Masse totale alim. HV | ~3,5 kg (MOT + condo + diode) | ~1,0–1,5 kg (SMPS + transfo ferrite + doubleur) |
| Contrôle de puissance | Duty cycle SSR (ON/OFF 120V AC) | **Continu** (variation de fréquence ou de duty PWM HF) |
| Puissance crête vs. moy. | Crête = nominale pendant phase ON | **Crête = puissance demandée** (vraie modulation) |
| Rendement | ~85 % (cuivre + fer) | ~90–93 % (ferrite, commutation rapide) |
| Bruit électrique | 60 Hz + harmoniques | 20–50 kHz + harmoniques (EMI) |
| Coût de récupération | ~5–15 $ (tout micro-ondes) | ~15–30 $ (fours inverter spécifiques) |

---

## 2. Avantages pour le Bohemian Lab

### 2.1 ⚖️ Gain de masse critique

Le budget de masse est **le** facteur limitant sur le pendule de
torsion. L'ensemble suspendu pèse ~9,3 kg (Phase 1) dont :

| Composant | MOT classique | Inverter |
|:---|:---|:---|
| Transfo HT | 2,5 kg | **0,5 kg** |
| Condensateur HV | 0,3 kg | 0,2 kg |
| Diode HV | 0,05 kg | 0,05 kg |
| Carte électronique | — | 0,3 kg |
| **Total alim. HV** | **~2,8 kg** | **~1,1 kg** |
| **Gain** | — | **−1,7 kg (−61 %)** |

En Phase 2 (2× magnétrons), le gain est doublé : **−3,4 kg**.

**Impact sur le pendule** :

$$I = 2Md^2 \quad \Rightarrow \quad T_0 = 2\pi\sqrt{\frac{I}{\kappa}}$$

Avec $M$ réduit de ~1,7 kg (Phase 1), $I$ diminue de ~17 %, ce qui
raccourcit $T_0$ de ~8 % — cycles plus rapides, davantage de données
par session.

### 2.2 🎛️ Modulation de puissance continue

C'est l'avantage **décisif** pour l'expérience :

- **Architecture actuelle** (SSR + MOT) : le magnétron est soit ON
  (pleine puissance crête), soit OFF. La « puissance moyenne » est
  contrôlée par le duty cycle — mais $P_{\text{crête}}$ reste
  constante. Les Nixie saturent pendant chaque phase ON si
  $P_{\text{crête}} > 300$ W.

- **Architecture inverter** : la puissance est modulée **en continu**
  de 0 à $P_{\text{max}}$ en variant la fréquence ou le rapport
  cyclique de l'onduleur HF. La puissance crête **est** la puissance
  demandée :

$$P_{\text{crête}} = P_{\text{moy}} = P_{\text{consigne}}$$

Conséquences :
1. **Respect du seuil Nixie** ($E < 20$ kV/m) à tout instant.
2. **Qualité du PID** : régulation proportionnelle au lieu de
   tout-ou-rien (bang-bang) → erreur statique ÷ 3×, ripple ÷ 20×
   (cf. simulation `012_inverter_vs_mot.py`).
3. **Gradient de phase stable** : le plasma voit une puissance RF
   constante, pas des pulses → le gradient $\nabla S$ est plus
   propre pour la mesure bohmienne.
4. **Contrôle fin de la qualité du plasma** : c'est l'apport le
   plus critique pour la physique de l'expérience — voir § 2.5.

### 2.3 🔋 Meilleur rendement → autonomie accrue

| Paramètre | MOT + onduleur | Inverter seul |
|:---|:---|:---|
| Batterie → magnétron | $\eta_{\text{ond}} \times \eta_{\text{MOT}} \approx 0{,}85 \times 0{,}85 = 72\%$ | $\eta_{\text{SMPS}} \approx 90\%$ |
| Puissance DC pour 200 W RF | $200 / 0{,}65 / 0{,}72 = 427$ W | $200 / 0{,}65 / 0{,}90 = 342$ W |
| Autonomie (90 Wh) | ~12,6 min | **~15,8 min (+25 %)** |

De plus, l'onduleur DC→AC séparé (composant #5, ~1 kg) devient
**superflu** — gain additionnel de ~1 kg de masse et ~$100.

### 2.4 🔇 Élimination de l'onduleur DC→AC

L'architecture actuelle nécessite un onduleur pur-sinus 120V AC
pour alimenter le MOT. Avec un inverter récupéré d'un four :

$$
\text{Batterie 18V} \;\xrightarrow{\text{boost DC-DC}}\;
170\text{V DC (bus)} \;\rightarrow\; \text{Carte inverter}
\;\rightarrow\; \text{Magnétron}
$$

L'onduleur AC est éliminé. Il faut par contre un **boost DC-DC
18V → 170V** pour remplacer le redresseur secteur de la carte
inverter. C'est un convertisseur plus simple, plus efficace (~95 %)
et plus léger qu'un onduleur sinusoïdal.

### 2.5 🔬 Contrôle fin de la qualité du plasma

C'est l'impact le plus profond pour la physique de l'expérience.
Dans un plasma micro-onde basse-pression de H₂O, la densité
électronique $n_e$ suit la puissance RF injectée avec une
constante de temps $\tau_{\text{plasma}}$ liée à la recombinaison
dissociative :

$$\frac{dn_e}{dt} = \nu_i(P_{\text{RF}})\, n_e - \alpha\, n_e^2$$

où $\nu_i$ est la fréquence d'ionisation (proportionnelle à
$P_{\text{RF}}$) et $\alpha$ le coefficient de recombinaison.

#### Plasma pulsé (MOT + SSR) — le problème

Avec l'architecture SSR à 10 Hz, le plasma subit des
**cycles ON/OFF de 100 ms** pendant lesquels :

- **Phase ON** : $n_e$ monte vers la valeur d'équilibre à
  $P_{\text{crête}} = 700$ W (valeur bien supérieure à la
  consigne de 200 W).
- **Phase OFF** : $n_e$ décroît exponentiellement avec
  $\tau_{\text{recombinaison}} \sim 10$–50 ms.

Le plasma ne se stabilise **jamais** — il oscille en permanence
entre un état sur-ionisé et un état sous-ionisé. Cette fluctuation
module le champ d'onde pilote $\psi(\mathbf{r}, t)$ et pollue
le gradient de phase :

$$\nabla S \;\propto\; \nabla \arg\!\left(\psi\right)
\quad \Rightarrow \quad
\delta(\nabla S) \,\propto\, \frac{\delta n_e}{n_e}$$

Le bruit de $\nabla S$ se retrouve directement dans la force
bohmienne mesurée par le pendule de torsion. C'est un bruit
**systématique**, pas statistique — il ne se moyenne pas.

#### Plasma continu (Inverter) — la solution

Avec la modulation continue de l'inverter :

- $P_{\text{RF}}(t) = P_{\text{consigne}} \pm \sigma$, avec
  $\sigma / P_{\text{consigne}} < 1\%$ (ripple mesuré à 0,9 %
  en simulation).
- $n_e(t)$ atteint un **vrai état stationnaire**
  $n_{e,\text{eq}}(P_{\text{consigne}})$ avec des fluctuations
  résiduelles $\delta n_e / n_e \sim 10^{-3}$.
- Le champ $\psi$ est stable → $\nabla S$ est propre →
  le signal de force sur le pendule n'est plus contaminé.

#### Gain quantitatif estimé

| Métrique | MOT + SSR | Inverter | Gain |
|:---|:---|:---|:---|
| Fluctuation $\delta n_e / n_e$ | ~30–50 % | **< 1 %** | **÷ 30–50×** |
| Ripple de $P_{\text{RF}}$ | 37,6 W ($\sigma$) | 1,9 W ($\sigma$) | **÷ 20×** |
| Bruit systématique sur $\nabla S$ | Dominant | Négligeable | — |
| SNR mesure pendule | Limité par pulsation | **Limité par bruit thermique** | ↑↑ |

En pratique, l'architecture inverter permet de passer d'un régime
où le **bruit systématique du plasma domine** à un régime où le
**bruit thermique et mécanique** du pendule redevient le facteur
limitant — situation normale pour une mesure de précision.

> 💡 **Implication expérimentale** — Avec un inverter, le nombre
> de cycles de pendule nécessaires pour atteindre un SNR donné
> diminue drastiquement. Une session de 15 min (autonomie batterie)
> pourrait suffire là où l'architecture MOT nécessiterait des
> sessions beaucoup plus longues avec moyennage intensif.

---

## 3. Risques et points d'attention

### 3.1 ⚡ EMI (interférences électromagnétiques)

L'onduleur HF (20–50 kHz) génère des harmoniques jusqu'à plusieurs
MHz. Dans un pendule de torsion sensible au micro-newton :

- **Risque** : couplage parasite dans les signaux ADC (Pirani,
  coupleur directionnel, thermocouple).
- **Mitigation** : blindage du module inverter dans un boîtier alu,
  filtres en mode commun sur les fils de capteurs, découplage LC sur
  l'alimentation ESP32.

### 3.2 🧩 Interface de contrôle

Les cartes inverter de fours Panasonic utilisent généralement un
**MCU propriétaire** (souvent un Renesas ou NXP) pour piloter les
IGBT. Deux approches :

| Approche | Principe | Complexité | Risque |
|:---|:---|:---|:---|
| **A. Réutiliser le MCU d'origine** | Injecter un signal analogique (0–5 V) sur la broche de consigne puissance du MCU inverter | Faible | Reverse-engineering nécessaire |
| **B. Remplacer le MCU** | L'ESP32 pilote directement les IGBT via un driver (IR2110, UCC3895…) | Élevée | Court-circuit IGBT → destruction |
| **C. Signal de commande PWM** | Beaucoup de cartes inverter acceptent un signal PWM/DC pour la consigne (connecteur du panneau de commande) | Faible | Identifier le bon connecteur |

**Recommandation** : approche **C** en priorité. Les fours inverter
Panasonic (série NN-SD, NN-SN) ont un **connecteur ribbon** entre le
panneau de commande et la carte inverter. Ce connecteur transmet
typiquement une consigne numérique (série ou PWM) pour le niveau
de puissance (10 niveaux). En interceptant ce signal, on peut
substituer l'ESP32 au panneau de commande.

### 3.3 🔒 Sécurité modifiée

| Risque | MOT classique | Inverter |
|:---|:---|:---|
| Énergie stockée (condensateur) | ~10 J (2100V, ~1 µF) | ~25 J (170V, ~470×2 µF bus DC) |
| Tension dangereuse | **4000 V** (sortie Villard) | **4000 V** (sortie doubleur) + **170 V** (bus DC) |
| Temps de décharge | ~30 s (résistance bleed) | ~2 s (résistance bleed bus) + ~30 s (HV) |
| Composants actifs | Passifs (transfo, diode, condo) | **IGBT sous tension → risque de mise en route involontaire** |

> ⚠️ **Point critique** — Le bus DC (170 V, haute capacité) reste
> chargé après coupure du secteur. Toujours décharger le bus DC
> avant intervention. Les IGBT peuvent s'emballer si le contrôle
> est défaillant → fusible HV rapide obligatoire.

### 3.4 💰 Sourçage au Canada

| Source | Modèle type | Prix estimé | Notes |
|:---|:---|:---|:---|
| Kijiji / Marketplace | Panasonic NN-SD/NN-SN (inverter) | 15–40 $ | Vérifier « inverter » sur l'étiquette |
| Magasin de pièces | Carte inverter Panasonic seule | 30–60 $ | Ex: F66459X90AP, A607Y3A10AP |
| Amazon.ca | Four inverter neuf (basique) | 80–120 $ | Panasonic NN-SN66, Samsung ME19R7041 |
| Walmart.ca | Clearance / open box | 50–80 $ | Vérifier « inverter technology » |

**Fours inverter identifiables** : Panasonic (quasi tous depuis 2010),
LG NeoChef (certains modèles), Samsung (gammes récentes). Les fours
**non-inverter** sont les plus courants en entrée de gamme —
vérifier l'étiquette arrière (« inverter » ou mention de la
fréquence > 50/60 Hz).

### 3.5 📏 Encombrement

La carte inverter typique mesure ~180 × 120 × 40 mm — plus compacte
que le MOT (150 × 120 × 120 mm). Mais elle nécessite une ventilation
active (ventilateur 40–60 mm) pour les IGBT. Prévoir un dissipateur
thermique si le ventilateur est retiré pour réduire le bruit
mécanique sur le pendule.

---

## 4. Architecture proposée (inverter)

### 4.1 Schéma fonctionnel

```
   ┌─────────────┐
   │ Batterie     │  18V DC, 90 Wh
   │ Makita       │
   └──────┬──────┘
          │
    ┌─────▼──────┐
    │ Boost DC-DC │  18V → 170V DC (bus)
    │ 500W        │  Module : XL4016 ou LTC3787
    │ η ≈ 94%     │  ~0,2 kg
    └─────┬──────┘
          │  170V DC bus
    ┌─────▼──────────────────────┐
    │  Carte inverter (récupérée) │
    │  IGBT + transfo ferrite     │
    │  + doubleur HV              │
    │  Consigne ← ESP32 (PWM)    │  ~0,8 kg
    └─────┬──────────────────────┘
          │  ~4000V DC
    ┌─────▼──────┐
    │ Magnétron   │  LG 2M213-01TAG
    │ 200–700W RF │  (filament via secondaire dédié)
    └────────────┘
```

### 4.2 Bilan de masse comparatif

| Composant | MOT classique | Inverter | Δ |
|:---|:---|:---|:---|
| Onduleur DC→AC | 1,0 kg | — | **−1,0** |
| MOT | 2,5 kg | — | **−2,5** |
| Condensateur HV | 0,3 kg | 0,2 kg | −0,1 |
| Diode HV | 0,05 kg | 0,05 kg | 0 |
| Boost DC-DC | — | 0,2 kg | +0,2 |
| Carte inverter | — | 0,8 kg | +0,8 |
| **Total alim.** | **3,85 kg** | **1,25 kg** | **−2,6 kg** |

En Phase 2 (×2) : gain total de **~5,2 kg** — réduction de ~45 %
de la masse totale suspendue, soit $I$ réduit de ~45 % et $T_0$ de
~26 %.

### 4.3 Impact sur le contrôle (PID)

Le passage à un inverter change fondamentalement la nature de la
boucle PID₁ (puissance RF) :

| Aspect | MOT + SSR (actuel) | Inverter + PWM |
|:---|:---|:---|
| Variable de commande | Duty cycle SSR (0–100 %) | **Tension de consigne (0–5 V)** ou PWM HF |
| Résolution | ~1 % (période SSR 100 ms) | **< 0,1 %** (12 bits DAC) |
| Bande passante | ~10 Hz (limité par SSR ZC) | **~1 kHz** (limité par boucle SMPS) |
| Linéarité | Non-linéaire (seuil magnétron) | **Quasi-linéaire** dans la plage de fonctionnement |
| Ripple de puissance | $\pm P_{\text{crête}}$ à la fréquence du SSR | **< 5 %** (filtrage LC interne) |

La boucle PID₂ (ionisation, 10 Hz) bénéficie directement de la
bande passante élargie — le contrôle de $n_e$ via $P_{\text{RF}}$
devient véritablement proportionnel au lieu de modulé en tout-ou-rien.

---

## 5. Compatibilité avec le magnétron 2M213-01TAG

Le LG 2M213-01TAG est un magnétron **standard** de micro-ondes
domestique (2,45 GHz, ~700 W). Il est compatible avec toute
alimentation fournissant :

| Paramètre | Spécification 2M213-01TAG | Fourni par inverter type |
|:---|:---|:---|
| $V_{\text{anode}}$ | 3 400–4 200 V DC | ✅ Ajustable 0–4 200 V |
| $I_{\text{anode}}$ | 0–300 mA | ✅ Limité par le SMPS |
| $V_{\text{filament}}$ | 3,15 V AC @ 10–11 A | ⚠️ Secondaire dédié requis |
| Mise en route | $V_{\text{anode}} > V_{\text{seuil}}$ (~2 800 V) | ✅ Contrôle par rampe |

> ⚠️ **Filament** — Le transfo ferrite de l'inverter a généralement
> un enroulement filament dédié (3,15 V AC HF). Vérifier que le
> magnétron récupéré tolère une alimentation filament à 20–50 kHz
> au lieu de 60 Hz. En pratique, le filament est un simple chauffage
> résistif (fil de tungstène) — la fréquence n'a pas d'importance.

---

## 6. Plan d'action

### Phase 0 — Validation (2 semaines)

- [ ] Acquérir un four inverter Panasonic usagé (Kijiji, ~20 $)
- [ ] Identifier la carte inverter et le connecteur de commande
- [ ] Documenter le pinout (reverse-engineering du câble ribbon)
- [ ] Tester le contrôle de puissance via signal externe (0–5 V)
- [ ] Mesurer la masse de l'ensemble (carte + transfo ferrite)
- [ ] Vérifier l'alimentation filament (fréquence, courant)

### Phase 1 — Intégration

- [ ] Concevoir le boost DC-DC 18V → 170V (≥ 500 W)
- [ ] Adapter le firmware ESP32 : remplacer la sortie SSR par une
      sortie DAC/PWM pour la consigne inverter
- [ ] Mettre à jour la simulation PID (bande passante élargie)
- [ ] Blindage EMI du module inverter (boîtier alu)
- [ ] Tests sur établi (magnétron + charge factice eau)

### Phase 2 — Bi-magnétron inverter

- [ ] Seconde carte inverter (même modèle)
- [ ] Réduction de la complexité : plus besoin de SSR ni d'onduleur
      → commutation directe par l'ESP32 (enable/disable IGBT)
- [ ] Mise à jour du bilan de masse et du moment d'inertie

---

## 7. Verdict préliminaire

| Critère | Note | Commentaire |
|:---|:---|:---|
| Gain de masse | ⭐⭐⭐⭐⭐ | −2,6 kg/magnétron — impact majeur sur $I$ et $T_0$ |
| Contrôle de puissance | ⭐⭐⭐⭐⭐ | Modulation continue — élimine le problème de saturation Nixie |
| Qualité du plasma | ⭐⭐⭐⭐⭐ | Fluctuations $\delta n_e/n_e$ ÷ 30–50× → SNR pendule limité par le bruit thermique, plus par le plasma |
| Rendement énergétique | ⭐⭐⭐⭐ | +25 % d'autonomie |
| Simplicité d'intégration | ⭐⭐⭐ | Reverse-engineering requis + boost DC-DC à concevoir |
| Coût | ⭐⭐⭐⭐ | ~20–40 $ (four usagé) vs. ~5–15 $ (MOT récupéré) |
| Risque EMI | ⭐⭐ | HF 20–50 kHz → filtrage sérieux nécessaire |
| Sécurité | ⭐⭐⭐ | Bus DC 170V + HV 4 kV — complexité accrue |

**Conclusion** : l'hypothèse inverter est **fortement favorable** au
projet. L'argument décisif n'est pas seulement la masse (÷ 3×) ou
l'autonomie (+25 %), mais le **contrôle fin de la qualité du
plasma** : la modulation continue supprime les oscillations de
$n_e$ induites par le bang-bang SSR, réduisant le bruit
systématique sur $\nabla S$ de ÷ 30–50×. Le pendule passe d'un
régime limité par les pulsations du plasma à un régime limité par
le bruit thermique — condition nécessaire pour une mesure
bohmienne significative. Le principal risque (EMI) est mitigeable.
Le reverse-engineering de la carte est le goulot d'étranglement —
mais les cartes Panasonic sont largement documentées par la
communauté (réparation DIY).

> 🔬 **Prochaine étape** : acquérir un four Panasonic inverter
> usagé et documenter le pinout de la carte. Simulation comparative
> dans [`experiments/012_inverter_vs_mot.py`](../experiments/012_inverter_vs_mot.py).

---

## Références

- Panasonic Inverter Technology : [brevet US6462321B1](https://patents.google.com/patent/US6462321B1)
- « Microwave Oven Inverter Power Supply » — application note Infineon AN2013-06
- Communauté réparation : [mikrocontroller.net — Panasonic inverter teardown](https://www.mikrocontroller.net/)
- LG 2M213-01TAG datasheet — spécifications anode/filament
