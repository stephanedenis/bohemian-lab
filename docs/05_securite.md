# ⚠️ Notes de Sécurité

[← Retour au README](../README.md) · [← Protocole de Validation](04_protocole.md)

---

## Introduction vulgarisée

Cette expérience n'est **pas un bricolage anodin**. Elle met en jeu :

- De la **haute tension mortelle** (4 000 volts — le cœur s'arrête à
  partir de 50 mA sous quelques dizaines de volts).
- Des **micro-ondes à haute puissance** (1 000 watts — un four
  micro-ondes ouvert qui vous cuit de l'intérieur, littéralement).
- Du **vide partiel** (risque d'implosion — un couvercle en Plexiglas
  qui lâche sous la pression atmosphérique projette des éclats à grande
  vitesse).
- Des **gaz toxiques** (ozone O₃ et oxydes d'azote NOₓ produits par
  le plasma — irritation respiratoire, lésions pulmonaires).

**Toute personne travaillant sur ce montage doit avoir lu et compris
cette section en intégralité.** Les risques ne sont pas théoriques :
ils sont réels, immédiats, et potentiellement mortels.

---

## 5.1 Risque RF — Rayonnement micro-ondes

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

- Le baril de 205 L est la **première barrière** : acier conducteur,
  atténuation > 40 dB (facteur 10 000 en puissance).
- Toutes les **ouvertures** (passages de câbles, hublots, joints)
  doivent être traitées :
  - Grilles métalliques maillées (maille < λ/10 = 1,2 cm).
  - Joints conducteurs (ruban de cuivre, tresse de masse).
  - Passages de câbles via **guides d'onde sous coupure** (tubes
    métalliques de diamètre < λ/2 = 6,1 cm et longueur > 3× diamètre).

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
de fuite. Ne jamais approcher le visage du baril lorsque le magnétron
est actif.

#### Équipements de protection individuelle (EPI)

- **Lunettes de protection RF** : inutiles (pas de protection efficace
  contre 2,45 GHz par des lunettes). La seule protection est le
  **confinement**.
- **Interrupteur d'urgence** : coupure immédiate de l'alimentation
  du magnétron, accessible sans se pencher vers le baril.

---

## 5.2 Haute Tension — Danger mortel

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

- **Disjoncteur différentiel 30 mA** en amont de l'alimentation.
  (Ne protège pas contre le choc initial, mais limite la durée.)
- **Contacts de sécurité** sur le couvercle du baril : coupure
  automatique si le baril est ouvert.
- **Résistance de décharge automatique** (« bleeder ») en
  parallèle du condensateur : décharge en ~ 30 secondes.
  **Ne pas se fier uniquement au bleeder** — toujours décharger
  manuellement en complément.
- **Signalétique** : autocollant « ⚡ HAUTE TENSION — DANGER DE MORT »
  visible sur le baril et sur l'alimentation.

#### Conduite en cas d'électrocution

1. **Ne pas toucher la victime** si elle est encore en contact avec
   la source.
2. Couper l'alimentation au disjoncteur.
3. Appeler les secours (**SAMU 15** ou **112** en France).
4. Si la victime est inconsciente et ne respire pas :
   **massage cardiaque + défibrillateur** (DAE) si disponible.

---

## 5.3 Risque d'implosion

### Nature du danger

La chambre à plasma est sous **vide partiel** (1–10 mbar, soit
100–1 000 fois moins que la pression atmosphérique). La pression
atmosphérique exerce une force considérable sur les parois :

$$F = \Delta P \times A$$

Pour un couvercle en Plexiglas de diamètre $d = 20$ cm :

$$A = \pi \left(\frac{d}{2}\right)^2 = \pi \times 0{,}01 = 0{,}0314 \; \text{m}^2$$

$$F = 10^5 \times 0{,}0314 \approx 3\,140 \; \text{N} \approx 320 \; \text{kg-force}$$

→ Trois tonnes par décimètre carré ! Si le Plexiglas cède, les éclats
sont projetés à grande vitesse.

### Mesures de protection

#### Dimensionnement du Plexiglas

Le PMMA (Plexiglas) a une résistance à la traction de ~ 70 MPa.
Pour un disque simplement appuyé sous pression uniforme, l'épaisseur
minimale est :

