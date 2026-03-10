"""
Expérience 008 — Analyse de sensibilité et faux positifs sur η.

Monte Carlo de propagation d'incertitudes sur le facteur de mérite :
    η = F_net / (P_abs / c) = κ · θ_max / (L · P_abs / c)

où :
    - κ    : constante de rappel du pendule (N·m/rad)
    - θ_max : amplitude angulaire mesurée (rad)
    - L    : bras de levier (m)
    - P_abs : puissance absorbée par le plasma (W)
    - c    : vitesse de la lumière (m/s)

Objectifs :
    1. Quantifier l'incertitude sur η en propageant les δ de chaque variable.
    2. Estimer les forces parasites (faux positifs, §4.1) :
       - Vent ionique F_ion (nul en chambre fermée, mais fuites possibles)
       - Effet Crookes F_crookes (gradient thermique + pression résiduelle)
       - Force de Laplace F_laplace (courant × champ magnétique terrestre)
    3. Déterminer la résolution minimale du pendule pour η > 1 à 3σ.
    4. Construire la matrice de décision (§4.6) :
       η < 1     → hypothèse infirmée
       η ≈ 1     → effets classiques seulement
       1 < η < 10 → résultat intéressant, investigation
       η > 10    → anomalie, vérification systématique

Sorties :
    - Figures dans data/008_*.png
    - Données dans data/008_*.csv et .npz
"""
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ═══════════════════════════════════════════════════════════════════════
# Constantes physiques
# ═══════════════════════════════════════════════════════════════════════

C_LUMIERE: float = 2.998e8       # Vitesse de la lumière (m/s)
K_B: float = 1.38e-23            # Constante de Boltzmann (J/K)
MU_0: float = 4 * np.pi * 1e-7  # Perméabilité du vide (H/m)
B_TERRE: float = 50e-6           # Champ magnétique terrestre (T)

# Paramètres nominaux du pendule (§3.6)
KAPPA: float = 1e-5         # Constante de rappel (N·m/rad)
L_BRAS: float = 0.2         # Bras de levier (m)
I_PENDULE: float = 0.5      # Moment d'inertie (kg·m²)
Q_MEC: float = 50           # Facteur de qualité mécanique
T_0: float = 2 * np.pi * np.sqrt(I_PENDULE / KAPPA)  # ≈ 444 s

# Paramètres de la cavité (§2.4, §3.2)
P_MAGNETRON: float = 1000.0   # Puissance magnétron (W)
ETA_COUPLAGE: float = 0.3     # Efficacité de couplage RF → plasma
P_ABS_NOM: float = P_MAGNETRON * ETA_COUPLAGE  # ≈ 300 W

# Force de pression de radiation classique
F_RAD: float = P_ABS_NOM / C_LUMIERE  # ≈ 1,0 µN


# ═══════════════════════════════════════════════════════════════════════
# 1) Calcul de η et propagation d'incertitudes
# ═══════════════════════════════════════════════════════════════════════

def calculer_eta(
    kappa: float,
    theta_max: float,
    l_bras: float,
    p_abs: float,
) -> float:
    """Calcule le facteur de mérite η.

    η = F_net / F_rad = (κ · θ_max / L) / (P_abs / c)

    Args:
        kappa: Constante de rappel du pendule (N·m/rad).
        theta_max: Amplitude angulaire maximale (rad).
        l_bras: Bras de levier (m).
        p_abs: Puissance absorbée (W).

    Returns:
        Facteur de mérite η (sans unité).
    """
    f_net = kappa * theta_max / l_bras  # Force nette (N)
    f_rad = p_abs / C_LUMIERE           # Pression de radiation (N)
    return f_net / f_rad


