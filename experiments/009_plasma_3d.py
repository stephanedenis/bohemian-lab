"""
Expérience 009 — Modèle 3D du plasma et vecteur de force bohmienne.

Étend le modèle 2D de l'expérience 003 au cas tridimensionnel en tenant
compte de la géométrie réelle du dispositif : cuve cylindrique (Ø250 × 250 mm)
avec magnétron décentré (~30° du N₁) monté AU-DESSUS de la cuve (z = d).

Questions traitées :
    1. Quelle est la FORME 3D du plasma dans le cylindre ?
       → n_e(r, θ, z) avec injection par le haut et décroissance axiale.
    2. Quel est le VECTEUR DE FORCE 3D ?
       → F_Q = (Fx, Fy, Fz) avec décomposition horizontale/verticale.

Modèle physique 3D :
    n_e(r, θ, z) = n_e0 × exp(−r²/σ_r²)                    [radial]
                       × [1 + ε × cos(θ − θ_mag)]           [azimutal]
                       × exp(−(z − z_max)² / σ_z²)          [axial]

    Le magnétron injecte par le haut → le plasma est plus dense près de
    z = d (le couvercle). Le paramètre z_max ∈ [0.6d, 0.85d] fixe le
    pic de densité axiale.

    Le potentiel quantique 3D est :
        Q(x, y, z) = −(ℏ²/2m) × (∇²R / R)

    où ∇² est le laplacien 3D et R(x,y,z) l'amplitude du champ EM
    atténué par le plasma.

    La force bohmienne 3D est F_Q = −∇Q = (−∂Q/∂x, −∂Q/∂y, −∂Q/∂z).

Sorties :
    - Coupes transversales (x,y) à différentes hauteurs z.
    - Coupe axiale (r,z) à θ = θ_mag et θ = θ_mag + π.
    - Isosurface 3D de n_e (visualisation Matplotlib).
    - Champ de vecteurs F_Q en 3D (quiver).
    - Décomposition F_horizontale vs F_verticale.
    - Données sauvegardées dans data/009_*.npy et data/009_forces_3d.csv.

Références :
    [1] Holland, P.R. (1993). The Quantum Theory of Motion, chap. 3–4.
    [2] Lieberman & Lichtenberg (2005). Principles of Plasma Discharges, chap. 5, 12.
    [3] Chen, F.F. (2016). Introduction to Plasma Physics, chap. 4.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter, laplace
from scipy.special import jn_zeros, jn

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

C: float = 299_792_458.0
HBAR: float = 1.054_571_817e-34
E_CHARGE: float = 1.602_176_634e-19
M_ELECTRON: float = 9.109_383_702e-31
EPSILON_0: float = 8.854_187_817e-12
MU_0: float = 4 * np.pi * 1e-7

# Géométrie de la cavité
A_CAVITE: float = 0.125            # rayon (m)
D_CAVITE: float = 0.250            # hauteur (m)

# Paramètres du magnétron
F_MAGNETRON: float = 2.45e9
OMEGA: float = 2 * np.pi * F_MAGNETRON
P_MAGNETRON: float = 1000.0        # puissance absorbée (W)

# Densité critique pour 2,45 GHz
N_E_CRITIQUE: float = (
    OMEGA**2 * EPSILON_0 * M_ELECTRON / E_CHARGE**2
)  # ≈ 7,4 × 10¹⁶ m⁻³


# ═══════════════════════════════════════════════════════════════════════
# Paramètres du modèle 3D
# ═══════════════════════════════════════════════════════════════════════

N_E0: float = 1.0 * N_E_CRITIQUE   # densité maximale (× n_e,c)
SIGMA_R: float = 0.6 * A_CAVITE    # largeur radiale (m)
SIGMA_Z: float = 0.35 * D_CAVITE   # largeur axiale (m)
Z_MAX_PLASMA: float = 0.75 * D_CAVITE  # pic axial (75 % de d, vers le haut)
EPSILON_ASYM: float = 0.35         # asymétrie azimutale
THETA_MAGNETRON: float = np.radians(30.0)  # position angulaire réelle (~30° du N₁)

# Résolution 3D — compromis mémoire/précision
N_XY: int = 80                     # points par axe x,y
N_Z: int = 60                      # points selon z


# ═══════════════════════════════════════════════════════════════════════
# Construction de la grille 3D
# ═══════════════════════════════════════════════════════════════════════

def creer_grille_3d(
    a: float = A_CAVITE,
    d: float = D_CAVITE,
    n_xy: int = N_XY,
    n_z: int = N_Z,
) -> dict[str, np.ndarray]:
    """Crée une grille cartésienne 3D (x, y, z) couvrant la cavité cylindrique.

    Args:
        a: Rayon de la cavité (m).
        d: Hauteur de la cavité (m).
        n_xy: Nombre de points par axe x et y.
        n_z: Nombre de points selon z.

    Returns:
        Dict avec clés 'X', 'Y', 'Z', 'R', 'Theta', 'masque',
        'dx', 'dz', 'x1d', 'y1d', 'z1d'.
    """
    x1d = np.linspace(-a, a, n_xy)
    y1d = np.linspace(-a, a, n_xy)
    z1d = np.linspace(0, d, n_z)
    dx = 2 * a / n_xy
    dz = d / n_z

    # Grilles 3D : (z, y, x) pour la convention numpy [k, j, i]
    X, Y, Z = np.meshgrid(x1d, y1d, z1d, indexing="ij")
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)

    # Masque cylindrique : intérieur de la cavité
    masque = (R <= a).astype(float)

    return {
        "X": X, "Y": Y, "Z": Z,
        "R": R, "Theta": Theta,
        "masque": masque,
        "dx": dx, "dz": dz,
        "x1d": x1d, "y1d": y1d, "z1d": z1d,
    }


# ═══════════════════════════════════════════════════════════════════════
# Profil de densité électronique 3D
# ═══════════════════════════════════════════════════════════════════════

def profil_densite_3d(
    R: np.ndarray,
    Theta: np.ndarray,
    Z: np.ndarray,
    n_e0: float = N_E0,
    sigma_r: float = SIGMA_R,
    sigma_z: float = SIGMA_Z,
    z_max: float = Z_MAX_PLASMA,
    epsilon: float = EPSILON_ASYM,
    theta_mag: float = THETA_MAGNETRON,
) -> np.ndarray:
    """Calcule la densité électronique 3D n_e(r, θ, z).

    Modèle :
        n_e(r, θ, z) = n_e0 × exp(−r²/σ_r²)
                            × [1 + ε × cos(θ − θ_mag)]
                            × exp(−(z − z_max)² / σ_z²)

    Le plasma est :
    - Confiné radialement (gaussienne, σ_r ≈ 60 % du rayon).
    - Asymétrique azimutalement (magnétron à θ_mag ≈ 30°).
    - Plus dense en haut (z_max ≈ 75 % de d) car le magnétron
      injecte depuis le couvercle supérieur.

    Args:
        R: Distance radiale (3D).
        Theta: Angle azimutal (3D).
        Z: Coordonnée axiale (3D).
        n_e0: Densité maximale (m⁻³).
        sigma_r: Largeur radiale (m).
        sigma_z: Largeur axiale (m).
        z_max: Position du pic axial (m).
        epsilon: Asymétrie azimutale.
        theta_mag: Direction du magnétron (rad).

    Returns:
        n_e(r, θ, z) — densité électronique 3D (m⁻³).
    """
    profil_radial = np.exp(-R**2 / sigma_r**2)
    modulation_azimutale = 1.0 + epsilon * np.cos(Theta - theta_mag)
    profil_axial = np.exp(-(Z - z_max)**2 / sigma_z**2)

    return n_e0 * profil_radial * modulation_azimutale * profil_axial


# ═══════════════════════════════════════════════════════════════════════
# Champ EM 3D — superposition des modes TM dans la cavité
# ═══════════════════════════════════════════════════════════════════════

def champ_em_3d(
    R: np.ndarray,
    Theta: np.ndarray,
    Z: np.ndarray,
    a: float = A_CAVITE,
    d: float = D_CAVITE,
) -> np.ndarray:
    """Calcule le champ E_z 3D par superposition de modes TM dans la cavité.

    Le magnétron excite principalement le mode TM₃₁₀ (f ≈ 2,44 GHz)
    mais sa position décentrée couple aussi TM₁₁₀ et TM₂₁₀.
    La dépendance axiale est cos(pπz/d) ; pour p=0, E_z est uniforme
    en z, mais les modes p>0 introduisent la structure axiale.

    Les coefficients de couplage sont estimés à partir de la position
    de l'antenne (r_ant, θ_mag, z=d).

    Args:
        R: Distance radiale (3D).
        Theta: Angle azimutal (3D).
        Z: Coordonnée axiale (3D).
        a: Rayon de la cavité (m).
        d: Hauteur de la cavité (m).

    Returns:
        E_z (normalisé), champ électrique axial 3D.
    """
    # Racines x'_mn de J_m(x) = 0 (modes TM_{mn?})
    # TM₃₁₀ (mode dominant) : m=3, n=1, p=0
    x_31 = jn_zeros(3, 1)[0]  # ≈ 6.380
    x_11 = jn_zeros(1, 1)[0]  # ≈ 3.832
    x_21 = jn_zeros(2, 1)[0]  # ≈ 5.136

    # Coefficients de couplage (relatifs) — estimés depuis la géométrie
    # TM₃₁₀ est le mode dominant, excité sélectivement
    c_310 = 1.0
    c_110 = 0.15   # couplage résiduel (faible, car m≠3)
    c_210 = 0.10   # encore plus faible
    c_311 = 0.20   # mode TM₃₁₁ avec dépendance axiale (p=1)

    # Calcul des contributions modales
    E_z = np.zeros_like(R)

    # TM₃₁₀ : J₃(x₃₁ r/a) × cos(3θ) × cos(0⋅πz/d) = indépendant de z
    E_z += c_310 * jn(3, x_31 * R / a) * np.cos(3 * (Theta - THETA_MAGNETRON))

    # TM₁₁₀ : couplage parasite
    E_z += c_110 * jn(1, x_11 * R / a) * np.cos(Theta - THETA_MAGNETRON)

    # TM₂₁₀ : couplage parasite
    E_z += c_210 * jn(2, x_21 * R / a) * np.cos(2 * (Theta - THETA_MAGNETRON))

    # TM₃₁₁ : premier mode avec structure axiale
    # cos(πz/d) → maximum au centre, zéro aux extrémités
    # MAIS l'injection par le haut favorise les modes pairs aussi
    E_z += c_311 * jn(3, x_31 * R / a) * np.cos(
        3 * (Theta - THETA_MAGNETRON)
    ) * np.cos(np.pi * Z / d)

    return E_z


# ═══════════════════════════════════════════════════════════════════════
# Amplitude et potentiel quantique 3D
# ═══════════════════════════════════════════════════════════════════════

def amplitude_onde_3d(
    n_e: np.ndarray,
    masque: np.ndarray,
    sigma_lissage: float = 2.0,
) -> np.ndarray:
    """Calcule l'amplitude R(x, y, z) du champ EM atténuée par le plasma 3D.

    R(x,y,z) = R₀ × exp(−α × n_e / n_e,c), lissé par diffraction.

    Args:
        n_e: Densité électronique 3D (m⁻³).
        masque: Masque cylindrique 3D.
        sigma_lissage: Largeur du lissage gaussien (pixels).

    Returns:
        Amplitude R (normalisée), 3D.
    """
    alpha = 1.5
    R = np.exp(-alpha * n_e / N_E_CRITIQUE)
    R = gaussian_filter(R, sigma=sigma_lissage)
    R = R * masque
    R_max = np.max(R)
    if R_max > 0:
        R /= R_max
    return R


def potentiel_quantique_3d(
    R: np.ndarray,
    dx: float,
    dz: float,
    masque: np.ndarray,
    hbar: float = HBAR,
    m: float = M_ELECTRON,
    sigma_lissage: float = 1.5,
) -> np.ndarray:
    """Calcule le potentiel quantique 3D : Q = −(ℏ²/2m)(∇²R/R).

    Le laplacien est calculé par scipy.ndimage.laplace sur la grille 3D.

    ⚠️ Comme pour le modèle 2D (003), les valeurs absolues sont des
    estimations. L'intérêt est dans la DIRECTION et l'ORDRE DE GRANDEUR.

    Args:
        R: Amplitude de l'onde 3D.
        dx: Pas de grille x,y (m).
        dz: Pas de grille z (m).
        masque: Masque cylindrique 3D.
        hbar: Constante de Planck réduite.
        m: Masse de la particule guidée.
        sigma_lissage: Lissage pré-laplacien (pixels).

    Returns:
        Q(x, y, z) — potentiel quantique 3D.
    """
    R_smooth = gaussian_filter(R, sigma=sigma_lissage)
    R_safe = np.maximum(R_smooth, 1e-12)

    # Laplacien 3D — utilise un pas moyen pour la normalisation
    # scipy.ndimage.laplace applique un stencil unitaire ;
    # on corrige par le pas de grille effectif
    lap_R = laplace(R_smooth) / dx**2

    prefacteur = -hbar**2 / (2 * m)
    Q = prefacteur * (lap_R / R_safe)
    Q = Q * masque

    # Écrêtage des artefacts de bord
    q_lim = np.nanpercentile(np.abs(Q[masque > 0]), 99)
    if q_lim > 0:
        Q = np.clip(Q, -q_lim, q_lim)

    return Q


def gradient_3d(
    Q: np.ndarray,
    dx: float,
    dz: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calcule ∇Q = (∂Q/∂x, ∂Q/∂y, ∂Q/∂z) par différences finies.

    Args:
        Q: Potentiel quantique 3D.
        dx: Pas x,y (m).
        dz: Pas z (m).

    Returns:
        Tuple (∂Q/∂x, ∂Q/∂y, ∂Q/∂z).
    """
    # np.gradient sur un tableau 3D de forme (nx, ny, nz)
    # retourne [∂Q/∂(axe0), ∂Q/∂(axe1), ∂Q/∂(axe2)]
    grad_x, grad_y, grad_z = np.gradient(Q, dx, dx, dz)
    return grad_x, grad_y, grad_z


