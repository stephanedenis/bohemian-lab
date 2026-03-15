# ⚠️ Notes de Sécurité

[← Retour au README](../README.md) · [← Protocole de Validation](04_protocole.md) · [Contrôle →](06_controle.md)

---

## Introduction vulgarisée

Cette expérience n'est **pas un bricolage anodin**. Elle met en jeu :

- De la **haute tension mortelle** (4 000 volts — le cœur s'arrête à
  partir de 50 mA sous quelques dizaines de volts).
- Des **micro-ondes à haute puissance** (1 000 watts — un four
  micro-ondes ouvert qui vous cuit de l'intérieur, littéralement).
- Du **vide partiel** (risque d'implosion — un couvercle en acrylique
  qui lâche sous la pression atmosphérique projette des éclats à grande
  vitesse).
- Des **gaz toxiques** (ozone O₃ et oxydes d'azote NOₓ produits par
  le plasma — irritation respiratoire, lésions pulmonaires).

**Toute personne travaillant sur ce montage doit avoir lu et compris
cette section en intégralité.** Les risques ne sont pas théoriques :
ils sont réels, immédiats, et potentiellement mortels.

---

## 5.1 Risque RF — Rayonnement micro-ondes

> 💡 **Retenez** — Les micro-ondes **cuisent les yeux** (cataracte
> irréversible) et les tissus. À 1 000 W, c'est un four ouvert
> pointé sur vous. **La seule protection : le confinement
> (cage de Faraday). Restez derrière l'acier.**

### Nature du danger

Les micro-ondes à 2,45 GHz sont absorbées par les tissus biologiques
contenant de l'eau (c'est-à-dire **tous les tissus**). L'énergie
absorbée se convertit en chaleur. À 1 000 W, l'exposition directe
provoque des **brûlures profondes** en quelques secondes.

L'organe le plus vulnérable est l'**œil** : le cristallin, mal irrigué
par le sang, ne peut pas dissiper la chaleur → risque de **cataracte
micro-onde** (opacification irréversible du cristallin).

### Limites d'exposition (normes)

| Norme | Limite (2,45 GHz) | Durée |
|:---|:---|:---|
| **ICNIRP** (2020) | 10 W/m² = 1 mW/cm² | Exposition continue (public) |
| **ICNIRP** (2020) | 50 W/m² = 5 mW/cm² | Exposition professionnelle |
| **IEEE C95.1** (2019) | 10 mW/cm² | Moyenne sur 6 min |
| **FCC** (USA) | 1 mW/cm² | Public général |

### Mesures de protection

#### Confinement (cage de Faraday)

- La chambre inox est la **première barrière** : acier inoxydable
  conducteur, atténuation > 47 dB (facteur 50 000 en puissance).
- Le couvercle acrylique est recouvert d'un **grillage métallique**
  (maille < 12 mm) pour fermer la cage de Faraday.
- Toutes les **ouvertures** (passages de câbles, joints)
  doivent être traitées :
  - Grilles métalliques maillées (maille < λ/10 = 1,2 cm).
  - Joints conducteurs (ruban de cuivre, tresse de masse).
  - Passages de câbles via **guides d'onde sous coupure** (tubes
    métalliques de diamètre < λ/2 = 6,1 cm et longueur > 3× diamètre).

#### Enceinte du pendule et confinement (baril de 205L)

La chambre inox est suspendue par le fil de torsion **à l'intérieur
du baril métallique de 205 litres**, qui repose au sol comme
référentiel fixe. Le baril cumule **cinq fonctions** :

1. **Enceinte du pendule** — Le baril protège le fil de torsion et
   la chambre suspendue des perturbations extérieures (vent, chocs,
   vibrations), ce qui est essentiel pour une expérience en extérieur.
2. **Double cage de Faraday** — En cas de défaillance du grillage sur
   le couvercle acrylique ou d'un joint mal serré, le baril en acier
   (atténuation ~ 48 dB supplémentaires) confine la totalité du
   rayonnement RF.
3. **Rétention d'éclats** — Si le couvercle en acrylique venait à
   céder sous vide, les éclats sont contenus dans le baril.