def propagation_incertitudes_analytique(
    kappa: float,
    theta_max: float,
    l_bras: float,
    p_abs: float,
    delta_kappa: float,
    delta_theta: float,
    delta_l: float,
    delta_p: float,
) -> tuple[float, float]:
    """Propagation analytique (premier ordre) de l'incertitude sur η.

    σ_η² = η² · [(δκ/κ)² + (δθ/θ)² + (δL/L)² + (δP/P)²]

    Args:
        kappa, theta_max, l_bras, p_abs: Valeurs nominales.
        delta_kappa, delta_theta, delta_l, delta_p: Incertitudes (1σ).

    Returns:
        Tuple (η, σ_η).
    """
    eta = calculer_eta(kappa, theta_max, l_bras, p_abs)
    var_relative = (
        (delta_kappa / kappa) ** 2
        + (delta_theta / theta_max) ** 2
        + (delta_l / l_bras) ** 2
        + (delta_p / p_abs) ** 2
    )
    sigma_eta = eta * np.sqrt(var_relative)
    return eta, sigma_eta


def monte_carlo_eta(
    n_tirages: int = 100_000,
    kappa_nom: float = KAPPA,
    theta_nom: float = 5e-6,
    l_nom: float = L_BRAS,
    p_nom: float = P_ABS_NOM,
    delta_kappa_rel: float = 0.10,
    delta_theta_rel: float = 0.20,
    delta_l_rel: float = 0.02,
    delta_p_rel: float = 0.10,
    seed: int = 42,
) -> dict:
    """Monte Carlo : tire les paramètres et calcule la distribution de η.

    Chaque paramètre suit une loi log-normale (positif par construction)
    avec coefficient de variation (CV) donné.

    Args:
        n_tirages: Nombre de tirages.
        kappa_nom: Valeur nominale de κ (N·m/rad).
        theta_nom: Amplitude angulaire nominale (rad).
        l_nom: Bras de levier nominal (m).
        p_nom: Puissance absorbée nominale (W).
        delta_*_rel: Incertitudes relatives (σ/μ).
        seed: Graine du générateur aléatoire.

    Returns:
        Dict avec eta_values, percentiles, statistiques.
    """
    rng = np.random.default_rng(seed)

    # Log-normale : µ_ln = ln(µ) − σ_ln²/2, σ_ln² = ln(1 + CV²)
    def tirer_lognorm(nom: float, cv: float, n: int) -> np.ndarray:
        if cv <= 0:
            return np.full(n, nom)
        sigma_ln = np.sqrt(np.log(1 + cv**2))
        mu_ln = np.log(nom) - sigma_ln**2 / 2
        return rng.lognormal(mu_ln, sigma_ln, n)

    kappas = tirer_lognorm(kappa_nom, delta_kappa_rel, n_tirages)
    thetas = tirer_lognorm(theta_nom, delta_theta_rel, n_tirages)
    ls = tirer_lognorm(l_nom, delta_l_rel, n_tirages)
    ps = tirer_lognorm(p_nom, delta_p_rel, n_tirages)

    etas = calculer_eta(kappas, thetas, ls, ps)

    return {
        "eta_values": etas,
        "mean": np.mean(etas),
        "median": np.median(etas),
        "std": np.std(etas),
        "p5": np.percentile(etas, 5),
        "p25": np.percentile(etas, 25),
        "p75": np.percentile(etas, 75),
        "p95": np.percentile(etas, 95),
        "p99": np.percentile(etas, 99),
        "prob_eta_gt_1": np.mean(etas > 1) * 100,
        "prob_eta_gt_10": np.mean(etas > 10) * 100,
        "kappas": kappas,
        "thetas": thetas,
        "ls": ls,
        "ps": ps,
    }


# ═══════════════════════════════════════════════════════════════════════
# 2) Estimation des forces parasites (faux positifs, §4.1)
# ═══════════════════════════════════════════════════════════════════════

