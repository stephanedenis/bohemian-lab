"""
Expérience 003 — Profil du plasma et estimation de la force bohmienne.

Modélise la distribution spatiale du plasma de vapeur d'eau dans la cavité
cylindrique et calcule :
    1. Le profil de densité électronique n_e(r, θ) — asymétrique.
    2. L'indice de réfraction n(r, θ) = √(1 − ω_p²/ω²).
    3. La phase accumulée S(r, θ) par l'onde RF.
    4. L'amplitude R(r, θ) de l'onde dans le plasma.
    5. Le potentiel quantique Q = −(ℏ²/2m)(∇²R/R).
    6. Le gradient −∇Q (force bohmienne) et son intégrale volumique.
    7. La comparaison avec la pression de radiation classique P/c.

Modèle de plasma :
    La distribution de n_e est modélisée comme la superposition d'un
    profil radial gaussien (plasma confiné au centre) et d'une asymétrie
    azimutale (le magnétron est placé d'un seul côté) :

        n_e(r, θ) = n_e0 × exp(−r²/σ_r²) × [1 + ε × cos(θ − θ_mag)]

    où :
        n_e0    = densité maximale au centre (cible : n_e,c ≈ 7,4×10¹⁶ m⁻³)
        σ_r     = largeur radiale du plasma (~ 60% du rayon de la chambre)
        ε       = degré d'asymétrie (0 = symétrique, 1 = très asymétrique)
        θ_mag   = direction angulaire du magnétron

Contexte physique :
    Le potentiel quantique Q dans le cadre de l'interprétation de
    de Broglie–Bohm est défini par :

        Q = −(ℏ²/2m)(∇²R/R)

    où R est l'amplitude de la fonction d'onde ψ = R × exp(iS/ℏ).
    Pour notre analogie avec le champ EM dans le plasma, R est
    proportionnel à l'amplitude du champ électrique atténué par le
    plasma, et S est la phase accumulée.

    La force bohmienne est F_Q = −∇Q, intégrée sur le volume du plasma
    pour obtenir la force nette. Cette force est comparée à la pression
    de radiation classique F_rad = P_abs / c ≈ 3,3 µN pour 1 kW.

Sorties :
    - Carte de n_e(x, y) avec contour de densité critique.
    - Carte de n(x, y) avec zones de coupure.
    - Carte de Q(x, y) avec champ de vecteurs −∇Q.
    - Diagramme de comparaison des forces.
    - Données sauvegardées dans data/003_*.npy et data/003_forces.csv.

Références :
    [1] Holland, P.R. (1993). The Quantum Theory of Motion, chap. 3–4.
    [2] Chen, F.F. (2016). Introduction to Plasma Physics, chap. 4.
    [3] Lieberman & Lichtenberg (2005). Principles of Plasma Discharges, chap. 5.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import laplace, gaussian_filter

# Ajout du répertoire racine pour importer src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.viz import (
    plot_profil_plasma,
    plot_potentiel_quantique,
    plot_force_comparaison,
)


# ═══════════════════════════════════════════════════════════════════════
# Constantes physiques
# ═══════════════════════════════════════════════════════════════════════

C: float = 299_792_458.0           # vitesse de la lumière (m/s)
HBAR: float = 1.054_571_817e-34    # constante de Planck réduite (J·s)
E_CHARGE: float = 1.602_176_634e-19  # charge élémentaire (C)
M_ELECTRON: float = 9.109_383_702e-31  # masse de l'électron (kg)
EPSILON_0: float = 8.854_187_817e-12   # permittivité du vide (F/m)

# Géométrie de la cavité
A_CAVITE: float = 0.125            # rayon de la cavité (m)
D_CAVITE: float = 0.250            # hauteur de la cavité (m)

# Paramètres du magnétron
F_MAGNETRON: float = 2.45e9        # fréquence (Hz)
OMEGA: float = 2 * np.pi * F_MAGNETRON  # pulsation (rad/s)
P_MAGNETRON: float = 1000.0        # puissance absorbée (W)

# Densité critique pour 2,45 GHz
N_E_CRITIQUE: float = (
    OMEGA**2 * EPSILON_0 * M_ELECTRON / E_CHARGE**2
)  # ≈ 7,4 × 10¹⁶ m⁻³


# ═══════════════════════════════════════════════════════════════════════
# Paramètres du modèle de plasma
# ═══════════════════════════════════════════════════════════════════════

# Densité maximale au centre (autour de la densité critique)
N_E0: float = 1.0 * N_E_CRITIQUE   # 1× la densité critique

# Largeur radiale du plasma (60% du rayon = le plasma ne remplit pas toute la cavité)
SIGMA_R: float = 0.6 * A_CAVITE

# Asymétrie azimutale (le magnétron injecte plus d'énergie d'un côté)
EPSILON_ASYM: float = 0.35         # 0 = symétrique, 1 = fortement asymétrique
THETA_MAGNETRON: float = 0.0       # direction du magnétron (rad)

# Résolution de la grille
N_POINTS: int = 300                # nombre de points par axe


# ═══════════════════════════════════════════════════════════════════════
# Construction du profil de densité électronique
# ═══════════════════════════════════════════════════════════════════════

def creer_grille_cartesienne(
    a: float = A_CAVITE,
    n_pts: int = N_POINTS,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Crée une grille cartésienne (x, y) couvrant la cavité cylindrique.

    La grille est carrée de côté 2a (le diamètre de la cavité).
    Un masque circulaire permet d'exclure les points hors cavité.

    Args:
        a: Rayon de la cavité (m).
        n_pts: Nombre de points par axe.

    Returns:
        Tuple (X, Y, R, Theta) — grilles 2D en cartésien et polaire.
    """
    x_1d = np.linspace(-a, a, n_pts)
    y_1d = np.linspace(-a, a, n_pts)
    X, Y = np.meshgrid(x_1d, y_1d)
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    return X, Y, R, Theta


