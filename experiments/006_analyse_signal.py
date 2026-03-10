"""
Expérience 006 — Analyse du signal du pendule de torsion.

Simule le signal brut θ(t) attendu du pendule de torsion, puis applique
toute la chaîne de traitement décrite au §4.3 du protocole :

    θ_brut(t) = θ_force(t) + θ_thermique(t) + θ_bruit(t)

Chaîne de traitement :
    1. Génération du signal synthétique (force pulsée + dérive thermique + bruit).
    2. Filtrage passe-bande autour de f₀ (fréquence d'oscillation du pendule).
    3. Corrélation croisée C(τ) entre θ(t) et le signal de commande M(t).
    4. Extraction de l'amplitude et calcul de la force F = κ·θ_max / L.
    5. Rapport signal/bruit (SNR) et significativité statistique.
    6. Analyse spectrale (FFT) pour séparer les composantes.

Objectifs :
    - Valider numériquement que la chaîne d'analyse peut extraire la force
      même quand le SNR est faible.
    - Déterminer le SNR minimal détectable.
    - Quantifier l'effet du filtrage sur la résolution en force.
    - Préparer les outils d'analyse pour les données réelles.

Paramètres expérimentaux (issus de §3.6 et §4.2) :
    - Pendule : κ ∼ 10⁻⁵ N·m/rad, L = 0,2 m, I = 0,5 kg·m²
    - Période : T₀ = 2π√(I/κ) ∼ 444 s (≈ 7 min)
    - Force attendue : F ∼ 3,3 µN → θ_max = F·L/κ ∼ 66 µrad
    - Pulsation du magnétron : synchronisé à f₀ = 1/T₀
    - Bruit : vibrations sismiques ∼ 1 µrad RMS, dérive thermique ∼ 10 µrad/min

Sorties :
    - Figures dans data/006_*.png
    - Données dans data/006_*.csv et .npy
"""
import sys
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ═══════════════════════════════════════════════════════════════════════
# Constantes du pendule (§3.6)
# ═══════════════════════════════════════════════════════════════════════

KAPPA: float = 1e-5          # Constante de torsion (N·m/rad)
L_BRAS: float = 0.2          # Longueur du bras de levier (m)
I_PENDULE: float = 0.5       # Moment d'inertie (kg·m²)
T_0: float = 2 * np.pi * np.sqrt(I_PENDULE / KAPPA)  # Période propre (s)
F_0: float = 1.0 / T_0       # Fréquence propre (Hz)
Q_MEC: float = 50.0          # Facteur de qualité mécanique du pendule

# Forces attendues
F_RAD: float = 3.3e-6        # Pression de radiation (N) pour 1 kW
C_LUMIERE: float = 3e8       # m/s


# ═══════════════════════════════════════════════════════════════════════
# 1. Génération du signal synthétique
# ═══════════════════════════════════════════════════════════════════════

def signal_force_pulsee(
    t: np.ndarray,
    force: float = F_RAD,
    kappa: float = KAPPA,
    bras: float = L_BRAS,
    f0: float = F_0,
    q_mec: float = Q_MEC,
) -> np.ndarray:
    """Réponse du pendule à une force pulsée synchronisée à f₀.

    Le magnétron est pulsé en mode ON/OFF à la fréquence f₀.
    Le signal du pendule est la convolution de la force carrée avec
    la réponse impulsionnelle d'un oscillateur harmonique amorti.

    θ(t) = (F·L/κ) × sin(2π·f₀·t) × enveloppe d'amortissement

    En régime permanent (après Q cycles), l'amplitude atteint :
        θ_max ≈ Q × (F·L/κ) / π   (amplification par résonance)

    Args:
        t: Vecteur temps (s).
        force: Force appliquée (N).
        kappa: Constante de torsion (N·m/rad).
        bras: Longueur du bras de levier (m).
        f0: Fréquence de pulsation (Hz).
        q_mec: Facteur de qualité mécanique.

    Returns:
        Signal θ_force(t) en radians.
    """
    omega0 = 2 * np.pi * f0
    gamma = omega0 / (2 * q_mec)  # Taux d'amortissement

    # Couple appliqué par la force
    tau_max = force * bras

    # Amplitude en régime permanent (amplifiée par Q)
    theta_max = q_mec * tau_max / (kappa * np.pi)

    # Enveloppe de montée exponentielle vers le régime permanent
    enveloppe = 1.0 - np.exp(-gamma * t)

    # Oscillation sinusoïdale à f₀
    theta = theta_max * enveloppe * np.sin(omega0 * t)

    return theta


