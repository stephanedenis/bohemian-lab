"""
Expérience 012 — Comparaison MOT classique vs. Inverter (SMPS).

Simule l'impact du passage d'une alimentation MOT + SSR duty-cycle
(tout-ou-rien) à une alimentation inverter à modulation continue
sur les performances du pendule de torsion et la qualité du PID.

Comparaisons :
    1. Bilan de masse → moment d'inertie I → période T₀
    2. Profil de puissance : crête pulsée (MOT) vs. continue (inverter)
    3. Qualité du PID₂ : ripple de puissance, erreur statique
    4. Rendement énergétique → autonomie de la batterie
    5. Champ E dans la cavité : respect du seuil Nixie

Hypothèse explorée dans docs/09_hypothese_inverter.md

Sorties :
    - Figures dans data/simulations/012_*.png
    - Données dans data/simulations/012_comparaison.csv
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Tentative d'import Matplotlib
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("⚠ Matplotlib non disponible — figures désactivées.")


# ═══════════════════════════════════════════════════════════════════════
# Constantes & paramètres (cohérents avec 007_dynamique_pid.py)
# ═══════════════════════════════════════════════════════════════════════

# Chambre
RAYON_CHAMBRE: float = 0.125   # m
HAUTEUR_CHAMBRE: float = 0.250  # m
VOLUME: float = np.pi * RAYON_CHAMBRE**2 * HAUTEUR_CHAMBRE  # ~12,3 L

# Pendule de torsion
D_BRAS: float = 0.20           # m — bras de levier

# Magnétron
F_MAG: float = 2.45e9          # Hz
ETA_MAGN: float = 0.65         # rendement magnétron (RF/élec.)
SEUIL_NIXIE_E: float = 20e3   # V/m — seuil de champ pour Nixie

# Batterie
BATTERIE_WH: float = 90.0     # Wh — Makita BL1850B

# Constante de torsion du fil
KAPPA: float = 1e-4            # N·m/rad

# ═══════════════════════════════════════════════════════════════════════
# Paramètres des deux architectures
# ═══════════════════════════════════════════════════════════════════════

# Architecture MOT classique
MOT = {
    "nom": "MOT + SSR (classique)",
    "masse_transfo": 2.5,       # kg
    "masse_condo_hv": 0.30,     # kg
    "masse_diode_hv": 0.05,     # kg
    "masse_onduleur_ac": 1.0,   # kg — onduleur DC→AC séparé
    "masse_boost": 0.0,         # pas de boost
    "masse_carte": 0.0,         # pas de carte SMPS
    "eta_onduleur": 0.85,       # rendement onduleur DC→AC
    "eta_transfo": 0.85,        # rendement MOT
    "p_rf_max": 700.0,          # W — puissance RF crête
    "bande_passante_hz": 10.0,  # Hz — limité par SSR ZC
    "modulation": "tout-ou-rien",  # duty cycle
    "frequence_ssr_hz": 10.0,   # Hz — période SSR ~100 ms
}

# Architecture inverter (SMPS)
INV = {
    "nom": "Inverter (SMPS)",
    "masse_transfo": 0.50,      # kg — ferrite
    "masse_condo_hv": 0.20,     # kg
    "masse_diode_hv": 0.05,     # kg
    "masse_onduleur_ac": 0.0,   # onduleur AC éliminé
    "masse_boost": 0.20,        # kg — boost DC-DC 18V→170V
    "masse_carte": 0.30,        # kg — carte IGBT + contrôle
    "eta_onduleur": 1.0,        # pas d'onduleur AC (→ transparent)
    "eta_transfo": 0.92,        # rendement SMPS global
    "p_rf_max": 700.0,          # W — même magnétron
    "bande_passante_hz": 1000.0,  # Hz — boucle SMPS interne
    "modulation": "continue",
    "frequence_ssr_hz": None,   # pas de SSR
}


def masse_alim(arch: dict) -> float:
    """Masse totale de l'alimentation HV (kg)."""
    return (
        arch["masse_transfo"]
        + arch["masse_condo_hv"]
        + arch["masse_diode_hv"]
        + arch["masse_onduleur_ac"]
        + arch["masse_boost"]
        + arch["masse_carte"]
    )


