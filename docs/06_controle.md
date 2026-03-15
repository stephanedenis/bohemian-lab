# 🎛️ Contrôle et Asservissement du Plasma

[← Retour au README](../README.md) · [← Notes de Sécurité](05_securite.md)

---

## Introduction vulgarisée

Le plasma de vapeur d'eau est un milieu **capricieux** : laissé sans
surveillance, il dérive hors du point de fonctionnement optimal en
quelques dizaines de millisecondes. C'est comme maintenir la
température d'une douche en ajustant le robinet — sauf qu'ici, le
« robinet » est la pression de gaz et la puissance micro-ondes, et
la « douche » est un plasma à 30 000 °C.

On confie cette tâche à un **micro-contrôleur embarqué** (ESP32) qui
mesure en permanence l'état du plasma et ajuste les paramètres pour
le maintenir au point de résonance $n_e \approx n_{e,c}$. C'est un
thermostat, mais pour un plasma.

Le contrôle est un problème **MIMO** (Multi-Input Multi-Output) :
**4 capteurs** alimentent **3 boucles PID** indépendantes à des
cadences différentes, chacune agissant sur un **actionneur** dédié.
Un watchdog de sécurité supervise l'ensemble.

---

## 6.1 Architecture globale

### Diagramme de boucle simplifié (SISO équivalent)

Le schéma suivant montre la boucle de rétroaction dans sa forme
classique à une seule entrée/sortie, avec le nœud de sommation ⊕
et le contrôleur PID **intégralement dans le MCU** :

![Boucle de rétroaction PID — Homéostasie du plasma](img/boucle_pid.svg)

La consigne $r(t)$ est la valeur cible de puissance réfléchie
$P_{r,0}$ (minimum → résonance). L'erreur $e(t) = P_r(t) - P_{r,0}$
alimente le régulateur PID qui produit la commande $u(t)$.

### Diagramme de bloc interne du MCU (MIMO réel)

En réalité, le contrôle est un problème MIMO avec 3 boucles
imbriquées à des cadences étagées :

![Architecture interne du MCU — Contrôle MIMO](img/mcu_interne.svg)

### Vue matérielle de l'ESP32 embarqué

Le diagramme suivant montre le câblage physique : 6 entrées ADC,
3 sorties PWM/GPIO, communication Wi-Fi et logging SD :

![Architecture de la boucle — ESP32 embarqué](img/esp32_architecture.svg)

---

## 6.2 Choix du microcontrôleur