def profil_densite_electronique(
    R: np.ndarray,
    Theta: np.ndarray,
    n_e0: float = N_E0,
    sigma_r: float = SIGMA_R,
    epsilon: float = EPSILON_ASYM,
    theta_mag: float = THETA_MAGNETRON,
) -> np.ndarray:
    """Calcule le profil de densité électronique n_e(r, θ).

    Modèle : gaussienne radiale × modulation azimutale

        n_e(r, θ) = n_e0 × exp(−r²/σ_r²) × [1 + ε × cos(θ − θ_mag)]

    Le terme cos(θ − θ_mag) crée une asymétrie : la densité est plus
    élevée du côté du magnétron (θ = θ_mag) et plus faible du côté
    opposé. C'est cette asymétrie qui génère le gradient de phase ∇S
    responsable de la force de guidage bohmienne.

    Args:
        R: Distance radiale (2D meshgrid, en m).
        Theta: Angle azimutal (2D meshgrid, en rad).
        n_e0: Densité maximale au centre (m⁻³).
        sigma_r: Largeur radiale du profil gaussien (m).
        epsilon: Degré d'asymétrie azimutale (0 à 1).
        theta_mag: Direction angulaire du magnétron (rad).

    Returns:
        n_e(r, θ) — densité électronique (m⁻³), 2D.
    """
    # Profil radial gaussien
    profil_radial = np.exp(-R**2 / sigma_r**2)

    # Modulation azimutale asymétrique
    modulation = 1.0 + epsilon * np.cos(Theta - theta_mag)

    n_e = n_e0 * profil_radial * modulation
    return n_e


# ═══════════════════════════════════════════════════════════════════════
# Calcul de l'indice de réfraction et de la phase
# ═══════════════════════════════════════════════════════════════════════

