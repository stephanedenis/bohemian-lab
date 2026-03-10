# 🧪 Protocole de Validation

[← Retour au README](../README.md) · [← Configuration Matérielle](03_materiel.md)

---

## Introduction vulgarisée

En science, **prouver** qu'un effet existe ne suffit pas : il faut aussi
prouver que cet effet n'est pas dû à autre chose. C'est le principe du
**contrôle expérimental**. Si on observe que la chambre tourne quand on
allume le magnétron, il faut s'assurer que ce n'est pas simplement parce
que l'air chaud pousse dessus, ou parce qu'un courant électrique crée un
champ magnétique parasite, ou parce que des ions soufflent comme un petit
ventilateur.

Cette section décrit toutes les précautions prises pour éliminer ces
« faux positifs » — les effets parasites qui pourraient mimer une force
de poussée — et la procédure exacte pour mener l'expérience de façon
rigoureuse. Le but est qu'un autre expérimentateur puisse **reproduire**
l'expérience en suivant ces étapes.

---

## 4.1 Élimination des biais — Faux positifs

### 4.1.1 Vent ionique

> 💡 **En termes simples** — Imaginez un ventilateur invisible à
> l'intérieur de la chambre : les ions positifs du plasma sont
> projetés vers les parois comme de minuscules billes de billard.
> On appelle cela le « vent ionique ». Mais comme la chambre est
> **complètement fermée**, ces billes frappent la paroi et rebondissent
> — la force vers la gauche est exactement annulée par la force
> vers la droite. Résultat net : zéro. C'est la 3ᵉ loi de Newton
> à l'intérieur d'une boîte fermée.

#### Le problème

Dans un plasma, les ions positifs sont accélérés par le champ électrique
et transfèrent leur quantité de mouvement au gaz neutre par collisions.
Ce phénomène, appelé **vent ionique** (ou vent électrique), peut créer
une force de l'ordre de quelques µN à mN, soit exactement l'ordre de
grandeur recherché.

#### La solution — Confinement hermétique

La chambre à plasma est **hermétiquement scellée** et sous vide partiel.
Le vent ionique ne peut pas transmettre de force à l'extérieur car :

- Il n'y a pas de fuite de gaz → pas de transfert convectif.
- La force du vent ionique est **interne** : le moment cinétique total
  des ions + paroi reste nul (3ᵉ loi de Newton).
- Toute force exercée par le vent ionique sur une paroi est exactement
  compensée par la force de réaction sur le plasma.

#### Vérification

- Test de référence avec **gaz noble** (argon) à la place de la vapeur
  d'eau : même pression, même puissance RF, mais pas de dissociation
  H-OH → le plasma est symétrique. Si une force est observée, elle est
  probablement due au vent ionique.
- Test sous **vide poussé** (< 0,1 mbar) : pas de plasma → pas de vent
  ionique. Toute force résiduelle est d'origine non-ionique.

---

### 4.1.2 Effet thermique