def force_vent_ionique(
    n_e: float = 7.4e16,
    t_e_ev: float = 2.0,
    a_surface: float = 0.01,
    fraction_fuite: float = 0.01,
) -> float:
    """Force de vent ionique (pression d'ions accélérés).

    Dans une chambre fermée, l'élan total des ions est nul (conservation
    de la quantité de mouvement). La force résiduelle vient uniquement
    des fuites ou des asymétries géométriques.

    F_ion ≈ fraction_fuite × n_e · k_B · T_e · A

    Args:
        n_e: Densité électronique (m⁻³).
        t_e_ev: Température électronique (eV).
        a_surface: Surface effective de l'asymétrie (m²).
        fraction_fuite: Fraction de dissymétrie (0 à 1).

    Returns:
        Force du vent ionique résiduel (N).
    """
    t_e_j = t_e_ev * 1.60e-19  # eV → J
    # Pression cinétique des ions
    p_ion = n_e * K_B * (t_e_ev * 11604.5)  # n·k_B·T_e
    return fraction_fuite * p_ion * a_surface


def force_crookes(
    p_mbar: float = 3.0,
    delta_t: float = 10.0,
    t_gaz: float = 400.0,
    a_surface: float = 0.005,
) -> float:
    """Force de Crookes (radiomètre de Crookes, gradient thermique).

    F_Crookes ≈ (P / T) · ΔT · A ≈ P · (ΔT/T) · A

    Pertinente à basse pression (1–10 mbar) avec gradient thermique.

    Args:
        p_mbar: Pression (mbar).
        delta_t: Gradient de température (K).
        t_gaz: Température du gaz (K).
        a_surface: Surface du pendule exposée (m²).

    Returns:
        Force de Crookes (N).
    """
    p_pa = p_mbar * 100  # mbar → Pa
    return p_pa * (delta_t / t_gaz) * a_surface


def force_laplace(
    courant: float = 0.01,
    longueur: float = 0.1,
    b_champ: float = B_TERRE,
) -> float:
    """Force de Laplace (courant × champ magnétique).

    F = I · L · B · sin(θ)

    Courant résiduel traversant le fil du pendule dans le champ terrestre.

    Args:
        courant: Courant de fuite (A).
        longueur: Longueur effective du conducteur (m).
        b_champ: Champ magnétique (T).

    Returns:
        Force de Laplace (N).
    """
    return courant * longueur * b_champ


def bilan_forces_parasites(verbose: bool = True) -> dict:
    """Calcule toutes les forces parasites et les compare à F_rad.

    Returns:
        Dict avec f_ion, f_crookes, f_laplace, f_total, f_rad, eta_parasites.
    """
    f_ion = force_vent_ionique()
    f_crk = force_crookes()
    f_lap = force_laplace()
    f_total = f_ion + f_crk + f_lap
    f_rad = F_RAD

    eta_par = f_total / f_rad

    if verbose:
        print("  Forces parasites estimées :")
        print(f"    Vent ionique  : {f_ion*1e6:.3f} µN")
        print(f"    Crookes       : {f_crk*1e6:.3f} µN")
        print(f"    Laplace       : {f_lap*1e6:.3f} µN")
        print(f"    ────────────────────────────")
        print(f"    Total faux +  : {f_total*1e6:.3f} µN")
        print(f"    F_rad (P/c)   : {f_rad*1e6:.3f} µN")
        print(f"    η_parasites   : {eta_par:.3f}")

    return {
        "f_ion": f_ion,
        "f_crookes": f_crk,
        "f_laplace": f_lap,
        "f_total": f_total,
        "f_rad": f_rad,
        "eta_parasites": eta_par,
    }


# ═══════════════════════════════════════════════════════════════════════
# 3) Résolution minimale du pendule pour η > 1 à 3σ
# ═══════════════════════════════════════════════════════════════════════