| Critère | Exigence | [ESP32](https://fr.wikipedia.org/wiki/ESP32) (choisi) | Alternative : [STM32](https://en.wikipedia.org/wiki/STM32) |
|:---|:---|:---|:---|
| ADC | ≥ 4 canaux, ≥ 12 bits, ≥ 1 kHz | 18 canaux, 12 bits, SAR ~ 1 kHz ✔ | 16 canaux, 12 bits, 1 MHz ✔✔ |
| PWM | ≥ 2 sorties, ≥ 10 bits | 16 canaux LEDC, 16 bits ✔ | 32 bits, DMA ✔✔ |
| Wi-Fi / BLE | Télémétrie temps réel | Intégré ✔ | Module externe requis ✘ |
| GPIO | Relais pompe, sécurité | 34 GPIO ✔ | 51+ GPIO ✔ |
| RTOS | Boucle déterministe | FreeRTOS intégré ✔ | FreeRTOS / bare-metal ✔ |
| Coût | Accessible | ~ 5 € ✔ | ~ 3–15 € ✔ |
| Blindage RF | Survie à côté du magnétron | Boîtier alu obligatoire ⚠️ | Idem ⚠️ |

**Verdict** : l'ESP32 est le meilleur rapport fonctionnalité/coût
grâce à son Wi-Fi intégré, indispensable puisqu'**aucun câble** ne
doit relier le pendule au référentiel fixe. Pour un temps réel
strict ou un ADC plus rapide, un STM32 (ARM Cortex-M4) serait
supérieur mais nécessiterait un module Wi-Fi externe.

### Placement physique

L'ESP32 est placé **dans le contrepoids** (côté B du plateau
porteur), à ~400 mm du magnétron, dans un boîtier aluminium blindé.
Communication exclusivement par **Wi-Fi** — aucun câble vers le
baril ou l'extérieur. Voir
[§3.6 Pendule de torsion](03_materiel.md#36-mesure--pendule-de-torsion)
pour la géométrie du plateau porteur.

---

## 6.3 Capteurs — Entrées (4 ADC + 2 surveillance)

### 6.3.1 Puissance RF réfléchie $P_r$ — **Signal-clé**

| Paramètre | Valeur |
|:---|:---|
| Capteur | [Coupleur directionnel](https://en.wikipedia.org/wiki/Directional_coupler) −20 dB + diode Schottky |
| Signal | 0–3,3 V DC (proportionnel à $P_r$) |
| Canal ADC | CH0 (prioritaire) |
| Cadence lecture | 1 kHz |
| Proxy de | Désaccord $f_p \neq f$ (résonance plasma) |

Le coupleur, inséré entre le magnétron et la chambre, prélève une
fraction de l'onde réfléchie. Après détection par diode Schottky,
le signal DC est proportionnel à $P_r$.

**Pourquoi c'est le signal-clé** : à la résonance ($f_p = 2{,}45$ GHz),
le couplage plasma–onde est maximal et $P_r$ est **minimal**. Toute
dérive de $n_e$ hors de $n_{e,c}$ augmente $P_r$ — c'est le signal
le plus rapide et le plus direct pour l'asservissement.

### 6.3.2 Pression $P$ — Jauge Pirani

| Paramètre | Valeur |
|:---|:---|
| Capteur | [Jauge Pirani](https://fr.wikipedia.org/wiki/Jauge_de_Pirani) |
| Plage | $10^{-3}$ – 100 mbar |
| Signal | 0–10 V → diviseur résistif → 0–3,3 V |
| Canal ADC | CH1 |
| Cadence lecture | 100 Hz |
| Proxy de | Densité de neutres $n_0$ |

La jauge Pirani mesure la pression par la variation de conductivité
thermique du gaz. La plage $10^{-3}$ – 100 mbar couvre parfaitement
le régime 2–5 mbar visé.

**Calibration** : la courbe Pirani n'est pas linéaire et dépend de la
nature du gaz. Pour la vapeur d'eau, utiliser la courbe du
constructeur ou calibrer in situ avec une jauge capacitive de
référence.

### 6.3.3 Luminosité plasma — Caméra Wi-Fi

| Paramètre | Valeur |
|:---|:---|
| Capteur | Caméra Wi-Fi au-dessus du grillage Faraday |
| Signal | Analyse d'image (luminosité moyenne RGB) |
| Canal | Via Wi-Fi (pas ADC directe) |
| Cadence lecture | 10 Hz (framerate caméra) |
| Proxy de | $n_e^2$ (recombinaison radiative $\propto n_e^2$) |

La caméra regarde le plasma à travers le maillage du grillage et le
couvercle acrylique. La luminosité globale est un proxy redondant de
la densité électronique. L'image fournit aussi une **cartographie
visuelle** du plasma en complément des 8 Nixie IN-13 (mode passif,
broches à la masse, lecture par caméra).

> 📐 **Distribution 3D** — La caméra voit le plasma **par le dessus**
> (vue intégrée en $z$). Or, la distribution $n_e(r,\theta,z)$ est
> tridimensionnelle et le pic de densité est à $z \approx 0{,}75d$
> selon le [modèle 3D](../experiments/009_plasma_3d.py).
> L'image 2D vue du dessus est une projection qui peut masquer la
> structure axiale. Voir [data/009_coupe_axiale_plasma.png](../data/simulations/009_coupe_axiale_plasma.png).

### 6.3.4 Température paroi $T_{\text{paroi}}$

| Paramètre | Valeur |
|:---|:---|
| Capteur | Thermocouple type K + [MAX31855](https://www.analog.com/en/products/max31855.html) |
| Plage | −200 °C – 1 350 °C (résolution 0,25 °C) |
| Interface | SPI |
| Cadence lecture | 1 Hz |
| Proxy de | $T_g$ (dérive thermique) |

Le thermocouple est collé sur la paroi **extérieure** de la chambre
inox. Il détecte la dérive thermique lente et sert de déclencheur de
sécurité si $T_{\text{paroi}} > T_{\text{max}}$.

### 6.3.5 Surveillance batterie (sécurité uniquement)

| Capteur | Signal | Canal | Seuil de coupure |
|:---|:---|:---|:---|
| Tension batterie (diviseur résistif 18V→3,3V) | 0–3,3 V | ADC4 | $V_{\text{bat}} < 15$ V (surdécharge) |
| NTC température batterie/onduleur | 0–3,3 V | ADC5 | $T_{\text{bat}} > 60$ °C, $T_{\text{ond}} > 80$ °C |

Ces deux canaux ne participent **pas** à la régulation du plasma.
Ils alimentent uniquement le **watchdog de sécurité** (§6.7).

---

## 6.4 Actionneurs — Sorties (3 canaux)

### 6.4.1 Électrovanne d'admission H₂O

> ⚠️ **Supprimée** — L'injection de vapeur d'eau se fait désormais par
> **septum + microseringue** (injection manuelle ponctuelle avant la
> mesure). L'électrovanne est retirée de l'architecture embarquée.
> Voir [12_controle_vapeur.md](12_controle_vapeur.md) §2 et §10 pour
> la justification complète (risque RF, couple parasite, complexité
> inutile). Le canal PWM0 / GPIO25 est **libéré** pour un usage futur.

~~| Paramètre | Valeur |~~
~~|:---|:---|~~
~~| Type | Proportionnelle (ou tout-ou-rien + PWM BF) |~~
~~| Commande | PWM 0,1–10 Hz via MOSFET |~~
~~| Canal | PWM0 |~~
~~| Effet | Contrôle $\dot{m}_{\text{in}}$ → pression $P$ → $n_e$ |~~

La dynamique de pression dans la chambre suit :

$$\frac{dP}{dt} = \frac{1}{V}\left(\dot{m}_{\text{in}} - S_p \cdot P\right)$$

où $V \approx 11{,}4$ L est le volume de la chambre et $S_p$ la
vitesse de pompage résiduelle (fuites). Le PID ajuste le duty cycle
PWM pour contrôler le débit moyen $\dot{m}_{\text{in}}$.

### 6.4.2 Puissance magnétron (SSR)

| Paramètre | Valeur |
|:---|:---|
| Type | [Relais statique (SSR)](https://fr.wikipedia.org/wiki/Relais_statique) passage par zéro |
| Commande | PWM HF (période ~ 100 ms → 10 Hz) |
| Canal | PWM1 |
| Effet | Ajuste le duty cycle → puissance moyenne → $T_e$ → taux d'ionisation |

Le SSR commute le transformateur HT du magnétron à passage par zéro
(zéro crossing) pour minimiser les transitoires. Le duty cycle
contrôle la puissance moyenne délivrée et donc $T_e$.

> ⚠️ **Sécurité** — Le SSR est aussi le **dispositif d'arrêt
> d'urgence** : le watchdog peut l'ouvrir à tout moment pour couper
> le magnétron. Voir [§5.2 Haute Tension](05_securite.md#52-haute-tension--danger-mortel).

### 6.4.3 Pompe à vide

| Paramètre | Valeur |
|:---|:---|
| Type | Signal analogique (0–3,3 V) ou relais ON/OFF |
| Canal | GPIO (relais) |
| Effet | Ajuste le pompage (puits de neutres) |

La pompe reste **externe et fixe** — elle n'est active que pendant
la phase de préparation. Pendant la mesure, la vanne d'isolement est
fermée et le tuyau déconnecté. Le PID₃ n'agit donc qu'en phase de
préparation. Voir
[§3.6 Pendule de torsion — connexion unique](03_materiel.md#36-mesure--pendule-de-torsion)
pour le protocole de déconnexion.

---

## 6.5 Les 3 boucles PID

Le contrôle MIMO est décomposé en **3 boucles PID indépendantes**
à cadences étagées — de la plus rapide à la plus lente. Cette
hiérarchie est volontaire : la boucle rapide stabilise d'abord la
résonance RF, puis la boucle moyenne ajuste l'ionisation, et la
boucle lente gère la pression de fond.

### 6.5.1 PID₁ — Boucle de résonance (rapide, 100 Hz)

> ⚠️ **Boucle suspendue** — Le PID₁ contrôlait la résonance en
> ajustant la pression via l'électrovanne (PWM0). L'électrovanne
> étant supprimée (injection manuelle par septum), PID₁ n'a plus
> d'actionneur. En pratique, la pression est injectée manuellement
> à ~3 mbar et dérive de < 0,08 mbar/15 min — suffisamment stable.
> Le PID₂ (puissance magnétron) compense la lente dérive de $n_e$.
> Si un actuateur de pression non-métallique non-perturbant est
> identifié à l'avenir (ex. micro-doseur piézo), PID₁ pourra être
> réactivé. Voir [12_controle_vapeur.md](12_controle_vapeur.md) §10.

| Paramètre | Valeur |
|:---|:---|
| Entrée principale | $P_r$ (puissance RF réfléchie) — CH0 |
| Entrée secondaire | $P$ (pression, comme borne de sécurité) |
| Erreur | $e_1(t) = P_r(t) - P_{r,0}$ |
| Consigne | $P_{r,0}$ = minimum de réflexion (résonance) |
| Sortie | ~~$u_1(t)$ → électrovanne H₂O (PWM0)~~ — **sans actionneur** |
| Cadence | **100 Hz** (période 10 ms) |

**Loi de commande** :

$$u_1(t) = K_{p1} \, e_1(t) + K_{i1} \int_0^t e_1(\tau) \, d\tau + K_{d1} \, \frac{de_1}{dt}$$

**Justification de la cadence** : le temps de résidence du gaz dans
la chambre est $\tau_{\text{rés}} \sim 10\text{–}100$ ms. La boucle
doit être plus rapide :

$$f_{\text{boucle}} > \frac{1}{\tau_{\text{rés}}} \approx 10\text{–}100 \; \text{Hz}$$

L'ESP32 (ADC SAR ~ 1 kHz) permet confortablement 100 Hz avec marge
pour le calcul PID.

**Constantes PID initiales** (à ajuster empiriquement par
[Ziegler-Nichols](https://fr.wikipedia.org/wiki/M%C3%A9thode_de_Ziegler-Nichols)
ou auto-tuning) :

| Paramètre | Valeur initiale | Remarque |
|:---|:---|:---|
| $K_{p1}$ | 1,0 | Gain proportionnel — début conservateur |
| $K_{i1}$ | 0,5 s⁻¹ | Intégrateur — élimine l'erreur statique |
| $K_{d1}$ | 0,01 s | Dérivateur — amorti les oscillations |
| Anti-windup | ±100 % duty | Borne de l'intégrateur |

> 📐 **Simulation PID** — Le script [007_dynamique_pid.py](../experiments/007_dynamique_pid.py)
> intègre numériquement le système couplé $(P, n_e, T_e)$ avec ces gains
> initiaux et valide la convergence vers $n_e \approx n_{e,c}$ en $< 200$ ms.
> L'auto-tuning Ziegler–Nichols y est également implémenté.

### 6.5.2 PID₂ — Boucle d'ionisation (moyenne, 10 Hz)

| Paramètre | Valeur |
|:---|:---|
| Entrée | Luminosité plasma (caméra, proxy de $n_e^2$) |
| Erreur | $e_2(t) = \text{Lum}(t) - \text{Lum}_0$ |
| Consigne | $\text{Lum}_0$ = luminosité cible (calibrée) |
| Sortie | $u_2(t)$ → duty cycle magnétron (PWM1) |
| Cadence | **10 Hz** |

**Loi de commande** :

$$u_2(t) = K_{p2} \, e_2(t) + K_{i2} \int_0^t e_2(\tau) \, d\tau + K_{d2} \, \frac{de_2}{dt}$$

Cette boucle est plus lente car la dynamique d'ionisation
($\tau_{\text{ion}} \sim 100$ ms) est plus lente que la dynamique
de pression. Elle ajuste la **puissance RF** pour maintenir le
taux d'ionisation cible — complémentaire de PID₁ qui ajuste la
pression.

**Constantes PID initiales** :

| Paramètre | Valeur initiale | Remarque |
|:---|:---|:---|
| $K_{p2}$ | 0,5 | Conservateur — le magnétron est brutal |
| $K_{i2}$ | 0,2 s⁻¹ | Lent pour éviter les oscillations de puissance |
| $K_{d2}$ | 0,005 s | Très faible — signal caméra bruité |

### 6.5.3 PID₃ — Boucle de pompage (lente, 1 Hz)

| Paramètre | Valeur |
|:---|:---|
| Entrée | Pression $P$ (jauge Pirani) — CH1 |
| Erreur | $e_3(t) = P(t) - P_0$ |
| Consigne | $P_0 \approx 3$ mbar |
| Sortie | $u_3(t)$ → pompe à vide (relais / analogique) |
| Cadence | **1 Hz** |

**Note importante** : cette boucle n'est active que **pendant la
phase de préparation** (pompe connectée). Pendant la mesure, la
vanne d'isolement est fermée, le tuyau déconnecté, et PID₃ est
désactivé. La stabilité de pression dépend alors uniquement de la
tenue au vide de la chambre ($\sim 0{,}005$ mbar/min de remontée).

### 6.5.4 Interactions entre boucles

Les 3 boucles ne sont pas totalement indépendantes — le plasma
couple les grandeurs physiques :

```
   Pression P ←──→ nₑ ←──→ Tₑ
       ↑                     ↑
     PID₁/PID₃            PID₂
   (vanne/pompe)        (magnétron)
```

| Interaction | Mécanisme | Risque | Mitigation |
|:---|:---|:---|:---|
| PID₁ ↔ PID₂ | ↑P → ↑nₑ → ↑Lum → PID₂ réduit magnétron → ↓Tₑ → ↓nₑ | Oscillation couplée | Cadences séparées (×10) |
| PID₁ ↔ PID₃ | PID₁ (vanne) et PID₃ (pompe) agissent tous deux sur P | Conflit | PID₃ désactivé en mesure |
| PID₂ ↔ T° | ↑puissance → ↑T paroi → watchdog coupe | Arrêt intempestif | Seuil $T_{\text{max}}$ conservateur |

La **séparation de cadences** (100:10:1) est la protection principale
contre les oscillations couplées : chaque boucle rapide apparaît
comme « instantanée » du point de vue de la boucle lente.

> 📐 **Confirmation numérique** — Le script [007_dynamique_pid.py](../experiments/007_dynamique_pid.py)
> simule les 3 boucles imbriquées (100, 10, 1 Hz) sur un modèle ODE
> couplé et confirme l'absence d'oscillation croisée lorsque le ratio
> de cadences est $\geq 10\times$.

---

## 6.6 Machine d'état du firmware

Le firmware s'organise en une **machine d'état finie** avec 6 états :

```
  ┌──────────┐  démarrage  ┌──────────┐  vide atteint  ┌───────────┐
  │   INIT   │────────────▶│  POMPAGE  │───────────────▶│ AMORÇAGE  │
  │          │             │  PID₃ ON  │                │ rampe SSR │
  └──────────┘             └──────────┘                └───────────┘
       │                        │                            │
       │                        │ anomalie            claquage confirmé
       │                        ▼                      (P_r chute)
       │                  ┌──────────┐                      │
       │                  │  ERREUR  │                      ▼
       │                  │ SSR OFF  │                ┌──────────┐
       │                  └──────────┘                │  PLASMA  │
       │                        ▲                     │ PID₂ ON  │
       │                        │ anomalie            └──────────┘
       │                        │                          │
       │                        │                     vanne fermée
       │                        │                     pompe déconnectée
       │                        │                          ▼
       │                        │                    ┌──────────┐
       │                        ├────────────────────│  MESURE  │
       │                        │                    │ PID₂ ON  │
       │                        │                    │ PID₃ OFF │
       │                        │                    └──────────┘
       │                        │                          │
       │                        │                          ▼
       │                        │                    ┌──────────┐
       └────────────────────────┘                    │   FIN    │
                 watchdog timeout                    │ SSR OFF  │
                                                     │ log flush│
                                                     └──────────┘
```

### Détail des états

| État | PID₁ | PID₂ | PID₃ | SSR | Wi-Fi | Description |
|:---|:---|:---|:---|:---|:---|:---|
| **INIT** | ✘ | ✘ | ✘ | OFF | Connexion | Auto-test ADC, calibration zéros, connexion dashboard |
| **POMPAGE** | ✘ | ✘ | ✔ | OFF | Actif | Pompe active, ajustement pression vers $P_0$ |
| **AMORÇAGE** | ✘ | ✘ | ✘ | **ON (rampe)** | Actif | Rampe progressive du duty SSR (5 % → cible). Watchdog $P_r$ **adaptatif** : attend la chute de $P_r$ au lieu de couper sur seuil haut. Le soft-start SSR minimise l'énergie réfléchie par pulse pendant l'amorçage. Timeout 5 s → ERREUR si pas de claquage. Voir [§14](14_adaptation_rf.md#5-solution--séquence-damorçage-firmware-soft-start-ssr). |
| **PLASMA** | ✔ | ✔ | ✔ | **ON** | Actif | Magnétron allumé, PID actifs, tuning. Seuil watchdog $P_r$ normal rétabli. |
| **MESURE** | ✔ | ✔ | ✘ | ON | Actif | Vanne fermée, pompe déconnectée, acquisition données |
| **ERREUR** | ✘ | ✘ | ✘ | **OFF** | Alerte | Anomalie détectée — magnétron coupé, LED+buzzer |
| **FIN** | ✘ | ✘ | ✘ | OFF | Log flush | Session terminée, écriture finale SD, extinction |

### Transitions

| De → Vers | Condition | Action |
|:---|:---|:---|
| INIT → POMPAGE | Auto-test OK + Wi-Fi connecté | Activer PID₃, démarrer logging |
| POMPAGE → AMORÇAGE | $P < P_0 + 0{,}5$ mbar (vide atteint) + injection H₂O confirmée | Pré-chauffe filament (2 s), puis rampe SSR à 5 %. Watchdog $P_r$ en mode **adaptatif** (attend chute, ne coupe pas). |
| AMORÇAGE → PLASMA | $P_r(t) < 0{,}50 \times P_r(t_0)$ (claquage confirmé) | Rampe progressive du duty SSR → cible. Activer PID₂. Rétablir seuil watchdog $P_r$ normal. |
| AMORÇAGE → ERREUR | Timeout 5 s sans chute de $P_r$ | Diagnostic : pression incorrecte, pas de gaz, fuite. SSR OFF. |
| PLASMA → MESURE | Opérateur envoie commande « fermer vanne » | Désactiver PID₃ |
| MESURE → FIN | Opérateur envoie « arrêt » ou $V_{\text{bat}} < 16$ V | Couper SSR, flush SD |
| * → ERREUR | Watchdog (voir §6.7) | **Couper SSR immédiatement** |
| ERREUR → INIT | Opérateur reset (bouton physique ou Wi-Fi) | Réinitialisation complète |

---

## 6.7 Watchdog de sécurité

Le watchdog est un **superviseur autonome** qui fonctionne
indépendamment des boucles PID. Il peut couper le magnétron (SSR)
**même sans connexion Wi-Fi** — c'est un mécanisme de dernier
recours. Voir [§5.2 Haute Tension](05_securite.md#52-haute-tension--danger-mortel)
pour le contexte de sécurité.

### Conditions de déclenchement

| Condition | Seuil | Tempo | Action |
|:---|:---|:---|:---|
| $P_r > P_{r,\text{max}}$ | Découplage total (onde non absorbée). **Désactivé** en état AMORÇAGE (VSWR élevé attendu, le soft-start SSR minimise l'énergie par pulse — voir [§14](14_adaptation_rf.md)) | 100 ms | SSR OFF + alerte |
| $T_{\text{paroi}} > T_{\text{max}}$ | 150 °C | 1 s | SSR OFF + alerte |
| Perte signal pression | Capteur déconnecté ($V_{\text{ADC}} < 10$ mV) | 500 ms | SSR OFF + alerte |
| $V_{\text{bat}} < 15$ V | Surdécharge Li-ion | Immédiat | SSR OFF + extinction |
| $T_{\text{bat}} > 60$ °C | Emballement thermique batterie | Immédiat | SSR OFF + buzzer continu |
| $T_{\text{ond}} > 80$ °C | Surchauffe onduleur | 5 s | SSR OFF + alerte |
| Timeout communication | > 5 s sans heartbeat MQTT | 5 s | SSR OFF + alerte |

### Implémentation

Le watchdog utilise le **timer matériel** de l'ESP32 (indépendant
du RTOS) avec un timeout de **500 ms**. La tâche PID doit « nourrir »
le watchdog à chaque cycle (100 Hz → alimentation toutes les 10 ms).
Si le firmware plante, le timer matériel expire et ouvre le SSR.

En complément, un **watchdog logiciel** vérifie les seuils du tableau
ci-dessus à 10 Hz (tâche FreeRTOS basse priorité).

---

## 6.8 Communication et télémétrie

### MQTT — Temps réel

L'ESP32 publie sur un broker MQTT (local ou cloud) à **1 Hz** :

| Topic | Payload (JSON) | Exemple |
|:---|:---|:---|
| `bohemian/état` | `{"state": "MESURE", "uptime_s": 342}` | État machine |
| `bohemian/capteurs` | `{"P_mbar": 3.12, "Pr_mW": 15.4, "lum": 2048, "T_paroi": 42.3}` | Lectures ADC |
| `bohemian/pid` | `{"e1": 0.02, "u1": 0.45, "e2": -12, "u2": 0.78}` | Erreurs et commandes PID |
| `bohemian/sécurité` | `{"V_bat": 17.8, "T_bat": 31, "T_ond": 55, "watchdog": "OK"}` | Surveillance |
| `bohemian/alerte` | `{"type": "SURCHAUFFE", "source": "onduleur", "T": 82}` | Alertes (retain=true) |

**Abonnements** (commandes opérateur → ESP32) :

| Topic | Payload | Action |
|:---|:---|:---|
| `bohemian/cmd/état` | `"MESURE"`, `"FIN"`, `"RESET"` | Transition machine d'état |
| `bohemian/cmd/consigne` | `{"Pr0": 10.0, "Lum0": 2000, "P0": 3.0}` | Mise à jour des consignes |
| `bohemian/cmd/pid` | `{"pid": 1, "Kp": 1.2, "Ki": 0.6, "Kd": 0.02}` | Tuning PID en temps réel |

### Logging SD — Données haute résolution

Le logging sur carte microSD capture **toutes les lectures ADC** à
la cadence maximale (100 Hz) :

**Format CSV** :

```csv
timestamp_ms,P_mbar,Pr_mW,lum_mV,T_paroi_C,V_bat_V,T_bat_C,duty_vanne,duty_RF,e1,e2,e3,état
0,3.12,15.4,2048,42.3,17.8,31.2,0.45,0.78,0.02,-12,0.12,MESURE
10,3.11,15.2,2052,42.3,17.8,31.2,0.44,0.78,0.01,-8,0.11,MESURE
```

| Colonne | Unité | Source |
|:---|:---|:---|
| `timestamp_ms` | ms depuis démarrage | Timer ESP32 |
| `P_mbar` | mbar | Jauge Pirani (calibrée) |
| `Pr_mW` | mW | Coupleur directionnel (calibré) |
| `lum_mV` | mV (0–3300) | Caméra luminosité (valeur brute) |
| `T_paroi_C` | °C | MAX31855 |
| `V_bat_V` | V | Diviseur résistif |
| `T_bat_C` | °C | NTC batterie |
| `duty_vanne` | 0–1 | Sortie PID₁ |
| `duty_RF` | 0–1 | Sortie PID₂ |
| `e1`, `e2`, `e3` | — | Erreurs PID |
| `état` | texte | Machine d'état |

**Rotation** : un fichier par session, nommé
`AAAA-MM-JJ_HHhMM_session.csv`. Estimation : 100 Hz × 13 colonnes ×
~20 octets/ligne ≈ **26 Ko/s** → **1,5 Mo/min** → ~23 Mo pour une
session de 15 min. Une carte SD de 4 Go suffit pour > 170 sessions.

### Dashboard (Grafana / Node-RED)

Un dashboard web (hébergé sur un Raspberry Pi ou un ordinateur portable)
s'abonne aux topics MQTT et affiche en temps réel :

- **Jauges** : pression, $P_r$, température, tension batterie
- **Graphes temporels** : signaux capteurs + commandes PID (30 s glissant)
- **Indicateur d'état** : couleur selon l'état machine (vert/jaune/rouge)
- **Boutons** : démarrer mesure, arrêter, reset, tuning PID

---

## 6.9 Bus de communication (I²C / SPI)

L'ESP32 communique avec les capteurs et périphériques via 2 bus :

| Bus | Périphérique | Adresse / CS | Usage |
|:---|:---|:---|:---|
| **SPI** | MAX31855 | CS = GPIO5 | Thermocouple type K → $T_{\text{paroi}}$ |
| **SPI** | Carte microSD | CS = GPIO15 | Logging CSV |
| **I²C** | ADS1115 | 0x48 | ADC 16 bits externe pour Pirani (meilleure résolution) |
| **I²C** | AS7343 | 0x39 | Capteur spectral 14 canaux — proxy $n_e$ (Hβ) et $T_e$ (Hα/Hβ). Voir [§10](10_capteur_spectral.md) |
| **ADC interne** | CH0 (GPIO36) | — | $P_r$ (coupleur directionnel) |
| **ADC interne** | CH4 (GPIO32) | — | $V_{\text{bat}}$ |
| **ADC interne** | CH5 (GPIO33) | — | NTC température |
| **GPIO** | PWM0 (GPIO25) | — | Électrovanne (MOSFET) |
| **GPIO** | PWM1 (GPIO26) | — | SSR magnétron |
| **GPIO** | GPIO27 | — | Relais pompe |
| **GPIO** | GPIO2 | — | LED alarme |
| **GPIO** | GPIO4 | — | Buzzer |

### Schéma des connexions

```
  ┌─────────── ESP32 DevKitC ───────────┐
  │                                      │
  │  GPIO36 (ADC) ← Coupleur dir. Pᵣ    │
  │  GPIO32 (ADC) ← V_bat (diviseur)    │
  │  GPIO33 (ADC) ← NTC T° batt/ond.   │
  │                                      │
  │  GPIO21 (SDA) ┐                      │
  │  GPIO22 (SCL) ┤─── I²C ──→ ADS1115  │
  │               │           + AS7343   │
  │                                      │
  │  GPIO18 (SCK) ┐                      │
  │  GPIO19 (MISO)┤─── SPI ──→ MAX31855 │
  │  GPIO5  (CS1) ┘              SD card │
  │  GPIO15 (CS2)─── SPI ───────┘       │
  │                                      │
  │  GPIO25 (PWM0)──→ MOSFET → Électrov.│
  │  GPIO26 (PWM1)──→ SSR → Magnétron   │
  │  GPIO27 ──────→ Relais → Pompe      │
  │                                      │
  │  GPIO2  ──────→ LED alarme          │
  │  GPIO4  ──────→ Buzzer              │
  │                                      │
  │  Wi-Fi ────→ MQTT (dashboard)       │
  └──────────────────────────────────────┘
```

---

## 6.10 Protection RF du microcontrôleur

À proximité d'un magnétron LG 2M213-01TAG (~700 W) à 2,45 GHz, l'ESP32 subirait des
interférences fatales sans protection. Mesures obligatoires :

| Mesure | Détail |
|:---|:---|
| **Boîtier aluminium** | ≥ 1 mm d'épaisseur, fermé sur 6 faces |
| **Feedthrough filtrés** | Traversées capacitives (100 nF) sur chaque fil |
| **Ferrites** | Anneaux ferrite sur chaque câble (capteurs, alimentation) |
| **Éloignement** | Côté B du plateau (~400 mm du magnétron) |
| **Blindage câbles** | Câbles blindés (tresse cuivre) entre capteurs et boîtier |

L'atténuation d'un boîtier aluminium 1 mm à 2,45 GHz est > 80 dB
(épaisseur de peau de l'aluminium à cette fréquence : $\delta \approx
1{,}7\;\mu\text{m}$ → facteur $e^{-d/\delta} \approx 10^{-256}$).
La protection est donc **largement suffisante** si le boîtier est
correctement fermé (pas de fente > $\lambda/20 \approx 6$ mm).

---

## 6.11 Séquence de démarrage

Voici la procédure complète de mise en route du système de contrôle :

| Étape | Action | Vérification | État MCU |
|:---|:---|:---|:---|
| 1 | Insérer batterie dans socle Makita | LED indicateur ON | — |
| 2 | Mettre onduleur sous tension | Voyant onduleur vert | — |
| 3 | Alimenter ESP32 (DC-DC 18V→5V) | LED ESP32 clignote | INIT |
| 4 | Attendre connexion Wi-Fi + dashboard | Dashboard affiche « INIT » | INIT |
| 5 | Vérifier auto-test ADC (tous signaux nominaux) | Dashboard : 6/6 ✔ | INIT |
| 6 | Connecter pompe + ouvrir vanne d'isolement | Pression affichée | INIT → POMPAGE |
| 7 | Pomper jusqu'à $P < P_0 + 0{,}5$ mbar | Dashboard : $P$ ≈ 3 mbar | POMPAGE |
| 8 | Injecter vapeur d'eau (si nécessaire) | $P$ stabilisée | POMPAGE |
| 9 | Démarrer magnétron (commande dashboard) | Rampe SSR 5 % → filament chauffe 2 s | POMPAGE → **AMORÇAGE** |
| 9b | Attendre claquage RF ($P_r$ chute > 50 %) | $P_r$ chute confirmée (< 5 s) | **AMORÇAGE** → PLASMA |
| 10 | Attendre stabilisation PID₂ (~10 s) | $e_2 < $ seuil | PLASMA |
| 11 | Fermer vanne + déconnecter pompe | Vanne fermée, tuyau retiré | PLASMA → MESURE |
| 12 | Attendre amortissement du pendule (~30 min) | Oscillations amorties | MESURE |
| 13 | Début de l'acquisition de données | Log CSV actif | MESURE |

---

## 6.12 Calibration des capteurs

Avant la première session, chaque capteur doit être calibré :

### Pirani (pression)

1. Pomper au vide limite de la pompe (~0,1 mbar) → noter $V_{\text{ADC,min}}$.
2. Remplir à pression atmosphérique (~1013 mbar) → noter $V_{\text{ADC,max}}$.
3. Interpoler sur 3–5 points intermédiaires (jauge capacitive de référence).
4. Stocker la courbe de calibration en EEPROM (10 points, interpolation linéaire par morceaux).

> ⚠️ La courbe Pirani dépend de la **nature du gaz** ! La vapeur
> d'eau a une conductivité thermique différente de l'air sec.
> Calibrer avec le gaz réel (vapeur d'eau) ou appliquer le facteur
> de correction du constructeur.

### Coupleur directionnel ($P_r$)

1. Magnétron éteint, charge fantôme (bécher d'eau) → $P_r = 0$ → noter $V_{\text{ADC,0}}$.
2. Magnétron allumé, sans chambre (charge fantôme) → $P_r$ max → noter $V_{\text{ADC,max}}$.
3. La relation $P_r = f(V_{\text{ADC}})$ est typiquement linéaire après détection diode Schottky.

### Luminosité (caméra)

Calibration relative : la valeur Lum₀ (consigne de PID₂) est ajustée
empiriquement pendant les premières sessions en observant la stabilité
du plasma.

### Thermocouple (MAX31855)

Le MAX31855 intègre sa propre compensation de soudure froide. Vérifier
avec un thermomètre de référence à température ambiante (un point suffit).

---

## Références

### Contrôle et automatique

1. **[Åström, K. J.](https://en.wikipedia.org/wiki/Karl_Johan_%C3%85str%C3%B6m) & Murray, R. M.** (2021). *Feedback Systems: An
   Introduction for Scientists and Engineers*. 2ᵉ édition, Princeton
   University Press. ISBN 978-0-691-21347-9.
   [Disponible en ligne](https://www.cds.caltech.edu/~murray/amwiki)
   (Chapitres 10–11 : PID, MIMO, interactions entre boucles.)

2. **[Ziegler, J. G.](https://en.wikipedia.org/wiki/John_G._Ziegler) & Nichols, N. B.** (1942). « Optimum Settings for
   Automatic Controllers ». *Transactions of the ASME*, 64(11), 759–768.
   (Méthode classique de réglage PID par oscillation critique.)

3. **[Skogestad, S.](https://folk.ntnu.no/skoge/) & Postlethwaite, I.** (2005). *Multivariable
   Feedback Control: Analysis and Design*. 2ᵉ édition, Wiley.
   ISBN 978-0-470-01167-6.
   (Analyse de stabilité et découplage des systèmes MIMO.)

### Microcontrôleurs et instrumentation

4. **Espressif Systems** (2023). *ESP32 Technical Reference Manual*.
   [docs.espressif.com](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/)
   (ADC, PWM LEDC, timers, FreeRTOS, Wi-Fi.)

5. **Analog Devices** (2023). *MAX31855 Datasheet — Cold-Junction
   Compensated Thermocouple-to-Digital Converter*.
   [analog.com](https://www.analog.com/en/products/max31855.html)

6. **Texas Instruments** (2020). *ADS1115 Datasheet — 16-Bit ADC
   with Integrated PGA*.
   [ti.com](https://www.ti.com/product/ADS1115)
   (ADC externe pour la jauge Pirani — résolution 16 bits, I²C.)

### Plasmas et contrôle de procédé

7. **Lieberman, M. A. & Lichtenberg, A. J.** (2005). *Principles of
   Plasma Discharges and Materials Processing*. 2ᵉ édition, Wiley.
   ISBN 978-0-471-72001-0.
   (Chapitre 11 : contrôle du plasma, diagnostics et rétroaction.)

8. **Chen, F. F.** (2016). *Introduction to Plasma Physics and Controlled
   Fusion*. 3ᵉ édition, Springer. ISBN 978-3-319-22308-7.

---

[← Notes de Sécurité](05_securite.md) · [Retour au README →](../README.md)