> 💡 **En termes simples** — Quand on chauffe un objet, il rayonne de la
> chaleur. En 1874, [William Crookes](https://fr.wikipedia.org/wiki/William_Crookes)
> a inventé le [radiomètre](https://fr.wikipedia.org/wiki/Radiom%C3%A8tre_de_Crookes)
> — un petit moulin à ailettes qui tourne sous l'effet de la chaleur.
> Notre chambre pourrait être un radiomètre involontaire : un côté plus
> chaud que l'autre pousse le gaz résiduel ou émet plus d'infrarouge.
> Pour distinguer la vraie force du « coup de chaleur », on fait un test
> avec de l'**eau liquide** (même chaleur, pas de plasma).

#### Le problème

L'absorption de 1 kW de micro-ondes chauffe la chambre et les parois.
Cette chaleur crée :

- **Dilatation thermique** asymétrique → déplacement du centre de masse.
- **Convection** si le système n'est pas sous vide → courants d'air.
- **Rayonnement infrarouge** asymétrique → pression de radiation thermique
  (effet Crookes).

#### La solution — Tirs pulsés

Le magnétron est activé en **mode pulsé** (quelques secondes ON, pause) :

- La composante thermique est un effet **lent** (constante de temps
  thermique $\tau_{\text{th}} \sim$ minutes).
- La composante de poussée est un effet **rapide** (synchrone avec le
  plasma, $\tau \sim$ ms).
- En analysant la **fréquence** du signal de déplacement, on peut
  séparer les deux contributions par filtrage temporel.

#### Vérification — Charge fantôme

Remplacement du plasma par une **charge fantôme** (récipient d'eau) qui
absorbe autant de puissance micro-onde mais sans créer de plasma :

- Mêmes effets thermiques (absorption de 1 kW).
- Pas de plasma → pas de gradient de phase → pas de force bohmienne.
- Toute force mesurée avec la charge fantôme est un **artefact thermique**.

La force mesurée avec le plasma moins la force mesurée avec la charge
fantôme donne la contribution nette du plasma :

$$F_{\text{plasma}} = F_{\text{mesuré}} - F_{\text{charge fantôme}}$$

---

### 4.1.3 Forces électromagnétiques parasites

> 💡 **En termes simples** — Un courant électrique dans un champ
> magnétique subit une force (c'est le principe du **moteur électrique**).
> Le magnétron est un puissant aimant, et le plasma contient des
> courants électriques. Ensemble, ils pourraient créer une force parasite
> qui mime la poussée recherchée. Pour le vérifier, on **retourne le
> montage à 180°** : un vrai artefact EM reste dans la même direction,
> une vraie force de guidage s'inverse.

#### Le problème

Le magnétron crée un champ magnétique intense (~ 0,1 T) et le courant
de décharge du plasma crée lui-même un champ magnétique. L'interaction
entre ces champs et les courants induits dans les parois métalliques
peut produire une **force de Laplace** :

$$\vec{F} = q\vec{v} \times \vec{B} \quad \text{ou} \quad \vec{F} = I\vec{L} \times \vec{B}$$

#### La solution — Inversion à 180°

Le dispositif interne (magnétron + antenne) est **retourné de 180°**
à l'intérieur de la chambre :

- Si la force est due à un artefact EM lié à la géométrie
  (câbles, position du magnétron), elle **conserve sa direction**
  par rapport au référentiel du labo.
- Si la force est due au guidage bohmien (gradient de phase),
  elle **s'inverse** avec le retournement du dispositif.

Ce test est **discriminant** : seule une vraie force liée à l'asymétrie
du plasma s'inverse proprement.

#### Vérification complémentaire — Blindage magnétique

Ajout de feuilles de mu-métal autour du magnétron pour réduire les
fuites de champ magnétique statique. Si la force diminue avec le
blindage magnétique, elle est probablement d'origine EM et non
quantique.

---

## 4.2 Procédure de Test

> 💡 **En termes simples** — La procédure suit la logique d'une
> [expérience contrôlée](https://fr.wikipedia.org/wiki/Exp%C3%A9rience_contr%C3%B4l%C3%A9e)
> en 5 étapes : (1) préparer, (2) étalonner l'instrument, (3) mesurer
> le « bruit » quand il ne se passe rien, (4) faire le vrai test,
> (5) refaire le test en changeant un paramètre pour s'assurer que
> ce n'est pas un hasard. Chaque étape est documentée et
> reproductible par un tiers.

### Conditions préalables — Météo

L'expérience se déroule **en extérieur**. Avant de commencer :

- **Pas de pluie** ni d'orage (sécurité électrique + humidité).
- Le vent n'est **plus un facteur limitant** pour le pendule : la chambre
  est suspendue à l'intérieur du baril fermé, totalement à l'abri.
- Éviter les heures de grand ensoleillement direct sur le baril
  (dérive thermique, atténuée par l'inertie de l'acier).

### Étape 1 — Mise sous vide et préparation

1. Assembler la chambre à vide avec l'alimentation embarquée
   (batterie Makita + onduleur + transfo HT). Vérifier l'étanchéité
   du joint silicone sur le couvercle acrylique.
2. Ouvrir la vanne d'isolement. Connecter le tuyau de la pompe à vide.
   La chambre est **bridée mécaniquement** (calage, pas de rotation).
3. Pomper jusqu'à $P < 1$ mbar. Vérifier l'absence de fuites
   ($< 10^{-3}$ mbar·L/s).
4. **Injection capillaire** de vapeur d'eau : ouvrir le micro-doseur
   pour atteindre $P \approx 2-5$ mbar.
5. **Fermer la vanne d'isolement** (quart de tour).
6. **Déconnecter le tuyau** de la pompe.
7. Vérifier qu'il n'y a **aucun lien mécanique** entre la chambre
   et le baril (hormis le fil de torsion).
8. Mettre sous tension l'ESP32 embarqué. Vérifier la connexion Wi-Fi
   et le signal des capteurs sur le dashboard.
9. Libérer la bride mécanique — la chambre est maintenant **libre
   de tourner** sur le fil de torsion.
10. **Fermer le baril.** Activer les caméras sans fil.

### Étape 2 — Calibration du pendule

1. Fermer le baril. Laisser le système au repos jusqu'à ce que les
   oscillations parasites soient amorties (~ 30 min).
2. Provoquer une oscillation libre en donnant une légère impulsion
   calibrée (masse connue lâchée sur un bras de levier).
3. Enregistrer la période d'oscillation $T_0$ via le signal PSD
   (minimum 10 oscillations complètes).
4. Calculer la constante de torsion :

$$\kappa = \frac{4\pi^2 I}{T_0^2}$$

5. Vérifier la linéarité : appliquer des forces calibrées connues
   (masses suspendues via poulie) et tracer $\theta = f(F)$.

### Étape 3 — Acquisition de référence

1. **Mesure à vide** : enregistrer 10 minutes de signal du pendule
   avec le magnétron éteint → bruit de fond et dérive.
2. **Mesure avec charge fantôme** : remplacer la vapeur d'eau par
   de l'eau liquide dans un récipient. Activer le magnétron en mode
   pulsé. Enregistrer 10 minutes → artefact thermique de référence.

### Étape 4 — Test principal

1. Rétablir la vapeur d'eau sous vide dans la chambre.
2. Activer le magnétron en mode **pulsé** : cycle ON/OFF synchronisé
   à la période mécanique $T_0$ du pendule.

   Fréquence de pulsation :

$$f_{\text{pulse}} = \frac{1}{T_0}$$

3. Enregistrer le déplacement angulaire via le **signal PSD** (laser
   + photodétecteur fixés au baril, données lues par l'ESP32 embarqué
   et transmises en Wi-Fi).
4. Enregistrer simultanément (via ESP32 embarqué) : courant du
   magnétron, pression de la chambre, luminosité du plasma (tubes
   Nixie), température des parois, position du spot laser (PSD).
5. Durée minimale : 20 cycles complets ($20 \times T_0$).

### Étape 5 — Tests de contrôle

1. **Inversion 180°** : retourner le dispositif interne, répéter le
   test. La force doit s'inverser.
2. **Gaz noble** : remplacer la vapeur d'eau par de l'argon à la
   même pression. Le plasma symétrique ne devrait pas produire de
   gradient de phase asymétrique.
3. **Sans plasma** : réduire la pression à < 0,01 mbar (pas de
   claquage). Le magnétron tourne dans le vide sans créer de plasma.

---

## 4.3 Analyse des données

> 💡 **En termes simples** — Le signal qu'on mesure est noyé dans
> du « bruit » — des vibrations parasites, des fluctuations de
> température. C'est comme essayer d'entendre quelqu'un chuchoter
> dans un concert de rock. L'astuce : on sait à quel **rythme**
> le chuchoteur parle (la fréquence de pulsation du magnétron).
> On peut donc « filtrer » le bruit et ne garder que le signal
> qui bat au bon rythme. C'est le principe de la
> [corrélation croisée](https://fr.wikipedia.org/wiki/Corr%C3%A9lation_crois%C3%A9e),
> utilisée aussi en radar et en astronomie.

### Extraction du signal

Le signal brut $\theta(t)$ contient :

- **Signal recherché** : oscillation à la fréquence $f_0 = 1/T_0$,
  en phase avec le magnétron.
- **Bruit** : vibrations sismiques (atténuées par la masse du baril),
  bruit thermique du fil. Le vent est **éliminé** par le confinement
  dans le baril.
- **Dérive** : composante thermique lente (tamponnée par l'inertie
  thermique du baril, mais présente en extérieur).

Traitement :

1. **Filtrage passe-bande** autour de $f_0$ :
   $f_{\text{bande}} = [f_0 - \Delta f, \; f_0 + \Delta f]$
   avec $\Delta f = f_0 / (2 \times Q_{\text{mec}})$ où $Q_{\text{mec}}$
   est le facteur de qualité mécanique du pendule.

2. **Corrélation croisée** entre $\theta(t)$ et le signal de commande
   du magnétron $M(t)$ :

$$C(\tau) = \int_0^T \theta(t) \cdot M(t - \tau) \, dt$$

   Un pic de corrélation à $\tau = 0$ (ou à un retard constant)
   confirme la synchronisation force-plasma.

3. **Rapport signal/bruit** (SNR) :

$$\text{SNR} = \frac{A_{\text{signal}}}{\sigma_{\text{bruit}}}$$

   Objectif : SNR > 3 (significativité à 3σ).

### Calcul de la force

À partir de l'amplitude $\theta_{\text{max}}$ mesurée :

$$F_{\text{mesuré}} = \frac{\kappa \cdot \theta_{\text{max}}}{L}$$

La force nette attribuable à l'effet plasma :

$$F_{\text{net}} = F_{\text{mesuré}} - F_{\text{charge fantôme}}$$

### Comparaison avec la prédiction

Ratio entre la force mesurée et la pression de radiation :

$$\eta = \frac{F_{\text{net}}}{P_{\text{abs}} / c}$$

- $\eta \approx 0$ → pas d'effet détectable, conforme à la physique
  classique.
- $\eta > 1$ → excès de force au-delà de la pression de radiation →
  candidat pour l'effet bohmien.
- $\eta \gg 1$ → résultat surprenant, nécessitant vérification
  indépendante et recherche d'artefact.

---

## 4.4 Critères de succès

> 💡 **En termes simples** — En science, un résultat n'est considéré
> comme « réel » que s'il est **reproductible** (on peut le refaire),
> **significatif** (il ne peut pas être dû au hasard), et **spécifique**
> (il disparaît quand on enlève l'ingrédient clé). Le seuil de
> « 3σ » signifie qu'il y a moins de 0,3 % de chances que le signal
> soit dû au hasard — c'est la convention utilisée en physique
> expérimentale avant de considérer un résultat comme
> [probant](https://fr.wikipedia.org/wiki/Significativit%C3%A9_statistique).

| Critère | Seuil |
|:---|:---|
| Reproductibilité | ≥ 5 essais avec résultat cohérent |
| Rapport signal/bruit | SNR > 3 (significativité 3σ) |
| Corrélation temporelle | Pic de corrélation croisée > 0,8 |
| Inversion 180° | Force inversée (même amplitude, signe opposé) |
| Charge fantôme | $F_{\text{charge fantôme}} < 0{,}3 \times F_{\text{mesuré}}$ |
| Gaz noble | $F_{\text{argon}} < 0{,}3 \times F_{\text{vapeur d'eau}}$ |

---

## 4.5 Objections anticipées et réponses

> 💡 **En termes simples** — Quand un scientifique présente un
> résultat qui défie les lois connues, la communauté lui oppose
> des **objections** — et c'est sain. Le but n'est pas de « prouver »
> qu'on a raison, mais de montrer qu'on a **pensé à tout** avant
> d'affirmer quoi que ce soit. Voici les objections les plus
> probables et les réponses expérimentales.

| Objection | Réponse |
|:---|:---|
| « C'est du vent ionique » | Système hermétique sous vide ; test argon négatif |
| « C'est un effet thermique » | Mode pulsé + charge fantôme de contrôle |
| « C'est une force EM parasite » | Inversion 180° + blindage mu-métal |
| « La pression de radiation suffit à expliquer » | Calcul explicite de $P/c$ et comparaison avec $F_{\text{mesuré}}$ |
| « Le potentiel quantique ne s'applique pas aux photons » | Discussion théorique dans [02_theorie.md](02_theorie.md#24-application-aux-photons-rf) |
| « La mécanique bohmienne ne prédit pas cela » | Le protocole est conçu pour tester l'hypothèse, pas pour la présumer vraie |

---

## 4.6 Attentes concrètes — Confirmer ou infirmer l'hypothèse

> 💡 **Ce que l'expérience tranche** — L'hypothèse bohmienne prédit une
> force excédentaire au-delà de la pression de radiation classique.
> Les résultats possibles sont bornés et interprétables.

### Grandeur clé : le ratio d'excès $\eta$

$$\eta = \frac{F_{\text{net}}}{P_{\text{abs}} / c}$$

où $F_{\text{net}}$ est la force nette mesurée (après soustraction de
la charge fantôme) et $P_{\text{abs}}/c$ est la pression de radiation
classique (~3,3 µN pour 1 kW).

### Scénarios de résultat

| Résultat | $\eta$ | Interprétation | Conséquence |
|:---|:---|:---|:---|
| **Nul** | $\eta < 1$ (compatible avec 0) | Pas de force au-delà de la physique classique | Hypothèse **infirmée** dans cette configuration |
| **Classique** | $\eta \approx 1$ | Force = pression de radiation seule | Physique classique confirmée, pas d'effet bohmien |
| **Excès modéré** | $1 < \eta < 10$ | Force excédentaire, ordre de grandeur µN | **Zone intéressante** — vérifications supplémentaires requises |
| **Excès fort** | $\eta > 10$ | Force bien au-delà de la pression de radiation | Résultat **anomal** — chercher artefacts en priorité |
| **Négatif** | $\eta < 0$ | Force dans le sens opposé | Artefact probable (thermique, EM) |

### Ce qui CONFIRME l'hypothèse (tous les critères requis)

1. **$\eta > 1$** de manière reproductible (≥ 5 essais, SNR > 3).
2. **L'inversion 180°** du fléau inverse le signe de la force
   (même amplitude, direction opposée).
3. **Le gradient Nixie corrèle** avec la force : la direction de
   l'asymétrie sur les 8 IN-13 pointe vers la direction de la force
   mesurée par le pendule.
4. **Le test au gaz noble (argon) est négatif** : $\eta_{\text{Ar}} < 0{,}3$.
   L'argon produit un plasma symétrique (pas de dissociation),
   donc pas de gradient de phase.
5. **La charge fantôme (eau liquide) est négative** :
   $F_{\text{fantôme}} < 0{,}3 \times F_{\text{mesuré}}$.
6. **Le test à vide (sans plasma) est négatif** :
   $F_{\text{vide}} \approx 0$.

### Ce qui INFIRME l'hypothèse

| Observation | Conclusion |
|:---|:---|
| $\eta \leq 1$ dans tous les essais | Pas de force excédentaire |
| La force ne s'inverse pas avec le retournement 180° | Artefact mécanique ou thermique |
| Le test argon donne $\eta \sim \eta_{\text{H₂O}}$ | La force n'est pas liée au gradient de phase (vapeur d'eau) |
| Les 8 Nixie montrent un champ symétrique malgré une force | Artefact non lié au plasma |
| La charge fantôme donne une force similaire | Effet purement thermique |

### Matrice décisionnelle

```
  Nixie symétriques?  ──OUI──→  Force mesurée?  ──NON──→  NULL (conforme)
          │                          │
         NON                        OUI
          │                          │
          ▼                          ▼
  Gradient visible  ──→  ARTEFACT probable (force sans
          │                gradient = cause mécanique/EM)
          │
          ▼
  Gradient corrèle
  avec direction force?  ──NON──→  Coïncidence ou artefact
          │
         OUI
          │
          ▼
  Inversion 180° OK?  ──NON──→  Artefact directionnel
          │
         OUI
          │
          ▼
  Argon négatif?  ──NON──→  Effet non spécifique au H₂O
          │
         OUI
          │
          ▼
  ✅ CANDIDAT POUR EFFET BOHMIEN
     → Publier + inviter réplication indépendante
```

---

## Références

1. **Tajmar, M. et al.** (2007). « Measurement of Gravitomagnetic and
   Acceleration Fields Around Rotating Superconductors ».
   *AIP Conference Proceedings*, 880, 1071.
   (Méthodologie de mesure de forces faibles et élimination des biais.)

2. **White, H. et al.** (2017). « Measurement of Impulsive Thrust from
   a Closed Radio-Frequency Cavity in Vacuum ». *Journal of Propulsion
   and Power*, 33(4), 830–841.
   [doi:10.2514/1.B36120](https://doi.org/10.2514/1.B36120)

3. **Cavendish, H.** (1798). « Experiments to Determine the Density of
   the Earth ». *Philosophical Transactions of the Royal Society*, 88,
   469–526.
   (Méthodologie du pendule de torsion et calibration.)

4. **Quinn, T. J. et al.** (2001). « A New Determination of $G$ Using
   Two Independent Methods ». *Physical Review Letters*, 87(11).
   [doi:10.1103/PhysRevLett.87.111101](https://doi.org/10.1103/PhysRevLett.87.111101)
   (Techniques modernes de balance de torsion.)

5. **Benvenuti, S.** (2013). « Systematic Effects in Torsion Balance
   Experiments ». Thèse de doctorat, University of Washington.
   (Catalogue complet des effets systématiques.)

6. **Crookes, W.** (1874). « On Attraction and Repulsion Resulting from
   Radiation ». *Philosophical Transactions of the Royal Society*,
   164, 501–527.
   [doi:10.1098/rstl.1874.0015](https://doi.org/10.1098/rstl.1874.0015)
   (Radiomètre de Crookes — forces thermiques parasites.)

7. **Oppenheim, A. V. & Willsky, A. S.** (1997). *Signals and Systems*.
   2ᵉ édition, Prentice Hall. ISBN 978-0-138-14104-0.
   (Corrélation croisée, filtrage, analyse fréquentielle.)

8. **Fisher, R. A.** (1925). *Statistical Methods for Research Workers*.
   Oliver & Boyd.
   (Fondements des tests de significativité statistique, seuil 3σ.)

---

[← Configuration Matérielle](03_materiel.md) · [Section suivante : Notes de Sécurité →](05_securite.md)