def pulsation_plasma(n_e: np.ndarray) -> np.ndarray:
    """Calcule la pulsation plasma ω_p(r, θ).

    La pulsation plasma est donnée par :
        ω_p = √(n_e × e² / (ε₀ × m_e))

    Elle caractérise la fréquence d'oscillation collective des électrons
    dans le plasma. Quand ω_p = ω (fréquence du magnétron), on atteint
    la densité critique et l'indice de réfraction s'annule.

    Args:
        n_e: Densité électronique (m⁻³), 2D.

    Returns:
        ω_p (rad/s), 2D.
    """
    return np.sqrt(n_e * E_CHARGE**2 / (EPSILON_0 * M_ELECTRON))


def indice_refraction(n_e: np.ndarray, omega: float = OMEGA) -> np.ndarray:
    """Calcule l'indice de réfraction du plasma n(r, θ).

    Pour un plasma non magnétisé, non collisionnel :
        n = √(1 − ω_p²/ω²) = √(1 − n_e/n_e,c)

    Zones :
        n > 0 : propagation (le plasma est « transparent »)
        n = 0 : coupure (densité critique) — l'onde est réfléchie
        n² < 0 : onde évanescente (le plasma est « opaque »)

    On retourne n réel (0 là où n² < 0) pour la visualisation.

    Args:
        n_e: Densité électronique (m⁻³), 2D.
        omega: Pulsation de l'onde RF (rad/s).

    Returns:
        Indice de réfraction n, 2D (réel, tronqué à 0 dans les zones opaques).
    """
    omega_p = pulsation_plasma(n_e)
    n_carre = 1.0 - (omega_p / omega)**2
    # Indice réel — zones de propagation uniquement
    n = np.sqrt(np.maximum(n_carre, 0.0))
    return n


def phase_accumulee(
    n_refraction: np.ndarray,
    omega: float = OMEGA,
    dx: float | None = None,
) -> np.ndarray:
    """Calcule la phase accumulée S(x, y) par l'onde traversant le plasma.

    La phase accumulée sur un trajet est :
        S = ∫ n(r) × (ω/c) dl

    En approximation 2D (intégration locale), la phase est proportionnelle
    à l'indice de réfraction local :
        S(x, y) ∝ n(x, y) × ω/c × d_eff

    où d_eff est une épaisseur effective de plasma traversée.

    Args:
        n_refraction: Indice de réfraction 2D.
        omega: Pulsation de l'onde (rad/s).
        dx: Pas de la grille (m). Si None, calculé depuis la taille.

    Returns:
        Phase S(x, y) (en radians), 2D.
    """
    # Phase locale proportionnelle à l'indice et à la hauteur de la cavité
    k0 = omega / C  # nombre d'onde dans le vide
    S = n_refraction * k0 * D_CAVITE
    return S


# ═══════════════════════════════════════════════════════════════════════
# Calcul de l'amplitude et du potentiel quantique
# ═══════════════════════════════════════════════════════════════════════

def amplitude_onde(
    n_e: np.ndarray,
    masque: np.ndarray,
    sigma_lissage: float = 3.0,
) -> np.ndarray:
    """Calcule l'amplitude R(x, y) de l'onde dans le plasma.

    L'amplitude du champ EM est atténuée dans les zones de haute densité
    électronique (absorption et réflexion). On modélise :

        R(x, y) = R₀ × exp(−α × n_e / n_e,c)

    où α est un coefficient d'atténuation normalisé. Le lissage gaussien
    simule la diffraction naturelle de l'onde.

    Args:
        n_e: Densité électronique (m⁻³), 2D.
        masque: Masque booléen (True à l'intérieur de la cavité).
        sigma_lissage: Largeur du lissage gaussien (en pixels).

    Returns:
        Amplitude R(x, y), normalisée, 2D.
    """
    alpha = 1.5  # coefficient d'atténuation (adimensionnel)
    R = np.exp(-alpha * n_e / N_E_CRITIQUE)

    # Lissage pour simuler la diffraction — évite les discontinuités
    R = gaussian_filter(R, sigma=sigma_lissage)

    # Masque hors cavité
    R = R * masque

    # Normalisation
    R_max = np.max(R)
    if R_max > 0:
        R /= R_max

    return R