4. **Confinement des gaz** — L'ozone ($\text{O}_3$) et les oxydes
   d'azote ($\text{NO}_x$) produits par le plasma restent piégés
   dans le baril jusqu'à la purge contrôlée.
5. **Stabilité thermique** — L'inertie thermique de l'acier tamponne
   les variations de température ambiante (soleil, nuages).

> ⚠️ **Le baril ne remplace pas** les protections primaires (grillage
> Faraday, joint silicone, épaisseur acrylique). C'est une couche de
> défense supplémentaire selon le principe de **défense en profondeur**.

#### Détection de fuites

- **Détecteur de fuites micro-ondes** obligatoire avant chaque
  session (disponible dans le commerce, ~ 20 €).
- Mesure à 5 cm de chaque joint, ouverture, câble.
- **Critère** : fuite < 5 mW/cm² à 5 cm de la surface.
- Si une fuite est détectée → **ARRÊT IMMÉDIAT** du magnétron,
  réparation du joint avant reprise.

#### Distance de sécurité

En cas de fuite hypothétique de 1 W (0,1 % de la puissance),
la densité de puissance à distance $r$ est :

$$S = \frac{P_{\text{fuite}}}{4\pi r^2}$$

Pour atteindre la limite de 1 mW/cm² = 10 W/m² :

$$r = \sqrt{\frac{P_{\text{fuite}}}{4\pi \times 10}} = \sqrt{\frac{1}{4\pi \times 10}} \approx 0{,}09 \; \text{m}$$

→ Même une fuite de 1 W est dangereuse **à moins de 10 cm** du point
de fuite. Ne jamais approcher le visage de la chambre lorsque le
magnétron est actif.

#### Équipements de protection individuelle (EPI)

- **Lunettes de protection RF** : inutiles (pas de protection efficace
  contre 2,45 GHz par des lunettes). La seule protection est le
  **confinement**.
- **Interrupteur d'urgence** : coupure immédiate de l'alimentation
  du magnétron, accessible sans se pencher vers la chambre.

---

## 5.2 Haute Tension — Danger mortel

> 💡 **Retenez** — Le condensateur du magnétron **tue même éteint**.
> 4 000 V × 300 mA = arrêt cardiaque instantané. **Toujours
> décharger avec la perche avant de toucher quoi que ce soit.**
> Le seuil de fibrillation ventriculaire n'est que de 50–100 mA
> (IEC 60479-1 [8]).

### Nature du danger

Le transformateur du magnétron délivre environ **4 000 V DC** à
**300 mA**. Cette combinaison est **immédiatement mortelle** :

- Le seuil de **fibrillation ventriculaire** est de 50–100 mA à
  travers le cœur.
- À 4 000 V, la résistance de la peau (~ 1 000 Ω peau sèche) ne
  constitue aucune protection : $I = V/R = 4000/1000 = 4$ A.
- Le courant traverse le corps en quelques millisecondes → **arrêt
  cardiaque**.

### Condensateur résiduel

**⚠️ DANGER CRITIQUE** — Le condensateur du circuit magnétron conserve
sa charge **après la mise hors tension**. Un magnétron éteint depuis
plusieurs minutes peut encore délivrer un choc mortel.

Énergie stockée :

$$E = \frac{1}{2} C V^2$$

Pour un condensateur typique ($C = 1 \; \mu\text{F}$, $V = 4\,000$ V) :

$$E = \frac{1}{2} \times 10^{-6} \times (4\,000)^2 = 8 \; \text{J}$$

8 joules suffisent largement à provoquer un arrêt cardiaque.

### Mesures de protection

#### Règles absolues

1. **Ne JAMAIS** travailler sur le circuit magnétron sous tension.
2. **Ne JAMAIS** toucher un composant du circuit HT sans avoir
   d'abord **déchargé le condensateur** manuellement.
3. **Toujours** utiliser une **perche de décharge** (résistance de
   10 kΩ / 10 W entre les bornes du condensateur) après mise hors
   tension.
