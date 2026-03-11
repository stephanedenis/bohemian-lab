"""
Expérience 011 — Analyse des données empiriques du pendule.

Applique le pipeline d'analyse du script 006 (simulation) aux données
réelles acquises par 010_acquisition.py :

    1. Chargement du CSV empirique (avec métadonnées).
    2. Filtrage passe-bande autour de f₀.
    3. Corrélation croisée θ(t) × M(t).
    4. Extraction de l'amplitude et calcul de la force.
    5. Calcul du rapport signal/bruit (SNR).
    6. Calcul de η = F_net / (P_abs/c).
    7. Comparaison avec les prédictions théoriques (006, 008, 009).
    8. Vérification des critères de succès (§4.4).
    9. Génération du rapport (JSON + figures).

Usage :
    # Analyse d'un fichier unique
    python experiments/011_analyse_empirique.py \\
        data/empirique/2026-04-15_14h30_test_principal_001.csv

    # Analyse d'une campagne complète
    python experiments/011_analyse_empirique.py \\
        --campagne data/empirique/2026-04-15_*.csv

    # Avec fichier de référence (charge fantôme)
    python experiments/011_analyse_empirique.py \\
        data/empirique/2026-04-15_15h15_test_principal_001.csv \\
        --fantome data/empirique/2026-04-15_15h00_reference_fantome_001.csv

Documentation : docs/08_acquisition.md, docs/04_protocole.md §4.3
"""
import argparse
import glob
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Réutilisation du pipeline de 006.
# Le nom de fichier commence par un chiffre → import via importlib.
import importlib.util

_chemin_006 = Path(__file__).resolve().parent / "006_analyse_signal.py"
_spec = importlib.util.spec_from_file_location("analyse_signal_006", _chemin_006)
_mod006 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod006)

filtrer_passe_bande = _mod006.filtrer_passe_bande
correlation_croisee = _mod006.correlation_croisee
extraire_force = _mod006.extraire_force
calculer_snr = _mod006.calculer_snr
KAPPA = _mod006.KAPPA
L_BRAS = _mod006.L_BRAS
Q_MEC = _mod006.Q_MEC
F_RAD = _mod006.F_RAD
C_LUMIERE = _mod006.C_LUMIERE


# ═══════════════════════════════════════════════════════════════════════
# Chargement des données empiriques
# ═══════════════════════════════════════════════════════════════════════