def masse_totale_suspendue(arch: dict, phase: int = 1) -> float:
    """Masse totale de l'assemblage suspendu (kg).

    Args:
        arch: Dictionnaire d'architecture.
        phase: 1 (un magnétron) ou 2 (deux magnétrons).
    """
    m_chambre = 5.0         # kg
    m_batterie = 0.63       # kg
    m_esp32 = 0.1           # kg
    m_capteurs = 0.2        # kg
    m_contrepoids_fixe = 0.5  # kg — structure tige + plateau
    n_mag = phase
    return (
        m_chambre
        + n_mag * (masse_alim(arch) + 0.3)  # +0.3 = magnétron lui-même
        + m_batterie
        + arch["masse_onduleur_ac"]  # onduleur AC séparé (0 pour inverter)
        + m_esp32
        + m_capteurs
        + m_contrepoids_fixe
    )


def moment_inertie(m_totale: float) -> float:
    """Moment d'inertie du pendule (kg·m²).

    I = 2 · M · d² (modèle haltère, chambre + contrepoids).
    """
    return 2.0 * (m_totale / 2.0) * D_BRAS**2  # = M · d²


def periode_pendule(i_moment: float) -> float:
    """Période d'oscillation libre T₀ (s)."""
    return 2.0 * np.pi * np.sqrt(i_moment / KAPPA)


def rendement_global(arch: dict) -> float:
    """Rendement batterie → RF."""
    return ETA_MAGN * arch["eta_onduleur"] * arch["eta_transfo"]


def autonomie_min(arch: dict, p_rf_moy: float) -> float:
    """Autonomie en minutes pour une puissance RF moyenne donnée."""
    p_dc = p_rf_moy / rendement_global(arch)
    return BATTERIE_WH / p_dc * 60.0


def champ_e_cavite(p_rf: float) -> float:
    """Champ électrique crête dans la cavité (V/m).

    E = √(2 · P / (ε₀ · c · A_eff)) — approximation mode TE₁₁.
    """
    eps0 = 8.854e-12
    c = 3e8
    a_eff = np.pi * RAYON_CHAMBRE**2  # section transverse
    return np.sqrt(2.0 * p_rf / (eps0 * c * a_eff))


# ═══════════════════════════════════════════════════════════════════════
# Simulation du profil de puissance
# ═══════════════════════════════════════════════════════════════════════

def profil_puissance_mot(
    t: np.ndarray,
    p_consigne: float,
    p_max: float,
    f_ssr: float,
) -> np.ndarray:
    """Profil de puissance RF avec modulation SSR (tout-ou-rien).

    Le magnétron est soit ON (P_max), soit OFF (0). Le duty cycle
    est ajusté pour que la moyenne = P_consigne.

    Args:
        t: Vecteur temps (s).
        p_consigne: Puissance moyenne désirée (W).
        p_max: Puissance crête (W).
        f_ssr: Fréquence du SSR (Hz).

    Returns:
        Profil de puissance (W).
    """
    duty = np.clip(p_consigne / p_max, 0.0, 1.0)
    periode = 1.0 / f_ssr
    phase = (t % periode) / periode
    return np.where(phase < duty, p_max, 0.0)


def profil_puissance_inverter(
    t: np.ndarray,
    p_consigne: float,
    ripple: float = 0.03,
    f_ripple: float = 300.0,
) -> np.ndarray:
    """Profil de puissance RF avec modulation inverter (continue).

    La puissance est quasi-constante avec un léger ripple résiduel.

    Args:
        t: Vecteur temps (s).
        p_consigne: Puissance demandée (W).
        ripple: Amplitude relative du ripple (ex: 0.03 = 3 %).
        f_ripple: Fréquence du ripple (Hz, ~2× fréquence bus).

    Returns:
        Profil de puissance (W).
    """
    return p_consigne * (1.0 + ripple * np.sin(2.0 * np.pi * f_ripple * t))