4. **Toujours** vérifier l'absence de tension au voltmètre **avant**
   toute intervention.
5. **Travailler à deux** : une personne manipule, l'autre surveille
   et peut intervenir en cas d'électrocution.

#### Dispositifs de sécurité

- **Coupure d'urgence via SSR** commandé par l'ESP32 embarqué
  (watchdog autonome). Le SSR interrompt l'alimentation 120 V AC
  du transformateur HT en quelques millisecondes.
- **Contacts de sécurité** sur le couvercle de la chambre : coupure
  automatique si la chambre est ouverte.
- **Résistance de décharge automatique** (« bleeder ») en
  parallèle du condensateur : décharge en ~ 30 secondes.
  **Ne pas se fier uniquement au bleeder** — toujours décharger
  manuellement en complément.
- **Signalétique** : autocollant « ⚡ HAUTE TENSION — DANGER DE MORT »
  visible sur la chambre et sur l'alimentation.

#### Conduite en cas d'électrocution

1. **Ne pas toucher la victime** si elle est encore en contact avec
   la source.
2. Couper l'alimentation au disjoncteur.
3. Appeler les secours : **911** (Québec).
4. Si la victime est inconsciente et ne respire pas :
   **massage cardiaque + défibrillateur** (DAE) si disponible.

---

## 5.3 Risque d'implosion

> 💡 **Retenez** — La pression atmosphérique pousse **500 kg** sur
> le couvercle. Si l'acrylique casse, ça explose vers l'extérieur
> comme un obus. **Ne jamais se placer face au couvercle lorsque
> la chambre est sous vide.** Le facteur de sécurité est de 2,9×
> (PMMA, $\sigma_t \approx 70$ MPa, ISO 7823-1 [11]).

### Nature du danger