def charger_csv_empirique(chemin: str | Path) -> dict:
    """Charge un fichier CSV empirique avec ses métadonnées.

    Lit les lignes commençant par '#' comme métadonnées clé-valeur,
    puis charge les données numériques.

    Args:
        chemin: Chemin vers le fichier CSV.

    Returns:
        Dict avec 'meta' (dict des métadonnées) et 'data' (dict des colonnes).
    """
    chemin = Path(chemin)
    meta: dict[str, str] = {}
    lignes_data: list[str] = []
    colonnes: list[str] = []

    with open(chemin, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith("#"):
                # Métadonnée : # clé: valeur
                if ":" in ligne:
                    cle, valeur = ligne[2:].split(":", 1)
                    meta[cle.strip()] = valeur.strip()
            elif not colonnes:
                # Première ligne non-commentaire = en-tête
                colonnes = ligne.split(",")
            else:
                lignes_data.append(ligne)

    # Parser les données numériques
    n_lignes = len(lignes_data)
    data: dict[str, np.ndarray | list[str]] = {}
    for col in colonnes:
        data[col] = []

    for ligne in lignes_data:
        champs = ligne.split(",")
        for i, col in enumerate(colonnes):
            if i < len(champs):
                val = champs[i]
                if col == "etat":
                    data[col].append(val)
                else:
                    try:
                        data[col].append(float(val))
                    except ValueError:
                        data[col].append(0.0)

    # Convertir en arrays numpy (sauf la colonne 'etat')
    for col in colonnes:
        if col != "etat":
            data[col] = np.array(data[col])

    # Extraire T₀ et κ des métadonnées (ou utiliser les défauts)
    t0 = float(meta.get("T0_s", "444.3"))
    kappa = float(meta.get("kappa_Nm_rad", "1e-5"))
    l_bras = float(meta.get("L_bras_m", "0.200"))
    fe = float(meta.get("fe_Hz", "100"))

    return {
        "meta": meta,
        "data": data,
        "colonnes": colonnes,
        "n_lignes": n_lignes,
        "T0": t0,
        "f0": 1.0 / t0,
        "kappa": kappa,
        "L_bras": l_bras,
        "fe": fe,
        "chemin": chemin,
    }


# ═══════════════════════════════════════════════════════════════════════
# Pipeline d'analyse
# ═══════════════════════════════════════════════════════════════════════

def analyser_essai(
    fichier: str | Path,
    fichier_fantome: str | Path | None = None,
    puissance_abs_W: float = 650.0,
    sauvegarder_figures: bool = True,
) -> dict:
    """Analyse complète d'un essai empirique.

    Applique la chaîne filtrage → corrélation → extraction force →
    SNR → η et compare aux prédictions théoriques.

    Args:
        fichier: Chemin du fichier CSV de l'essai.
        fichier_fantome: Chemin du fichier CSV de la charge fantôme (optionnel).
        puissance_abs_W: Puissance absorbée estimée (W).
        sauvegarder_figures: Si True, génère les figures .png.

    Returns:
        Dict des résultats (η, SNR, force, etc.).
    """
    print(f"\n📊 Chargement : {Path(fichier).name}")

    # 1. Charger les données
    essai = charger_csv_empirique(fichier)
    meta = essai["meta"]
    data = essai["data"]

    t_ms = data["timestamp_ms"]
    t = t_ms / 1000.0  # Convertir en secondes
    theta = data["psd_urad"] * 1e-6  # Convertir µrad → rad
    commande = data["commande_mag"]
    fe = essai["fe"]
    f0 = essai["f0"]
    T0 = essai["T0"]
    kappa = essai["kappa"]
    l_bras = essai["L_bras"]

    print(f"   {essai['n_lignes']} lignes, {t[-1]:.1f} s, fe = {fe:.0f} Hz")
    print(f"   T₀ = {T0:.1f} s, f₀ = {f0:.4e} Hz")
    print(f"   κ = {kappa:.2e} N·m/rad, L = {l_bras:.3f} m")

    # 2. Filtrage passe-bande
    print("\n▶ Filtrage passe-bande autour de f₀")
    theta_filtre = filtrer_passe_bande(theta, fe, f_centre=f0)

    # 3. Corrélation croisée
    print("▶ Corrélation croisée θ(t) × M(t)")
    tau, corr = correlation_croisee(theta_filtre, commande, fe)

    # Pic de corrélation
    idx_pic = np.argmax(np.abs(corr))
    tau_pic = tau[idx_pic]
    corr_pic = corr[idx_pic]
    print(f"   Pic : C = {corr_pic:.3f} à τ = {tau_pic:.1f} s")

    # 4. Extraction de la force
    print("▶ Extraction de la force")
    resultat_force = extraire_force(
        theta_filtre, t,
        kappa=kappa, bras=l_bras, q_mec=Q_MEC,
    )
    force_mesuree = resultat_force["force_extraite_N"]
    print(f"   θ_max = {resultat_force['theta_max_urad']:.2f} µrad")
    print(f"   F_extraite = {resultat_force['force_extraite_uN']:.3f} µN")

    # 5. Charge fantôme (si fournie)
    force_fantome = 0.0
    if fichier_fantome:
        print(f"\n▶ Analyse de la charge fantôme : {Path(fichier_fantome).name}")
        fantome = charger_csv_empirique(fichier_fantome)
        theta_fant = fantome["data"]["psd_urad"] * 1e-6
        t_fant = fantome["data"]["timestamp_ms"] / 1000.0
        theta_fant_filtre = filtrer_passe_bande(theta_fant, fantome["fe"], f_centre=f0)
        res_fant = extraire_force(
            theta_fant_filtre, t_fant,
            kappa=kappa, bras=l_bras, q_mec=Q_MEC,
        )
        force_fantome = res_fant["force_extraite_N"]
        print(f"   F_fantôme = {force_fantome * 1e6:.3f} µN")

    # 6. Force nette
    force_nette = force_mesuree - force_fantome
    print(f"\n▶ Force nette = {force_nette * 1e6:.3f} µN")

    # 7. Rapport signal/bruit
    print("▶ Rapport signal/bruit")
    # Pour le SNR, on utilise la première moitié (avant régime permanent)
    # comme estimation du bruit
    n_moitie = len(theta_filtre) // 2
    bruit_estime = np.std(theta_filtre[:n_moitie])
    signal_estime = np.std(theta_filtre[n_moitie:])
    snr = signal_estime / bruit_estime if bruit_estime > 0 else float("inf")
    print(f"   SNR = {snr:.1f}")

    # 8. Calcul de η
    f_rad = puissance_abs_W / C_LUMIERE  # Pression de radiation classique
    eta = force_nette / f_rad if f_rad > 0 else 0.0
    print(f"\n▶ Calcul de η")
    print(f"   F_rad (P/c) = {f_rad * 1e6:.3f} µN  (P_abs = {puissance_abs_W:.0f} W)")
    print(f"   η = F_net / (P/c) = {eta:.3f}")

    # Correction 3D (§009) : η_total = η_H / cos(55°)
    eta_total = eta / np.cos(np.radians(55))
    print(f"   η_total (corrigé 3D) = {eta_total:.3f}")

    # 9. Vérification des critères (§4.4)
    criteres = {
        "snr_gt_3": snr > 3,
        "correlation_gt_0.8": abs(corr_pic) > 0.8,
        "fantome_lt_0.3": (
            force_fantome < 0.3 * force_mesuree
            if force_fantome > 0 else True
        ),
    }

    print(f"\n▶ Critères de succès (§4.4)")
    for nom, ok in criteres.items():
        print(f"   {'✔' if ok else '✘'} {nom}")

    # 10. Comparaison avec les prédictions
    print(f"\n▶ Comparaison théorie vs mesure")
    print(f"   {'Grandeur':<25s} {'Théorie':>12s} {'Mesure':>12s} {'Écart':>10s}")
    print(f"   {'─' * 60}")

    predictions = {
        "F_rad (µN)": (F_RAD * 1e6, force_nette * 1e6),
        "SNR": (12.0, snr),
        "Corrélation pic": (0.85, abs(corr_pic)),
    }
    for nom, (theo, mes) in predictions.items():
        ecart = ((mes - theo) / theo * 100) if theo != 0 else 0
        print(f"   {nom:<25s} {theo:>12.3f} {mes:>12.3f} {ecart:>+9.1f} %")

    # 11. Résultats
    resultats = {
        "date": meta.get("date", ""),
        "type": meta.get("type", ""),
        "fichier": str(Path(fichier).name),
        "n_lignes": essai["n_lignes"],
        "duree_s": float(t[-1]),
        "T0_mesure_s": T0,
        "kappa_Nm_rad": kappa,
        "theta_max_urad": resultat_force["theta_max_urad"],
        "force_extraite_uN": resultat_force["force_extraite_uN"],
        "force_fantome_uN": force_fantome * 1e6,
        "force_nette_uN": force_nette * 1e6,
        "P_abs_W": puissance_abs_W,
        "F_rad_uN": f_rad * 1e6,
        "eta_H": eta,
        "eta_total": eta_total,
        "snr": snr,
        "correlation_pic": float(corr_pic),
        "correlation_tau_s": float(tau_pic),
        "criteres_succes": criteres,
    }

    # 12. Figures
    if sauvegarder_figures:
        generer_figures_analyse(
            t, theta, theta_filtre, commande,
            tau, corr, eta, eta_total,
            essai, resultats,
        )

    return resultats


# ═══════════════════════════════════════════════════════════════════════
# Génération des figures
# ═══════════════════════════════════════════════════════════════════════

def generer_figures_analyse(
    t: np.ndarray,
    theta: np.ndarray,
    theta_filtre: np.ndarray,
    commande: np.ndarray,
    tau: np.ndarray,
    corr: np.ndarray,
    eta: float,
    eta_total: float,
    essai: dict,
    resultats: dict,
) -> None:
    """Génère les figures d'analyse et les sauvegarde.

    Args:
        t: Vecteur temps (s).
        theta: Signal brut (rad).
        theta_filtre: Signal filtré (rad).
        commande: Signal de commande du magnétron.
        tau: Retards de la corrélation croisée.
        corr: Corrélation croisée normalisée.
        eta: Ratio η horizontal.
        eta_total: Ratio η corrigé 3D.
        essai: Dict des données chargées.
        resultats: Dict des résultats calculés.
    """
    import matplotlib.pyplot as plt

    chemin = essai["chemin"]
    base = chemin.parent / chemin.stem
    T0 = essai["T0"]
    f0 = essai["f0"]
    fe = essai["fe"]

    # ── Figure 1 : Signal brut + filtré + commande ──────────────────
    fig1, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    axes[0].plot(t / T0, theta * 1e6, "b-", linewidth=0.5, alpha=0.7)
    axes[0].set_ylabel("θ brut (µrad)")
    axes[0].set_title("Signal brut du pendule")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t / T0, theta_filtre * 1e6, "r-", linewidth=0.8)
    axes[1].set_ylabel("θ filtré (µrad)")
    axes[1].set_title(f"Signal filtré (passe-bande autour de f₀ = {f0:.4e} Hz)")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(t / T0, commande, "k-", linewidth=0.5)
    axes[2].set_ylabel("M(t)")
    axes[2].set_title("Commande magnétron")
    axes[2].set_ylim(-0.2, 1.2)
    axes[2].set_xlabel(f"Temps (×T₀ = {T0:.0f} s)")
    axes[2].grid(True, alpha=0.3)

    fig1.suptitle(
        f"Analyse 011 — {chemin.stem}\nSignal du pendule",
        fontsize=14, fontweight="bold",
    )
    plt.tight_layout()
    chemin_fig1 = f"{base}_analyse_signal.png"
    fig1.savefig(chemin_fig1, dpi=150, bbox_inches="tight")
    print(f"  💾 Figure → {chemin_fig1}")

    # ── Figure 2 : Spectre FFT ──────────────────────────────────────
    fig2, ax2 = plt.subplots(figsize=(12, 5))

    n_fft = len(t)
    freqs_fft = np.fft.rfftfreq(n_fft, d=1.0 / fe)
    spectre = np.abs(np.fft.rfft(theta_filtre)) / n_fft

    ax2.semilogy(freqs_fft * 1e3, spectre * 1e6, "b-", linewidth=1)
    ax2.axvline(f0 * 1e3, color="red", linestyle="--",
                label=f"f₀ = {f0 * 1e3:.3f} mHz")
    ax2.set_xlabel("Fréquence (mHz)")
    ax2.set_ylabel("Amplitude (µrad)")
    ax2.set_title("Analyse spectrale — FFT du signal filtré")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 20 * f0 * 1e3)
    plt.tight_layout()
    chemin_fig2 = f"{base}_analyse_fft.png"
    fig2.savefig(chemin_fig2, dpi=150, bbox_inches="tight")
    print(f"  💾 Figure → {chemin_fig2}")

    # ── Figure 3 : Corrélation croisée ──────────────────────────────
    fig3, ax3 = plt.subplots(figsize=(12, 5))

    masque = np.abs(tau) <= 5 * T0
    ax3.plot(tau[masque] / T0, corr[masque], "b-", linewidth=1)
    ax3.axvline(0, color="red", linestyle="--", alpha=0.5)
    ax3.axhline(0, color="gray", linestyle=":", alpha=0.5)

    idx_pic = np.argmax(np.abs(corr[masque]))
    ax3.plot(tau[masque][idx_pic] / T0, corr[masque][idx_pic],
             "ro", markersize=10, zorder=5,
             label=f"Pic : C = {corr[masque][idx_pic]:.3f}")
    ax3.set_xlabel(f"Retard τ (×T₀ = {T0:.0f} s)")
    ax3.set_ylabel("C(τ) normalisée")
    ax3.set_title("Corrélation croisée θ(t) ⊗ M(t)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    chemin_fig3 = f"{base}_analyse_correlation.png"
    fig3.savefig(chemin_fig3, dpi=150, bbox_inches="tight")
    print(f"  💾 Figure → {chemin_fig3}")

    # ── Figure 4 : η — Comparaison théorie vs mesure ────────────────
    fig4, ax4 = plt.subplots(figsize=(10, 6))

    # Zones de décision (§4.6)
    ax4.axhspan(0, 1, alpha=0.12, color="red", label="η < 1 : INFIRMÉ")
    ax4.axhspan(1, 10, alpha=0.12, color="orange", label="1 < η < 10 : INTÉRESSANT")
    ax4.axhspan(10, 20, alpha=0.12, color="green", label="η > 10 : ANOMALIE")

    # Point mesuré
    ax4.barh(["η_H (mesuré)", "η_total (corrigé 3D)"],
             [eta, eta_total],
             color=["#3498db", "#e74c3c"], height=0.4)

    # Prédiction Monte-Carlo (008) : IC 90 % ≈ [0,6 ; 1,5]
    ax4.axvline(0.98, color="green", linestyle="--", linewidth=2,
                label="Prédiction MC (médiane = 0,98)")
    ax4.axvspan(0.6, 1.5, alpha=0.1, color="green")

    ax4.set_xlabel("η = F_net / (P/c)")
    ax4.set_title(
        f"Résultat — η mesuré vs prédiction\n"
        f"η_H = {eta:.3f}, η_total = {eta_total:.3f}",
        fontsize=13, fontweight="bold",
    )
    ax4.legend(loc="upper right", fontsize=9)
    ax4.set_xlim(0, max(eta_total * 1.5, 3))
    ax4.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    chemin_fig4 = f"{base}_analyse_eta.png"
    fig4.savefig(chemin_fig4, dpi=150, bbox_inches="tight")
    print(f"  💾 Figure → {chemin_fig4}")

    plt.close("all")


# ═══════════════════════════════════════════════════════════════════════
# Mode campagne
# ═══════════════════════════════════════════════════════════════════════

def analyser_campagne(
    fichiers: list[str],
    fichier_fantome: str | None = None,
    puissance_abs_W: float = 650.0,
) -> dict:
    """Analyse une campagne complète (multiple essais).

    Produit un rapport de synthèse avec reproductibilité et
    vérification des critères de succès (§4.4).

    Args:
        fichiers: Liste des chemins CSV.
        fichier_fantome: Chemin CSV de la charge fantôme.
        puissance_abs_W: Puissance absorbée (W).

    Returns:
        Dict du rapport de campagne.
    """
    import matplotlib.pyplot as plt

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Analyse de campagne — Mode multi-essais                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"\n  {len(fichiers)} fichiers à analyser\n")

    resultats_tous: list[dict] = []

    for fichier in sorted(fichiers):
        try:
            res = analyser_essai(
                fichier,
                fichier_fantome=fichier_fantome,
                puissance_abs_W=puissance_abs_W,
                sauvegarder_figures=True,
            )
            resultats_tous.append(res)
        except Exception as e:
            print(f"  ⚠️  Erreur sur {Path(fichier).name} : {e}")

    if not resultats_tous:
        print("❌ Aucun essai analysé avec succès.")
        return {}

    # Extraire les η
    etas = [r["eta_H"] for r in resultats_tous]
    snrs = [r["snr"] for r in resultats_tous]
    forces = [r["force_nette_uN"] for r in resultats_tous]

    # Reproductibilité (§4.4 : ≥ 5 essais cohérents)
    n_essais = len(etas)
    eta_moyen = np.mean(etas)
    eta_std = np.std(etas)
    snr_moyen = np.mean(snrs)

    print("\n" + "═" * 60)
    print("  RAPPORT DE CAMPAGNE")
    print("═" * 60)
    print(f"""
  Nombre d'essais      : {n_essais}
  η_H (moyenne ± σ)    : {eta_moyen:.3f} ± {eta_std:.3f}
  SNR (moyenne)         : {snr_moyen:.1f}
  Force nette (moy.)    : {np.mean(forces):.3f} µN

  Reproductibilité      : {'✔' if n_essais >= 5 else '✘'} (≥ 5 essais requis, {n_essais} réalisés)
  SNR > 3 (tous)        : {'✔' if all(s > 3 for s in snrs) else '✘'}
  η cohérent (σ/µ < 30%) : {'✔' if eta_std / max(abs(eta_moyen), 1e-10) < 0.3 else '✘'}
""")

    # Vérification globale des critères §4.4
    tous_criteres = {}
    for r in resultats_tous:
        for k, v in r["criteres_succes"].items():
            if k not in tous_criteres:
                tous_criteres[k] = []
            tous_criteres[k].append(v)

    print("  Critères de succès (§4.4) :")
    for nom, vals in tous_criteres.items():
        pct = sum(1 for v in vals if v) / len(vals) * 100
        print(f"    {'✔' if pct == 100 else '✘'} {nom} : {pct:.0f} % des essais")

    # Diagnostic final
    if eta_moyen > 1 and snr_moyen > 3:
        print("\n  🟢 RÉSULTAT : EXCÈS DE FORCE DÉTECTÉ (η > 1)")
        print("     → Candidat pour effet bohmien — vérifications requises")
    elif eta_moyen > 0.5:
        print("\n  🟡 RÉSULTAT : SIGNAL MARGINAL")
        print("     → Augmenter le nombre d'essais ou la durée d'acquisition")
    else:
        print("\n  🔴 RÉSULTAT : PAS D'EXCÈS DÉTECTÉ (η ≤ 1)")
        print("     → Hypothèse infirmée dans cette configuration")

    # Figure récapitulative
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # η par essai
    ax = axes[0]
    ax.bar(range(n_essais), etas, color="#3498db", alpha=0.7)
    ax.axhline(1, color="red", linestyle="--", linewidth=2, label="η = 1")
    ax.axhline(eta_moyen, color="green", linestyle="-",
               label=f"Moyenne = {eta_moyen:.3f}")
    ax.fill_between(range(n_essais),
                     eta_moyen - eta_std, eta_moyen + eta_std,
                     alpha=0.2, color="green")
    ax.set_xlabel("Essai #")
    ax.set_ylabel("η_H")
    ax.set_title("Reproductibilité de η")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # SNR par essai
    ax = axes[1]
    ax.bar(range(n_essais), snrs, color="#2ecc71", alpha=0.7)
    ax.axhline(3, color="red", linestyle="--", linewidth=2, label="Seuil 3σ")
    ax.set_xlabel("Essai #")
    ax.set_ylabel("SNR")
    ax.set_title("Rapport signal/bruit")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Force nette par essai
    ax = axes[2]
    ax.bar(range(n_essais), forces, color="#e74c3c", alpha=0.7)
    ax.axhline(F_RAD * 1e6, color="blue", linestyle="--",
               label=f"F_rad = {F_RAD * 1e6:.1f} µN")
    ax.set_xlabel("Essai #")
    ax.set_ylabel("F_net (µN)")
    ax.set_title("Force nette extraite")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.suptitle("Rapport de campagne — Bohemian Lab",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()

    # Sauvegarder dans le dossier du premier fichier
    dossier = Path(fichiers[0]).parent
    maintenant = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    chemin_fig = dossier / f"{maintenant}_campagne_rapport.png"
    fig.savefig(chemin_fig, dpi=150, bbox_inches="tight")
    print(f"\n  💾 Figure campagne → {chemin_fig}")
    plt.close("all")

    # Sauvegarder le rapport JSON
    rapport = {
        "date": maintenant,
        "n_essais": n_essais,
        "fichiers": [str(Path(f).name) for f in fichiers],
        "eta_H_moyen": eta_moyen,
        "eta_H_std": eta_std,
        "snr_moyen": snr_moyen,
        "force_nette_moy_uN": float(np.mean(forces)),
        "criteres_succes_globaux": {
            k: all(v) for k, v in tous_criteres.items()
        },
        "resultats_individuels": resultats_tous,
    }

    chemin_json = dossier / f"{maintenant}_campagne_resultats.json"
    with open(chemin_json, "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
    print(f"  💾 Rapport JSON → {chemin_json}")

    return rapport


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée
# ═══════════════════════════════════════════════════════════════════════

def main() -> None:
    """Point d'entrée principal — parsing des arguments."""
    parser = argparse.ArgumentParser(
        description="Analyse des données empiriques — Bohemian Lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  # Analyse d'un fichier
  python 011_analyse_empirique.py data/empirique/2026-04-15_test_principal_001.csv

  # Avec soustraction de la charge fantôme
  python 011_analyse_empirique.py \\
      data/empirique/test_principal_001.csv \\
      --fantome data/empirique/reference_fantome_001.csv

  # Campagne complète
  python 011_analyse_empirique.py --campagne data/empirique/2026-04-15_*.csv
        """,
    )

    parser.add_argument("fichiers", nargs="*",
                        help="Fichier(s) CSV à analyser")
    parser.add_argument("--fantome", type=str, default=None,
                        help="Fichier CSV de la charge fantôme")
    parser.add_argument("--puissance", type=float, default=650.0,
                        help="Puissance absorbée en watts (défaut: 650)")
    parser.add_argument("--campagne", action="store_true",
                        help="Mode campagne (analyse multi-essais)")
    parser.add_argument("--no-figures", action="store_true",
                        help="Ne pas générer les figures")

    args = parser.parse_args()

    if not args.fichiers:
        parser.print_help()
        sys.exit(1)

    # Expand des globs
    fichiers_resolus = []
    for patron in args.fichiers:
        matches = glob.glob(patron)
        if matches:
            fichiers_resolus.extend(matches)
        else:
            fichiers_resolus.append(patron)

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 011 — Analyse des données empiriques         ║")
    print("║  Pipeline : filtrage → corrélation → force → η           ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    if args.campagne or len(fichiers_resolus) > 1:
        analyser_campagne(
            fichiers_resolus,
            fichier_fantome=args.fantome,
            puissance_abs_W=args.puissance,
        )
    else:
        resultats = analyser_essai(
            fichiers_resolus[0],
            fichier_fantome=args.fantome,
            puissance_abs_W=args.puissance,
            sauvegarder_figures=not args.no_figures,
        )

        # Sauvegarder le rapport JSON
        chemin = Path(fichiers_resolus[0])
        chemin_json = chemin.parent / f"{chemin.stem}_resultats.json"
        with open(chemin_json, "w", encoding="utf-8") as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n  💾 Résultats → {chemin_json}")

        # Verdict
        eta = resultats["eta_H"]
        print(f"\n  {'🟢' if eta > 1 else '🔴'} η_H = {eta:.3f}  "
              f"→ {'EXCÈS DÉTECTÉ' if eta > 1 else 'PAS D EXCÈS'}")

    print("\n✅ Analyse 011 terminée.\n")


if __name__ == "__main__":
    main()
