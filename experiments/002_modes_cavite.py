"""
Expérience 002 — Modes de résonance de la cavité cylindrique.

Calcule les fréquences de résonance TM_{mnp} et TE_{mnp} de la chambre
à vide cylindrique (inox 3 gallons) et identifie les modes compatibles
avec le magnétron à 2,45 GHz.

Contexte physique :
    La cavité cylindrique du Bohemian Lab a pour dimensions :
        - Rayon intérieur : a = 125 mm (diamètre 250 mm)
        - Hauteur :         d = 250 mm

    Les fréquences de résonance sont données par (Pozar, chap. 6) :

        f_{mnp} = c / (2π) × √[(x_mn / a)² + (pπ / d)²]

    où x_mn est le n-ième zéro de J_m (mode TM) ou de J'_m (mode TE).

    Le mode TM₃₁₀ à 2,44 GHz est quasi parfaitement accordé avec le
    magnétron (2,45 GHz). Ce script vérifie et visualise ce résultat.

Sorties :
    - Tableau de tous les modes ≤ 4 GHz.
    - Diagramme en barres coloré (vert = compatible, gris = hors bande).
    - Carte du champ E_z(r, θ) pour le mode TM₃₁₀.
    - Coupe radiale E_z(r) à θ = 0.
    - Données sauvegardées dans data/002_modes_cavite.csv et .npy.

Références :
    [1] Pozar, D.M. (2012). Microwave Engineering, 4e éd., chap. 6.
    [2] Jackson, J.D. (1998). Classical Electrodynamics, chap. 8.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.special import jn_zeros, jnp_zeros, jn

# Ajout du répertoire racine au sys.path pour importer src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.viz import plot_modes_cavite, plot_champ_cavite


# ═══════════════════════════════════════════════════════════════════════
# Constantes physiques et géométrie de la cavité
# ═══════════════════════════════════════════════════════════════════════

C: float = 299_792_458.0       # vitesse de la lumière (m/s)
A: float = 0.125               # rayon de la cavité (m) — 125 mm
D: float = 0.250               # hauteur de la cavité (m) — 250 mm
F_MAGNETRON: float = 2.45e9    # fréquence du magnétron (Hz)

# Nombre maximal d'indices à explorer
M_MAX: int = 7    # indice azimutal m (0, 1, …, M_MAX-1)
N_MAX: int = 4    # indice radial n (1, 2, …, N_MAX)
P_MAX: int = 3    # indice axial p (0, 1, …, P_MAX)


# ═══════════════════════════════════════════════════════════════════════
# Calcul des fréquences de résonance
# ═══════════════════════════════════════════════════════════════════════

def frequence_tm(m: int, n: int, p: int, a: float, d: float) -> float:
    """Fréquence de résonance du mode TM_{mnp} d'une cavité cylindrique.

    La condition aux limites impose E_z = 0 sur la paroi latérale,
    soit J_m(x_mn × r/a) = 0 en r = a → x_mn est le n-ième zéro de J_m.

    Pour le mode axial, p = 0 signifie un champ uniforme selon z
    (mode « en galette »), p > 0 introduit des nœuds axiaux.

    Args:
        m: Indice azimutal (nombre de nœuds angulaires).
        n: Indice radial (numéro du zéro de J_m, commence à 1).
        p: Indice axial (nombre de demi-longueurs d'onde en z).
        a: Rayon de la cavité (m).
        d: Hauteur de la cavité (m).

    Returns:
        Fréquence en Hz.
    """
    # n-ième zéro de J_m (scipy numérote à partir de 1)
    x_mn = jn_zeros(m, n)[-1]  # le n-ième zéro
    k_r = x_mn / a             # nombre d'onde radial
    k_z = p * np.pi / d         # nombre d'onde axial
    k = np.sqrt(k_r**2 + k_z**2)
    return C * k / (2 * np.pi)


def frequence_te(m: int, n: int, p: int, a: float, d: float) -> float:
    """Fréquence de résonance du mode TE_{mnp} d'une cavité cylindrique.

    La condition aux limites impose ∂H_z/∂r = 0 en r = a (paroi conductrice),
    soit J'_m(x'_mn × r/a) = 0 en r = a → x'_mn est le n-ième zéro de J'_m.

    Note : le mode TE_{mn0} n'existe pas (p ≥ 1 requis pour TE).

    Args:
        m: Indice azimutal.
        n: Indice radial (numéro du zéro de J'_m, commence à 1).
        p: Indice axial (≥ 1 pour les modes TE).
        a: Rayon de la cavité (m).
        d: Hauteur de la cavité (m).

    Returns:
        Fréquence en Hz.
    """
    if p < 1:
        return float("inf")  # TE_{mn0} n'existe pas
    # n-ième zéro de J'_m (dérivée de J_m)
    xp_mn = jnp_zeros(m, n)[-1]
    k_r = xp_mn / a
    k_z = p * np.pi / d
    k = np.sqrt(k_r**2 + k_z**2)
    return C * k / (2 * np.pi)


def calculer_tous_les_modes(
    a: float = A,
    d: float = D,
    f_max: float = 4.0e9,
) -> list[dict]:
    """Calcule tous les modes TM et TE dont la fréquence est inférieure à f_max.

    Parcourt systématiquement les indices (m, n, p) et filtre les modes
    dont la fréquence dépasse f_max.

    Args:
        a: Rayon de la cavité (m).
        d: Hauteur de la cavité (m).
        f_max: Fréquence maximale à considérer (Hz).

    Returns:
        Liste triée de dicts contenant les informations de chaque mode.
    """
    modes: list[dict] = []

    # --- Modes TM_{mnp} ---
    for m in range(M_MAX):
        for n in range(1, N_MAX + 1):
            for p in range(P_MAX + 1):
                try:
                    f = frequence_tm(m, n, p, a, d)
                    if f <= f_max:
                        ecart = abs(f - F_MAGNETRON)
                        compatible = "✔" if ecart < 50e6 else ""
                        modes.append({
                            "nom": f"TM_{m}{n}{p}",
                            "type": "TM",
                            "m": m, "n": n, "p": p,
                            "freq": f,
                            "ecart_MHz": ecart / 1e6,
                            "compatible": compatible,
                        })
                except (ValueError, IndexError):
                    pass

    # --- Modes TE_{mnp} (p ≥ 1) ---
    for m in range(M_MAX):
        for n in range(1, N_MAX + 1):
            for p in range(1, P_MAX + 1):
                try:
                    f = frequence_te(m, n, p, a, d)
                    if f <= f_max:
                        ecart = abs(f - F_MAGNETRON)
                        compatible = "✔" if ecart < 50e6 else ""
                        modes.append({
                            "nom": f"TE_{m}{n}{p}",
                            "type": "TE",
                            "m": m, "n": n, "p": p,
                            "freq": f,
                            "ecart_MHz": ecart / 1e6,
                            "compatible": compatible,
                        })
                except (ValueError, IndexError):
                    pass

    # Tri par fréquence croissante
    modes.sort(key=lambda m: m["freq"])
    return modes


# ═══════════════════════════════════════════════════════════════════════
# Calcul du champ E_z d'un mode TM_{mnp}
# ═══════════════════════════════════════════════════════════════════════

def champ_ez_tm(
    m: int,
    n: int,
    r: np.ndarray,
    theta: np.ndarray,
    a: float = A,
) -> np.ndarray:
    """Calcule la distribution du champ E_z(r, θ) pour un mode TM_{mnp}.

    La composante axiale du champ électrique dans une cavité cylindrique
    pour un mode TM_{mnp} est proportionnelle à :

        E_z(r, θ) = J_m(x_mn × r / a) × cos(m × θ)

    (La dépendance en z est cos(pπz/d), ici on prend z = 0.)

    Le profil radial est une fonction de Bessel J_m, et le profil
    angulaire est un cosinus de période m. Le mode TM₃₁₀ présente
    donc 3 lobes azimutaux (m=3) et un profil radial avec un seul
    maximum radial avant la paroi (n=1).

    Args:
        m: Indice azimutal.
        n: Indice radial.
        r: Coordonnées radiales (1D array).
        theta: Coordonnées angulaires (1D array).
        a: Rayon de la cavité (m).

    Returns:
        Tableau 2D de E_z(theta, r) normalisé.
    """
    x_mn = jn_zeros(m, n)[-1]
    R, Theta = np.meshgrid(r, theta)

    # Profil radial : J_m(x_mn × r / a)
    # Profil azimutal : cos(m × θ)
    E_z = jn(m, x_mn * R / a) * np.cos(m * Theta)

    # Normalisation à [-1, 1]
    E_z_max = np.max(np.abs(E_z))
    if E_z_max > 0:
        E_z /= E_z_max

    return E_z


# ═══════════════════════════════════════════════════════════════════════
# Sauvegarde des résultats
# ═══════════════════════════════════════════════════════════════════════

def sauvegarder_resultats(
    modes: list[dict],
    chemin_csv: str = "data/002_modes_cavite.csv",
    chemin_npy: str = "data/002_modes_cavite.npy",
) -> None:
    """Sauvegarde la table des modes en CSV et NumPy.

    Args:
        modes: Liste de dicts de modes (sortie de calculer_tous_les_modes).
        chemin_csv: Chemin du fichier CSV.
        chemin_npy: Chemin du fichier NumPy.
    """
    import csv

    # CSV — lisible par un humain
    chemin = Path(chemin_csv)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "mode", "type", "m", "n", "p",
            "frequence_Hz", "frequence_GHz", "ecart_MHz", "compatible_2.45GHz",
        ])
        for mode in modes:
            writer.writerow([
                mode["nom"], mode["type"], mode["m"], mode["n"], mode["p"],
                f"{mode['freq']:.1f}", f"{mode['freq']/1e9:.4f}",
                f"{mode['ecart_MHz']:.1f}", mode["compatible"],
            ])
    print(f"  💾 Données CSV sauvegardées → {chemin_csv}")

    # NumPy — exploitable programmatiquement
    noms = [m["nom"] for m in modes]
    freqs = np.array([m["freq"] for m in modes])
    np.save(chemin_npy, {"noms": noms, "frequences_Hz": freqs})
    print(f"  💾 Données NumPy sauvegardées → {chemin_npy}")


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 002 — Modes de résonance de la cavité        ║")
    print("║  Chambre inox 3 gal : Ø250 mm × 250 mm (a=125, d=250)   ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    # ── Étape 1 : calcul de tous les modes ──────────────────────────
    print("▶ Calcul des modes TM et TE (f ≤ 4 GHz)…\n")
    modes = calculer_tous_les_modes(a=A, d=D, f_max=4.0e9)

    # Affichage du tableau
    print(f"  {'Mode':<10} {'Fréquence':>12} {'Écart':>10} {'Compatible':>12}")
    print(f"  {'─'*10} {'─'*12} {'─'*10} {'─'*12}")
    for mode in modes:
        f_ghz = mode["freq"] / 1e9
        print(
            f"  {mode['nom']:<10} {f_ghz:>10.4f} GHz"
            f" {mode['ecart_MHz']:>8.1f} MHz"
            f" {mode['compatible']:>10}"
        )

    # Modes compatibles
    compatibles = [m for m in modes if m["compatible"]]
    print(f"\n  ✅ {len(compatibles)} mode(s) compatible(s) avec 2,45 GHz :")
    for m in compatibles:
        print(
            f"     → {m['nom']} à {m['freq']/1e9:.4f} GHz"
            f" (écart = {m['ecart_MHz']:.1f} MHz)"
        )

    # ── Étape 2 : diagramme des fréquences ──────────────────────────
    print("\n▶ Génération du diagramme des modes…")
    fig1 = plot_modes_cavite(
        modes,
        f_cible=F_MAGNETRON,
        delta_f=0.3e9,
        titre=(
            "Modes de résonance — Cavité cylindrique\n"
            f"a = {A*1e3:.0f} mm, d = {D*1e3:.0f} mm — "
            f"Magnétron 2,45 GHz"
        ),
        sauvegarde="data/002_modes_diagramme.png",
    )

    # ── Étape 3 : champ E_z du mode TM₃₁₀ ─────────────────────────
    print("\n▶ Calcul du champ E_z(r, θ) du mode TM₃₁₀…")

    # Grille polaire haute résolution
    n_r = 200
    n_theta = 360
    r = np.linspace(0, A, n_r)
    theta = np.linspace(0, 2 * np.pi, n_theta)

    E_z_310 = champ_ez_tm(m=3, n=1, r=r, theta=theta, a=A)

    fig2 = plot_champ_cavite(
        r=r, theta=theta, E_z=E_z_310,
        m=3, n=1, p=0, a=A,
        titre=(
            "Mode TM$_{310}$ — Champ $E_z(r, \\theta)$\n"
            f"f = 2,44 GHz — Cavité Ø{A*2e3:.0f} mm × {D*1e3:.0f} mm"
        ),
        sauvegarde="data/002_champ_TM310.png",
    )

    # ── Étape 4 : mode TM₀₁₀ (référence) ──────────────────────────
    print("\n▶ Calcul du champ E_z(r, θ) du mode TM₀₁₀ (référence)…")
    E_z_010 = champ_ez_tm(m=0, n=1, r=r, theta=theta, a=A)

    fig3 = plot_champ_cavite(
        r=r, theta=theta, E_z=E_z_010,
        m=0, n=1, p=0, a=A,
        titre=(
            "Mode TM$_{010}$ — Champ $E_z(r, \\theta)$ (référence)\n"
            f"f = 0,92 GHz — Mode fondamental symétrique"
        ),
        sauvegarde="data/002_champ_TM010.png",
    )

    # ── Étape 5 : mode TM₁₁₀ ──────────────────────────────────────
    print("\n▶ Calcul du champ E_z(r, θ) du mode TM₁₁₀…")
    E_z_110 = champ_ez_tm(m=1, n=1, r=r, theta=theta, a=A)

    fig4 = plot_champ_cavite(
        r=r, theta=theta, E_z=E_z_110,
        m=1, n=1, p=0, a=A,
        titre=(
            "Mode TM$_{110}$ — Champ $E_z(r, \\theta)$\n"
            f"f = 1,46 GHz — Mode dipolaire"
        ),
        sauvegarde="data/002_champ_TM110.png",
    )

    # ── Étape 6 : figure comparative multi-modes ────────────────────
    print("\n▶ Figure comparative des modes TM₀₁₀, TM₁₁₀, TM₃₁₀…")

    fig5, axes = plt.subplots(1, 3, figsize=(18, 5), subplot_kw={"polar": True})
    R_mesh, Theta_mesh = np.meshgrid(r, theta)

    for ax, (m_idx, n_idx, label, champ) in zip(axes, [
        (0, 1, "TM$_{010}$ — 0,92 GHz", E_z_010),
        (1, 1, "TM$_{110}$ — 1,46 GHz", E_z_110),
        (3, 1, "TM$_{310}$ — 2,44 GHz ✔", E_z_310),
    ]):
        vmax = np.max(np.abs(champ))
        ax.pcolormesh(
            Theta_mesh, R_mesh * 1e3, champ,
            cmap="RdBu_r", shading="gouraud",
            vmin=-vmax, vmax=vmax,
        )
        ax.set_title(label, fontsize=11, pad=15)
        ax.set_ylim(0, A * 1e3)
        ax.set_rticks([25, 50, 75, 100, 125])
        ax.set_rlabel_position(45)

    fig5.suptitle(
        "Comparaison des modes TM — Champ $E_z(r, \\theta)$",
        fontsize=14, fontweight="bold", y=1.05,
    )
    plt.tight_layout()
    fig5.savefig("data/002_comparaison_modes.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/002_comparaison_modes.png")

    # ── Étape 7 : analyse physique du mode TM₃₁₀ ───────────────────
    print("\n" + "═" * 60)
    print("  ANALYSE PHYSIQUE — Mode TM₃₁₀")
    print("═" * 60)

    f_310 = frequence_tm(3, 1, 0, A, D)
    x_31 = jn_zeros(3, 1)[-1]

    print(f"""
  Mode dominant : TM₃₁₀
  Fréquence :     {f_310/1e9:.4f} GHz (magnétron : 2,4500 GHz)
  Écart :         {abs(f_310 - F_MAGNETRON)/1e6:.1f} MHz
  Accord :        {'EXCELLENT' if abs(f_310 - F_MAGNETRON) < 50e6 else 'BON'}

  Paramètres du mode :
    m = 3  →  3 lobes azimutaux (symétrie hexagonale partielle)
    n = 1  →  1 maximum radial (1er zéro de J₃, x₃₁ = {x_31:.3f})
    p = 0  →  champ uniforme selon z (mode « en galette »)

  Interprétation pour l'expérience :
    Le champ E_z présente 6 régions alternées (3 positives, 3 négatives)
    réparties sur 360°. Cette structure angulaire NON uniforme est
    favorable à la création d'un gradient de phase asymétrique lorsque
    le plasma modifie localement l'indice de réfraction.

    Si le plasma est plus dense d'un côté (asymétrie naturelle due
    à la position du magnétron), l'onde accumule une phase différente
    dans chaque lobe → ∇S ≠ 0 → force de guidage bohmienne.

  Modes voisins pouvant être excités par la largeur spectrale
  du magnétron (Δf ~ 50 MHz) :
    - TM₃₁₀ à {f_310/1e9:.2f} GHz (mode principal)""")

    # Recherche des modes proches dans la bande ±50 MHz
    for mode in modes:
        if mode["nom"] != "TM_310" and mode["ecart_MHz"] < 250:
            print(
                f"    - {mode['nom']} à {mode['freq']/1e9:.2f} GHz"
                f" (écart = {mode['ecart_MHz']:.0f} MHz)"
            )

    # ── Étape 8 : sauvegarde des données ────────────────────────────
    print("\n▶ Sauvegarde des données…")
    sauvegarder_resultats(modes)

    # Sauvegarde du champ TM₃₁₀
    np.save("data/002_champ_TM310.npy", E_z_310)
    print("  💾 Champ TM₃₁₀ sauvegardé → data/002_champ_TM310.npy")

    print("\n✅ Expérience 002 terminée.\n")
    plt.show()