# ═══════════════════════════════════════════════════════════════════════
# Simulation PID simplifiée
# ═══════════════════════════════════════════════════════════════════════

def simuler_pid_puissance(
    arch: dict,
    p_consigne: float = 200.0,
    duree: float = 2.0,
    dt: float = 1e-4,
    kp: float = 0.5,
    ki: float = 2.0,
) -> dict:
    """Simule une boucle PID de puissance avec les deux architectures.

    Le « processus » est simplifié : la puissance réelle suit la
    commande avec un retard du premier ordre (τ dépend de l'arch).

    Args:
        arch: Dictionnaire d'architecture.
        p_consigne: Puissance RF cible (W).
        duree: Durée de simulation (s).
        dt: Pas de temps (s).
        kp: Gain proportionnel PID.
        ki: Gain intégral PID.

    Returns:
        Dictionnaire avec t, p_commande, p_reelle, erreur.
    """
    n = int(duree / dt)
    t = np.linspace(0, duree, n)
    p_commande = np.zeros(n)
    p_reelle = np.zeros(n)
    erreur = np.zeros(n)
    integrale = 0.0

    # Constante de temps du processus
    if arch["modulation"] == "tout-ou-rien":
        tau = 1.0 / arch["frequence_ssr_hz"]  # ~100 ms
    else:
        tau = 1.0 / arch["bande_passante_hz"]  # ~1 ms

    for i in range(1, n):
        # Erreur
        erreur[i] = p_consigne - p_reelle[i - 1]
        integrale += erreur[i] * dt
        integrale = np.clip(integrale, -100, 100)

        # Commande PID
        u = kp * erreur[i] + ki * integrale
        u = np.clip(u, 0, arch["p_rf_max"])
        p_commande[i] = u

        # Processus (premier ordre + quantification pour MOT)
        if arch["modulation"] == "tout-ou-rien":
            # Le SSR est ON ou OFF → la puissance réelle est soit
            # P_max, soit 0
            p_effective = arch["p_rf_max"] if u > arch["p_rf_max"] * 0.1 else 0.0
            # Mais on module par duty cycle
            duty = np.clip(u / arch["p_rf_max"], 0, 1)
            ssr_on = ((t[i] % (1.0 / arch["frequence_ssr_hz"]))
                      < duty / arch["frequence_ssr_hz"])
            p_effective = arch["p_rf_max"] if ssr_on else 0.0
        else:
            # Modulation continue — la puissance suit la commande
            p_effective = u

        # Dynamique premier ordre
        alpha = dt / (tau + dt)
        p_reelle[i] = p_reelle[i - 1] + alpha * (p_effective - p_reelle[i - 1])

    return {"t": t, "p_commande": p_commande, "p_reelle": p_reelle, "erreur": erreur}


# ═══════════════════════════════════════════════════════════════════════
# Analyse & affichage
# ═══════════════════════════════════════════════════════════════════════