# ═══════════════════════════════════════════════════════════════════════
# Force bohmienne 3D
# ═══════════════════════════════════════════════════════════════════════

def force_bohmienne_3d(
    grad_Qx: np.ndarray,
    grad_Qy: np.ndarray,
    grad_Qz: np.ndarray,
    n_e: np.ndarray,
    masque: np.ndarray,
    dx: float,
    dz: float,
) -> dict[str, float]:
    """Calcule la force bohmienne nette 3D : F = ∫ ρ(−∇Q) dV.

    Décompose le résultat en composante horizontale (mesurable par le
    pendule de torsion) et composante verticale (non mesurable).

    Args:
        grad_Qx, grad_Qy, grad_Qz: Composantes de ∇Q (3D).
        n_e: Densité électronique 3D.
        masque: Masque cylindrique.
        dx: Pas x,y (m).
        dz: Pas z (m).

    Returns:
        Dict avec Fx, Fy, Fz, F_horiz, F_vert, F_total, angle_horiz,
        angle_elev, et ratio_horiz_vert.
    """
    dV = dx * dx * dz
    rho = n_e * masque

    Fx = -np.nansum(rho * grad_Qx * dV)
    Fy = -np.nansum(rho * grad_Qy * dV)
    Fz = -np.nansum(rho * grad_Qz * dV)

    F_horiz = np.sqrt(Fx**2 + Fy**2)
    F_vert = abs(Fz)
    F_total = np.sqrt(Fx**2 + Fy**2 + Fz**2)

    angle_horiz = np.degrees(np.arctan2(Fy, Fx))
    angle_elev = np.degrees(np.arctan2(Fz, F_horiz))

    ratio = F_horiz / F_vert if F_vert > 0 else float("inf")

    return {
        "Fx": Fx, "Fy": Fy, "Fz": Fz,
        "F_horiz": F_horiz,
        "F_vert": F_vert,
        "F_total": F_total,
        "angle_horiz_deg": angle_horiz,
        "angle_elev_deg": angle_elev,
        "ratio_horiz_vert": ratio,
    }