La chambre à vide inox est sous **vide partiel** (2–5 mbar en fonctionnement,
certifiée jusqu'à 29 inHg soit ~ 31 mbar absolu). La pression atmosphérique
exerce une force considérable sur le couvercle :

$$F = \Delta P \times A$$

Pour le couvercle en acrylique de diamètre $d = 250$ mm :

$$A = \pi \left(\frac{d}{2}\right)^2 = \pi \times 0{,}015\,625 \approx 0{,}0491 \; \text{m}^2$$

$$F = 10^5 \times 0{,}0491 \approx 4\,910 \; \text{N} \approx 500 \; \text{kg-force}$$

→ Près d'une **demi-tonne** de pression sur le couvercle ! Le risque
principal est la rupture de l'acrylique et la projection d'éclats.

### Mesures de protection

#### Couvercle acrylique 3/4"

Le couvercle en acrylique (PMMA) d'épaisseur **3/4" (19 mm)** est
spécifiquement dimensionné pour cette chambre certifiée 0–29 inHg.

Vérifions le facteur de sécurité. Le PMMA a une résistance à la
traction de ~ 70 MPa. Pour un disque simplement appuyé sous pression
uniforme, l'épaisseur minimale est :

$$t_{\min} = \frac{d}{2} \sqrt{\frac{3 \, \Delta P \, (1 + \nu)}{8 \, \sigma_{\text{adm}}}}$$

avec $\sigma_{\text{adm}} = 70/4 = 17{,}5$ MPa (facteur de sécurité 4)
et $\nu = 0{,}37$ (coefficient de Poisson du PMMA) :

$$t_{\min} = \frac{0{,}250}{2} \sqrt{\frac{3 \times 10^5 \times 1{,}37}{8 \times 17{,}5 \times 10^6}} \approx 6{,}6 \; \text{mm}$$

L'épaisseur réelle de **19 mm** offre un facteur de sécurité
$19/6{,}6 \approx 2{,}9\times$ au-delà du dimensionnement déjà conservateur
(à facteur 4 sur la contrainte). La chambre est **certifiée** par le
fabriquant pour 29 inHg, ce qui apporte une garantie supplémentaire.

#### Joint d'étanchéité en silicone

Le joint en silicone assure l'étanchéité entre la bride inox et
le couvercle acrylique. Le silicone résiste jusqu'à ~ 200 °C et
est compatible avec le vide (faible dégazage). Vérifier toutefois
sa tenue face à l'ozone ($\text{O}_3$) produit par le plasma.

#### Vérifications

- Inspection visuelle de l'acrylique **avant chaque utilisation** :
  absence de fissures, rayures profondes, jaunissement (signe de
  dégradation UV ou thermique).
- **Test de pression** : pomper au vide et maintenir 30 minutes.
  Vérifier l'absence de déformation visible ou de bruit.
- **Grillage de protection** : le grillage métallique de la cage de
  Faraday, plaqué sur la face extérieure du couvercle, sert aussi de
  rétention d'éclats en cas de rupture. Double fonction.
- **Baril de confinement** : pendant l'expérience, le baril de 205L
  entourant l'ensemble constitue une **troisième barrière** contre
  la projection d'éclats.
- **Ne jamais** se placer face au couvercle acrylique pendant la
  mise sous vide ou pendant le fonctionnement du plasma.

---

## 5.4 Risque gazeux — Ozone et NOₓ

> 💡 **Retenez** — L'ozone est **inodore après 5 minutes** — votre
> nez s'adapte et ment. VLEP = 0,1 ppm (INRS ED 6294 [5]).
> En cas de doute, **éloignez-vous côté au vent**.

### Nature du danger

Le plasma de vapeur d'eau produit des espèces chimiques toxiques :

| Espèce | Formule | Source | Seuil (VLEP 8h) | Effets |
|:---|:---|:---|:---|:---|
| Ozone | O₃ | Recombinaison O + O₂ | 0,1 ppm | Irritation respiratoire, œdème pulmonaire |
| Monoxyde d'azote | NO | Plasma en air résiduel | 25 ppm | Toxique par inhalation |
| Dioxyde d'azote | NO₂ | Oxydation de NO | 3 ppm | Très toxique, corrosif, œdème pulmonaire |
| Peroxyde d'hydrogène | H₂O₂ | Recombinaison OH + OH | 1 ppm | Irritation des muqueuses |

*VLEP = Valeur Limite d'Exposition Professionnelle (moyenne sur 8h)*

L'ozone est particulièrement insidieux : il a une odeur détectable
(~ 0,01 ppm), mais l'odorat **s'adapte** en quelques minutes, et on
cesse de le sentir alors que la concentration augmente.

### Mesures de protection

#### Ventilation — Expérience en extérieur

L'expérience se déroule **en extérieur** (cour, terrain dégagé),
ce qui procure une ventilation naturelle largement suffisante pour
disperser l'ozone et les NOₓ produits par le plasma.

- **Se positionner dos au vent** (ou perpendiculairement) pour
  que les gaz soient emportés loin de l'opérateur.
- La chambre doit être **purgée** à l'air propre avant ouverture
  après une session de plasma.
- Par temps **calme** (vent < 5 km/h), la dispersion est plus lente :
  prévoir un ventilateur portatif ou un extracteur sur batterie
  dirigé vers l'ouvrage.

#### Détection

- **Détecteur d'ozone** (tubes colorimétriques Dräger ou détecteur
  électrochimique) : à utiliser régulièrement pendant les sessions,
  même en extérieur.
- Seuil d'alerte : 0,1 ppm (VLEP).
- Seuil d'évacuation : 0,3 ppm (s'éloigner de l'ouvrage, côté
  au vent).

#### Protection individuelle

- **Masque FFP3** avec cartouche à charbon actif si vent calme
  ou stagnation atmosphérique.
- En extérieur, le risque gazeux est fortement réduit mais reste
  non nul lors de l'ouverture du baril/chambre après une session.

---

## 5.5 Alimentation embarquée — Batterie lithium-ion et onduleur

> 💡 **Retenez** — Une batterie Li-ion en emballement thermique
> produit du **fluorure d'hydrogène (HF)** — gaz mortel. **Ne pas
> ouvrir le baril**, ne pas utiliser d'eau. Extincteur CO₂ ou
> classe D uniquement (NFPA 10 [10]). Exigences de sécurité
> des batteries Li-ion : IEC 62133 [9].

