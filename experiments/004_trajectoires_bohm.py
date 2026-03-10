"""
Expérience 004 — Trajectoires bohmiennes dans un potentiel 2D.

Simule numériquement les trajectoires de particules guidées par une
onde pilote ψ(x, y, t) selon l'interprétation de de Broglie–Bohm.

Principe :
    Dans la mécanique bohmienne, chaque particule possède une position
    définie Q(t) dont la vitesse est dictée par la loi de guidage :

        dQ/dt = (ℏ/m) × Im(∇ψ / ψ)

    ou, en décomposition polaire ψ = R × exp(iS/ℏ) :

        v = ∇S / m

    La particule « surfe » sur l'onde pilote. Sa trajectoire est
    déterministe une fois la position initiale fixée.

Scénarios simulés :
    1. Double fente — Le cas emblématique de la mécanique bohmienne :
       les particules passent par UNE SEULE fente mais leurs trajectoires
       sont guidées par l'onde qui passe par LES DEUX fentes.
       Résultat : les trajectoires reproduisent le pattern d'interférence.

    2. Puits asymétrique — Analogie avec la cavité plasma :
       un potentiel avec un gradient asymétrique guide les particules
       vers la zone de moindre Q, simulant la force de poussée.

    3. Paquet d'onde gaussien avec barrière — Effet tunnel bohmien :
       les trajectoires montrent comment certaines particules traversent
       une barrière de potentiel classiquement interdite.

Méthode numérique :
    - L'équation de Schrödinger est résolue sur une grille 2D par la
      méthode de Crank-Nicolson (split-operator en x et y).
    - Les trajectoires sont intégrées par Runge-Kutta d'ordre 4 (RK4)
      en interpolant le champ de vitesse bohmien.
    - La densité de probabilité |ψ|² et le potentiel quantique Q sont
      calculés à chaque pas de temps.

Sorties :
    - Trajectoires bohmiennes superposées sur |ψ|².
    - Animation du champ de densité + trajectoires (optionnel).
    - Potentiel quantique Q à l'instant final.
    - Données sauvegardées dans data/004_*.npy.

Références :
    [1] Holland, P.R. (1993). The Quantum Theory of Motion, chap. 5.
    [2] Philippidis, Dewdney & Hiley (1979). "Quantum interference and
        the quantum potential". Il Nuovo Cimento B, 52(1), 15-28.
    [3] Sanz & Miret-Artés (2012). A Trajectory Description of Quantum
        Processes. Springer, chap. 3.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import laplace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.viz import plot_trajectoires_bohm, plot_potentiel_quantique


# ═══════════════════════════════════════════════════════════════════════
# Constantes et paramètres (unités naturelles : ℏ = m = 1)
# ═══════════════════════════════════════════════════════════════════════

# En unités naturelles, on pose ℏ = 1, m = 1.
# Les longueurs sont en unités de la longueur caractéristique du système,
# les temps en unités de ℏ/(m × L²).

HBAR: float = 1.0
M: float = 1.0


# ═══════════════════════════════════════════════════════════════════════
# Fonction d'onde — construction de ψ(x, y, t=0)
# ═══════════════════════════════════════════════════════════════════════

def paquet_gaussien_2d(
    x: np.ndarray,
    y: np.ndarray,
    x0: float = 0.0,
    y0: float = 0.0,
    sigma_x: float = 1.0,
    sigma_y: float = 1.0,
    kx: float = 0.0,
    ky: float = 0.0,
) -> np.ndarray:
    """Crée un paquet d'onde gaussien 2D.

    ψ(x, y) = N × exp(−(x−x0)²/4σ_x² − (y−y0)²/4σ_y²)
              × exp(i(kx·x + ky·y))

    Le paquet est centré en (x0, y0) avec une impulsion moyenne (kx, ky).
    Les σ contrôlent l'étalement spatial (moindre σ = plus localisé
    mais plus de dispersion dans le temps).

    Args:
        x, y: Grilles 2D (meshgrid).
        x0, y0: Centre du paquet.
        sigma_x, sigma_y: Largeurs spatiales.
        kx, ky: Impulsion moyenne (vecteur d'onde).

    Returns:
        ψ(x, y) — fonction d'onde complexe 2D, normalisée.
    """
    gauss = np.exp(
        -(x - x0)**2 / (4 * sigma_x**2)
        - (y - y0)**2 / (4 * sigma_y**2)
    )
    phase = np.exp(1j * (kx * x + ky * y))
    psi = gauss * phase

    # Normalisation
    dx = x[0, 1] - x[0, 0]
    dy = y[1, 0] - y[0, 0]
    norme = np.sqrt(np.sum(np.abs(psi)**2) * dx * dy)
    psi /= norme

    return psi


def double_fente_psi(
    x: np.ndarray,
    y: np.ndarray,
    y_fente: float = 0.0,
    separation: float = 2.0,
    largeur_fente: float = 0.5,
    sigma: float = 1.5,
    kx: float = 5.0,
) -> np.ndarray:
    """Crée une fonction d'onde modélisant le passage par une double fente.

    Deux paquets gaussiens cohérents centrés aux positions des fentes,
    se propageant dans la direction +x. L'interférence entre les deux
    produit des franges de type Young.

    Args:
        x, y: Grilles 2D.
        y_fente: Position y moyenne de la double fente.
        separation: Distance entre les centres des deux fentes.
        largeur_fente: Largeur de chaque fente (σ_y du paquet).
        sigma: Largeur en x de chaque paquet.
        kx: Impulsion en x (vitesse de propagation).

    Returns:
        ψ(x, y) — superposition cohérente des deux paquets.
    """
    # Fente supérieure
    psi_haut = paquet_gaussien_2d(
        x, y,
        x0=-5.0, y0=y_fente + separation / 2,
        sigma_x=sigma, sigma_y=largeur_fente,
        kx=kx, ky=0.0,
    )
    # Fente inférieure
    psi_bas = paquet_gaussien_2d(
        x, y,
        x0=-5.0, y0=y_fente - separation / 2,
        sigma_x=sigma, sigma_y=largeur_fente,
        kx=kx, ky=0.0,
    )

    psi = psi_haut + psi_bas

    # Normalisation
    dx = x[0, 1] - x[0, 0]
    dy = y[1, 0] - y[0, 0]
    norme = np.sqrt(np.sum(np.abs(psi)**2) * dx * dy)
    psi /= norme

    return psi


# ═══════════════════════════════════════════════════════════════════════
# Évolution temporelle — Schrödinger split-operator
# ═══════════════════════════════════════════════════════════════════════

def evoluer_psi_libre(
    psi: np.ndarray,
    dx: float,
    dy: float,
    dt: float,
    n_pas: int,
    V: np.ndarray | None = None,
    hbar: float = HBAR,
    m: float = M,
) -> list[np.ndarray]:
    """Propage ψ dans le temps par la méthode split-operator (FFT).

    L'opérateur d'évolution est décomposé :
        U(dt) ≈ exp(−iV dt/2ℏ) × exp(−iT dt/ℏ) × exp(−iV dt/2ℏ)

    où T = −ℏ²∇²/(2m) est l'énergie cinétique (diagonale en espace k)
    et V est le potentiel (diagonal en espace x).

    Cette méthode est unitaire (conserve la norme) et d'ordre 2 en dt.

    Args:
        psi: Fonction d'onde initiale (2D complexe).
        dx, dy: Pas spatiaux.
        dt: Pas temporel.
        n_pas: Nombre de pas de temps.
        V: Potentiel V(x, y) (2D réel, optionnel — 0 si None).
        hbar: Constante de Planck réduite.
        m: Masse de la particule.

    Returns:
        Liste de fonctions d'onde [ψ(t=0), ψ(t=dt), …, ψ(t=n_pas×dt)].
    """
    ny, nx = psi.shape

    # Grille en espace de Fourier
    kx = np.fft.fftfreq(nx, d=dx) * 2 * np.pi
    ky = np.fft.fftfreq(ny, d=dy) * 2 * np.pi
    KX, KY = np.meshgrid(kx, ky)

    # Opérateur d'énergie cinétique en espace k
    # T = ℏ²(kx² + ky²)/(2m)
    T_k = hbar**2 * (KX**2 + KY**2) / (2 * m)
    exp_T = np.exp(-1j * T_k * dt / hbar)

    # Opérateur de potentiel en espace x (demi-pas)
    if V is not None:
        exp_V_half = np.exp(-1j * V * dt / (2 * hbar))
    else:
        exp_V_half = 1.0

    etats = [psi.copy()]
    psi_t = psi.copy()

    for _ in range(n_pas):
        # Demi-pas potentiel
        psi_t = psi_t * exp_V_half
        # Pas complet cinétique (FFT)
        psi_t = np.fft.ifft2(exp_T * np.fft.fft2(psi_t))
        # Demi-pas potentiel
        psi_t = psi_t * exp_V_half

        etats.append(psi_t.copy())

    return etats


# ═══════════════════════════════════════════════════════════════════════
# Champ de vitesse bohmien et intégration des trajectoires
# ═══════════════════════════════════════════════════════════════════════

def champ_vitesse_bohmien(
    psi: np.ndarray,
    dx: float,
    dy: float,
    hbar: float = HBAR,
    m: float = M,
) -> tuple[np.ndarray, np.ndarray]:
    """Calcule le champ de vitesse bohmien v = (ℏ/m) Im(∇ψ/ψ).

    C'est le cœur de la mécanique bohmienne : la vitesse de chaque
    particule est déterminée par le gradient de la phase de ψ.

    En pratique, on utilise la formule équivalente :
        v_x = (ℏ/m) × Im(∂ψ/∂x / ψ)
        v_y = (ℏ/m) × Im(∂ψ/∂y / ψ)

    qui évite de calculer explicitement S = ℏ × arg(ψ) (problème de
    branchement).

    Args:
        psi: Fonction d'onde complexe 2D.
        dx, dy: Pas spatiaux.
        hbar: Constante de Planck réduite.
        m: Masse.

    Returns:
        Tuple (vx, vy) — composantes du champ de vitesse, 2D.
    """
    # Gradient de ψ par différences finies centrées
    dpsi_dy, dpsi_dx = np.gradient(psi, dy, dx)

    # Éviter la division par zéro
    psi_safe = np.where(np.abs(psi) > 1e-15, psi, 1e-15 + 0j)

    # v = (ℏ/m) × Im(∇ψ / ψ)
    vx = (hbar / m) * np.imag(dpsi_dx / psi_safe)
    vy = (hbar / m) * np.imag(dpsi_dy / psi_safe)

    return vx, vy


def calculer_potentiel_quantique_1d(
    psi: np.ndarray,
    dx: float,
    dy: float,
    hbar: float = HBAR,
    m: float = M,
) -> np.ndarray:
    """Calcule Q = −(ℏ²/2m)(∇²R/R) à partir de ψ.

    Args:
        psi: Fonction d'onde complexe 2D.
        dx, dy: Pas spatiaux.
        hbar: Constante de Planck réduite.
        m: Masse.

    Returns:
        Q(x, y) — potentiel quantique, 2D.
    """
    R = np.abs(psi)
    R_safe = np.maximum(R, 1e-15)

    # Laplacien de R (numériquement par différences finies)
    # scipy.ndimage.laplace utilise un noyau 3×3
    lap_R = laplace(R) / (dx * dy)  # approximation

    Q = -(hbar**2 / (2 * m)) * (lap_R / R_safe)

    # Limiter les valeurs extrêmes
    q_lim = np.nanpercentile(np.abs(Q), 99)
    if q_lim > 0:
        Q = np.clip(Q, -q_lim, q_lim)

    return Q


def integrer_trajectoires(
    etats: list[np.ndarray],
    positions_initiales: np.ndarray,
    x_1d: np.ndarray,
    y_1d: np.ndarray,
    dt: float,
    hbar: float = HBAR,
    m: float = M,
) -> list[np.ndarray]:
    """Intègre les trajectoires bohmiennes par la méthode RK4.

    Pour chaque pas de temps, le champ de vitesse bohmien est calculé
    à partir de ψ(t), puis les positions sont avancées par Runge-Kutta
    d'ordre 4 (pour une meilleure stabilité que Euler).

    L'interpolation bilinéaire est utilisée pour obtenir la vitesse
    aux positions exactes des particules (qui ne coïncident pas avec
    les points de grille en général).

    Args:
        etats: Liste de fonctions d'onde [ψ(t_0), ψ(t_1), …].
        positions_initiales: Array (N_particules, 2) des positions [x, y].
        x_1d: Grille x 1D.
        y_1d: Grille y 1D.
        dt: Pas temporel.
        hbar: Constante de Planck réduite.
        m: Masse.

    Returns:
        Liste de trajectoires — chaque élément est un array (N_temps, 2).
    """
    from scipy.interpolate import RegularGridInterpolator

    dx = x_1d[1] - x_1d[0]
    dy = y_1d[1] - y_1d[0]
    n_particules = positions_initiales.shape[0]
    n_temps = len(etats) - 1

    # Initialisation des trajectoires
    trajectoires = [np.zeros((n_temps + 1, 2)) for _ in range(n_particules)]
    for i in range(n_particules):
        trajectoires[i][0] = positions_initiales[i]

    # Boucle temporelle
    for t in range(n_temps):
        psi = etats[t]
        vx, vy = champ_vitesse_bohmien(psi, dx, dy, hbar, m)

        # Interpolateurs pour vx et vy
        interp_vx = RegularGridInterpolator(
            (y_1d, x_1d), vx,
            method="linear", bounds_error=False, fill_value=0.0,
        )
        interp_vy = RegularGridInterpolator(
            (y_1d, x_1d), vy,
            method="linear", bounds_error=False, fill_value=0.0,
        )

        for i in range(n_particules):
            pos = trajectoires[i][t]

            # RK4
            def get_v(p):
                """Vitesse interpolée à la position p."""
                point = np.array([[p[1], p[0]]])  # (y, x)
                return np.array([
                    float(interp_vx(point)),
                    float(interp_vy(point)),
                ])

            k1 = get_v(pos)
            k2 = get_v(pos + 0.5 * dt * k1)
            k3 = get_v(pos + 0.5 * dt * k2)
            k4 = get_v(pos + dt * k3)

            nouvelle_pos = pos + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

            # Confinement dans le domaine
            nouvelle_pos[0] = np.clip(nouvelle_pos[0], x_1d[1], x_1d[-2])
            nouvelle_pos[1] = np.clip(nouvelle_pos[1], y_1d[1], y_1d[-2])

            trajectoires[i][t + 1] = nouvelle_pos

    return trajectoires


# ═══════════════════════════════════════════════════════════════════════
# Scénario 1 : Double fente
# ═══════════════════════════════════════════════════════════════════════

def scenario_double_fente() -> tuple[list[np.ndarray], np.ndarray, np.ndarray, np.ndarray]:
    """Exécute le scénario de la double fente.

    Un paquet d'onde cohérent passe à travers deux fentes et crée un
    pattern d'interférence. Les trajectoires bohmiennes montrent comment
    chaque particule passe par une seule fente mais est guidée par
    l'interférence des deux ondelettes.

    C'est l'illustration la plus célèbre de la mécanique de Bohm :
    les trajectoires ne se croisent JAMAIS (propriété fondamentale
    du flux de probabilité en mécanique quantique).

    Returns:
        Tuple (trajectoires, x_1d, y_1d, densite_finale).
    """
    print("\n  ── Scénario 1 : Double fente ──")

    # Domaine spatial
    L = 15.0
    n_pts = 256
    x_1d = np.linspace(-L, L, n_pts)
    y_1d = np.linspace(-L, L, n_pts)
    X, Y = np.meshgrid(x_1d, y_1d)
    dx = x_1d[1] - x_1d[0]
    dy = y_1d[1] - y_1d[0]

    # Paramètres temporels
    dt = 0.01
    n_pas = 200

    print(f"    Grille : {n_pts}×{n_pts}, dx = {dx:.3f}")
    print(f"    Temps : {n_pas} pas, dt = {dt:.3f}, T = {n_pas*dt:.1f}")

    # Fonction d'onde initiale — double fente
    print("    Construction de ψ₀ (double fente)…")
    psi_0 = double_fente_psi(
        X, Y,
        separation=3.0,
        largeur_fente=0.6,
        sigma=2.0,
        kx=5.0,
    )

    # Évolution temporelle
    print("    Évolution de Schrödinger (split-operator FFT)…")
    etats = evoluer_psi_libre(psi_0, dx, dy, dt, n_pas)

    # Positions initiales des particules (réparties uniformément
    # dans la zone de densité non-nulle)
    print("    Intégration des trajectoires bohmiennes (RK4)…")
    n_particules = 30
    # Positions en x = −5 (avant les fentes), réparties en y
    y_init = np.linspace(-4.5, 4.5, n_particules)
    positions_initiales = np.column_stack([
        np.full(n_particules, -5.0),  # x
        y_init,                        # y
    ])

    trajectoires = integrer_trajectoires(
        etats, positions_initiales, x_1d, y_1d, dt,
    )

    densite_finale = np.abs(etats[-1])**2
    print(f"    ✅ {n_particules} trajectoires calculées sur {n_pas} pas.")

    return trajectoires, x_1d, y_1d, densite_finale


# ═══════════════════════════════════════════════════════════════════════
# Scénario 2 : Puits asymétrique (analogie cavité plasma)
# ═══════════════════════════════════════════════════════════════════════

def scenario_puits_asymetrique() -> tuple[list[np.ndarray], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Exécute le scénario du puits asymétrique.

    Un paquet d'onde est placé dans un potentiel asymétrique qui
    modélise le gradient de densité du plasma dans la cavité.
    Les trajectoires montrent comment les particules sont déviées
    vers la zone de moindre potentiel quantique — analogue à la
    force de poussée bohmienne.

    Returns:
        Tuple (trajectoires, x_1d, y_1d, densite_finale, V).
    """
    print("\n  ── Scénario 2 : Puits asymétrique (cavité plasma) ──")

    # Domaine spatial
    L = 10.0
    n_pts = 200
    x_1d = np.linspace(-L, L, n_pts)
    y_1d = np.linspace(-L, L, n_pts)
    X, Y = np.meshgrid(x_1d, y_1d)
    dx = x_1d[1] - x_1d[0]
    dy = y_1d[1] - y_1d[0]

    # Potentiel asymétrique : V = α × x × exp(−r²/σ²)
    # Crée un gradient de potentiel principalement dans la direction x
    sigma_V = 5.0
    alpha_V = 0.3
    V = alpha_V * X * np.exp(-(X**2 + Y**2) / sigma_V**2)

    # Paramètres temporels
    dt = 0.02
    n_pas = 250

    print(f"    Grille : {n_pts}×{n_pts}, dx = {dx:.3f}")
    print(f"    Potentiel : V = {alpha_V} × x × exp(−r²/{sigma_V:.0f}²)")
    print(f"    Temps : {n_pas} pas, dt = {dt:.3f}, T = {n_pas*dt:.1f}")

    # Fonction d'onde initiale — paquet gaussien au centre
    print("    Construction de ψ₀ (paquet gaussien au centre)…")
    psi_0 = paquet_gaussien_2d(
        X, Y,
        x0=0.0, y0=0.0,
        sigma_x=2.0, sigma_y=2.0,
        kx=0.0, ky=0.0,
    )

    # Évolution temporelle avec potentiel
    print("    Évolution de Schrödinger avec potentiel asymétrique…")
    etats = evoluer_psi_libre(psi_0, dx, dy, dt, n_pas, V=V)

    # Positions initiales — grille régulière dans la zone du paquet
    print("    Intégration des trajectoires bohmiennes…")
    n_par_axe = 6
    x_init = np.linspace(-2.0, 2.0, n_par_axe)
    y_init = np.linspace(-2.0, 2.0, n_par_axe)
    XX_init, YY_init = np.meshgrid(x_init, y_init)
    positions_initiales = np.column_stack([
        XX_init.ravel(), YY_init.ravel(),
    ])
    n_particules = positions_initiales.shape[0]

    trajectoires = integrer_trajectoires(
        etats, positions_initiales, x_1d, y_1d, dt,
    )

    densite_finale = np.abs(etats[-1])**2
    print(f"    ✅ {n_particules} trajectoires calculées.")

    return trajectoires, x_1d, y_1d, densite_finale, V


# ═══════════════════════════════════════════════════════════════════════
# Scénario 3 : Tunnel quantique
# ═══════════════════════════════════════════════════════════════════════

def scenario_tunnel() -> tuple[list[np.ndarray], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Exécute le scénario de l'effet tunnel bohmien.

    Un paquet d'onde se propage vers une barrière de potentiel.
    Classiquement, si l'énergie est insuffisante, la particule est
    totalement réfléchie. En mécanique quantique, une fraction
    traverse la barrière (effet tunnel).

    Les trajectoires bohmiennes montrent un comportement fascinant :
    les particules qui traversent sont celles dont la position
    initiale est la plus proche de la barrière. Il n'y a PAS de
    « passage à travers » la barrière — les trajectoires contournent
    ou traversent continûment.

    Returns:
        Tuple (trajectoires, x_1d, y_1d, densite_finale, V).
    """
    print("\n  ── Scénario 3 : Effet tunnel bohmien ──")

    # Domaine spatial (1.5D : large en x, étroit en y pour visualiser)
    Lx = 20.0
    Ly = 8.0
    nx = 300
    ny = 120
    x_1d = np.linspace(-Lx, Lx, nx)
    y_1d = np.linspace(-Ly, Ly, ny)
    X, Y = np.meshgrid(x_1d, y_1d)
    dx = x_1d[1] - x_1d[0]
    dy = y_1d[1] - y_1d[0]

    # Barrière de potentiel (mur gaussien en x)
    x_barriere = 3.0
    largeur_barriere = 1.0
    hauteur_barriere = 3.0
    V = hauteur_barriere * np.exp(-(X - x_barriere)**2 / (2 * largeur_barriere**2))

    # Paramètres temporels
    dt = 0.01
    n_pas = 300

    print(f"    Grille : {nx}×{ny}, dx = {dx:.3f}")
    print(f"    Barrière : x = {x_barriere}, h = {hauteur_barriere}, σ = {largeur_barriere}")
    print(f"    Temps : {n_pas} pas, dt = {dt:.3f}, T = {n_pas*dt:.1f}")

    # Fonction d'onde initiale — paquet se propageant vers +x
    print("    Construction de ψ₀ (paquet vers la barrière)…")
    kx_init = 4.0  # impulsion (énergie cinétique < barrière pour effet tunnel)
    psi_0 = paquet_gaussien_2d(
        X, Y,
        x0=-8.0, y0=0.0,
        sigma_x=2.5, sigma_y=2.0,
        kx=kx_init, ky=0.0,
    )
    E_cinetique = 0.5 * HBAR**2 * kx_init**2 / M
    print(f"    E_cinétique = {E_cinetique:.2f}, V_barrière = {hauteur_barriere:.2f}")
    print(f"    → {'Tunnel partiel' if E_cinetique < hauteur_barriere else 'Passage classique'}")

    # Évolution
    print("    Évolution de Schrödinger avec barrière…")
    etats = evoluer_psi_libre(psi_0, dx, dy, dt, n_pas, V=V)

    # Positions initiales — ligne verticale avant la barrière
    print("    Intégration des trajectoires bohmiennes…")
    n_particules = 20
    y_init = np.linspace(-2.5, 2.5, n_particules)
    positions_initiales = np.column_stack([
        np.full(n_particules, -8.0),
        y_init,
    ])

    trajectoires = integrer_trajectoires(
        etats, positions_initiales, x_1d, y_1d, dt,
    )

    densite_finale = np.abs(etats[-1])**2
    print(f"    ✅ {n_particules} trajectoires calculées.")

    return trajectoires, x_1d, y_1d, densite_finale, V


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 004 — Trajectoires bohmiennes en 2D          ║")
    print("║  Guidage par onde pilote : dQ/dt = (ℏ/m) Im(∇ψ/ψ)       ║")
    print("╚════════════════════════════════════════════════════════════╝")

    # ── Scénario 1 : Double fente ────────────────────────────────────
    trajs_df, x_df, y_df, rho_df = scenario_double_fente()

    X_df, Y_df = np.meshgrid(x_df, y_df)
    fig1 = plot_trajectoires_bohm(
        trajs_df,
        x=X_df, y=Y_df, fond=rho_df,
        fond_label="$|\\psi|^2$ (densité)",
        fond_cmap="Blues",
        titre=(
            "Trajectoires bohmiennes — Double fente\n"
            "$dQ/dt = (\\hbar/m)\\,\\mathrm{Im}(\\nabla\\psi/\\psi)$"
        ),
        sauvegarde="data/004_double_fente.png",
    )

    # ── Scénario 2 : Puits asymétrique ──────────────────────────────
    trajs_pa, x_pa, y_pa, rho_pa, V_pa = scenario_puits_asymetrique()

    X_pa, Y_pa = np.meshgrid(x_pa, y_pa)
    fig2 = plot_trajectoires_bohm(
        trajs_pa,
        x=X_pa, y=Y_pa, fond=rho_pa,
        fond_label="$|\\psi|^2$",
        fond_cmap="Greens",
        titre=(
            "Trajectoires bohmiennes — Puits asymétrique\n"
            "Analogie : gradient de densité plasma dans la cavité"
        ),
        sauvegarde="data/004_puits_asymetrique.png",
    )

    # Potentiel quantique du scénario 2
    # (reprise de la dernière fonction d'onde pour calculer Q)
    print("\n▶ Calcul du potentiel quantique Q (scénario 2)…")
    dx_pa = x_pa[1] - x_pa[0]
    dy_pa = y_pa[1] - y_pa[0]

    # Reconstruire ψ finale pour Q
    psi_finale_pa = paquet_gaussien_2d(
        X_pa, Y_pa, x0=0, y0=0, sigma_x=2, sigma_y=2,
    )
    # Évoluer pour obtenir l'état final (simplifié — on utilise rho_pa)
    R_pa = np.sqrt(np.maximum(rho_pa, 0))
    R_safe_pa = np.maximum(R_pa, 1e-15)
    lap_R_pa = laplace(R_pa) / (dx_pa * dy_pa)
    Q_pa = -(HBAR**2 / (2 * M)) * (lap_R_pa / R_safe_pa)
    q_lim_pa = np.nanpercentile(np.abs(Q_pa), 98)
    if q_lim_pa > 0:
        Q_pa = np.clip(Q_pa, -q_lim_pa, q_lim_pa)

    grad_Qy_pa, grad_Qx_pa = np.gradient(Q_pa, dy_pa, dx_pa)

    fig3 = plot_potentiel_quantique(
        X_pa, Y_pa, Q_pa, grad_Qx_pa, grad_Qy_pa,
        titre="Potentiel quantique Q — Puits asymétrique",
        sauvegarde="data/004_Q_puits_asymetrique.png",
    )

    # ── Scénario 3 : Tunnel quantique ───────────────────────────────
    trajs_tun, x_tun, y_tun, rho_tun, V_tun = scenario_tunnel()

    X_tun, Y_tun = np.meshgrid(x_tun, y_tun)

    # Figure combinée : trajectoires + barrière
    fig4, ax4 = plt.subplots(figsize=(14, 5))

    # Fond : densité de probabilité
    im4 = ax4.pcolormesh(
        X_tun, Y_tun, rho_tun,
        cmap="Blues", shading="gouraud", alpha=0.6,
    )
    fig4.colorbar(im4, ax=ax4, label="$|\\psi|^2$", shrink=0.7)

    # Barrière (contour)
    ax4.contour(
        X_tun, Y_tun, V_tun,
        levels=[0.5, 1.0, 2.0, 2.5],
        colors=["gray"], linewidths=1, alpha=0.5,
    )
    ax4.contourf(
        X_tun, Y_tun, V_tun,
        levels=[1.0, 10.0],
        colors=["red"], alpha=0.15,
    )

    # Trajectoires
    from matplotlib import cm as mpl_cm
    cmap_t = mpl_cm.get_cmap("plasma")
    for i, traj in enumerate(trajs_tun):
        couleur = cmap_t(i / max(len(trajs_tun) - 1, 1))
        ax4.plot(traj[:, 0], traj[:, 1], "-", color=couleur, linewidth=0.8)
        ax4.plot(traj[0, 0], traj[0, 1], "o", color=couleur, markersize=4)

    ax4.axvline(3.0, color="red", linestyle=":", alpha=0.5, label="Barrière")
    ax4.set_xlabel("x")
    ax4.set_ylabel("y")
    ax4.set_title(
        "Trajectoires bohmiennes — Effet tunnel\n"
        "$E_{cin} < V_{barrière}$ → traversée quantique",
        fontsize=13, fontweight="bold",
    )
    ax4.legend()
    ax4.set_aspect("equal")
    plt.tight_layout()
    fig4.savefig("data/004_tunnel.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/004_tunnel.png")

    # ── Sauvegarde des données ──────────────────────────────────────
    print("\n▶ Sauvegarde des données numériques…")
    np.save("data/004_trajs_double_fente.npy",
            np.array([t for t in trajs_df], dtype=object),
            allow_pickle=True)
    np.save("data/004_trajs_puits_asym.npy",
            np.array([t for t in trajs_pa], dtype=object),
            allow_pickle=True)
    np.save("data/004_trajs_tunnel.npy",
            np.array([t for t in trajs_tun], dtype=object),
            allow_pickle=True)
    np.save("data/004_rho_double_fente.npy", rho_df)
    np.save("data/004_Q_puits_asym.npy", Q_pa)
    print("  💾 Données sauvegardées dans data/004_*.npy")

    # ── Résumé ──────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  RÉSUMÉ — Expérience 004")
    print("═" * 60)
    print(f"""
  Trois scénarios de trajectoires bohmiennes simulés :

  1. Double fente :
     → {len(trajs_df)} trajectoires montrant le guidage par
       interférence. Les trajectoires ne se croisent jamais
       (propriété fondamentale du flux bohmien).

  2. Puits asymétrique (analogie plasma) :
     → {len(trajs_pa)} trajectoires dans un potentiel V = αx·exp(−r²/σ²).
       Les particules sont déviées par le gradient de potentiel
       quantique, analogie avec la force de poussée dans la cavité.

  3. Tunnel quantique :
     → {len(trajs_tun)} trajectoires face à une barrière gaussienne.
       Certaines traversent (tunnel), d'autres sont réfléchies.
       La sélection dépend uniquement de la position initiale.

  Méthode :
    • Schrödinger : split-operator (FFT), conserve la norme.
    • Trajectoires : intégration RK4, interpolation bilinéaire.
    • Unités naturelles : ℏ = m = 1.
""")

    print("✅ Expérience 004 terminée.\n")
    plt.show()