def resolution_minimale(
    eta_cible: float = 1.0,
    n_sigma: float = 3.0,
    kappa: float = KAPPA,
    l_bras: float = L_BRAS,
    p_abs: float = P_ABS_NOM,
    delta_kappa_rel: float = 0.10,
    delta_p_rel: float = 0.10,
) -> dict:
    """Détermine θ_min tel que η − n_σ · σ_η > η_cible.

    En supposant que l'incertitude dominante est δθ :
        η = κ·θ/(L·P/c)
        Pour η − n_σ·σ_η ≥ η_cible, avec σ_η ≈ η·δθ/θ (approximation),
        on obtient θ_min ≈ η_cible · L · P_abs / (c · κ) / (1 − n_σ · CV_θ)

    Args:
        eta_cible: Seuil η à dépasser (défaut 1.0).
        n_sigma: Nombre de sigmas (défaut 3).
        kappa: Constante de rappel (N·m/rad).
        l_bras: Bras de levier (m).
        p_abs: Puissance absorbée (W).
        delta_kappa_rel: Incertitude relative sur κ.
        delta_p_rel: Incertitude relative sur P_abs.

    Returns:
        Dict avec theta_min, f_min, eta_nominal, eta_3sigma.
    """
    f_rad = p_abs / C_LUMIERE  # Force de radiation (N)

    # θ pour η_cible = 1 exactement :
    theta_eta1 = eta_cible * l_bras * f_rad / kappa

    # Avec l'incertitude combinée κ et P
    cv_combinee = np.sqrt(delta_kappa_rel**2 + delta_p_rel**2)
    # Pour que η_lower = η − n_σ·σ_η ≥ η_cible :
    # η ≥ η_cible / (1 − n_σ · CV)  (si n_σ·CV < 1)
    facteur = 1.0 / (1.0 - n_sigma * cv_combinee)
    theta_min = theta_eta1 * facteur

    f_min = kappa * theta_min / l_bras

    eta_nominal = calculer_eta(kappa, theta_min, l_bras, p_abs)

    return {
        "theta_min_rad": theta_min,
        "theta_min_urad": theta_min * 1e6,
        "f_min_uN": f_min * 1e6,
        "eta_nominal": eta_nominal,
        "facteur_securite": facteur,
        "cv_combinee": cv_combinee,
    }


# ═══════════════════════════════════════════════════════════════════════
# 4) Matrice de décision (§4.6)
# ═══════════════════════════════════════════════════════════════════════

def classifier_eta(eta: float, sigma_eta: float) -> str:
    """Classifie un résultat η selon la matrice de décision §4.6.

    Args:
        eta: Facteur de mérite mesuré.
        sigma_eta: Incertitude (1σ).

    Returns:
        Classification textuelle.
    """
    eta_lower = eta - 3 * sigma_eta
    eta_upper = eta + 3 * sigma_eta

    if eta_upper < 1.0:
        return "INFIRMÉ (η + 3σ < 1)"
    elif eta_lower < 1.0:
        return "INDÉCIS (η ± 3σ chevauche 1)"
    elif eta_lower >= 1.0 and eta < 10.0:
        return "INTÉRESSANT (1 < η < 10 à 3σ)"
    elif eta >= 10.0:
        return "ANOMALIE (η > 10) → vérification systématique"
    else:
        return "CLASSIQUE (η ≈ 1)"


def matrice_decision(
    eta_values: np.ndarray,
    theta_values: np.ndarray,
) -> dict:
    """Construit la matrice de décision pour un scan de θ.

    Args:
        eta_values: Array de η pour chaque θ.
        theta_values: Array de θ correspondant.

    Returns:
        Dict avec classifications et seuils.
    """
    classifications = []
    for eta_v in eta_values:
        # Estimation grossière de sigma_eta (CV ~ 20 %)
        sigma = 0.20 * eta_v
        classifications.append(classifier_eta(eta_v, sigma))

    return {
        "theta_values": theta_values,
        "eta_values": eta_values,
        "classifications": classifications,
    }


# ═══════════════════════════════════════════════════════════════════════
# 5) Scan de sensibilité avec budget d'erreur
# ═══════════════════════════════════════════════════════════════════════