# ═══════════════════════════════════════════════════════════════════════
# Visualisations 3D spécifiques
# ═══════════════════════════════════════════════════════════════════════

def plot_coupes_transversales(
    grille: dict,
    n_e: np.ndarray,
    z_indices: list[int],
    sauvegarde: str | None = None,
) -> "plt.Figure":
    """Affiche des coupes transversales (x,y) de n_e à différentes hauteurs z.

    Args:
        grille: Dict retourné par creer_grille_3d().
        n_e: Densité électronique 3D.
        z_indices: Indices des coupes selon l'axe z.
        sauvegarde: Chemin de sauvegarde.

    Returns:
        Figure matplotlib.
    """
    import matplotlib.pyplot as plt

    n_coupes = len(z_indices)
    fig, axes = plt.subplots(1, n_coupes, figsize=(5 * n_coupes, 5))
    if n_coupes == 1:
        axes = [axes]

    x1d = grille["x1d"]
    y1d = grille["y1d"]
    z1d = grille["z1d"]
    X2d, Y2d = np.meshgrid(x1d, y1d, indexing="ij")

    vmax = np.max(n_e)

    for ax, kz in zip(axes, z_indices):
        coupe = n_e[:, :, kz]
        z_val = z1d[kz] * 1e3  # mm

        im = ax.pcolormesh(
            X2d * 1e3, Y2d * 1e3, coupe,
            cmap="inferno", shading="gouraud",
            vmin=0, vmax=vmax,
        )
        fig.colorbar(im, ax=ax, label="$n_e$ (m⁻³)", shrink=0.8)

        # Contour de la cavité
        cercle = plt.Circle(
            (0, 0), A_CAVITE * 1e3,
            fill=False, edgecolor="white", linewidth=2, linestyle="--",
        )
        ax.add_patch(cercle)

        # Position du magnétron
        r_mag = 0.5 * A_CAVITE
        x_mag = r_mag * np.cos(THETA_MAGNETRON) * 1e3
        y_mag = r_mag * np.sin(THETA_MAGNETRON) * 1e3
        ax.plot(x_mag, y_mag, "w*", markersize=12, label="Magnétron")

        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.set_title(f"z = {z_val:.0f} mm")
        ax.set_aspect("equal")

    fig.suptitle(
        "Coupes transversales $n_e(x, y)$ à différentes hauteurs",
        fontsize=14, fontweight="bold", y=1.02,
    )
    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