### Nature du danger

L'assemblage suspendu comprend une **batterie Li-ion Makita 18 V**
(5–6 Ah, 90–108 Wh) et un **onduleur 120 V AC** qui alimente le
transformateur HT du magnétron. Ce système embarqué introduit des
risques spécifiques :

| Risque | Description | Probabilité |
|:---|:---|:---|
| **Emballement thermique** (thermal runaway) | Court-circuit interne → incendie/explosion de la batterie | Faible (BMS intégré), mais catastrophique |
| **Incendie Li-ion en espace confiné** | Flamme + gaz toxiques (HF, PF₅) dans le baril fermé | Faible |
| **Choc électrique 120 V** | Sortie onduleur accessible lors d'une intervention | Modérée |
| **Surchauffe onduleur** | 1 200 W dans un espace fermé → risque thermique | Modérée |

### Mesures de protection

#### Batterie

- Utiliser **exclusivement des batteries Makita authentiques** (BMS
  intégré : protection contre surcharge, surdécharge, surintensité,
  court-circuit, surtempérature).
- **Ne jamais modifier** le pack batterie ou contourner le BMS.
- Inspecter visuellement la batterie avant chaque session :
  - Pas de gonflement, fissure ou odeur.
  - Contacts propres et non corrodés.
  - Température ambiante entre 0 °C et 40 °C.
- **Ne pas laisser la batterie en plein soleil** avant le montage
  (risque de surchauffe → dégradation des cellules).
- Prévoir un **sac ignifuge Li-ion** (LiPo bag) à portée de main
  pour stocker la batterie en cas d'anomalie.

#### Onduleur

- L'onduleur produit du **120 V AC** — mêmes précautions que pour
  toute alimentation secteur.
