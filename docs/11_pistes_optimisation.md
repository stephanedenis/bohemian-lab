# 🔧 Pistes d'Optimisation de la Qualité du Plasma

[← Retour au README](../README.md) · [← Implications](07_implications.md)

---

## Résumé exécutif

La force bohmienne mesurable au pendule dépend de la **qualité** du
plasma — c'est-à-dire de la stabilité, de l'homogénéité contrôlable
et de la raideur des gradients de $n_e$. Six pistes d'optimisation
sont identifiées, classées ici de la plus immédiate à la plus
spéculative. Trois d'entre elles sont réalisables **en Phase 1**
avec le matériel actuel ou un investissement < 50 $ :

| # | Piste | Phase | Coût | Impact sur $\eta$ |
|:--|:------|:-----:|:----:|:------------------|
| 1 | [Revêtement cuivre de la cavité](#1-revêtement-cuivre-de-la-cavité) | **1** | **~10 $** | $Q \times 4{,}5$ → phase cumulée ×4,5 |
| 2 | [Architecture inverter](#2-architecture-inverter) | **1** | ~20 $ | $\delta n_e / n_e$ ÷ 30–50× |
| 3 | [Capteur spectral AS7343](#3-capteur-spectral-as7343) | **1** | ~22 $ | PID spectral → stabilité ↑↑ |
| 4 | [Résonance exacte à la coupure](#4-résonance-exacte-à-la-coupure) | 1–2 | ~0 $ | $\nabla n$ diverge à $\omega_p = \omega$ |
| 5 | [Superposition multimode](#5-superposition-multimode) | 2 | ~0 $ | $\nabla^2 R / R$ ×3–10 |
| 6 | [Gradient abrupt — champ magnétique axial](#6-gradient-abrupt--champ-magnétique-axial) | 2–3 | ~50–200 $ | $\nabla^2 R / R$ ×10–100 |
| 7 | [Non-équilibre quantique profond](#7-non-équilibre-quantique-profond) | 3+ | > 500 $ | Inconnu (spéculatif) |

Les trois premières pistes sont déjà documentées en détail dans leurs
documents dédiés. Ce document les résume et développe les pistes 4–7.

---

## 1. Revêtement cuivre de la cavité

### Le problème

La cavité cylindrique en acier inoxydable 304 a un facteur de qualité
relativement bas à cause de la faible conductivité de l'inox :

$$R_s = \sqrt{\frac{\omega \mu_0}{2 \sigma}} \quad \Rightarrow \quad
Q \propto \frac{1}{R_s} \propto \sqrt{\sigma}$$

| Matériau | $\sigma$ (S/m) | $\delta$ à 2,45 GHz | $R_s$ (mΩ) | $Q$ estimé |
|:---------|:--------------:|:-------------------:|:-----------:|:----------:|
| **Inox 304** (actuel) | $1{,}4 \times 10^6$ | 8,6 µm | 83 | **~280** |
| **Cuivre** | $5{,}8 \times 10^7$ | 1,3 µm | 13 | **~1 800** |
| Aluminium | $3{,}5 \times 10^7$ | 1,7 µm | 17 | ~1 400 |

Le facteur de qualité gouverne le **nombre de traversées** du plasma
par chaque photon piégé dans la cavité. Chaque traversée accumule de
la phase $\Delta S$ dans le potentiel quantique. Avec $Q \approx 280$
(inox brut), le photon moyen ne fait que ~280 allers-retours. Avec
$Q \approx 1\,800$ (cuivre), il en fait ~1 800 — la phase cumulée
est multipliée par le même facteur.

### La solution : feuille de cuivre autoadhésive

On n'a **pas besoin** de remplacer la chambre par une cavité en cuivre
massif. Il suffit de tapisser l'intérieur de la chambre inox avec de
la **feuille de cuivre autoadhésive** (ruban EMI/blindage) :

#### Pourquoi ça marche

Les courants RF circulent dans l'**épaisseur de peau** $\delta$ à la
surface du conducteur. À 2,45 GHz, $\delta_{\text{Cu}} = 1{,}34$ µm.
Une feuille de cuivre standard de **35 µm** d'épaisseur représente :

$$\frac{35\;\mu\text{m}}{1{,}34\;\mu\text{m}} = \mathbf{26}\;\text{épaisseurs de peau}$$

L'atténuation à travers cette épaisseur est de ~228 dB — les
micro-ondes ne « voient » **que** le cuivre, pas l'inox en dessous.
La cavité se comporte comme si elle était en cuivre massif.

> 💡 **Analogie** — C'est exactement le principe utilisé dans l'industrie
> des guides d'ondes et des cavités résonantes : un placage de quelques
> microns de cuivre ou d'argent suffit. Ici, 35 µm est largement
> surdimensionné.

#### Facteur de qualité réaliste

Le $Q$ idéal (cuivre parfait) est ~1 800. En pratique, les **joints
entre bandes** de feuille, les **rugosités** de l'adhésif et les
**défauts de contact** réduisent le $Q$ effectif. Estimation
conservative :

$$Q_{\text{réaliste}} \approx 0{,}7 \times Q_{\text{idéal}} \approx \mathbf{1\,280}$$

$$\boxed{\frac{Q_{\text{cuivre}}}{Q_{\text{inox}}} \approx 4{,}5\times}$$

C'est un gain très significatif — et réversible (on peut retirer le
ruban cuivre pour comparer les deux régimes).

#### Spécifications du ruban

| Paramètre | Valeur |
|:---|:---|
| Produit type | Ruban cuivre EMI autoadhésif (3M 1181, Würth, générique Amazon) |
| Épaisseur cuivre | 35 µm (standard) ou 70 µm (renforcé) |
| Largeur | 50 mm typique (rouleaux de 5–20 m) |
| Adhésif | Acrylique conducteur (important !) ou non conducteur |
| Prix | **~5–15 $ CAD** pour un rouleau de 50 mm × 20 m |
| Surface à couvrir | ~2 450 cm² (paroi latérale + fond) |
| Quantité requise | ~5 m de ruban de 50 mm (une seule couche, recouvrement 12 mm) |

> ⚠️ **Adhésif conducteur obligatoire** — Utiliser du ruban avec un
> adhésif **conducteur** (conductivité à travers l'épaisseur). Sinon,
> les recouvrements entre bandes créent des discontinuités de courant
> de surface → pertes et réduction du $Q$. Les rubans 3M 1181 et 1182
> ont un adhésif acrylique conducteur.

#### Protocole de pose

1. **Nettoyer** l'intérieur de la chambre inox (acétone → isopropanol).
2. **Appliquer** les bandes de ruban cuivre verticalement sur la paroi
   latérale, avec un **recouvrement ≥ 12 mm** ($\lambda/10$) entre
   bandes adjacentes. Lisser avec un chiffon ou une raclette.
3. **Fond** : appliquer des bandes en étoile ou en spirale, avec
   recouvrement. Le fond n'a pas besoin d'être aussi soigné (densité
   de courant plus faible pour les modes TM$_{mn0}$).
4. **Ne pas couvrir le couvercle** — il est déjà protégé par le grillage
   Faraday (cuivre ou inox, maille < 12 mm).
5. **Tubes Nixie IN-13** : coller les tubes **par-dessus** le cuivre.
   Les broches sont mises à la masse — elles font contact avec le
   cuivre maintenant, ce qui est correct (la masse de la cavité est
   la surface interne).
6. **Vérifier** l'absence de bulles d'air et de déchirures. Les gaps
   > 6 mm ($\lambda/20$) dégradent le $Q$.

#### Compatibilité avec le vide et le plasma

| Préoccupation | Analyse | Verdict |
|:---|:---|:---|
| **Dégazage de l'adhésif** sous vide | À 2–5 mbar, l'adhésif acrylique a un taux de dégazage très faible. Le plasma est dominé par H₂O injectée. | ✅ Acceptable |
| **Sputtering du cuivre** par le plasma | Le sputtering est significatif pour des ions > 50 eV. Dans un plasma H₂O à 2–5 mbar, $T_i \approx 0{,}05$ eV → sputtering négligeable | ✅ Négligeable |
| **Oxydation du cuivre** | La vapeur d'eau à haute température forme CuO en surface. À 2–5 mbar et ~50 °C (paroi), très lent | ⚠️ Brunissement après ~100 h — cosmétique |
| **Tenue thermique** | Adhésif acrylique stable jusqu'à ~150 °C. Paroi < 100 °C en fonctionnement normal | ✅ OK |
| **Masse ajoutée** | 35 µm × 0,245 m² × 8 900 kg/m³ ≈ **76 g** | ✅ Négligeable vs. 5 kg |

#### Impact sur la bande passante

Un $Q$ plus élevé signifie une cavité **plus sélective** en fréquence :

$$\Delta f = \frac{f}{Q}$$

| Configuration | $Q$ | $\Delta f$ (MHz) | Compatible magnétron ? |
|:---|:---|:---|:---|
| Inox brut | 280 | 8,6 | ✅ (largeur magnétron ~10–50 MHz) |
| **Cuivre (réaliste)** | **1 280** | **1,9** | ✅ **Oui** — le magnétron est verrouillé par le plasma (*injection locking*) |

Le magnétron est un oscillateur qui se **verrouille** sur la fréquence
de résonance de la cavité chargée (plasma inclus). Avec un $Q$ de 1 280,
la bande de capture du *injection locking* est encore ~2 MHz, largement
suffisante pour accrocher le magnétron. Voir Pozar [1], chap. 12.

#### Verdict

$$\boxed{Q \approx 280 \;\xrightarrow{\text{feuille cuivre 35 µm}}\;
Q \approx 1\,280 \quad (+350\,\%) \quad \text{pour} \sim 10\;\text{CAD et 1 h de travail}}$$

**C'est l'optimisation au meilleur rapport coût/impact du projet.**
Réversible, non destructive, compatible vide et plasma. À faire
**avant** la Phase 1.

---

## 2. Architecture inverter

> 📖 **Documentation complète** :
> [09_hypothese_inverter.md](09_hypothese_inverter.md)

### Résumé

Remplacer l'alimentation MOT classique (transfo 50/60 Hz + SSR) par
un **convertisseur haute fréquence** (SMPS 20–50 kHz) récupéré d'un
four micro-ondes inverter (Panasonic). L'inverter permet une
**modulation continue** de la puissance RF au lieu du bang-bang SSR.

### Impact sur la qualité du plasma

| Métrique | MOT + SSR | Inverter | Gain |
|:---|:---|:---|:---|
| Fluctuation $\delta n_e / n_e$ | ~30–50 % | **< 1 %** | **÷ 30–50×** |
| Ripple de $P_{\text{RF}}$ | 37,6 W (σ) | 1,9 W (σ) | ÷ 20× |
| $P_{\text{crête}} = P_{\text{moy}}$ ? | Non (bang-bang) | **Oui** | Nixie préservés |
| Masse alim. HV | 3,85 kg | 1,25 kg | −2,6 kg |

Le plasma atteint un **vrai état stationnaire** au lieu d'osciller
entre sur-ionisation (phase ON) et sous-ionisation (phase OFF).
Le gradient $\nabla S$ est propre → le signal de force n'est plus
contaminé par les pulsations du plasma.

### Coût et complexité

~20 $ (four usagé) + reverse-engineering du connecteur de commande.
Voir le [plan d'action détaillé](09_hypothese_inverter.md#6-plan-daction).

---

## 3. Capteur spectral AS7343

> 📖 **Documentation complète** :
> [10_capteur_spectral.md](10_capteur_spectral.md)

### Résumé

Ajouter un capteur multi-spectral 14 canaux (ams-OSRAM AS7343) sur
le bus I²C de l'ESP32 pour fournir un proxy **spectralement résolu**
de $n_e$ (raie Hβ 486 nm) et $T_e$ (ratio Hα/Hβ) au lieu de la
luminosité globale de la caméra Wi-Fi.

### Impact sur la qualité du plasma

| Aspect | Caméra Wi-Fi (actuel) | AS7343 |
|:---|:---|:---|
| Grandeur mesurée | Luminosité globale ($\propto n_e^2$) | **Intensité Hβ** ($\propto n_e$) |
| Spécificité | Intègre tout (plasma + parasites) | **Sélectif** (raie isolée) |
| Proxy $T_e$ | Non | **Oui** (ratio Hα/Hβ) |
| Boucle PID | PID₂ (luminosité) | PID₂ amélioré + PID₄ optionnel ($T_e$) |

Le PID spectral stabilise le plasma à un point de fonctionnement
plus précis et détecte les dérives de $T_e$ — invisible à la caméra.

### Coût

~22 $ (breakout SparkFun SEN-23220 Qwiic). Un seul capteur suffit
(pas besoin de combiner avec l'AS7331 UV).

---

## 4. Résonance exacte à la coupure

### Principe physique

La force bohmienne est proportionnelle au **gradient de phase**
$\nabla S$ accumulée par l'onde RF dans le plasma. L'indice de
réfraction du plasma est :

$$n = \sqrt{1 - \frac{\omega_p^2}{\omega^2}}
    = \sqrt{1 - \frac{n_e}{n_{e,c}}}$$

À la **coupure** ($n_e = n_{e,c}$), l'indice s'annule ($n \to 0$)
et son gradient diverge :

$$\nabla n \;\xrightarrow{n_e \to n_{e,c}}\; -\infty$$

La transition propagation/réflexion (zone de coupure) est alors
concentrée dans une couche mince (~mm) où $\nabla^2 R / R$ est
maximal → $Q$ (potentiel quantique) maximal → force bohmienne
maximale.

### Situation actuelle

Le PID₁ (§6.5.1) vise déjà $P_r$ minimal → résonance cavity-plasma
→ $n_e \approx n_{e,c}$. Mais la cadence de 100 Hz et la résolution
du SSR (bang-bang, 10 Hz) limitent la **durée** pendant laquelle le
plasma reste exactement à la coupure.

### Améliorations possibles

| Amélioration | Mécanisme | Difficulté | Phase |
|:---|:---|:---|:---|
| **Inverter** (piste 2) | Élimine les oscillations ON/OFF → le plasma reste à la coupure en continu | Moyenne | **1** |
| **AS7343** (piste 3) | Le proxy Hβ est plus sensible aux dérives de $n_e$ que $P_r$ → réaction plus fine | Faible | **1** |
| **PID sur FPGA** | Boucle à 10 kHz au lieu de 100 Hz → temps de réponse ÷ 100 | Élevée | 2–3 |
| **Lock-in spectral** | Modulation de $P_{\text{RF}}$ à ~1 kHz + démodulation synchrone de Hβ → détection ultra-sensible de $\delta n_e$ | Élevée | 3 |

> 💡 **Les pistes 1–3 cumulées** (cuivre + inverter + AS7343) sont
> probablement suffisantes pour maintenir la coupure avec une
> précision $\delta n_e / n_{e,c} < 1\%$. Le FPGA et le lock-in
> ne sont pertinents que si les résultats Phase 1 le justifient.

### Effet sur le potentiel quantique

À la coupure exacte, le profil radial de $n_e$ passe par la valeur
critique. La largeur de la **zone de transition** entre propagation
et réflexion détermine la raideur de $\nabla Q$ :

| $n_e / n_{e,c}$ | Largeur de transition | $|\nabla Q|$ relatif |
|:---|:---|:---|
| 0,7 | ~100 mm (étalé) | 1× (référence) |
| 0,9 | ~50 mm | ~3× |
| **1,0** (coupure) | **~10–30 mm** | **~10–30×** |
| > 1,0 (surcritique) | Réflexion abrupte, < 10 mm | > 30× |

La simulation [003_profil_plasma.py](../experiments/003_profil_plasma.py)
montre cette dépendance : la force bohmienne croît **très fortement**
quand $n_e$ approche $n_{e,c}$ (cf. scan d'asymétrie, fig. 4).

---

## 5. Superposition multimode

### Principe physique

Le champ EM dans la cavité n'est pas un mode pur TM₃₁₀ — le magnétron
a une **largeur spectrale** $\Delta f \sim 10$–50 MHz qui excite
plusieurs modes simultanément. D'après le
[calcul des modes propres](../experiments/002_modes_cavite.py), les
modes proches de 2,45 GHz sont :

| Mode | Fréquence (GHz) | Écart (MHz) |
|:---|:---|:---|
| TM₃₁₀ | 2,44 | −10 |
| TM₁₂₀ | 2,68 | +230 |
| TE₅₁₁ | 2,70 | +250 |
| TE₂₁₁ | 2,10 | −350 |

Seul le TM₃₁₀ est dans la bande du magnétron. Mais si le $Q$ de la
cavité augmente (piste 1), les modes deviennent plus étroits et
**mieux séparés** — le TM₃₁₀ est excité plus proprement.

### Comment ça aide la force bohmienne

La superposition de 2+ modes proches crée des **battements spatiaux**
— des variations rapides de l'amplitude $R(\mathbf{r})$ à l'échelle
de quelques mm. Le potentiel quantique est sensible à la **courbure**
de $R$ :

$$Q = -\frac{\hbar^2}{2m}\frac{\nabla^2 R}{R}$$

Des variations spatiales rapides (petite échelle) produisent un
$\nabla^2 R / R$ bien plus grand qu'un profil lisse — et donc un
$\nabla Q$ plus intense. Le [modèle 3D](../experiments/009_plasma_3d.py)
montre que l'ajout du mode TM₃₁₁ ($p = 1$, variation axiale) au
TM₃₁₀ structure déjà le champ verticalement.

### Levier d'action

| Méthode | Principe | Phase |
|:---|:---|:---|
| **Largeur spectrale du magnétron** | Le magnétron excite naturellement les modes dans sa bande. Pas de contrôle. | 1 (passif) |
| **Géométrie de l'iris** | La position, la taille et la forme de l'iris favorisennt certains modes. Ajustable. | 1–2 |
| **Cavité à géométrie perturbée** | Insérer un petit obstacle conducteur (vis inox) qui brise la symétrie → couplage entre modes normalement orthogonaux | 2 |
| **Source RF à état solide** | Remplacer le magnétron par un amplificateur RF (LDMOS, 200 W, ~300 $) piloté par un VCO. Balayer la fréquence pour exciter sélectivement plusieurs modes. | 3 |

> 💡 La méthode la plus simple est l'**iris ajustable** : une fenêtre
> de taille et position variable dans le grillage Faraday. En Phase 1,
> on peut déjà tester différentes positions de l'iris et observer
> l'effet sur la carte Nixie (symétrie vs. asymétrie du champ).

### Gain estimé

Avec 2 modes d'amplitude comparable (battement spatial ~$\lambda/4$
≈ 30 mm) :

$$\frac{|\nabla^2 R / R|_{\text{bimode}}}{|\nabla^2 R / R|_{\text{monomode}}}
\approx 3\text{–}10\times$$

Ce gain est cumulatif avec celui de la coupure exacte (piste 4).

---

## 6. Gradient abrupt — Champ magnétique axial

### Principe physique

La distribution de $n_e$ dans un plasma non magnétisé est un profil
gaussien lisse (largeur ~60 % du rayon). Un **champ magnétique
statique axial** ($B_0 \sim 50$–200 G) confine les électrons autour
des lignes de champ, créant des structures spatiales fines :

- **Filaments de plasma** (instabilité de filamentation),
- **Stries de ionisation** (instabilité de Rayleigh-Taylor plasma),
- **Colonne de plasma** étroite le long de l'axe.

Ces structures ont des échelles caractéristiques de quelques mm,
bien plus petites que le profil gaussien uniforme. Le $\nabla^2 R / R$
est amplifié de ×10–100 dans les zones de transition abrupte.

### Réalisation pratique

| Option | Principe | Champ (G) | Masse | Coût |
|:---|:---|:---|:---|:---|
| **A. Aimants permanents** | Aimants NdFeB (⌀ 25 mm × 10 mm) empilés sous le fond de la chambre | 50–100 | ~200 g | ~20 $ |
| **B. Bobine de Helmholtz** | Paire de bobines (⌀ 300 mm, 100 tours, 2 A) de part et d'autre de la chambre | 50–200 | ~1 kg | ~50 $ |
| **C. Solénoïde** | Enroulé autour de la chambre (200 tours, ⌀ cuivre 1 mm) | 100–300 | ~0,5 kg | ~30 $ |

> ⚠️ **Impact sur le pendule** — Toute masse magnétique ajoutée doit
> être compensée par le contrepoids. Un solénoïde ou des aimants
> créent aussi un **champ B externe** qui peut interagir avec les
> matériaux ferromagnétiques du MOT ou de l'onduleur côté contrepoids.
> Prévoir un blindage magnétique (µ-métal) si nécessaire.

### Interaction champ B × micro-ondes

Le champ magnétique modifie la **fréquence cyclotron** des électrons :

$$f_{ce} = \frac{eB}{2\pi m_e} = 2{,}80 \times B \;\text{(MHz, avec $B$ en gauss)}$$

| $B$ (G) | $f_{ce}$ (MHz) | Rapport $f_{ce} / f$ |
|:---|:---|:---|
| 50 | 140 | 0,057 |
| 100 | 280 | 0,114 |
| 200 | 560 | 0,229 |
| **875** | **2 450** | **1,000** (résonance cyclotron !) |

À 875 G, $f_{ce} = f$ — c'est la **résonance cyclotron électronique**
(ECR). L'absorption des micro-ondes par le plasma est maximale. Mais
875 G nécessiterait un électroaimant puissant (~5 kg, ~200 W).

Pour la Phase 2, des champs modérés (**50–200 G**) suffisent à
structurer le plasma sans atteindre l'ECR. L'ECR resterait une piste
Phase 3 avec un électroaimant dédié.

### Diagnostics

Le champ B modifie la carte Nixie : les 8 tubes ne verront plus un
gradient azimutal lisse mais des **structures fines** (filaments,
asymétrie renforcée). La caméra Wi-Fi et l'AS7343 doivent confirmer
que la structuration est réelle et non un artefact de saturation.

### Phase et risques

| Critère | Évaluation |
|:---|:---|
| Phase | **2–3** (après validation Phase 1 sans champ B) |
| Coût | 20–200 $ selon l'option |
| Masse ajoutée | 0,2–1 kg (à compenser) |
| Risque principal | Couplage magnétique parasite avec le MOT/onduleur |
| Gain potentiel | $\nabla^2 R / R$ ×10–100 dans les zones de transition |

---

## 7. Non-équilibre quantique profond

### Principe théorique

Dans la mécanique de de Broglie–Bohm, la condition d'*équilibre
quantique* est $\rho = |\psi|^2$. Valentini (1991, 2002) montre que
si $\rho \neq |\psi|^2$, les prédictions de dBB **divergent** de la
MQ standard. Colin & Struyve (2007) estiment un temps de relaxation
$\tau_{\text{relax}}$ vers l'équilibre — si le système est perturbé
plus vite que $\tau_{\text{relax}}$, le non-équilibre est maintenu.

### Application au plasma

Un plasma micro-onde pulsé à une fréquence $f_{\text{pulse}} >
1 / \tau_{\text{relax}}$ pourrait maintenir un état de non-équilibre
quantique permanent. La question est : quel est $\tau_{\text{relax}}$
dans un plasma H₂O ?

| Régime de pulsation | Technologie | $f_{\text{pulse}}$ | Difficulté |
|:---|:---|:---|:---|
| SSR classique | SSR passage par zéro | ~10 Hz | Déjà disponible |
| Inverter | SMPS, modulation PWM | ~kHz–10 kHz | Phase 1 |
| **RF pulsée nanoseconde** | Source à état solide (GaN HEMT) | **~MHz–GHz** | **Phase 3+** |

### Faisabilité

Les sources RF à état solide (amplificateurs GaN) capables de produire
des pulses nanoseconde à 2,45 GHz existent sur le marché (utilisées en
accélérateurs de particules, médecine, radar). Leur coût est > 500 $
pour 200 W de puissance crête, et l'intégration avec la cavité
nécessite un redesign complet de l'alimentation.

### Verdict

Cette piste est **hautement spéculative** — on ne connaît pas
$\tau_{\text{relax}}$ pour un plasma macroscopique, et il n'est pas
certain qu'il soit accessible avec des technologies actuelles. Elle
n'est pertinente que si les résultats Phase 1 montrent un signal
positif qu'on cherche à amplifier.

| Critère | Évaluation |
|:---|:---|
| Phase | **3+** (post-publication) |
| Coût | > 500 $ (source GaN + driver) |
| Fondement théorique | Valentini (1991, 2002), Colin & Struyve (2007) |
| Gain potentiel | **Inconnu** — pourrait être le facteur décisif ou nul |
| Risque | Très élevé — piste exploratoire pure |

---

## 8. Synthèse — Ordre d'implémentation

### Phase 1 : les « quick wins » (< 50 $ total)

Ces trois optimisations sont **cumulatives** et réalisables avant le
premier allumage du plasma :

```
  ┌──────────────────────────────────────────────────────┐
  │  PHASE 1 — Optimisations pré-expérience (~50 $)       │
  │                                                        │
  │  1. Feuille cuivre intérieure (~10 $, 1 h)             │
  │     → Q ×4,5 → phase cumulée ×4,5                     │
  │                                                        │
  │  2. Inverter (~20 $, reverse-eng.)                     │
  │     → δn_e/n_e ÷ 30–50× → plasma stationnaire         │
  │                                                        │
  │  3. AS7343 (~22 $, I²C plug & play)                    │
  │     → PID spectral → stabilité Hβ/Hα                  │
  │                                                        │
  │  4. Coupure exacte (0 $, firmware PID)                 │
  │     → Bénéfice automatique des pistes 2+3              │
  └──────────────────────────────────────────────────────┘
```

**Impact cumulé estimé** sur la force bohmienne mesurable :

$$\eta_{\text{effectif}} \approx \eta_{\text{intrinsèque}} \times
\underbrace{Q / Q_0}_{\text{cuivre}} \times
\underbrace{\frac{1}{1 + (\delta n_e / n_e)^2}}_{\text{inverter}} \times
\underbrace{f(\text{PID}_{\text{spectral}})}_{\text{AS7343}}$$

Avec les valeurs Phase 1 :
- Cuivre : $Q / Q_0 = 4{,}5\times$
- Inverter : le facteur de bruit systématique passe de dominant à
  négligeable
- AS7343 + coupure : stabilisation à $n_e \approx n_{e,c}$ avec
  $\delta n_e / n_{e,c} < 1\%$

### Phase 2 : exploration systématique

| Piste | Prérequis | Action |
|:---|:---|:---|
| Multimode | Résultat Phase 1 positif | Tester 2–3 positions d'iris, documenter carte Nixie |
| Champ B axial | Résultat Phase 1 positif | Aimants NdFeB sous le fond (~20 $), observer structuration |

### Phase 3 : pistes avancées

| Piste | Prérequis | Action |
|:---|:---|:---|
| Source RF à état solide | Publication Phase 2 | Amplificateur LDMOS 200 W + VCO → balayage multimode |
| ECR (875 G) | Publication Phase 2 | Électroaimant dédié → absorption RF maximale |
| Pulsation nanoseconde | Résultat positif confirmé | Source GaN → exploration du non-équilibre quantique |

---

## 9. Tableau de coûts récapitulatif

| Piste | Phase | Coût | Masse ajoutée | Réversible ? |
|:---|:---|:---|:---|:---|
| Feuille cuivre | 1 | **~10 $** | 76 g | ✅ Oui |
| Inverter | 1 | ~20 $ | −2,6 kg (gain !) | ✅ Oui |
| AS7343 | 1 | ~22 $ | < 5 g | ✅ Oui |
| Coupure exacte (firmware) | 1 | 0 $ | 0 | ✅ Oui |
| Iris ajustable | 1–2 | ~5 $ | < 50 g | ✅ Oui |
| Aimants NdFeB | 2 | ~20 $ | ~200 g | ✅ Oui |
| Solénoïde / Helmholtz | 2–3 | ~50 $ | ~0,5–1 kg | ✅ Oui |
| Source RF état solide | 3 | ~300 $ | ~0,5 kg | ✅ Oui |
| Source GaN ns | 3+ | > 500 $ | ~0,3 kg | ✅ Oui |

> 💡 **Toutes les pistes sont réversibles** — on peut toujours revenir
> à la configuration de base (inox nu, MOT classique, caméra seule)
> pour comparer les résultats. Cette réversibilité est essentielle
> pour une démarche scientifique rigoureuse.

---

## Références

1. **Pozar, D. M.** (2012). *Microwave Engineering*. 4ᵉ édition, Wiley.
   ISBN 978-0-470-63155-3.
   (Chap. 6 : facteur de qualité des cavités résonantes ;
   chap. 12 : injection locking des oscillateurs.)

2. **Matthaei, G., Young, L. & Jones, E. M. T.** (1964). *Microwave
   Filters, Impedance-Matching Networks, and Coupling Structures*.
   McGraw-Hill. (Référence classique sur les cavités haute Q.)

3. **3M** (2020). *Technical Data Sheet — Copper Foil Tape 1181/1182*.
   Adhésif acrylique conducteur, épaisseur 35 µm, résistance < 0,005 Ω.

4. **Valentini, A.** (1991). « Signal-locality, uncertainty, and the
   subquantum H-theorem ». *Physics Letters A*, 156(1–2), 5–11.

5. **Colin, S. & Struyve, W.** (2007). « Quantum non-equilibrium and
   relaxation to quantum equilibrium for a class of de Broglie–Bohm-type
   theories ». *New Journal of Physics*, 9, 306.

6. **Lieberman, M. A. & Lichtenberg, A. J.** (2005). *Principles of
   Plasma Discharges and Materials Processing*. 2ᵉ édition, Wiley.
   (Chap. 13 : ECR et plasmas magnétisés.)

7. **Chen, F. F.** (2016). *Introduction to Plasma Physics and Controlled
   Fusion*. 3ᵉ édition, Springer.
   (Chap. 5 : diffusion dans un champ magnétique, confinement.)

8. **Jackson, J. D.** (1999). *Classical Electrodynamics*. 3ᵉ édition,
   Wiley. (Chap. 8 : cavités résonantes, facteur Q, résistance de
   surface.)

---

[← Implications](07_implications.md) · [Retour au README →](../README.md)