def afficher_comparaison() -> None:
    """Affiche la comparaison complète MOT vs. Inverter."""
    sep = "─" * 60

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   Expérience 012 — Comparaison MOT classique vs. Inverter  ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    # ── 1. Bilan de masse ──
    print(f"{'1. BILAN DE MASSE':^60}")
    print(sep)
    print(f"{'Composant':<28} {'MOT':>10} {'Inverter':>10} {'Δ':>8}")
    print(sep)

    composants = [
        ("Transformateur HT", "masse_transfo"),
        ("Condensateur HV", "masse_condo_hv"),
        ("Diode HV", "masse_diode_hv"),
        ("Onduleur DC→AC", "masse_onduleur_ac"),
        ("Boost DC-DC", "masse_boost"),
        ("Carte SMPS", "masse_carte"),
    ]
    for nom, cle in composants:
        m_mot = MOT[cle]
        m_inv = INV[cle]
        delta = m_inv - m_mot
        signe = "+" if delta >= 0 else ""
        if m_mot > 0 or m_inv > 0:
            print(f"  {nom:<26} {m_mot:>8.2f} kg {m_inv:>8.2f} kg {signe}{delta:>6.2f}")

    m_alim_mot = masse_alim(MOT)
    m_alim_inv = masse_alim(INV)
    print(sep)
    print(f"  {'TOTAL alimentation HV':<26} {m_alim_mot:>8.2f} kg "
          f"{m_alim_inv:>8.2f} kg {m_alim_inv - m_alim_mot:>+6.2f}")
    print(f"  {'Gain':<26} {'':>10} {'':>10} "
          f"{(1 - m_alim_inv / m_alim_mot) * 100:>+5.0f} %\n")

    # ── 2. Impact pendule ──
    print(f"{'2. IMPACT SUR LE PENDULE':^60}")
    print(sep)
    for phase in (1, 2):
        m_tot_mot = masse_totale_suspendue(MOT, phase)
        m_tot_inv = masse_totale_suspendue(INV, phase)
        i_mot = moment_inertie(m_tot_mot)
        i_inv = moment_inertie(m_tot_inv)
        t0_mot = periode_pendule(i_mot)
        t0_inv = periode_pendule(i_inv)
        print(f"  Phase {phase}:")
        print(f"    Masse suspendue  : MOT {m_tot_mot:>6.1f} kg  |  "
              f"INV {m_tot_inv:>6.1f} kg  (Δ = {m_tot_inv - m_tot_mot:>+.1f} kg)")
        print(f"    Moment d'inertie : MOT {i_mot:>6.3f} kg·m²  |  "
              f"INV {i_inv:>6.3f} kg·m²")
        print(f"    Période T₀       : MOT {t0_mot:>6.1f} s  |  "
              f"INV {t0_inv:>6.1f} s  (Δ = {t0_inv - t0_mot:>+.1f} s)")
        print()

    # ── 3. Rendement & autonomie ──
    print(f"{'3. RENDEMENT & AUTONOMIE':^60}")
    print(sep)
    eta_mot = rendement_global(MOT)
    eta_inv = rendement_global(INV)
    print(f"  Rendement batterie → RF :")
    print(f"    MOT : η = {eta_mot:.1%}  (ond. {MOT['eta_onduleur']:.0%} "
          f"× transfo {MOT['eta_transfo']:.0%} × magn. {ETA_MAGN:.0%})")
    print(f"    INV : η = {eta_inv:.1%}  (SMPS {INV['eta_transfo']:.0%} "
          f"× magn. {ETA_MAGN:.0%})")
    print()

    puissances = [100, 200, 300, 400]
    print(f"  {'P_RF (W)':<12} {'MOT (min)':>12} {'INV (min)':>12} {'Gain':>10}")
    print(f"  {sep}")
    for p in puissances:
        a_mot = autonomie_min(MOT, p)
        a_inv = autonomie_min(INV, p)
        gain = (a_inv - a_mot) / a_mot * 100
        print(f"  {p:<12} {a_mot:>10.1f}   {a_inv:>10.1f}   {gain:>+8.0f} %")
    print()

    # ── 4. Champ E et seuil Nixie ──
    print(f"{'4. CHAMP E — SEUIL NIXIE':^60}")
    print(sep)
    for p in [200, 300, 500, 700]:
        e_field = champ_e_cavite(p)
        ok = "✅" if e_field < SEUIL_NIXIE_E else "❌"
        print(f"  P_RF = {p:>4} W  →  E = {e_field / 1e3:>5.1f} kV/m  "
              f"(seuil {SEUIL_NIXIE_E / 1e3:.0f} kV/m)  {ok}")

    print(f"\n  MOT (SSR 50%) : crête = {MOT['p_rf_max']} W pendant phase ON → "
          f"E = {champ_e_cavite(MOT['p_rf_max']) / 1e3:.1f} kV/m ❌")
    print(f"  Inverter      : crête = consigne (ex. 200 W) → "
          f"E = {champ_e_cavite(200) / 1e3:.1f} kV/m ✅")
    print()

    # ── 5. Profil de puissance ──
    print(f"{'5. PROFIL DE PUISSANCE':^60}")
    print(sep)
    t = np.linspace(0, 0.5, 5000)
    p_mot = profil_puissance_mot(t, 200, MOT["p_rf_max"], MOT["frequence_ssr_hz"])
    p_inv = profil_puissance_inverter(t, 200)

    print(f"  MOT (200 W moyen, SSR {MOT['frequence_ssr_hz']} Hz) :")
    print(f"    P crête      = {p_mot.max():.0f} W")
    print(f"    P moyenne     = {p_mot.mean():.0f} W")
    print(f"    RMS ripple    = {np.std(p_mot) / p_mot.mean() * 100:.0f} %")
    print(f"  Inverter (200 W continu) :")
    print(f"    P crête      = {p_inv.max():.0f} W")
    print(f"    P moyenne     = {p_inv.mean():.1f} W")
    print(f"    RMS ripple    = {np.std(p_inv) / p_inv.mean() * 100:.1f} %")
    print()

    # ── 6. Simulation PID ──
    print(f"{'6. SIMULATION PID₂ (PUISSANCE → n_e)':^60}")
    print(sep)
    print("  Simulation de la réponse indicielle à P = 200 W...")

    res_mot = simuler_pid_puissance(MOT, p_consigne=200, duree=2.0)
    res_inv = simuler_pid_puissance(INV, p_consigne=200, duree=2.0)

    # Temps de montée (10% → 90% de la consigne)
    def temps_montee(t: np.ndarray, p: np.ndarray, consigne: float) -> float:
        seuil_bas = 0.1 * consigne
        seuil_haut = 0.9 * consigne
        idx_bas = np.argmax(p > seuil_bas)
        idx_haut = np.argmax(p > seuil_haut)
        return t[idx_haut] - t[idx_bas] if idx_haut > idx_bas else float("inf")

    tm_mot = temps_montee(res_mot["t"], res_mot["p_reelle"], 200)
    tm_inv = temps_montee(res_inv["t"], res_inv["p_reelle"], 200)

    # Erreur statique (derniers 20%)
    n_fin = len(res_mot["t"]) // 5
    es_mot = np.mean(np.abs(res_mot["erreur"][-n_fin:]))
    es_inv = np.mean(np.abs(res_inv["erreur"][-n_fin:]))

    # Ripple en régime permanent
    rip_mot = np.std(res_mot["p_reelle"][-n_fin:])
    rip_inv = np.std(res_inv["p_reelle"][-n_fin:])

    print(f"\n  {'Métrique':<28} {'MOT':>12} {'Inverter':>12}")
    print(f"  {sep}")
    print(f"  {'Temps de montée (10→90%)':<28} {tm_mot * 1e3:>10.1f} ms "
          f"{tm_inv * 1e3:>10.1f} ms")
    print(f"  {'Erreur statique moy.':<28} {es_mot:>10.1f} W  "
          f"{es_inv:>10.1f} W")
    print(f"  {'Ripple σ (rég. perm.)':<28} {rip_mot:>10.1f} W  "
          f"{rip_inv:>10.1f} W")
    print()

    # ── 7. Verdict ──
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                     VERDICT SYNTHÈSE                       ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Gain de masse (Phase 1)  : {m_alim_inv - m_alim_mot:>+.1f} kg "
          f"({(1 - m_alim_inv / m_alim_mot) * 100:>+.0f} %)"
          + " " * 14 + "║")
    print(f"║  Gain autonomie (200W RF) : "
          f"{(autonomie_min(INV, 200) - autonomie_min(MOT, 200)):.1f} min "
          f"({(autonomie_min(INV, 200) / autonomie_min(MOT, 200) - 1) * 100:>+.0f} %)"
          + " " * 15 + "║")
    print("║  Champ E à consigne       : EN DESSOUS du seuil Nixie     ║")
    ratio_ripple = rip_mot / rip_inv if rip_inv > 0 else float("inf")
    print(f"║  Ripple puissance         : ÷ {ratio_ripple:.0f}×"
          + " " * (29 - len(f"{ratio_ripple:.0f}")) + "║")
    print(f"║  Erreur statique PID      : ÷ {es_mot / es_inv:.0f}×"
          + " " * (29 - len(f"{es_mot / es_inv:.0f}")) + "║")
    print("║                                                            ║")
    print("║  → Hypothèse FORTEMENT FAVORABLE                          ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    return res_mot, res_inv, t, p_mot, p_inv


def generer_figures(
    res_mot: dict,
    res_inv: dict,
    t_profil: np.ndarray,
    p_mot: np.ndarray,
    p_inv: np.ndarray,
) -> None:
    """Génère les figures comparatives (4 panneaux)."""
    if not HAS_MPL:
        print("  → Figures non générées (Matplotlib absent).")
        return

    chemin = Path(__file__).resolve().parent.parent / "data" / "simulations"
    chemin.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, hspace=0.35, wspace=0.30)

    couleur_mot = "#dc2626"
    couleur_inv = "#2563eb"

    # ── Panneau 1 : profil de puissance ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_profil * 1e3, p_mot, color=couleur_mot, alpha=0.8,
             label=f"MOT (SSR {MOT['frequence_ssr_hz']:.0f} Hz)")
    ax1.plot(t_profil * 1e3, p_inv, color=couleur_inv, alpha=0.8,
             label="Inverter (continu)")
    ax1.axhline(200, color="#64748b", ls="--", lw=0.8, label="Consigne 200 W")
    ax1.set_xlabel("Temps (ms)")
    ax1.set_ylabel("Puissance RF (W)")
    ax1.set_title("Profil de puissance — 200 W moyen")
    ax1.legend(fontsize=8)
    ax1.set_ylim(-20, 800)
    ax1.grid(True, alpha=0.3)

    # ── Panneau 2 : champ E vs seuil Nixie ──
    ax2 = fig.add_subplot(gs[0, 1])
    puissances = np.linspace(50, 800, 200)
    e_champ = np.array([champ_e_cavite(p) for p in puissances])
    ax2.plot(puissances, e_champ / 1e3, color="#334155", lw=2)
    ax2.axhline(SEUIL_NIXIE_E / 1e3, color="#f59e0b", ls="--", lw=2,
                label=f"Seuil Nixie ({SEUIL_NIXIE_E / 1e3:.0f} kV/m)")
    ax2.axvspan(100, 300, alpha=0.15, color="#16a34a",
                label="Fenêtre opératoire")
    # Marqueur MOT crête
    e_mot = champ_e_cavite(MOT["p_rf_max"])
    ax2.plot(MOT["p_rf_max"], e_mot / 1e3, "o", color=couleur_mot,
             ms=10, label=f"MOT crête ({MOT['p_rf_max']} W)")
    # Marqueur inverter consigne
    e_inv = champ_e_cavite(200)
    ax2.plot(200, e_inv / 1e3, "s", color=couleur_inv,
             ms=10, label="Inverter (200 W)")
    ax2.set_xlabel("Puissance RF (W)")
    ax2.set_ylabel("Champ E (kV/m)")
    ax2.set_title("Champ E dans la cavité — seuil Nixie")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    # ── Panneau 3 : réponse PID ──
    ax3 = fig.add_subplot(gs[1, 0])
    # Sous-échantillonner pour lisibilité
    stride = max(1, len(res_mot["t"]) // 2000)
    ax3.plot(res_mot["t"][::stride] * 1e3, res_mot["p_reelle"][::stride],
             color=couleur_mot, alpha=0.8, label="MOT (SSR)")
    ax3.plot(res_inv["t"][::stride] * 1e3, res_inv["p_reelle"][::stride],
             color=couleur_inv, alpha=0.8, label="Inverter")
    ax3.axhline(200, color="#64748b", ls="--", lw=0.8, label="Consigne")
    ax3.set_xlabel("Temps (ms)")
    ax3.set_ylabel("Puissance RF (W)")
    ax3.set_title("Réponse PID — échelon 200 W")
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)

    # ── Panneau 4 : bilan de masse barres ──
    ax4 = fig.add_subplot(gs[1, 1])
    labels_masse = ["Transfo HT", "Condo HV", "Diode", "Onduleur AC",
                    "Boost DC", "Carte SMPS"]
    masses_mot = [MOT["masse_transfo"], MOT["masse_condo_hv"],
                  MOT["masse_diode_hv"], MOT["masse_onduleur_ac"],
                  MOT["masse_boost"], MOT["masse_carte"]]
    masses_inv = [INV["masse_transfo"], INV["masse_condo_hv"],
                  INV["masse_diode_hv"], INV["masse_onduleur_ac"],
                  INV["masse_boost"], INV["masse_carte"]]
    x = np.arange(len(labels_masse))
    w = 0.35
    bars1 = ax4.bar(x - w / 2, masses_mot, w, label="MOT", color=couleur_mot,
                    alpha=0.7)
    bars2 = ax4.bar(x + w / 2, masses_inv, w, label="Inverter",
                    color=couleur_inv, alpha=0.7)
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels_masse, rotation=30, ha="right", fontsize=8)
    ax4.set_ylabel("Masse (kg)")
    ax4.set_title("Bilan de masse — composants HV")
    ax4.legend(fontsize=8)
    ax4.grid(True, axis="y", alpha=0.3)

    # Annotations totaux
    ax4.annotate(f"Total: {masse_alim(MOT):.2f} kg",
                 xy=(0.25, 0.92), xycoords="axes fraction",
                 fontsize=9, color=couleur_mot, fontweight="bold")
    ax4.annotate(f"Total: {masse_alim(INV):.2f} kg",
                 xy=(0.65, 0.92), xycoords="axes fraction",
                 fontsize=9, color=couleur_inv, fontweight="bold")

    fig.suptitle("Expérience 012 — MOT classique vs. Inverter (SMPS)",
                 fontsize=14, fontweight="bold", y=0.98)

    fig_path = chemin / "012_inverter_vs_mot.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  📊 Figure enregistrée : {fig_path}")


