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

### Étape 1 — Mise sous vide

1. Assembler la chambre à vide. Vérifier l'étanchéité du joint
   silicone sur le couvercle acrylique.
2. Connecter la pompe à vide. Atteindre une pression $P < 1$ mbar.
3. Vérifier l'absence de fuites au détecteur (débit de fuite
   $< 10^{-3}$ mbar·L/s).
4. **Injection capillaire** de vapeur d'eau : ouvrir le micro-doseur
   pour atteindre $P \approx 1-5$ mbar de vapeur d'eau.

### Étape 2 — Calibration du pendule

1. Laisser le système au repos jusqu'à ce que les oscillations
   parasites soient amorties (~ 30 min).
2. Provoquer une oscillation libre en donnant une légère impulsion
   calibrée (masse connue lâchée sur un bras de levier).
3. Enregistrer la période d'oscillation $T_0$ par vidéo (minimum
   10 oscillations complètes).
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

3. Enregistrer en vidéo le déplacement du bras de torsion.
4. Enregistrer simultanément : courant du magnétron, pression de la
   chambre, luminosité du plasma (tubes Nixie), température des parois.
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

### Extraction du signal

Le signal brut $\theta(t)$ contient :

- **Signal recherché** : oscillation à la fréquence $f_0 = 1/T_0$,
  en phase avec le magnétron.
- **Bruit** : vibrations sismiques, courants d'air, bruit thermique
  du fil.
- **Dérive** : composante thermique lente.

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

| Objection | Réponse |
|:---|:---|
| « C'est du vent ionique » | Système hermétique sous vide ; test argon négatif |
| « C'est un effet thermique » | Mode pulsé + charge fantôme de contrôle |
| « C'est une force EM parasite » | Inversion 180° + blindage mu-métal |
| « La pression de radiation suffit à expliquer » | Calcul explicite de $P/c$ et comparaison avec $F_{\text{mesuré}}$ |
| « Le potentiel quantique ne s'applique pas aux photons » | Discussion théorique dans [02_theorie.md](02_theorie.md#24-application-aux-photons-rf) |
| « La mécanique bohmienne ne prédit pas cela » | Le protocole est conçu pour tester l'hypothèse, pas pour la présumer vraie |

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

---

[← Configuration Matérielle](03_materiel.md) · [Section suivante : Notes de Sécurité →](05_securite.md)