def plot_coupe_axiale(
    grille: dict,
    champ_3d: np.ndarray,
    theta_coupe: float = 0.0,
    label: str = "$n_e$",
    cmap: str = "inferno",
    titre: str = "Coupe axiale $(r, z)$",
    sauvegarde: str | None = None,
) -> "plt.Figure":
    """Affiche une coupe axiale (r, z) du champ 3D passant par θ_coupe.

    Combine deux demi-plans : θ_coupe (à droite) et θ_coupe + π (à gauche),
    comme une coupe de méridien.

    Args:
        grille: Dict retourné par creer_grille_3d().
        champ_3d: Champ scalaire 3D à couper.
        theta_coupe: Angle de la coupe (rad).
        label: Étiquette de la colorbar.
        cmap: Palette de couleurs.
        titre: Titre du graphique.
        sauvegarde: Chemin de sauvegarde.

    Returns:
        Figure matplotlib.
    """
    import matplotlib.pyplot as plt

    x1d = grille["x1d"]
    y1d = grille["y1d"]
    z1d = grille["z1d"]

    # Indices les plus proches du plan θ_coupe
    # On prend la coupe y=0 tournée de theta_coupe
    # Approximation : prendre la ligne x>0 pour θ et x<0 pour θ+π
    n_xy = len(x1d)

    # Demi-plan à θ_coupe : interpoler le long de la direction θ_coupe
    n_r = n_xy // 2
    r_1d = np.linspace(0, A_CAVITE, n_r)
    n_z = len(z1d)

    coupe_droite = np.zeros((n_r, n_z))
    coupe_gauche = np.zeros((n_r, n_z))

    for ir, r_val in enumerate(r_1d):
        # Point à θ_coupe
        xp = r_val * np.cos(theta_coupe)
        yp = r_val * np.sin(theta_coupe)
        ix = np.argmin(np.abs(x1d - xp))
        iy = np.argmin(np.abs(y1d - yp))
        coupe_droite[ir, :] = champ_3d[ix, iy, :]

        # Point à θ_coupe + π (opposé)
        xn = r_val * np.cos(theta_coupe + np.pi)
        yn = r_val * np.sin(theta_coupe + np.pi)
        ixn = np.argmin(np.abs(x1d - xn))
        iyn = np.argmin(np.abs(y1d - yn))
        coupe_gauche[ir, :] = champ_3d[ixn, iyn, :]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Demi-plan gauche (r négatif = côté opposé au magnétron)
    R_gauche, Z_gauche = np.meshgrid(-r_1d[::-1], z1d, indexing="ij")
    im1 = ax.pcolormesh(
        R_gauche * 1e3, Z_gauche * 1e3, coupe_gauche[::-1, :],
        cmap=cmap, shading="gouraud",
    )

    # Demi-plan droit (côté magnétron)
    R_droite, Z_droite = np.meshgrid(r_1d, z1d, indexing="ij")
    im2 = ax.pcolormesh(
        R_droite * 1e3, Z_droite * 1e3, coupe_droite,
        cmap=cmap, shading="gouraud",
        vmin=im1.get_clim()[0], vmax=im1.get_clim()[1],
    )

    fig.colorbar(im2, ax=ax, label=label, shrink=0.8)

    # Contour de la cavité
    ax.plot(
        [-A_CAVITE * 1e3, -A_CAVITE * 1e3, A_CAVITE * 1e3, A_CAVITE * 1e3],
        [0, D_CAVITE * 1e3, D_CAVITE * 1e3, 0],
        "w--", linewidth=2,
    )
    ax.plot([-A_CAVITE * 1e3, A_CAVITE * 1e3], [0, 0], "w--", linewidth=2)

    # Position du magnétron (en haut, côté droit)
    ax.annotate(
        "MAGNÉTRON ↓",
        xy=(0.5 * A_CAVITE * np.cos(theta_coupe) * 1e3, D_CAVITE * 1e3),
        fontsize=10, color="white", fontweight="bold",
        ha="center", va="bottom",
    )

    # Annotations
    ax.set_xlabel("r (mm) — ← opposé | magnétron →", fontsize=12)
    ax.set_ylabel("z (mm) — fond ↓ | couvercle ↑", fontsize=12)
    ax.set_title(titre, fontsize=14, fontweight="bold")
    ax.set_aspect("equal")

    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


def plot_isosurface_plasma(
    grille: dict,
    n_e: np.ndarray,
    niveau: float | None = None,
    sauvegarde: str | None = None,
) -> "plt.Figure":
    """Affiche l'isosurface 3D de n_e à un niveau donné (marching cubes simulé).

    Utilise la visualisation par scatter 3D pondérée pour simuler
    l'isosurface sans dépendance VTK.

    Args:
        grille: Dict retourné par creer_grille_3d().
        n_e: Densité électronique 3D.
        niveau: Niveau d'isosurface (m⁻³). Défaut : 50 % de max.
        sauvegarde: Chemin de sauvegarde.

    Returns:
        Figure matplotlib.
    """
    import matplotlib.pyplot as plt

    if niveau is None:
        niveau = 0.5 * np.max(n_e)

    X = grille["X"]
    Y = grille["Y"]
    Z = grille["Z"]
    masque = grille["masque"]

    # Sélection des points proches de l'isosurface
    ecart = np.abs(n_e - niveau)
    seuil = 0.1 * niveau
    iso_mask = (ecart < seuil) & (masque > 0)

    x_iso = X[iso_mask] * 1e3
    y_iso = Y[iso_mask] * 1e3
    z_iso = Z[iso_mask] * 1e3
    c_iso = n_e[iso_mask]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    scatter = ax.scatter(
        x_iso, y_iso, z_iso,
        c=c_iso, cmap="plasma", s=8, alpha=0.4,
        edgecolors="none",
    )
    fig.colorbar(scatter, ax=ax, label="$n_e$ (m⁻³)", shrink=0.6)

    # Cylindre de la cavité (contour)
    theta_c = np.linspace(0, 2 * np.pi, 60)
    x_c = A_CAVITE * np.cos(theta_c) * 1e3
    y_c = A_CAVITE * np.sin(theta_c) * 1e3
    ax.plot(x_c, y_c, zs=0, zdir="z", color="gray",
            linestyle="--", alpha=0.5, linewidth=1)
    ax.plot(x_c, y_c, zs=D_CAVITE * 1e3, zdir="z", color="gray",
            linestyle="--", alpha=0.5, linewidth=1)

    # Position du magnétron
    ax.scatter(
        [0.5 * A_CAVITE * np.cos(THETA_MAGNETRON) * 1e3],
        [0.5 * A_CAVITE * np.sin(THETA_MAGNETRON) * 1e3],
        [D_CAVITE * 1e3],
        color="red", s=100, marker="*", label="Magnétron",
    )

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_zlabel("z (mm)")
    ax.set_title(
        f"Isosurface plasma — $n_e$ = {niveau:.1e} m⁻³\n"
        f"(≈ {niveau/N_E_CRITIQUE*100:.0f} % de $n_{{e,c}}$)",
        fontsize=13, fontweight="bold",
    )
    ax.legend(loc="upper right")

    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