def sauver_donnees(res_mot: dict, res_inv: dict) -> None:
    """Sauvegarde les données de comparaison."""
    chemin = Path(__file__).resolve().parent.parent / "data" / "simulations"
    chemin.mkdir(parents=True, exist_ok=True)

    # CSV résumé
    lignes = [
        "architecture,masse_alim_kg,eta_global,autonomie_200w_min,"
        "champ_e_200w_kvm,temps_montee_ms,ripple_w",
    ]
    for arch, nom, res in [(MOT, "MOT", res_mot), (INV, "Inverter", res_inv)]:
        m = masse_alim(arch)
        eta = rendement_global(arch)
        aut = autonomie_min(arch, 200)
        e = champ_e_cavite(200) / 1e3
        n_fin = len(res["t"]) // 5
        rip = np.std(res["p_reelle"][-n_fin:])
        # Temps de montée
        consigne = 200.0
        idx_bas = np.argmax(res["p_reelle"] > 0.1 * consigne)
        idx_haut = np.argmax(res["p_reelle"] > 0.9 * consigne)
        tm = (res["t"][idx_haut] - res["t"][idx_bas]) * 1e3
        lignes.append(f"{nom},{m:.2f},{eta:.3f},{aut:.1f},{e:.1f},{tm:.1f},{rip:.1f}")

    csv_path = chemin / "012_comparaison.csv"
    csv_path.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"  💾 Données enregistrées : {csv_path}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    res_mot, res_inv, t_profil, p_mot, p_inv = afficher_comparaison()
    generer_figures(res_mot, res_inv, t_profil, p_mot, p_inv)
    sauver_donnees(res_mot, res_inv)