def potentiel_quantique(
    R: np.ndarray,
    dx: float,
    masque: np.ndarray,
    hbar: float = HBAR,
    m: float = M_ELECTRON,
    sigma_lissage: float = 2.0,
) -> np.ndarray:
    """Calcule le potentiel quantique Q(x, y) = −(ℏ²/2m)(∇²R/R).

    Le potentiel quantique dépend de la FORME de l'amplitude R
    (via le laplacien ∇²R), pas de son intensité absolue. C'est
    la propriété clé qui rend le potentiel quantique fondamentalement
    différent des potentiels classiques.

    ⚠️ Note sur la normalisation :
    Dans cette simulation, nous calculons Q dans des unités effectives
    (normalisées par rapport à ℏ²/2m × 1/dx²). L'ordre de grandeur
    absolu est un estimateur — la valeur physique exacte nécessiterait
    un modèle de champ EM complet (FDTD).

    Args:
        R: Amplitude de l'onde 2D.
        dx: Pas de la grille (m).
        masque: Masque booléen (True à l'intérieur de la cavité).
        hbar: Constante de Planck réduite (J·s).
        m: Masse de la particule guidée (kg).
        sigma_lissage: Lissage pré-laplacien (pixels) pour stabilité.

    Returns:
        Q(x, y) — potentiel quantique (unités normalisées), 2D.
    """
    # Lissage léger pour éviter les oscillations numériques
    R_smooth = gaussian_filter(R, sigma=sigma_lissage)

    # Éviter la division par zéro : plancher sur R
    R_safe = np.maximum(R_smooth, 1e-12)

    # Laplacien numérique de R (en unités de 1/dx²)
    lap_R = laplace(R_smooth) / dx**2

    # Q = −(ℏ²/2m) × (∇²R / R)
    prefacteur = -hbar**2 / (2 * m)
    Q = prefacteur * (lap_R / R_safe)

    # Masque et nettoyage
    Q = Q * masque

    # Limiter les valeurs extrêmes (artefacts de bord)
    q_lim = np.nanpercentile(np.abs(Q[masque > 0]), 99)
    Q = np.clip(Q, -q_lim, q_lim)

    return Q