- En régime continu à 1 200 W, le rendement de ~ 85 % implique
  ~ 200 W de pertes thermiques. Assurer un **dégagement de chaleur**
  (l'onduleur ne doit pas être noyé dans un isolant).
- Vérifier que l'onduleur dispose de protections intégrées :
  - Surintensité (fusible ou disjoncteur).
  - Surtempérature (arrêt automatique).
  - Court-circuit (coupure immédiate).
- Raccorder l'onduleur à la batterie **avant** de connecter la
  charge (transfo HT). Ne jamais brancher sous charge.

#### Surveillance par l'ESP32 embarqué

L'ESP32 embarqué doit monitorer en continu :

- **Tension batterie** (via diviseur résistif) : couper le système
  si $V_{\text{bat}} < 15$ V (seuil de surdécharge).
- **Température batterie** (thermocouple ou NTC collé sur le pack) :
  couper si $T > 60$ °C.
- **Température onduleur** : couper si $T > 80$ °C.
- En cas d'anomalie, le watchdog de l'ESP32 ouvre le **SSR du
  magnétron** même sans connexion Wi-Fi.

> ⚠️ **En cas d'emballement thermique** — NE PAS ouvrir le baril.
> Éloigner tout le monde à > 5 m. Laisser refroidir.
> Appeler les secours : **911**. Ne PAS utiliser d'eau sur un feu
> de batterie lithium — utiliser l'extincteur CO₂ ou un extincteur
> spécifique Li-ion (classe D).

---

## 5.6 Risque RF pendant l'amorçage — Puissance réfléchie

> 💡 **Retenez** — Avant la formation du plasma, **~90 % de la
> puissance micro-onde revient dans le magnétron**. Sans protection,
> c'est 630 W qui chauffent l'anode au lieu d'ioniser le gaz.
> **Le firmware soft-start SSR est la protection principale.**

### Nature du danger

Lorsque le magnétron est allumé et qu'il n'y a pas encore de plasma
(ou que le plasma se perd transitoirement), la cavité présente une
impédance fortement désadaptée. La puissance réfléchie :

- **Échauffe l'anode** du magnétron → réduit sa durée de vie.
- Provoque du ***mode jumping*** → fréquence instable, couplage
  erratique, possible arc interne destructeur.
- **Stress le condensateur HT** (courant réduit → tension monte).

Ce problème se produit à **chaque allumage** (transition POMPAGE →
PLASMA) et à chaque perte transitoire du plasma pendant la mesure.

### Mesure de protection — Firmware soft-start SSR

La protection du magnétron repose sur le **firmware** : une rampe
progressive du duty cycle SSR (3 % → 5 % → 10 % → 20 % → 43 %)
minimise l'énergie réfléchie par pulse pendant la phase d'amorçage.
Le magnétron domestique LG 2M213-01TAG (~15 $) est traité comme un
**consommable** dont la durée de vie réduite par le VSWR est un
compromis acceptable face à la préservation de la sensibilité du
pendule de torsion.

| Paramètre | Valeur |
|:---|:---|
| Stratégie | Rampe progressive duty SSR (soft-start) |
| Masse ajoutée | **0 kg** |
| Coût | **0 $** (firmware uniquement) |
| Durée de vie magnétron estimée | ~2 000 h (vs 10 000 h nominal) |
| Coût magnétron de remplacement | ~15 $ |
| Statut | 🔶 **À implémenter** dans le firmware |

> 💡 **Pourquoi pas de circulateur ?** — Un circulateur ferrite WR-340
> ajouterait **3–6 kg** sur le bras du pendule (circulateur + charge
> à eau + plomberie), ce qui est incompatible avec un système de
> torsion conçu pour détecter des micro-newtons.

Voir [§14 — Adaptation RF et Amorçage](14_adaptation_rf.md) pour
les spécifications complètes, l'algorithme d'amorçage et la
justification de l'approche « consommable ».

### Séquence d'amorçage firmware

Le firmware doit implémenter un **nouvel état AMORÇAGE** avec une
rampe progressive de puissance et des seuils de watchdog adaptatifs.
Voir [§14 §5](14_adaptation_rf.md#5-solution--séquence-damorçage-firmware-soft-start-ssr)
et [§6.6](06_controle.md#66-machine-détat-du-firmware).

---

## 5.7 Récapitulatif des équipements de sécurité

| Équipement | Obligatoire | Usage |
|:---|:---|:---|
| SSR + watchdog ESP32 (coupure magnétron) | ✅ | Protection électrique embarquée |
| Firmware soft-start SSR (rampe d'amorçage) | ✅ | Protection magnétron contre puissance réfléchie (VSWR amorçage). [§14](14_adaptation_rf.md) |
| Perche de décharge HT | ✅ | Décharge du condensateur |
| Multimètre (CAT III/IV) | ✅ | Vérification d'absence de tension |
| Détecteur de fuites micro-ondes | ✅ | Contrôle du blindage RF |
| Extincteur CO₂ | ✅ | Feu électrique / batterie Li-ion |
| Sac ignifuge Li-ion (LiPo bag) | 🔶 Recommandé | Confinement batterie en cas d'anomalie |
| Ventilateur portatif (vent calme) | 🔶 Recommandé | Dispersion des gaz par vent faible |
| Grillage de protection | ✅ | Rétention d'éclats |
| Baril de 205L (confinement) | ✅ | Double cage Faraday + rétention éclats + gaz |
| Détecteur d'ozone | 🔶 Recommandé | Monitoring de la qualité d'air |
| Défibrillateur (DAE) | 🔶 Recommandé | Réanimation |
| Lunettes de sécurité | ✅ | Protection contre éclats |
| Gants isolants (1 000 V) | ✅ | Manipulation HT |

---

## 5.8 Checklist pré-expérience

Avant **chaque session**, vérifier :

**Alimentation embarquée :**
- [ ] Batterie Makita inspectée (pas de gonflement, contacts propres)
- [ ] Batterie chargée (indicateur LED ≥ 75 %)
- [ ] Température batterie < 40 °C avant montage
- [ ] Onduleur testé (mise sous tension brève sans charge)

**Sécurité électrique :**
- [ ] Condensateur HT déchargé si le circuit a été sous tension
      (perche + multimètre)
- [ ] Interrupteur d'urgence / SSR fonctionnel et accessible

**Chaîne RF et confinement :**
- [ ] Joint silicone de la chambre en bon état, bien serré
- [ ] Couvercle acrylique inspecté (pas de fissure, pas de jaunissement)
- [ ] Grillage de protection en place sur le couvercle (Faraday + éclats)
- [ ] Détecteur de fuites micro-ondes : scan complet < 5 mW/cm²

**Pendule et baril :**
- [ ] Aucun lien mécanique entre la chambre et le baril
      (hormis le fil de torsion)
- [ ] Chambre suspendue librement (pas de frottement ni butoir)
- [ ] Baril de 205L fermé autour de l'ensemble (double confinement)

**Environnement :**
- [ ] **Conditions météo vérifiées** : pas de pluie, pas d'orage
- [ ] Positionnement dos au vent, zone dégagée
- [ ] Détecteur d'ozone en marche (si disponible)

**Communication et secours :**
- [ ] ESP32 connecté en Wi-Fi, dashboard visible
- [ ] Caméras sans fil actives
- [ ] Deuxième personne présente et informée de la procédure d'urgence
- [ ] Téléphone à portée de main (urgences : **911**)
- [ ] Extincteur CO₂ + sac ignifuge Li-ion à portée de main

---

## Références normatives

1. **ICNIRP** (2020). « Guidelines for Limiting Exposure to
   Electromagnetic Fields (100 kHz to 300 GHz) ». *Health Physics*,
   118(5), 483–524.
   [doi:10.1097/HP.0000000000001210](https://doi.org/10.1097/HP.0000000000001210)

2. **IEEE C95.1-2019**. *IEEE Standard for Safety Levels with Respect
   to Human Exposure to Electric, Magnetic, and Electromagnetic Fields,
   0 Hz to 300 GHz*. IEEE Standards Association.
   [standards.ieee.org](https://standards.ieee.org/standard/C95_1-2019.html)

3. **Directive 2013/35/UE** du Parlement européen et du Conseil relative
   aux prescriptions minimales de sécurité et de santé relatives à
   l'exposition des travailleurs aux risques dus aux champs
   électromagnétiques.

4. **INRS** (France). « Champs électromagnétiques ». Dossier web.
   [inrs.fr/risques/champs-electromagnetiques](https://www.inrs.fr/risques/champs-electromagnetiques.html)

5. **INRS ED 6294** (2019). « Ozone — Fiche toxicologique ». INRS.
   [inrs.fr/fichetox/ozone](https://www.inrs.fr/publications/bdd/fichetox/fiche.html?refINRS=FICHETOX_43)

6. **NF C18-510** (2012). *Opérations sur les ouvrages et installations
   électriques et dans un environnement électrique — Prévention du
   risque électrique*. AFNOR.

7. **Norme NF EN 61010-1** (2010). *Règles de sécurité pour appareils
   électriques de mesurage, de régulation et de laboratoire*.

8. **IEC 60479-1** (2018). *Effects of current on human beings and
   livestock — Part 1: General aspects*. IEC.
   (Seuil de fibrillation ventriculaire : 50–100 mA, 50 Hz, trajet
   main–main ou main–pied.)

9. **IEC 62133-2** (2017). *Secondary cells and batteries containing
   alkaline or other non-acid electrolytes — Safety requirements for
   portable sealed secondary lithium cells*. IEC.
   (Exigences de sécurité BMS, tests d'emballement thermique.)

10. **NFPA 10** (2022). *Standard for Portable Fire Extinguishers*.
    National Fire Protection Association.
    (Classe D pour feux de métaux / batteries lithium.)

11. **ISO 7823-1** (2003). *Plastics — Poly(methyl methacrylate)
    sheets — Types, dimensions and characteristics*. ISO.
    ($\sigma_t \approx 70$ MPa, $\nu = 0{,}37$ pour le PMMA coulé.)

---

[← Protocole de Validation](04_protocole.md) · [Section suivante : Contrôle et Asservissement →](06_controle.md)