$$t_{\min} = \frac{d}{2} \sqrt{\frac{3 \, \Delta P \, (1 + \nu)}{8 \, \sigma_{\text{adm}}}}$$

avec un coefficient de sécurité de 4 ($\sigma_{\text{adm}} = 70/4 = 17{,}5$ MPa)
et $\nu = 0{,}37$ (coefficient de Poisson du PMMA) :

$$t_{\min} = \frac{0{,}20}{2} \sqrt{\frac{3 \times 10^5 \times 1{,}37}{8 \times 17{,}5 \times 10^6}} \approx 5{,}3 \; \text{mm}$$

**Épaisseur requise : minimum 15 mm** (facteur de sécurité supplémentaire
×3 pour tenir compte du vieillissement, des micro-fissures, et de
l'échauffement par les micro-ondes).

#### Vérifications

- Inspection visuelle du Plexiglas **avant chaque utilisation** :
  absence de fissures, rayures profondes, jaunissement (signe de
  dégradation UV).
- **Test de pression** : pomper au vide et maintenir 30 minutes.
  Vérifier l'absence de déformation visible ou de bruit.
- **Grillage de protection** : placer un grillage métallique devant
  le hublot en Plexiglas pour retenir les éclats en cas de rupture.
- **Ne jamais** se placer face au hublot en Plexiglas pendant la
  mise sous vide ou pendant le fonctionnement du plasma.

---

## 5.4 Risque gazeux — Ozone et NOₓ

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

#### Ventilation

- **Ventilation mécanique** obligatoire dans l'espace de travail :
  hotte aspirante ou extracteur d'air orienté vers l'extérieur.
- Débit minimal recommandé : 10 renouvellements d'air par heure.
- Le baril doit être **purgé** à l'air propre avant ouverture
  après une session de plasma.

#### Détection

- **Détecteur d'ozone** (tubes colorimétriques Dräger ou détecteur
  électrochimique) : à utiliser régulièrement pendant les sessions.
- Seuil d'alerte : 0,1 ppm (VLEP).
- Seuil d'évacuation : 0,3 ppm.

#### Protection individuelle

- **Masque FFP3** avec cartouche à charbon actif si ventilation
  insuffisante.
- **Travail en extérieur** recommandé si possible (garage ouvert,
  atelier ventilé).

---

## 5.5 Récapitulatif des équipements de sécurité

| Équipement | Obligatoire | Usage |
|:---|:---|:---|
| Disjoncteur différentiel 30 mA | ✅ | Protection électrique |
| Perche de décharge HT | ✅ | Décharge du condensateur |
| Multimètre (CAT III/IV) | ✅ | Vérification d'absence de tension |
| Détecteur de fuites micro-ondes | ✅ | Contrôle du blindage RF |
| Extincteur CO₂ | ✅ | Feu électrique |
| Ventilation mécanique | ✅ | Évacuation des gaz toxiques |
| Grillage de protection | ✅ | Rétention d'éclats |
| Détecteur d'ozone | 🔶 Recommandé | Monitoring de la qualité d'air |
| Défibrillateur (DAE) | 🔶 Recommandé | Réanimation |
| Lunettes de sécurité | ✅ | Protection contre éclats |
| Gants isolants (1 000 V) | ✅ | Manipulation HT |

---

## 5.6 Checklist pré-expérience

Avant **chaque session**, vérifier :

- [ ] Disjoncteur différentiel 30 mA fonctionnel (test bouton)
- [ ] Interrupteur d'urgence accessible et testé
- [ ] Condensateur HT déchargé (perche + multimètre)
- [ ] Joints du baril en bon état, bien serrés
- [ ] Détecteur de fuites micro-ondes : scan complet < 5 mW/cm²
- [ ] Plexiglas inspecté (pas de fissure, pas de jaunissement)
- [ ] Grillage de protection en place devant le hublot
- [ ] Ventilation en marche
- [ ] Passage d'air dégagé vers l'extérieur
- [ ] Détecteur d'ozone en marche (si disponible)
- [ ] Deuxième personne présente et informée de la procédure d'urgence
- [ ] Téléphone à portée de main (numéro SAMU : 15 / Urgences : 112)
- [ ] Extincteur CO₂ à portée de main

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

---

[← Protocole de Validation](04_protocole.md) · [Retour au README →](../README.md)