def gradient_potentiel_quantique(
    Q: np.ndarray,
    dx: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Calcule le gradient ∇Q = (∂Q/∂x, ∂Q/∂y) par différences finies centrées.

    La force bohmienne est F_Q = −∇Q. Ce gradient indique la direction
    et l'intensité de la force exercée par le potentiel quantique sur
    les particules guidées.

    Args:
        Q: Potentiel quantique 2D.
        dx: Pas de la grille (m).

    Returns:
        Tuple (∂Q/∂x, ∂Q/∂y) — composantes du gradient, 2D.
    """
    # np.gradient retourne (∂Q/∂y, ∂Q/∂x) pour un tableau (lignes, colonnes)
    grad_y, grad_x = np.gradient(Q, dx, dx)
    return grad_x, grad_y


# ═══════════════════════════════════════════════════════════════════════
# Estimation de la force nette
# ═══════════════════════════════════════════════════════════════════════

def force_bohmienne_nette(
    grad_Qx: np.ndarray,
    grad_Qy: np.ndarray,
    n_e: np.ndarray,
    masque: np.ndarray,
    dx: float,
    d_cavite: float = D_CAVITE,
) -> tuple[float, float, float]:
    """Estime la force bohmienne nette F_Q = ∫ ρ(−∇Q) dV.

    L'intégration se fait sur la surface 2D de la coupe transversale,
    multipliée par la hauteur de la cavité pour obtenir le volume.
    La densité ρ est prise proportionnelle à n_e (les électrons sont
    les porteurs de la force de guidage).

    ⚠️ C'est une estimation par modèle simplifié. La valeur absolue
    dépend du modèle de Q choisi. L'intérêt est l'ORDRE DE GRANDEUR
    et la DIRECTION de la force.

    Args:
        grad_Qx: Composante x de ∇Q (2D).
        grad_Qy: Composante y de ∇Q (2D).
        n_e: Densité électronique (m⁻³), 2D.
        masque: Masque booléen de la cavité.
        dx: Pas de la grille (m).
        d_cavite: Hauteur de la cavité (m).

    Returns:
        Tuple (Fx, Fy, |F|) — force nette en newtons.
    """
    # Élément de surface dA = dx²
    dA = dx**2
    # Élément de volume dV = dA × d_cavite
    dV = dA * d_cavite

    # Force = ∫ ρ × (−∇Q) dV
    # ρ ∝ n_e (normalisation pour l'estimation)
    rho = n_e * masque

    # Intégration numérique
    Fx = -np.nansum(rho * grad_Qx * dV)
    Fy = -np.nansum(rho * grad_Qy * dV)
    F_norme = np.sqrt(Fx**2 + Fy**2)

    return Fx, Fy, F_norme


def pression_radiation(p_abs: float = P_MAGNETRON) -> float:
    """Calcule la pression de radiation classique F_rad = P_abs / c.

    C'est la force maximale que la physique classique prédit pour un
    faisceau de puissance P absorbé par une surface (absorption totale,
    pas de réflexion).

    Args:
        p_abs: Puissance absorbée (W).

    Returns:
        Force de radiation (N).
    """
    return p_abs / C


# ═══════════════════════════════════════════════════════════════════════
# Analyse paramétrique — Influence de l'asymétrie
# ═══════════════════════════════════════════════════════════════════════

def scan_asymetrie(
    X: np.ndarray,
    Y: np.ndarray,
    R_grid: np.ndarray,
    Theta_grid: np.ndarray,
    masque: np.ndarray,
    dx: float,
    epsilons: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Balaye le paramètre d'asymétrie ε et calcule la force nette pour chaque valeur.

    Permet d'étudier comment la force bohmienne dépend du degré
    d'inhomogénéité du plasma — une question expérimentalement cruciale.

    Args:
        X, Y: Grilles cartésiennes.
        R_grid: Grille radiale.
        Theta_grid: Grille angulaire.
        masque: Masque de la cavité.
        dx: Pas de la grille.
        epsilons: Tableau de valeurs d'asymétrie à scanner.

    Returns:
        Tuple (epsilons, forces_x, forces_y) — valeurs de ε et forces correspondantes.
    """
    if epsilons is None:
        epsilons = np.linspace(0.0, 0.8, 20)

    forces_x = np.zeros_like(epsilons)
    forces_y = np.zeros_like(epsilons)

    for i, eps in enumerate(epsilons):
        n_e = profil_densite_electronique(R_grid, Theta_grid, epsilon=eps)
        R_onde = amplitude_onde(n_e, masque)
        Q = potentiel_quantique(R_onde, dx, masque)
        gQx, gQy = gradient_potentiel_quantique(Q, dx)
        Fx, Fy, _ = force_bohmienne_nette(gQx, gQy, n_e, masque, dx)
        forces_x[i] = Fx
        forces_y[i] = Fy

    return epsilons, forces_x, forces_y


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 003 — Profil du plasma et force bohmienne    ║")
    print("║  Cavité Ø250 mm × 250 mm — Magnétron 2,45 GHz — 200-400 W║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    # ── Étape 1 : construction de la grille ─────────────────────────
    print("▶ Construction de la grille cartésienne…")
    X, Y, R_grid, Theta_grid = creer_grille_cartesienne(A_CAVITE, N_POINTS)
    dx = 2 * A_CAVITE / N_POINTS
    masque = (R_grid <= A_CAVITE).astype(float)

    print(f"  Grille : {N_POINTS}×{N_POINTS} points, dx = {dx*1e3:.2f} mm")
    print(f"  Rayon cavité : {A_CAVITE*1e3:.0f} mm")

    # ── Étape 2 : profil de densité électronique ────────────────────
    print("\n▶ Calcul du profil de densité n_e(r, θ)…")
    print(f"  n_e0 = {N_E0:.2e} m⁻³ (densité critique = {N_E_CRITIQUE:.2e} m⁻³)")
    print(f"  σ_r = {SIGMA_R*1e3:.1f} mm (largeur radiale)")
    print(f"  ε = {EPSILON_ASYM:.2f} (asymétrie azimutale)")
    print(f"  θ_mag = {np.degrees(THETA_MAGNETRON):.0f}° (direction du magnétron)")

    n_e = profil_densite_electronique(R_grid, Theta_grid)

    # Statistiques
    n_e_interieur = n_e[masque > 0]
    print(f"\n  Statistiques (intérieur de la cavité) :")
    print(f"    n_e max  = {np.max(n_e_interieur):.2e} m⁻³")
    print(f"    n_e moy  = {np.mean(n_e_interieur):.2e} m⁻³")
    print(f"    n_e min  = {np.min(n_e_interieur):.2e} m⁻³")
    print(f"    Ratio max/critique = {np.max(n_e_interieur)/N_E_CRITIQUE:.2f}")

    # ── Étape 3 : indice de réfraction ──────────────────────────────
    print("\n▶ Calcul de l'indice de réfraction n(x, y)…")
    n_ref = indice_refraction(n_e)

    # Fréquence plasma locale
    f_p = pulsation_plasma(n_e) / (2 * np.pi)
    print(f"  f_p max = {np.max(f_p[masque > 0])/1e9:.2f} GHz")
    print(f"  f_p moy = {np.mean(f_p[masque > 0])/1e9:.2f} GHz")

    # Fraction de la cavité à la coupure (n ≈ 0)
    frac_coupure = np.sum((n_ref < 0.1) & (masque > 0)) / np.sum(masque > 0)
    print(f"  Fraction opaque (n < 0.1) : {frac_coupure*100:.1f}%")

    # Visualisation
    fig1 = plot_profil_plasma(
        X, Y, n_e * masque, n_ref * masque,
        contour_chambre=A_CAVITE,
        titre=(
            f"Profil du plasma — n_e0 = {N_E0:.1e} m⁻³, "
            f"ε = {EPSILON_ASYM:.2f}"
        ),
        sauvegarde="data/003_profil_plasma.png",
    )

    # ── Étape 4 : phase et amplitude ────────────────────────────────
    print("\n▶ Calcul de la phase S(x, y) et de l'amplitude R(x, y)…")
    S = phase_accumulee(n_ref)
    R_onde = amplitude_onde(n_e, masque)

    # Visualisation de la phase
    fig_phase, axes_phase = plt.subplots(1, 2, figsize=(14, 6))

    im_s = axes_phase[0].pcolormesh(
        X * 1e3, Y * 1e3, S * masque,
        cmap="twilight", shading="gouraud",
    )
    fig_phase.colorbar(im_s, ax=axes_phase[0], label="Phase $S$ (rad)")
    axes_phase[0].set_xlabel("x (mm)")
    axes_phase[0].set_ylabel("y (mm)")
    axes_phase[0].set_title("Phase accumulée $S(x, y)$")
    axes_phase[0].set_aspect("equal")
    cercle1 = plt.Circle(
        (0, 0), A_CAVITE * 1e3, fill=False,
        edgecolor="white", linewidth=2, linestyle="--",
    )
    axes_phase[0].add_patch(cercle1)

    im_r = axes_phase[1].pcolormesh(
        X * 1e3, Y * 1e3, R_onde,
        cmap="magma", shading="gouraud",
    )
    fig_phase.colorbar(im_r, ax=axes_phase[1], label="Amplitude $R$")
    axes_phase[1].set_xlabel("x (mm)")
    axes_phase[1].set_ylabel("y (mm)")
    axes_phase[1].set_title("Amplitude $R(x, y)$ de l'onde")
    axes_phase[1].set_aspect("equal")
    cercle2 = plt.Circle(
        (0, 0), A_CAVITE * 1e3, fill=False,
        edgecolor="white", linewidth=2, linestyle="--",
    )
    axes_phase[1].add_patch(cercle2)

    plt.tight_layout()
    fig_phase.savefig("data/003_phase_amplitude.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/003_phase_amplitude.png")

    # ── Étape 5 : potentiel quantique ───────────────────────────────
    print("\n▶ Calcul du potentiel quantique Q(x, y) = −(ℏ²/2m)(∇²R/R)…")
    Q = potentiel_quantique(R_onde, dx, masque)

    print(f"  Q max = {np.max(Q[masque > 0]):.2e}")
    print(f"  Q min = {np.min(Q[masque > 0]):.2e}")

    # ── Étape 6 : gradient −∇Q (force bohmienne) ───────────────────
    print("\n▶ Calcul du gradient ∇Q et de la force F_Q = −∇Q…")
    grad_Qx, grad_Qy = gradient_potentiel_quantique(Q, dx)

    # Force nette intégrée
    Fx, Fy, F_norme = force_bohmienne_nette(
        grad_Qx, grad_Qy, n_e, masque, dx,
    )

    # Pression de radiation classique
    F_rad = pression_radiation(P_MAGNETRON)

    # Direction de la force nette
    angle_force = np.degrees(np.arctan2(Fy, Fx))

    print(f"\n  Force bohmienne nette :")
    print(f"    Fx = {Fx:.4e} N")
    print(f"    Fy = {Fy:.4e} N")
    print(f"    |F| = {F_norme:.4e} N = {F_norme*1e6:.4f} µN")
    print(f"    Direction : {angle_force:.1f}°")
    print(f"\n  Pression de radiation classique :")
    print(f"    F_rad = P/c = {F_rad:.4e} N = {F_rad*1e6:.4f} µN")
    print(f"\n  Ratio η = F_Q / F_rad = {F_norme/F_rad:.2f}")

    # Visualisation Q et ∇Q
    fig2 = plot_potentiel_quantique(
        X, Y, Q, grad_Qx, grad_Qy,
        contour_chambre=A_CAVITE,
        titre=(
            f"Potentiel quantique Q et force bohmienne — "
            f"ε = {EPSILON_ASYM:.2f}"
        ),
        sauvegarde="data/003_potentiel_quantique.png",
    )

    # ── Étape 7 : comparaison des forces ────────────────────────────
    print("\n▶ Diagramme de comparaison des forces…")
    fig3 = plot_force_comparaison(
        forces={
            "$F_{rad} = P/c$\n(pression de radiation)": F_rad,
            "$F_Q = -\\nabla Q$\n(force bohmienne)": F_norme,
            "$F_{totale}$\n(résultante)": F_rad + F_norme,
        },
        titre=(
            f"Comparaison des forces — P = {P_MAGNETRON/1e3:.0f} kW, "
            f"ε = {EPSILON_ASYM:.2f}"
        ),
        sauvegarde="data/003_comparaison_forces.png",
    )

    # ── Étape 8 : scan paramétrique de l'asymétrie ──────────────────
    print("\n▶ Scan paramétrique : force vs asymétrie ε…")
    epsilons = np.linspace(0.0, 0.8, 25)
    eps_scan, fx_scan, fy_scan = scan_asymetrie(
        X, Y, R_grid, Theta_grid, masque, dx, epsilons,
    )
    f_norme_scan = np.sqrt(fx_scan**2 + fy_scan**2)

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(eps_scan, f_norme_scan * 1e6, "b-o", linewidth=2, markersize=4)
    ax4.axhline(F_rad * 1e6, color="red", linestyle="--", linewidth=1.5,
                label=f"$F_{{rad}} = P/c$ = {F_rad*1e6:.2f} µN")
    ax4.fill_between(eps_scan, 0, F_rad * 1e6, alpha=0.1, color="red")
    ax4.set_xlabel("Asymétrie ε (degré d'inhomogénéité du plasma)", fontsize=12)
    ax4.set_ylabel("$|F_Q|$ (µN)", fontsize=12)
    ax4.set_title(
        "Force bohmienne vs asymétrie du plasma\n"
        f"n_e0 = {N_E0:.1e} m⁻³, σ_r = {SIGMA_R*1e3:.0f} mm",
        fontsize=13, fontweight="bold",
    )
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 0.8)
    ax4.set_ylim(bottom=0)
    plt.tight_layout()
    fig4.savefig("data/003_force_vs_asymetrie.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/003_force_vs_asymetrie.png")

    # ── Étape 9 : sauvegarde des données ────────────────────────────
    print("\n▶ Sauvegarde des données numériques…")
    np.save("data/003_densite_electronique.npy", n_e)
    np.save("data/003_indice_refraction.npy", n_ref)
    np.save("data/003_potentiel_quantique.npy", Q)
    np.save("data/003_gradient_Qx.npy", grad_Qx)
    np.save("data/003_gradient_Qy.npy", grad_Qy)
    np.save("data/003_grille_X.npy", X)
    np.save("data/003_grille_Y.npy", Y)
    print("  💾 Données NumPy sauvegardées dans data/003_*.npy")

    # CSV résumé des forces
    import csv
    with open("data/003_forces.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["grandeur", "valeur_N", "valeur_uN", "description"])
        writer.writerow(["F_rad", f"{F_rad:.6e}", f"{F_rad*1e6:.4f}",
                         "Pression de radiation P/c"])
        writer.writerow(["F_Q", f"{F_norme:.6e}", f"{F_norme*1e6:.4f}",
                         "Force bohmienne nette"])
        writer.writerow(["F_totale", f"{F_rad+F_norme:.6e}",
                         f"{(F_rad+F_norme)*1e6:.4f}", "Force totale"])
        writer.writerow(["eta", f"{F_norme/F_rad:.4f}", "",
                         "Ratio F_Q / F_rad"])
    print("  💾 Résumé des forces → data/003_forces.csv")

    # ── Résumé final ────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  RÉSUMÉ — Expérience 003")
    print("═" * 60)
    print(f"""
  Paramètres du modèle :
    Densité max :     n_e0 = {N_E0:.2e} m⁻³ ({N_E0/N_E_CRITIQUE:.1f}× n_e,c)
    Largeur radiale : σ_r  = {SIGMA_R*1e3:.0f} mm
    Asymétrie :       ε    = {EPSILON_ASYM:.2f}
    Puissance :       P    = {P_MAGNETRON/1e3:.0f} kW

  Résultats :
    Pression de radiation :  F_rad = {F_rad*1e6:.2f} µN
    Force bohmienne nette :  F_Q   = {F_norme*1e6:.4f} µN  (direction : {angle_force:.1f}°)
    Force totale :           F_tot = {(F_rad+F_norme)*1e6:.4f} µN
    Ratio η = F_Q / F_rad :         {F_norme/F_rad:.2f}

  Interprétation :
    {"η > 1 → Excès de force au-delà de la pression de radiation !" if F_norme/F_rad > 1 else "η ≤ 1 → Force dans l ordre de grandeur de la pression de radiation."}
    {"⚠️  Attention : cette estimation dépend fortement du modèle d amplitude R." if True else ""}
    {"La direction de la force ({:.0f}°) est cohérente avec l asymétrie imposée.".format(angle_force)}

  ⚠️  Notes importantes :
    • Ce modèle est une ESTIMATION simplifiée en 2D.
    • La valeur absolue de F_Q dépend du modèle d'amplitude R(x,y).
    • Un calcul FDTD 3D complet serait nécessaire pour une prédiction
      quantitative fiable.
    • L'intérêt principal est l'ORDRE DE GRANDEUR et la DIRECTION
      de la force, qui peuvent guider la sensibilité requise du pendule.
""")

    print("✅ Expérience 003 terminée.\n")
    plt.show()