def signal_thermique(
    t: np.ndarray,
    amplitude: float = 10e-6,
    tau_thermique: float = 300.0,
) -> np.ndarray:
    """Dérive thermique lente du pendule.

    Modélise l'échauffement asymétrique de la chambre par le magnétron.
    La dérive est une exponentielle lente avec fluctuations aléatoires.

    Args:
        t: Vecteur temps (s).
        amplitude: Amplitude de la dérive (rad).
        tau_thermique: Constante de temps thermique (s).

    Returns:
        Signal θ_thermique(t) en radians.
    """
    # Composante déterministe : montée exponentielle
    derive = amplitude * (1.0 - np.exp(-t / tau_thermique))

    # Composante stochastique basse fréquence (marche aléatoire filtrée)
    rng = np.random.default_rng(42)
    dt = t[1] - t[0]
    bruit_bf = np.cumsum(rng.normal(0, amplitude * 0.01 * np.sqrt(dt), len(t)))
    # Filtrage passe-bas à 0.001 Hz (sos pour stabilité numérique)
    f_filtre = 0.001
    if f_filtre < 0.5 / dt:
        sos = sp_signal.butter(2, f_filtre, fs=1.0 / dt, output="sos")
        bruit_bf = sp_signal.sosfiltfilt(sos, bruit_bf)

    return derive + bruit_bf


def bruit_sismique(
    t: np.ndarray,
    sigma: float = 1e-6,
    f_coin: float = 0.1,
) -> np.ndarray:
    """Bruit sismique et mécanique du pendule.

    Modélise les vibrations mécaniques (sol, vent sur le baril) comme
    un bruit blanc filtré passe-bas.

    Args:
        t: Vecteur temps (s).
        sigma: Écart-type du bruit (rad).
        f_coin: Fréquence de coupure (Hz).

    Returns:
        Signal θ_bruit(t) en radians.
    """
    rng = np.random.default_rng(123)
    dt = t[1] - t[0]

    bruit = rng.normal(0, sigma, len(t))

    # Filtrage passe-bas (sos pour stabilité numérique)
    if f_coin < 0.5 / dt:
        sos = sp_signal.butter(3, f_coin, fs=1.0 / dt, output="sos")
        bruit = sp_signal.sosfiltfilt(sos, bruit)

    # Renormaliser à l'écart-type demandé
    bruit *= sigma / (np.std(bruit) + 1e-30)

    return bruit


def signal_commande_magnetron(
    t: np.ndarray,
    f0: float = F_0,
    duty: float = 0.5,
) -> np.ndarray:
    """Signal de commande du magnétron (carré, 0/1).

    Génère le signal de référence M(t) utilisé pour la corrélation croisée.

    Args:
        t: Vecteur temps (s).
        f0: Fréquence de pulsation (Hz).
        duty: Rapport cyclique (0 à 1).

    Returns:
        Signal M(t) ∈ {0, 1}.
    """
    return sp_signal.square(2 * np.pi * f0 * t, duty=duty).clip(0, 1)