def budget_erreur(
    kappa: float = KAPPA,
    theta: float = 5e-6,
    l_bras: float = L_BRAS,
    p_abs: float = P_ABS_NOM,
    delta_kappa_rel: float = 0.10,
    delta_theta_rel: float = 0.20,
    delta_l_rel: float = 0.02,
    delta_p_rel: float = 0.10,
) -> dict:
    """Décompose le budget d'erreur sur η par source.

    Contribution de chaque source :
        (σ_η/η)² = (δκ/κ)² + (δθ/θ)² + (δL/L)² + (δP/P)²

    Returns:
        Dict avec contributions relatives et absolues.
    """
    eta = calculer_eta(kappa, theta, l_bras, p_abs)

    sources = {
        "κ (constante de rappel)": delta_kappa_rel,
        "θ (amplitude angulaire)": delta_theta_rel,
        "L (bras de levier)": delta_l_rel,
        "P_abs (puissance absorbée)": delta_p_rel,
    }

    total_var = sum(cv**2 for cv in sources.values())
    sigma_eta = eta * np.sqrt(total_var)

    contributions = {}
    for nom, cv in sources.items():
        contributions[nom] = {
            "cv": cv * 100,  # %
            "part_variance": cv**2 / total_var * 100,  # %
            "sigma_eta_partiel": eta * cv,
        }

    return {
        "eta": eta,
        "sigma_eta": sigma_eta,
        "sigma_rel": sigma_eta / eta * 100,
        "contributions": contributions,
    }


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import csv

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 008 — Analyse de sensibilité sur η           ║")
    print("║  Monte Carlo, faux positifs et matrice de décision       ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    # ── Étape 1 : Paramètres nominaux ────────────────────────────────
    print("▶ Paramètres nominaux")
    print(f"    κ     = {KAPPA:.0e} N·m/rad")
    print(f"    L     = {L_BRAS} m")
    print(f"    P_abs = {P_ABS_NOM:.0f} W (η_couplage = {ETA_COUPLAGE})")
    print(f"    F_rad = P/c = {F_RAD*1e6:.2f} µN")
    print(f"    T₀    = {T_0:.0f} s ≈ {T_0/60:.1f} min")

    # ── Étape 2 : Bilan des forces parasites ─────────────────────────
    print("\n▶ Bilan des forces parasites (§4.1)")
    parasites = bilan_forces_parasites(verbose=True)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    noms = ["Vent ionique\n(résiduel)", "Effet Crookes\n(∆T)", "Force Laplace\n(I×B)"]
    forces = [parasites["f_ion"] * 1e6,
              parasites["f_crookes"] * 1e6,
              parasites["f_laplace"] * 1e6]
    couleurs = ["#e74c3c", "#f39c12", "#3498db"]

    barres = ax1.bar(noms, forces, color=couleurs, edgecolor="black", linewidth=0.5)
    ax1.axhline(F_RAD * 1e6, color="green", linestyle="--", linewidth=2,
                label=f"$F_{{rad}}$ = P/c = {F_RAD*1e6:.2f} µN")
    ax1.set_ylabel("Force (µN)")
    ax1.set_title(
        "Expérience 008 — Bilan des forces parasites (faux positifs)\n"
        "Estimation des biais systématiques vs. pression de radiation",
        fontsize=12, fontweight="bold",
    )
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis="y")

    # Annotations
    for barre, f in zip(barres, forces):
        ax1.annotate(f"{f:.3f} µN", xy=(barre.get_x() + barre.get_width() / 2,
                     barre.get_height()), ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    fig1.savefig("data/008_forces_parasites.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/008_forces_parasites.png")

    # ── Étape 3 : Budget d'erreur nominal ──────────────────────────
    print("\n▶ Budget d'erreur sur η (θ = 5 µrad)")
    theta_nominal = 5e-6  # rad (amplitude attendue pour η ≈ 5)
    budget = budget_erreur(theta=theta_nominal)

    print(f"    η nominal     = {budget['eta']:.2f}")
    print(f"    σ_η           = {budget['sigma_eta']:.2f}")
    print(f"    σ_η / η       = {budget['sigma_rel']:.1f} %")
    print("    Contributions au budget :")
    for nom, contrib in budget["contributions"].items():
        print(f"      {nom:30s} : CV = {contrib['cv']:.0f} %, "
              f"part = {contrib['part_variance']:.0f} %")

    # Diagramme en camembert
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 6))

    labels_budget = list(budget["contributions"].keys())
    parts = [v["part_variance"] for v in budget["contributions"].values()]
    couleurs_budget = ["#e74c3c", "#2ecc71", "#3498db", "#9b59b6"]

    ax2a.pie(parts, labels=labels_budget, autopct="%1.0f%%",
             colors=couleurs_budget, startangle=140,
             wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax2a.set_title("Répartition du budget d'erreur\n"
                   f"(σ_η/η = {budget['sigma_rel']:.0f} %)",
                   fontsize=12, fontweight="bold")

    # Barres de contribution absolue
    sigmas_partiels = [v["sigma_eta_partiel"] for v in budget["contributions"].values()]
    ax2b.barh(labels_budget, sigmas_partiels, color=couleurs_budget,
              edgecolor="black", linewidth=0.5)
    ax2b.set_xlabel("σ_η (contribution partielle)")
    ax2b.set_title("Contributions absolues à σ_η", fontsize=12, fontweight="bold")
    ax2b.grid(True, alpha=0.3, axis="x")

    plt.tight_layout()
    fig2.savefig("data/008_budget_erreur.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/008_budget_erreur.png")

    # ── Étape 4 : Monte Carlo ──────────────────────────────────────
    print("\n▶ Monte Carlo (N = 100 000 tirages)")
    mc = monte_carlo_eta(n_tirages=100_000, theta_nom=theta_nominal)

    print(f"    η moyen     = {mc['mean']:.2f}")
    print(f"    η médian    = {mc['median']:.2f}")
    print(f"    σ_η (MC)    = {mc['std']:.2f}")
    print(f"    IC 90 %     = [{mc['p5']:.2f}, {mc['p95']:.2f}]")
    print(f"    IC 99 %     = [{np.percentile(mc['eta_values'], 0.5):.2f}, "
          f"{mc['p99']:.2f}]")
    print(f"    P(η > 1)    = {mc['prob_eta_gt_1']:.1f} %")
    print(f"    P(η > 10)   = {mc['prob_eta_gt_10']:.1f} %")

    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(16, 6))

    # Histogramme de η
    counts, bins, patches = ax3a.hist(
        mc["eta_values"], bins=200, density=True,
        color="#3498db", alpha=0.7, edgecolor="none",
    )
    ax3a.axvline(mc["mean"], color="red", linestyle="-", linewidth=2,
                  label=f"Moyenne = {mc['mean']:.2f}")
    ax3a.axvline(mc["p5"], color="orange", linestyle="--",
                  label=f"IC 90 % : [{mc['p5']:.2f}, {mc['p95']:.2f}]")
    ax3a.axvline(mc["p95"], color="orange", linestyle="--")
    ax3a.axvline(1.0, color="green", linestyle=":", linewidth=2,
                  label="η = 1 (seuil classique)")
    ax3a.set_xlabel("η")
    ax3a.set_ylabel("Densité de probabilité")
    ax3a.set_title(
        "Distribution Monte Carlo de η\n"
        f"(N = 100 000, θ_nom = {theta_nominal*1e6:.0f} µrad)",
        fontsize=12, fontweight="bold",
    )
    ax3a.legend(fontsize=9)
    ax3a.grid(True, alpha=0.3)

    # Scatterplot κ vs θ coloré par η
    subsample = np.random.choice(len(mc["kappas"]), 5000, replace=False)
    scatter = ax3b.scatter(
        mc["kappas"][subsample] * 1e5,
        mc["thetas"][subsample] * 1e6,
        c=mc["eta_values"][subsample],
        cmap="plasma", s=2, alpha=0.5,
        vmin=0, vmax=min(20, mc["p99"]),
    )
    plt.colorbar(scatter, ax=ax3b, label="η")
    ax3b.set_xlabel("κ (×10⁻⁵ N·m/rad)")
    ax3b.set_ylabel("θ_max (µrad)")
    ax3b.set_title("Espace des paramètres (κ, θ) → η",
                    fontsize=12, fontweight="bold")
    ax3b.grid(True, alpha=0.3)

    plt.tight_layout()
    fig3.savefig("data/008_monte_carlo.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/008_monte_carlo.png")

    # ── Étape 5 : Résolution minimale ──────────────────────────────
    print("\n▶ Résolution minimale pour η > 1 à 3σ")
    res_min = resolution_minimale()

    print(f"    θ_min        = {res_min['theta_min_urad']:.2f} µrad")
    print(f"    F_min        = {res_min['f_min_uN']:.3f} µN")
    print(f"    η_nominal    = {res_min['eta_nominal']:.2f}")
    print(f"    Facteur de sécurité = {res_min['facteur_securite']:.2f}")

    # ── Étape 6 : Matrice de décision ──────────────────────────────
    print("\n▶ Matrice de décision (§4.6)")

    theta_scan = np.logspace(-7, -4, 50)  # 0,1 µrad → 100 µrad
    eta_scan = calculer_eta(KAPPA, theta_scan, L_BRAS, P_ABS_NOM)
    matrice = matrice_decision(eta_scan, theta_scan)

    fig4, ax4 = plt.subplots(figsize=(14, 7))

    # Zones de classification
    ax4.axhspan(0, 1, alpha=0.15, color="red", label="η < 1 : INFIRMÉ")
    ax4.axhspan(1, 10, alpha=0.15, color="orange", label="1 < η < 10 : INTÉRESSANT")
    ax4.axhspan(10, 100, alpha=0.15, color="green", label="η > 10 : ANOMALIE")

    # Courbe η(θ)
    ax4.loglog(theta_scan * 1e6, eta_scan, "b-", linewidth=2.5,
               label="η(θ) nominal")

    # Bande d'incertitude (±1σ, CV = 25 %)
    cv_total = 0.25
    ax4.fill_between(
        theta_scan * 1e6,
        eta_scan * (1 - cv_total),
        eta_scan * (1 + cv_total),
        alpha=0.2, color="blue", label=f"±{cv_total*100:.0f} % (1σ)",
    )
    ax4.fill_between(
        theta_scan * 1e6,
        eta_scan * (1 - 3 * cv_total),
        eta_scan * (1 + 3 * cv_total),
        alpha=0.08, color="blue", label=f"±{3*cv_total*100:.0f} % (3σ)",
    )

    # Marqueurs
    ax4.axhline(1, color="gray", linestyle=":", linewidth=1)
    ax4.axhline(10, color="gray", linestyle=":", linewidth=1)

    # Résolution minimale
    ax4.axvline(res_min["theta_min_urad"], color="red", linestyle="--",
                label=f"θ_min = {res_min['theta_min_urad']:.1f} µrad (η > 1 à 3σ)")

    # Force parasite équivalente
    theta_parasite = parasites["f_total"] * L_BRAS / KAPPA
    eta_parasite = calculer_eta(KAPPA, theta_parasite, L_BRAS, P_ABS_NOM)
    ax4.axvline(theta_parasite * 1e6, color="purple", linestyle="-.",
                label=f"θ faux positifs = {theta_parasite*1e6:.2f} µrad "
                      f"(η_par = {eta_parasite:.2f})")

    ax4.set_xlabel("Amplitude angulaire θ_max (µrad)")
    ax4.set_ylabel("Facteur de mérite η")
    ax4.set_title(
        "Expérience 008 — Matrice de décision η(θ)\n"
        "Classification du résultat selon le §4.6 du protocole",
        fontsize=13, fontweight="bold",
    )
    ax4.legend(loc="upper left", fontsize=9)
    ax4.grid(True, alpha=0.3, which="both")
    ax4.set_xlim(theta_scan[0] * 1e6, theta_scan[-1] * 1e6)
    ax4.set_ylim(0.01, 200)

    plt.tight_layout()
    fig4.savefig("data/008_matrice_decision.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/008_matrice_decision.png")

    # ── Sauvegarde des données ───────────────────────────────────────
    print("\n▶ Sauvegarde des données")

    # MC distribution
    np.savez(
        "data/008_monte_carlo.npz",
        eta_values=mc["eta_values"],
        kappas=mc["kappas"],
        thetas=mc["thetas"],
        ps=mc["ps"],
    )
    print("  💾 Distribution MC → data/008_monte_carlo.npz")

    # Matrice de décision
    with open("data/008_matrice_decision.csv", "w", newline="",
              encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["theta_rad", "theta_urad", "eta", "classification"])
        for j in range(len(matrice["theta_values"])):
            writer.writerow([
                f"{matrice['theta_values'][j]:.6e}",
                f"{matrice['theta_values'][j]*1e6:.4f}",
                f"{matrice['eta_values'][j]:.4f}",
                matrice["classifications"][j],
            ])
    print("  💾 Matrice de décision → data/008_matrice_decision.csv")

    # Forces parasites
    with open("data/008_forces_parasites.csv", "w", newline="",
              encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "force_N", "force_uN", "eta_equivalent"])
        for nom, f_val in [
            ("Vent ionique", parasites["f_ion"]),
            ("Crookes", parasites["f_crookes"]),
            ("Laplace", parasites["f_laplace"]),
            ("Total parasites", parasites["f_total"]),
            ("Radiation P/c", parasites["f_rad"]),
        ]:
            eta_eq = f_val / parasites["f_rad"]
            writer.writerow([nom, f"{f_val:.6e}", f"{f_val*1e6:.4f}",
                            f"{eta_eq:.4f}"])
    print("  💾 Forces parasites → data/008_forces_parasites.csv")

    # ── Résumé ──────────────────────────────────────────────────────
    classification_nominale = classifier_eta(mc["mean"], mc["std"])

    print("\n" + "═" * 60)
    print("  RÉSUMÉ — Expérience 008")
    print("═" * 60)
    print(f"""
  Facteur de mérite :
    η = F_net / (P_abs / c) = κ·θ_max / (L · P_abs / c)

  Paramètres nominaux :
    κ = {KAPPA:.0e} N·m/rad,  L = {L_BRAS} m,  P_abs = {P_ABS_NOM:.0f} W
    F_rad = P/c = {F_RAD*1e6:.2f} µN

  Monte Carlo (N = 100 000, θ = {theta_nominal*1e6:.0f} µrad) :
    η = {mc['mean']:.2f} ± {mc['std']:.2f}
    IC 90 % = [{mc['p5']:.2f}, {mc['p95']:.2f}]
    P(η > 1) = {mc['prob_eta_gt_1']:.0f} %
    Classification : {classification_nominale}

  Forces parasites (faux positifs) :
    Total = {parasites['f_total']*1e6:.3f} µN
    η_parasites = {parasites['eta_parasites']:.3f}
    → {'Négligeable' if parasites['eta_parasites'] < 0.1 
       else 'À surveiller' if parasites['eta_parasites'] < 0.5 
       else 'CRITIQUE — correction nécessaire'}

  Résolution minimale (η > 1 à 3σ) :
    θ_min = {res_min['theta_min_urad']:.1f} µrad
    F_min = {res_min['f_min_uN']:.2f} µN

  Budget d'erreur (contribution dominante) :
    {"θ (amplitude)" if budget['contributions']['θ (amplitude angulaire)']['part_variance'] > 40 
     else "κ (constante de rappel)"}
    → Priorité : réduire l'incertitude sur cette mesure.

  Matrice de décision (§4.6) :
    ┌───────────────┬───────────────────────────────────┐
    │  η < 1        │ Hypothèse bohmienne infirmée      │
    │  η ≈ 1        │ Effets classiques seulement       │
    │  1 < η < 10   │ Résultat intéressant              │
    │  η > 10       │ Anomalie → vérification           │
    └───────────────┴───────────────────────────────────┘
""")
    print("✅ Expérience 008 terminée.\n")
    plt.show()