def plot_force_3d(
    grille: dict,
    grad_Qx: np.ndarray,
    grad_Qy: np.ndarray,
    grad_Qz: np.ndarray,
    masque: np.ndarray,
    sauvegarde: str | None = None,
) -> "plt.Figure":
    """Affiche le champ de vecteurs de force bohmienne F_Q = −∇Q en 3D.

    Sous-échantillonne la grille pour la lisibilité.

    Args:
        grille: Dict retourné par creer_grille_3d().
        grad_Qx, grad_Qy, grad_Qz: Composantes de ∇Q (3D).
        masque: Masque cylindrique.
        sauvegarde: Chemin de sauvegarde.

    Returns:
        Figure matplotlib.
    """
    import matplotlib.pyplot as plt

    X = grille["X"]
    Y = grille["Y"]
    Z = grille["Z"]

    # Sous-échantillonnage
    pas = max(1, X.shape[0] // 8)
    pas_z = max(1, X.shape[2] // 6)

    x_s = X[::pas, ::pas, ::pas_z] * 1e3
    y_s = Y[::pas, ::pas, ::pas_z] * 1e3
    z_s = Z[::pas, ::pas, ::pas_z] * 1e3
    fx = -grad_Qx[::pas, ::pas, ::pas_z]
    fy = -grad_Qy[::pas, ::pas, ::pas_z]
    fz = -grad_Qz[::pas, ::pas, ::pas_z]
    m_s = masque[::pas, ::pas, ::pas_z]

    # Filtrer les points à l'intérieur de la cavité
    inside = m_s > 0
    x_f = x_s[inside]
    y_f = y_s[inside]
    z_f = z_s[inside]
    fx_f = fx[inside]
    fy_f = fy[inside]
    fz_f = fz[inside]

    # Norme pour la couleur
    norme = np.sqrt(fx_f**2 + fy_f**2 + fz_f**2)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")

    # Normaliser la longueur des flèches
    n_max = np.nanpercentile(norme, 95)
    if n_max > 0:
        scale = 20 / n_max  # échelle visuelle
    else:
        scale = 1.0

    ax.quiver(
        x_f, y_f, z_f,
        fx_f * scale, fy_f * scale, fz_f * scale,
        length=1.0, normalize=False,
        color=plt.cm.hot(norme / max(n_max, 1e-30)),
        alpha=0.7, linewidth=1.0,
    )

    # Contour du cylindre
    theta_c = np.linspace(0, 2 * np.pi, 60)
    x_c = A_CAVITE * np.cos(theta_c) * 1e3
    y_c = A_CAVITE * np.sin(theta_c) * 1e3
    ax.plot(x_c, y_c, zs=0, zdir="z", color="gray",
            linestyle="--", alpha=0.5)
    ax.plot(x_c, y_c, zs=D_CAVITE * 1e3, zdir="z", color="gray",
            linestyle="--", alpha=0.5)

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_zlabel("z (mm)")
    ax.set_title(
        "Champ de force bohmienne 3D — $\\vec{F}_Q = -\\nabla Q$",
        fontsize=13, fontweight="bold",
    )

    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


def plot_decomposition_force(
    resultats: dict[str, float],
    f_rad: float,
    sauvegarde: str | None = None,
) -> "plt.Figure":
    """Compare F_horizontale, F_verticale et F_radiation.

    Args:
        resultats: Dict retourné par force_bohmienne_3d().
        f_rad: Force de pression de radiation P/c.
        sauvegarde: Chemin de sauvegarde.

    Returns:
        Figure matplotlib.
    """
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # ---- Panneau 1 : barres ----
    noms = [
        "$F_{horiz}$\n(mesurable)",
        "$F_{vert}$\n(non mesurable)",
        "$F_{total}$\n(3D)",
        "$F_{rad} = P/c$",
    ]
    valeurs = [
        resultats["F_horiz"] * 1e6,
        resultats["F_vert"] * 1e6,
        resultats["F_total"] * 1e6,
        f_rad * 1e6,
    ]
    couleurs = ["#2ecc71", "#e74c3c", "#3498db", "#95a5a6"]

    barres = ax1.bar(noms, valeurs, color=couleurs, edgecolor="white", width=0.5)
    for barre, v in zip(barres, valeurs):
        ax1.text(
            barre.get_x() + barre.get_width() / 2,
            barre.get_height() + max(valeurs) * 0.02,
            f"{v:.3f} µN", ha="center", fontsize=10, fontweight="bold",
        )
    ax1.set_ylabel("Force (µN)")
    ax1.set_title("Décomposition 3D de la force bohmienne", fontweight="bold")
    ax1.grid(True, axis="y", alpha=0.3)

    # ---- Panneau 2 : vecteur de force en projection ----
    Fx = resultats["Fx"]
    Fy = resultats["Fy"]
    Fz = resultats["Fz"]
    F_max = resultats["F_total"]

    if F_max > 0:
        # Vue (x, y) — plan horizontal
        ax2.arrow(
            0, 0, Fx / F_max, Fy / F_max,
            head_width=0.05, head_length=0.03,
            fc="#2ecc71", ec="#2ecc71", linewidth=2,
        )
        ax2.text(
            Fx / F_max * 1.15, Fy / F_max * 1.15,
            f"$F_{{horiz}}$ ({resultats['angle_horiz_deg']:.1f}°)",
            fontsize=11, color="#2ecc71",
        )

        # Flèche verticale (projetée comme indicateur)
        ax2.arrow(
            0, 0, 0, Fz / F_max,
            head_width=0.05, head_length=0.03,
            fc="#e74c3c", ec="#e74c3c", linewidth=2, linestyle="--",
        )
        ax2.text(
            0.05, Fz / F_max * 1.1,
            f"$F_z$ (↑)",
            fontsize=11, color="#e74c3c",
        )

    # Direction du magnétron
    ax2.arrow(
        0, 0,
        0.6 * np.cos(THETA_MAGNETRON), 0.6 * np.sin(THETA_MAGNETRON),
        head_width=0.03, head_length=0.02,
        fc="gray", ec="gray", linewidth=1, alpha=0.5,
    )
    ax2.text(
        0.65 * np.cos(THETA_MAGNETRON),
        0.65 * np.sin(THETA_MAGNETRON),
        "mag.", fontsize=9, color="gray",
    )

    ax2.set_xlim(-1.3, 1.3)
    ax2.set_ylim(-1.3, 1.3)
    ax2.set_aspect("equal")
    ax2.set_xlabel("$F_x / |F|$")
    ax2.set_ylabel("$F_y / |F|$ ou $F_z / |F|$")
    ax2.set_title("Direction du vecteur force (normalisé)", fontweight="bold")
    ax2.axhline(0, color="gray", linewidth=0.5)
    ax2.axvline(0, color="gray", linewidth=0.5)
    ax2.grid(True, alpha=0.2)

    fig.suptitle(
        f"Force 3D — élévation {resultats['angle_elev_deg']:.1f}°, "
        f"ratio H/V = {resultats['ratio_horiz_vert']:.2f}",
        fontsize=14, fontweight="bold", y=1.02,
    )
    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import csv

    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  Expérience 009 — Modèle 3D du plasma et force bohmienne     ║")
    print("║  Cavité Ø250×250 mm — Magnétron décentré à 30° (au-dessus)   ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    # ── Étape 1 : grille 3D ─────────────────────────────────────────
    print("▶ Construction de la grille 3D…")
    grille = creer_grille_3d()
    X = grille["X"]
    Y = grille["Y"]
    Z = grille["Z"]
    R_grid = grille["R"]
    Theta_grid = grille["Theta"]
    masque = grille["masque"]
    dx = grille["dx"]
    dz = grille["dz"]

    n_total = N_XY * N_XY * N_Z
    mem_mb = n_total * 8 / 1e6  # float64
    print(f"  Grille : {N_XY}×{N_XY}×{N_Z} = {n_total:,} points")
    print(f"  dx = {dx*1e3:.2f} mm, dz = {dz*1e3:.2f} mm")
    print(f"  Mémoire par champ : ~{mem_mb:.1f} Mo")

    # ── Étape 2 : densité électronique 3D ───────────────────────────
    print("\n▶ Calcul du profil 3D de densité n_e(r, θ, z)…")
    print(f"  n_e0 = {N_E0:.2e} m⁻³ (= {N_E0/N_E_CRITIQUE:.1f}× n_e,c)")
    print(f"  σ_r = {SIGMA_R*1e3:.1f} mm, σ_z = {SIGMA_Z*1e3:.1f} mm")
    print(f"  z_max plasma = {Z_MAX_PLASMA*1e3:.0f} mm "
          f"({Z_MAX_PLASMA/D_CAVITE*100:.0f} % de d)")
    print(f"  ε = {EPSILON_ASYM:.2f}, θ_mag = {np.degrees(THETA_MAGNETRON):.0f}°")

    n_e = profil_densite_3d(R_grid, Theta_grid, Z)

    # Statistiques
    n_e_int = n_e[masque > 0]
    print(f"\n  Statistiques intérieures :")
    print(f"    n_e max = {np.max(n_e_int):.2e} m⁻³")
    print(f"    n_e moy = {np.mean(n_e_int):.2e} m⁻³")
    print(f"    ratio max/n_e,c = {np.max(n_e_int)/N_E_CRITIQUE:.2f}")

    # ── Étape 3 : visualisation des coupes transversales ────────────
    print("\n▶ Coupes transversales (x, y) à z = fond, milieu, haut…")
    z_idx_fond = N_Z // 10         # ≈ 10 % de d
    z_idx_milieu = N_Z // 2        # 50 %
    z_idx_pic = int(0.75 * N_Z)    # 75 % (pic plasma)
    z_idx_haut = int(0.95 * N_Z)   # 95 % (près du couvercle)

    fig_coupes = plot_coupes_transversales(
        grille, n_e,
        z_indices=[z_idx_fond, z_idx_milieu, z_idx_pic, z_idx_haut],
        sauvegarde="data/009_coupes_transversales.png",
    )

    # ── Étape 4 : coupe axiale (r, z) ──────────────────────────────
    print("\n▶ Coupe axiale (r, z) dans le plan du magnétron…")
    fig_axiale = plot_coupe_axiale(
        grille, n_e,
        theta_coupe=THETA_MAGNETRON,
        label="$n_e$ (m⁻³)",
        titre=(
            f"Coupe méridienne du plasma — θ = {np.degrees(THETA_MAGNETRON):.0f}°\n"
            f"Magnétron en haut, injection vers le bas"
        ),
        sauvegarde="data/009_coupe_axiale_plasma.png",
    )

    # ── Étape 5 : isosurface 3D ────────────────────────────────────
    print("\n▶ Isosurface 3D du plasma…")
    fig_iso = plot_isosurface_plasma(
        grille, n_e,
        niveau=0.5 * N_E_CRITIQUE,
        sauvegarde="data/009_isosurface_plasma.png",
    )

    # ── Étape 6 : amplitude et potentiel quantique 3D ──────────────
    print("\n▶ Calcul de l'amplitude R(x, y, z) et du potentiel Q(x, y, z)…")
    R_onde = amplitude_onde_3d(n_e, masque)
    Q = potentiel_quantique_3d(R_onde, dx, dz, masque)

    Q_int = Q[masque > 0]
    print(f"  Q max = {np.max(Q_int):.2e}")
    print(f"  Q min = {np.min(Q_int):.2e}")

    # Coupe axiale de Q
    fig_q_axiale = plot_coupe_axiale(
        grille, Q,
        theta_coupe=THETA_MAGNETRON,
        label="Q (unités norm.)",
        cmap="viridis",
        titre="Coupe axiale — Potentiel quantique $Q(r, z)$",
        sauvegarde="data/009_coupe_axiale_Q.png",
    )

    # ── Étape 7 : gradient 3D et force bohmienne ───────────────────
    print("\n▶ Calcul du gradient 3D ∇Q et de la force F_Q = −∇Q…")
    grad_Qx, grad_Qy, grad_Qz = gradient_3d(Q, dx, dz)

    resultats = force_bohmienne_3d(
        grad_Qx, grad_Qy, grad_Qz,
        n_e, masque, dx, dz,
    )

    F_rad = P_MAGNETRON / C

    print(f"\n  Force bohmienne 3D :")
    print(f"    Fx = {resultats['Fx']:.4e} N")
    print(f"    Fy = {resultats['Fy']:.4e} N")
    print(f"    Fz = {resultats['Fz']:.4e} N")
    print(f"    |F_horiz| = {resultats['F_horiz']:.4e} N "
          f"= {resultats['F_horiz']*1e6:.4f} µN")
    print(f"    |F_vert|  = {resultats['F_vert']:.4e} N "
          f"= {resultats['F_vert']*1e6:.4f} µN")
    print(f"    |F_total| = {resultats['F_total']:.4e} N "
          f"= {resultats['F_total']*1e6:.4f} µN")
    print(f"    Direction horizontale : {resultats['angle_horiz_deg']:.1f}°")
    print(f"    Élévation : {resultats['angle_elev_deg']:.1f}°")
    print(f"    Ratio H/V : {resultats['ratio_horiz_vert']:.2f}")
    print(f"\n  Pression de radiation :")
    print(f"    F_rad = P/c = {F_rad:.4e} N = {F_rad*1e6:.4f} µN")
    eta_horiz = resultats["F_horiz"] / F_rad if F_rad > 0 else 0
    eta_total = resultats["F_total"] / F_rad if F_rad > 0 else 0
    print(f"    η_horiz = F_horiz / F_rad = {eta_horiz:.2f}")
    print(f"    η_total = F_total / F_rad = {eta_total:.2f}")

    # ── Étape 8 : champ de force 3D ────────────────────────────────
    print("\n▶ Visualisation du champ de force 3D…")
    fig_force = plot_force_3d(
        grille, grad_Qx, grad_Qy, grad_Qz, masque,
        sauvegarde="data/009_force_3d.png",
    )

    # ── Étape 9 : décomposition H/V ────────────────────────────────
    print("\n▶ Comparaison F_horizontale vs F_verticale…")
    fig_decomp = plot_decomposition_force(
        resultats, F_rad,
        sauvegarde="data/009_decomposition_force.png",
    )

    # ── Étape 10 : scan paramétrique z_max ──────────────────────────
    print("\n▶ Scan paramétrique : force vs position axiale du plasma…")
    z_max_values = np.linspace(0.3 * D_CAVITE, 0.95 * D_CAVITE, 15)
    forces_scan = {"z_max_mm": [], "F_horiz_uN": [], "F_vert_uN": [],
                   "F_total_uN": [], "ratio_HV": []}

    for zm in z_max_values:
        n_e_scan = profil_densite_3d(R_grid, Theta_grid, Z, z_max=zm)
        R_scan = amplitude_onde_3d(n_e_scan, masque)
        Q_scan = potentiel_quantique_3d(R_scan, dx, dz, masque)
        gx, gy, gz = gradient_3d(Q_scan, dx, dz)
        res = force_bohmienne_3d(gx, gy, gz, n_e_scan, masque, dx, dz)
        forces_scan["z_max_mm"].append(zm * 1e3)
        forces_scan["F_horiz_uN"].append(res["F_horiz"] * 1e6)
        forces_scan["F_vert_uN"].append(res["F_vert"] * 1e6)
        forces_scan["F_total_uN"].append(res["F_total"] * 1e6)
        forces_scan["ratio_HV"].append(res["ratio_horiz_vert"])

    fig_scan, (ax_s1, ax_s2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax_s1.plot(forces_scan["z_max_mm"], forces_scan["F_horiz_uN"],
               "g-o", label="$F_{horiz}$ (mesurable)", linewidth=2, markersize=4)
    ax_s1.plot(forces_scan["z_max_mm"], forces_scan["F_vert_uN"],
               "r-s", label="$F_{vert}$ (non mesurable)", linewidth=2, markersize=4)
    ax_s1.plot(forces_scan["z_max_mm"], forces_scan["F_total_uN"],
               "b-^", label="$F_{total}$", linewidth=2, markersize=4)
    ax_s1.axhline(F_rad * 1e6, color="gray", linestyle="--",
                  label=f"$F_{{rad}} = P/c$ = {F_rad*1e6:.2f} µN")
    ax_s1.set_ylabel("Force (µN)")
    ax_s1.set_title(
        "Force bohmienne vs position axiale du pic plasma",
        fontweight="bold",
    )
    ax_s1.legend(fontsize=9)
    ax_s1.grid(True, alpha=0.3)

    ax_s2.plot(forces_scan["z_max_mm"], forces_scan["ratio_HV"],
               "k-d", linewidth=2, markersize=5)
    ax_s2.axhline(1, color="gray", linestyle=":", alpha=0.5)
    ax_s2.set_xlabel("$z_{max}$ plasma (mm) — fond ← | → couvercle")
    ax_s2.set_ylabel("Ratio $F_{horiz} / F_{vert}$")
    ax_s2.set_title("Répartition horizontale vs verticale", fontweight="bold")
    ax_s2.grid(True, alpha=0.3)

    plt.tight_layout()
    fig_scan.savefig("data/009_force_vs_zmax.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/009_force_vs_zmax.png")

    # ── Étape 11 : sauvegarde des données ───────────────────────────
    print("\n▶ Sauvegarde des données numériques…")
    np.savez_compressed(
        "data/009_plasma_3d.npz",
        n_e=n_e,
        Q=Q,
        R_onde=R_onde,
        grad_Qx=grad_Qx,
        grad_Qy=grad_Qy,
        grad_Qz=grad_Qz,
        x1d=grille["x1d"],
        y1d=grille["y1d"],
        z1d=grille["z1d"],
    )
    print("  💾 Données 3D compressées → data/009_plasma_3d.npz")

    with open("data/009_forces_3d.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "grandeur", "valeur_N", "valeur_uN", "description",
        ])
        writer.writerow([
            "Fx", f"{resultats['Fx']:.6e}",
            f"{resultats['Fx']*1e6:.4f}", "Composante x",
        ])
        writer.writerow([
            "Fy", f"{resultats['Fy']:.6e}",
            f"{resultats['Fy']*1e6:.4f}", "Composante y",
        ])
        writer.writerow([
            "Fz", f"{resultats['Fz']:.6e}",
            f"{resultats['Fz']*1e6:.4f}", "Composante z (verticale)",
        ])
        writer.writerow([
            "F_horiz", f"{resultats['F_horiz']:.6e}",
            f"{resultats['F_horiz']*1e6:.4f}", "Force horizontale (mesurable)",
        ])
        writer.writerow([
            "F_vert", f"{resultats['F_vert']:.6e}",
            f"{resultats['F_vert']*1e6:.4f}", "Force verticale (non mesurable)",
        ])
        writer.writerow([
            "F_total", f"{resultats['F_total']:.6e}",
            f"{resultats['F_total']*1e6:.4f}", "Force totale 3D",
        ])
        writer.writerow([
            "F_rad", f"{F_rad:.6e}",
            f"{F_rad*1e6:.4f}", "Pression de radiation P/c",
        ])
        writer.writerow([
            "eta_horiz", f"{eta_horiz:.4f}", "",
            "Ratio F_horiz / F_rad",
        ])
        writer.writerow([
            "eta_total", f"{eta_total:.4f}", "",
            "Ratio F_total / F_rad",
        ])
        writer.writerow([
            "angle_horiz", f"{resultats['angle_horiz_deg']:.2f}", "deg",
            "Direction horizontale de la force",
        ])
        writer.writerow([
            "angle_elev", f"{resultats['angle_elev_deg']:.2f}", "deg",
            "Angle d'élévation de la force",
        ])
        writer.writerow([
            "ratio_HV", f"{resultats['ratio_horiz_vert']:.4f}", "",
            "Ratio F_horiz / F_vert",
        ])
    print("  💾 Forces 3D → data/009_forces_3d.csv")

    # Sauvegarde du scan paramétrique
    with open("data/009_scan_zmax.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "z_max_mm", "F_horiz_uN", "F_vert_uN", "F_total_uN", "ratio_HV",
        ])
        for i in range(len(forces_scan["z_max_mm"])):
            writer.writerow([
                f"{forces_scan['z_max_mm'][i]:.1f}",
                f"{forces_scan['F_horiz_uN'][i]:.6f}",
                f"{forces_scan['F_vert_uN'][i]:.6f}",
                f"{forces_scan['F_total_uN'][i]:.6f}",
                f"{forces_scan['ratio_HV'][i]:.4f}",
            ])
    print("  💾 Scan paramétrique → data/009_scan_zmax.csv")

    # ── Résumé final ────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("  RÉSUMÉ — Expérience 009 : Modèle 3D Plasma & Force")
    print("═" * 64)
    print(f"""
  FORME 3D DU PLASMA :
    Le plasma forme une « calotte allongée » (ellipsoïde tronqué)
    à l'intérieur du cylindre, avec :
    • Maximum de densité décalé vers le HAUT (z ≈ {Z_MAX_PLASMA*1e3:.0f} mm
      soit {Z_MAX_PLASMA/D_CAVITE*100:.0f} % de la hauteur) car le
      magnétron injecte depuis le couvercle supérieur.
    • Asymétrie azimutale centrée sur θ ≈ {np.degrees(THETA_MAGNETRON):.0f}°
      (position réelle du magnétron, ~30° du N₁).
    • Confinement radial gaussien (σ_r = {SIGMA_R*1e3:.0f} mm),
      le plasma ne remplit pas tout le cylindre.

    En coupe axiale : le plasma ressemble à une « goutte »
    suspendue depuis le couvercle, plus étroite vers le fond.

  VECTEUR DE FORCE 3D :
    Fx = {resultats['Fx']*1e6:.4f} µN
    Fy = {resultats['Fy']*1e6:.4f} µN
    Fz = {resultats['Fz']*1e6:.4f} µN

    |F_horizontale| = {resultats['F_horiz']*1e6:.4f} µN  (direction {resultats['angle_horiz_deg']:.1f}°)
    |F_verticale|   = {resultats['F_vert']*1e6:.4f} µN  ({"↑ vers le haut" if resultats['Fz'] > 0 else "↓ vers le bas"})
    |F_totale|      = {resultats['F_total']*1e6:.4f} µN

    Ratio H/V = {resultats['ratio_horiz_vert']:.2f}
    Angle d'élévation = {resultats['angle_elev_deg']:.1f}°

  IMPLICATIONS POUR LE PENDULE :
    Le pendule de torsion ne mesure que la composante HORIZONTALE.
    {"→ Le ratio H/V > 1 est favorable : la majorité de la force est mesurable." if resultats['ratio_horiz_vert'] > 1 else "→ Le ratio H/V < 1 signifie qu'une part importante de la force est verticale et NON mesurable par le pendule."}
    {"→ La force verticale (Fz) crée une variation de poids apparente, détectable par une balance mais pas par le pendule de torsion." if resultats['F_vert'] > resultats['F_horiz'] else ""}

    η_horiz = F_horiz / F_rad = {eta_horiz:.2f}
    η_total = F_total / F_rad = {eta_total:.2f}

  ⚠️  LIMITATIONS :
    • Modèle semi-analytique (pas FDTD).
    • Le profil axial gaussien est un choix phénoménologique.
    • Résolution 3D réduite ({N_XY}×{N_XY}×{N_Z}) pour le temps de calcul.
    • Un calcul FDTD 3D complet améliorerait la prédiction quantitative.
""")

    print("✅ Expérience 009 terminée.\n")