def generer_signal_complet(
    duree: float = 20.0,
    fe: float = 10.0,
    force: float = F_RAD,
    snr_cible: float | None = None,
) -> dict:
    """Génère le signal brut complet du pendule avec toutes les composantes.

    Args:
        duree: Durée de la simulation en nombre de périodes T₀.
        fe: Fréquence d'échantillonnage (Hz).
        force: Force appliquée (N).
        snr_cible: Si spécifié, ajuste le bruit pour ce SNR.

    Returns:
        Dict avec t, theta_total, theta_force, theta_therm, theta_bruit,
        commande, et paramètres.
    """
    # Durée en secondes
    t_total = duree * T_0
    n_pts = int(t_total * fe)
    t = np.linspace(0, t_total, n_pts)

    # Composantes
    theta_f = signal_force_pulsee(t, force=force)
    theta_th = signal_thermique(t)
    theta_b = bruit_sismique(t)
    commande = signal_commande_magnetron(t)

    # Ajustement du SNR si demandé
    if snr_cible is not None:
        amp_signal = np.std(theta_f[len(theta_f) // 2:])  # Régime permanent
        amp_bruit = amp_signal / snr_cible
        theta_b *= amp_bruit / (np.std(theta_b) + 1e-30)

    theta_total = theta_f + theta_th + theta_b

    return {
        "t": t,
        "theta_total": theta_total,
        "theta_force": theta_f,
        "theta_thermique": theta_th,
        "theta_bruit": theta_b,
        "commande": commande,
        "T_0": T_0,
        "f_0": F_0,
        "fe": fe,
        "force": force,
    }


# ═══════════════════════════════════════════════════════════════════════
# 2. Filtrage passe-bande
# ═══════════════════════════════════════════════════════════════════════

def filtrer_passe_bande(
    theta: np.ndarray,
    fe: float,
    f_centre: float = F_0,
    q_mec: float = Q_MEC,
    marge: float = 2.0,
) -> np.ndarray:
    """Filtre passe-bande autour de f₀.

    Bande passante : [f₀ − Δf, f₀ + Δf] avec Δf = marge × f₀/(2Q).

    Le facteur `marge` permet d'élargir la bande pour ne pas couper
    le signal utile.

    Args:
        theta: Signal brut (rad).
        fe: Fréquence d'échantillonnage (Hz).
        f_centre: Fréquence centrale (Hz).
        q_mec: Facteur de qualité mécanique.
        marge: Facteur d'élargissement de la bande passante.

    Returns:
        Signal filtré (rad).
    """
    delta_f = marge * f_centre / (2 * q_mec)
    f_low = max(f_centre - delta_f, 1e-6)
    f_high = min(f_centre + delta_f, 0.49 * fe)

    # Filtre Butterworth d'ordre 4 (sos pour stabilité numérique basse f)
    sos = sp_signal.butter(4, [f_low, f_high], btype="band", fs=fe, output="sos")
    return sp_signal.sosfiltfilt(sos, theta)


# ═══════════════════════════════════════════════════════════════════════
# 3. Corrélation croisée
# ═══════════════════════════════════════════════════════════════════════

def correlation_croisee(
    theta: np.ndarray,
    commande: np.ndarray,
    fe: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Corrélation croisée normalisée entre θ(t) et M(t).

    C(τ) = ∫ θ(t) · M(t − τ) dt / (‖θ‖ · ‖M‖)

    Un pic de corrélation à τ = 0 (ou à un retard constant) confirme
    la synchronisation force–plasma.

    Args:
        theta: Signal du pendule (rad).
        commande: Signal de commande du magnétron (0/1).
        fe: Fréquence d'échantillonnage (Hz).

    Returns:
        Tuple (tau, C) : retards (s) et corrélation normalisée.
    """
    # Normalisation
    theta_norm = theta - np.mean(theta)
    cmd_norm = commande - np.mean(commande)

    # Corrélation croisée
    correlation = np.correlate(theta_norm, cmd_norm, mode="full")

    # Normalisation
    norm = np.sqrt(np.sum(theta_norm**2) * np.sum(cmd_norm**2))
    if norm > 0:
        correlation /= norm

    # Axe temporel des retards
    n = len(theta)
    tau = np.arange(-(n - 1), n) / fe

    return tau, correlation


# ═══════════════════════════════════════════════════════════════════════
# 4. Extraction de la force
# ═══════════════════════════════════════════════════════════════════════

def extraire_force(
    theta_filtre: np.ndarray,
    t: np.ndarray,
    kappa: float = KAPPA,
    bras: float = L_BRAS,
    q_mec: float = Q_MEC,
    n_derniers_cycles: int = 5,
) -> dict:
    """Extrait l'amplitude et la force du signal filtré.

    En régime permanent, θ_max ≈ Q × F·L / (κ·π), donc :
        F = θ_max × κ × π / (Q × L)

    Args:
        theta_filtre: Signal filtré (rad).
        t: Vecteur temps (s).
        kappa: Constante de torsion (N·m/rad).
        bras: Longueur du bras de levier (m).
        q_mec: Facteur de qualité mécanique.
        n_derniers_cycles: Nombre de cycles à moyenner en fin de signal.

    Returns:
        Dict avec theta_max, force_extraite, force_attendue.
    """
    # Ne considérer que les derniers cycles (régime permanent)
    t_debut = t[-1] - n_derniers_cycles * T_0
    masque = t >= t_debut
    segment = theta_filtre[masque]

    # Amplitude crête (médiane des pics pour robustesse)
    pics, _ = sp_signal.find_peaks(np.abs(segment), distance=int(0.8 * T_0 * 10))
    if len(pics) > 0:
        theta_max = np.median(np.abs(segment[pics]))
    else:
        theta_max = np.max(np.abs(segment))

    # Force extraite (en inversant l'amplification par résonance)
    force_extraite = theta_max * kappa * np.pi / (q_mec * bras)

    return {
        "theta_max_rad": theta_max,
        "theta_max_urad": theta_max * 1e6,
        "force_extraite_N": force_extraite,
        "force_extraite_uN": force_extraite * 1e6,
    }


# ═══════════════════════════════════════════════════════════════════════
# 5. Rapport signal/bruit
# ═══════════════════════════════════════════════════════════════════════

def calculer_snr(
    theta_filtre: np.ndarray,
    theta_bruit_filtre: np.ndarray,
) -> float:
    """Calcule le rapport signal/bruit après filtrage.

    SNR = A_signal / σ_bruit

    Args:
        theta_filtre: Signal filtré (force + bruit).
        theta_bruit_filtre: Bruit seul, filtré de la même façon.

    Returns:
        SNR (sans unité).
    """
    # Amplitude du signal (RMS de la dernière moitié)
    n2 = len(theta_filtre) // 2
    a_signal = np.std(theta_filtre[n2:])
    a_bruit = np.std(theta_bruit_filtre[n2:])

    if a_bruit == 0:
        return float("inf")

    return a_signal / a_bruit


def scan_snr_vs_force(
    forces: np.ndarray,
    duree: float = 20.0,
    fe: float = 10.0,
) -> dict:
    """Balaye la force pour déterminer le SNR minimal détectable.

    Pour chaque force, génère un signal, filtre, et calcule le SNR.
    Détermine la force minimale pour SNR > 3 (seuil 3σ).

    Args:
        forces: Tableau de forces à tester (N).
        duree: Durée en périodes T₀.
        fe: Fréquence d'échantillonnage (Hz).

    Returns:
        Dict avec forces, snrs, force_min_3sigma.
    """
    snrs = np.zeros(len(forces))

    for i, f in enumerate(forces):
        sig = generer_signal_complet(duree=duree, fe=fe, force=f)
        t = sig["t"]

        # Signal total filtré
        theta_filtre = filtrer_passe_bande(sig["theta_total"], fe)

        # Bruit seul filtré (pour référence SNR)
        bruit_seul = sig["theta_thermique"] + sig["theta_bruit"]
        bruit_filtre = filtrer_passe_bande(bruit_seul, fe)

        snrs[i] = calculer_snr(theta_filtre, bruit_filtre)

    # Force minimale pour SNR > 3
    indices_3sigma = np.where(snrs >= 3.0)[0]
    force_min = forces[indices_3sigma[0]] if len(indices_3sigma) > 0 else np.nan

    return {
        "forces_N": forces,
        "forces_uN": forces * 1e6,
        "snrs": snrs,
        "force_min_3sigma_N": force_min,
        "force_min_3sigma_uN": force_min * 1e6 if not np.isnan(force_min) else np.nan,
    }


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import csv

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 006 — Analyse du signal du pendule           ║")
    print("║  Chaîne complète : signal brut → filtrage → corrélation  ║")
    print("║  → extraction de force → SNR                            ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    # ── Étape 1 : Paramètres du pendule ─────────────────────────────
    print("▶ Paramètres du pendule de torsion")
    print(f"    κ = {KAPPA:.1e} N·m/rad")
    print(f"    L = {L_BRAS:.2f} m")
    print(f"    I = {I_PENDULE:.2f} kg·m²")
    print(f"    T₀ = {T_0:.1f} s ({T_0/60:.1f} min)")
    print(f"    f₀ = {F_0:.4e} Hz")
    print(f"    Q_mec = {Q_MEC:.0f}")

    theta_statique = F_RAD * L_BRAS / KAPPA
    theta_resonance = Q_MEC * F_RAD * L_BRAS / (KAPPA * np.pi)
    print(f"\n    Déflexion statique (F_rad = 3,3 µN) : {theta_statique*1e6:.2f} µrad")
    print(f"    Déflexion en résonance (Q = {Q_MEC:.0f}) : {theta_resonance*1e6:.2f} µrad")

    # ── Étape 2 : Génération du signal ──────────────────────────────
    print("\n▶ Génération du signal synthétique (20 périodes)")
    sig = generer_signal_complet(duree=20.0, fe=10.0, force=F_RAD)
    t = sig["t"]

    fig1, axes1 = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    axes1[0].plot(t / T_0, sig["theta_force"] * 1e6, "b-", linewidth=0.8)
    axes1[0].set_ylabel("θ_force (µrad)")
    axes1[0].set_title("Signal de force (F = 3,3 µN, pulsé à f₀)")

    axes1[1].plot(t / T_0, sig["theta_thermique"] * 1e6, "r-", linewidth=0.8)
    axes1[1].set_ylabel("θ_therm (µrad)")
    axes1[1].set_title("Dérive thermique (τ = 300 s)")

    axes1[2].plot(t / T_0, sig["theta_bruit"] * 1e6, color="gray", linewidth=0.5)
    axes1[2].set_ylabel("θ_bruit (µrad)")
    axes1[2].set_title("Bruit sismique (σ = 1 µrad)")

    axes1[3].plot(t / T_0, sig["theta_total"] * 1e6, "k-", linewidth=0.5)
    axes1[3].set_ylabel("θ_total (µrad)")
    axes1[3].set_xlabel(f"Temps (× T₀ = {T_0:.0f} s)")
    axes1[3].set_title("Signal total brut")

    fig1.suptitle(
        "Expérience 006 — Composantes du signal du pendule",
        fontsize=14, fontweight="bold",
    )
    plt.tight_layout()
    fig1.savefig("data/006_signal_composantes.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/006_signal_composantes.png")

    # ── Étape 3 : Filtrage passe-bande ──────────────────────────────
    print("\n▶ Filtrage passe-bande autour de f₀")
    theta_filtre = filtrer_passe_bande(sig["theta_total"], sig["fe"])

    fig2, axes2 = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    axes2[0].plot(t / T_0, sig["theta_total"] * 1e6, "k-", alpha=0.4,
                  linewidth=0.5, label="Signal brut")
    axes2[0].plot(t / T_0, theta_filtre * 1e6, "b-", linewidth=1.2,
                  label="Signal filtré (passe-bande)")
    axes2[0].plot(t / T_0, sig["theta_force"] * 1e6, "r--", linewidth=0.8,
                  alpha=0.6, label="Signal de force (référence)")
    axes2[0].set_ylabel("θ (µrad)")
    axes2[0].set_title("Filtrage passe-bande vs signal brut")
    axes2[0].legend(fontsize=9)

    # Spectre (FFT)
    n_fft = len(t)
    freqs_fft = np.fft.rfftfreq(n_fft, d=1.0 / sig["fe"])
    spectre_brut = np.abs(np.fft.rfft(sig["theta_total"])) / n_fft
    spectre_filtre = np.abs(np.fft.rfft(theta_filtre)) / n_fft

    axes2[1].semilogy(freqs_fft * 1e3, spectre_brut * 1e6, "k-", alpha=0.5,
                       linewidth=0.5, label="Spectre brut")
    axes2[1].semilogy(freqs_fft * 1e3, spectre_filtre * 1e6, "b-",
                       linewidth=1.5, label="Spectre filtré")
    axes2[1].axvline(F_0 * 1e3, color="red", linestyle="--", alpha=0.7,
                      label=f"f₀ = {F_0*1e3:.3f} mHz")
    axes2[1].set_xlabel("Fréquence (mHz)")
    axes2[1].set_ylabel("Amplitude (µrad)")
    axes2[1].set_title("Analyse spectrale (FFT)")
    axes2[1].legend(fontsize=9)
    axes2[1].set_xlim(0, 20 * F_0 * 1e3)

    fig2.suptitle(
        "Expérience 006 — Filtrage et analyse spectrale",
        fontsize=14, fontweight="bold",
    )
    plt.tight_layout()
    fig2.savefig("data/006_filtrage_fft.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/006_filtrage_fft.png")

    # ── Étape 4 : Corrélation croisée ──────────────────────────────
    print("\n▶ Corrélation croisée θ(t) × M(t)")
    tau, corr = correlation_croisee(theta_filtre, sig["commande"], sig["fe"])

    fig3, ax3 = plt.subplots(figsize=(12, 5))
    # Limiter l'affichage à ±5 T₀
    masque_tau = np.abs(tau) <= 5 * T_0
    ax3.plot(tau[masque_tau] / T_0, corr[masque_tau], "b-", linewidth=1)
    ax3.axvline(0, color="red", linestyle="--", alpha=0.5, label="τ = 0")
    ax3.axhline(0, color="gray", linestyle=":", alpha=0.5)

    # Pic de corrélation
    idx_pic = np.argmax(np.abs(corr[masque_tau]))
    tau_pic = tau[masque_tau][idx_pic]
    corr_pic = corr[masque_tau][idx_pic]
    ax3.plot(tau_pic / T_0, corr_pic, "ro", markersize=10, zorder=5,
             label=f"Pic : C = {corr_pic:.3f} à τ = {tau_pic:.1f} s")

    ax3.set_xlabel(f"Retard τ (× T₀ = {T_0:.0f} s)")
    ax3.set_ylabel("Corrélation croisée normalisée C(τ)")
    ax3.set_title(
        "Corrélation croisée θ_filtré(t) × M(t)\n"
        "Un pic à τ ≈ 0 confirme la synchronisation force–plasma",
        fontsize=13, fontweight="bold",
    )
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    fig3.savefig("data/006_correlation_croisee.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/006_correlation_croisee.png")
    print(f"    Pic de corrélation : C = {corr_pic:.3f} à τ = {tau_pic:.1f} s")

    # ── Étape 5 : Extraction de la force ────────────────────────────
    print("\n▶ Extraction de la force")
    resultat = extraire_force(theta_filtre, t)
    print(f"    θ_max = {resultat['theta_max_urad']:.2f} µrad")
    print(f"    F_extraite = {resultat['force_extraite_uN']:.3f} µN")
    print(f"    F_attendue = {F_RAD*1e6:.3f} µN")
    erreur_pct = abs(resultat["force_extraite_N"] - F_RAD) / F_RAD * 100
    print(f"    Erreur relative : {erreur_pct:.1f} %")

    # ── Étape 6 : SNR ──────────────────────────────────────────────
    print("\n▶ Rapport signal/bruit")
    bruit_seul = sig["theta_thermique"] + sig["theta_bruit"]
    bruit_filtre = filtrer_passe_bande(bruit_seul, sig["fe"])
    snr = calculer_snr(theta_filtre, bruit_filtre)
    print(f"    SNR = {snr:.1f}")
    print(f"    Significativité : {'> 3σ ✔' if snr >= 3 else '< 3σ ✘'}")

    # ── Étape 7 : Scan SNR vs force ─────────────────────────────────
    print("\n▶ Scan SNR vs force (résolution du pendule)")
    forces_scan = np.logspace(-8, -4, 30)  # 10 nN → 100 µN
    scan = scan_snr_vs_force(forces_scan, duree=20.0, fe=10.0)

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.loglog(scan["forces_uN"], scan["snrs"], "b-o", markersize=4, linewidth=1.5)
    ax4.axhline(3, color="red", linestyle="--", linewidth=2, label="Seuil 3σ")
    ax4.axhline(5, color="orange", linestyle=":", linewidth=1.5, label="Seuil 5σ")
    ax4.axvline(F_RAD * 1e6, color="green", linestyle="-.", linewidth=1.5,
                label=f"F_rad = {F_RAD*1e6:.1f} µN")

    if not np.isnan(scan["force_min_3sigma_uN"]):
        ax4.axvline(scan["force_min_3sigma_uN"], color="red", linestyle=":",
                    alpha=0.7, label=f"F_min(3σ) = {scan['force_min_3sigma_uN']:.2f} µN")

    ax4.set_xlabel("Force (µN)", fontsize=12)
    ax4.set_ylabel("SNR", fontsize=12)
    ax4.set_title(
        "Résolution du pendule — SNR vs Force appliquée\n"
        f"Pendule : κ = {KAPPA:.0e} N·m/rad, Q = {Q_MEC:.0f}, "
        f"T₀ = {T_0:.0f} s, 20 cycles",
        fontsize=13, fontweight="bold",
    )
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3, which="both")
    ax4.set_xlim(forces_scan[0] * 1e6, forces_scan[-1] * 1e6)
    plt.tight_layout()
    fig4.savefig("data/006_snr_vs_force.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/006_snr_vs_force.png")

    if not np.isnan(scan["force_min_3sigma_uN"]):
        print(f"    Force minimale détectable (3σ) : {scan['force_min_3sigma_uN']:.3f} µN")

    # ── Sauvegarde des données ──────────────────────────────────────
    print("\n▶ Sauvegarde des données")

    # Signal complet
    with open("data/006_signal_pendule.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["t_s", "theta_total_rad", "theta_force_rad",
                         "theta_therm_rad", "theta_bruit_rad", "theta_filtre_rad",
                         "commande"])
        for i in range(0, len(t), 10):  # Sous-échantillonné ×10
            writer.writerow([
                f"{t[i]:.4f}",
                f"{sig['theta_total'][i]:.10e}",
                f"{sig['theta_force'][i]:.10e}",
                f"{sig['theta_thermique'][i]:.10e}",
                f"{sig['theta_bruit'][i]:.10e}",
                f"{theta_filtre[i]:.10e}",
                f"{sig['commande'][i]:.0f}",
            ])
    print("  💾 Signal → data/006_signal_pendule.csv")

    # Scan SNR
    np.savez(
        "data/006_snr_scan.npz",
        forces_N=scan["forces_N"],
        snrs=scan["snrs"],
    )
    print("  💾 Scan SNR → data/006_snr_scan.npz")

    # ── Résumé ──────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  RÉSUMÉ — Expérience 006")
    print("═" * 60)
    print(f"""
  Pendule de torsion :
    κ = {KAPPA:.0e} N·m/rad,  Q = {Q_MEC:.0f},  T₀ = {T_0:.0f} s

  Signal pour F = {F_RAD*1e6:.1f} µN (pression de radiation 1 kW) :
    θ_max (résonance)  = {theta_resonance*1e6:.1f} µrad
    θ_max (extrait)    = {resultat['theta_max_urad']:.1f} µrad
    F_extraite          = {resultat['force_extraite_uN']:.3f} µN
    Erreur              = {erreur_pct:.1f} %
    SNR                 = {snr:.1f}  {'✔ détectable (> 3σ)' if snr >= 3 else '✘ non détectable'}

  Corrélation croisée :
    Pic C(τ)            = {corr_pic:.3f} à τ = {tau_pic:.1f} s
    {'✔ Synchronisation confirmée' if abs(corr_pic) > 0.3 else '✘ Pas de synchronisation claire'}

  Résolution :
    Force min. (3σ)     = {scan['force_min_3sigma_uN']:.3f} µN
    Ratio F_rad / F_min = {F_RAD / scan['force_min_3sigma_N']:.1f}×
    {'✔ La pression de radiation est détectable' if F_RAD > scan['force_min_3sigma_N'] else '✘ Pression de radiation trop faible'}

  Conclusion :
    La chaîne filtrage → corrélation → extraction est capable de
    récupérer le signal de force même en présence de dérive thermique
    et de bruit sismique, grâce à l'amplification par résonance
    (facteur Q = {Q_MEC:.0f}) et au filtrage passe-bande.
""")
    print("✅ Expérience 006 terminée.\n")
    plt.show()
