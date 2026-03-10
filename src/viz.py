"""
Utilitaires de visualisation quantique — Bohemian Lab.

Ce module centralise toutes les fonctions de visualisation réutilisables
du projet : sphère de Bloch, modes de cavité, profils de champ, plasma,
potentiel quantique, trajectoires bohmiennes.

Usage:
    from src.viz import (
        bloch_sphere,
        statevector_to_bloch,
        plot_modes_cavite,
        plot_champ_cavite,
        plot_profil_plasma,
        plot_potentiel_quantique,
        plot_trajectoires_bohm,
        plot_force_comparaison,
    )
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1 — Sphère de Bloch (qubit unique)
# ═══════════════════════════════════════════════════════════════════════

def statevector_to_bloch(statevector: np.ndarray) -> tuple[float, float, float]:
    """Convertit un statevector |ψ⟩ en coordonnées (x, y, z) sur la sphère de Bloch.

    Args:
        statevector: Vecteur d'état complexe à 2 composantes [α, β].

    Returns:
        Triplet (x, y, z) de coordonnées cartésiennes sur la sphère unité.
    """
    alpha, beta = statevector[0], statevector[1]
    x = 2 * (alpha.conj() * beta).real
    y = 2 * (alpha.conj() * beta).imag
    z = abs(alpha) ** 2 - abs(beta) ** 2
    return x, y, z


def bloch_sphere(statevector: np.ndarray, title: str = "État quantique") -> None:
    """Affiche l'état d'un qubit sur la sphère de Bloch (matplotlib).

    Args:
        statevector: Vecteur d'état complexe à 2 composantes.
        title: Titre du graphique.

    Returns:
        Figure matplotlib (ou objet Qiskit si disponible).
    """
    try:
        from qiskit.visualization import plot_bloch_vector
        x, y, z = statevector_to_bloch(statevector)
        return plot_bloch_vector([x, y, z], title=title)
    except ImportError:
        raise ImportError("qiskit requis : pip install qiskit")


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2 — Modes de résonance d'une cavité cylindrique
# ═══════════════════════════════════════════════════════════════════════

def plot_modes_cavite(
    modes: list[dict],
    f_cible: float = 2.45e9,
    delta_f: float = 0.3e9,
    titre: str = "Modes de résonance — Cavité cylindrique",
    sauvegarde: str | None = None,
) -> plt.Figure:
    """Diagramme en barres des fréquences de résonance de la cavité.

    Colore les modes proches de la fréquence cible (magnétron 2,45 GHz).

    Args:
        modes: Liste de dicts {'nom': str, 'freq': float (Hz), 'type': str}.
        f_cible: Fréquence cible en Hz (défaut 2,45 GHz).
        delta_f: Tolérance en Hz pour la coloration (défaut 300 MHz).
        titre: Titre du graphique.
        sauvegarde: Chemin de fichier pour sauvegarder la figure (optionnel).

    Returns:
        Figure matplotlib.
    """
    # Tri par fréquence croissante
    modes_tries = sorted(modes, key=lambda m: m["freq"])

    noms = [m["nom"] for m in modes_tries]
    freqs = [m["freq"] / 1e9 for m in modes_tries]  # en GHz
    f_cible_ghz = f_cible / 1e9
    delta_ghz = delta_f / 1e9

    # Couleurs : vert si proche de 2,45 GHz, gris sinon
    couleurs = []
    for f in freqs:
        ecart = abs(f - f_cible_ghz)
        if ecart < 0.05:
            couleurs.append("#2ecc71")    # vert vif — excellent accord
        elif ecart < delta_ghz:
            couleurs.append("#f39c12")    # orange — proche
        else:
            couleurs.append("#95a5a6")    # gris — hors bande

    fig, ax = plt.subplots(figsize=(14, 6))
    barres = ax.barh(noms, freqs, color=couleurs, edgecolor="white", height=0.6)

    # Ligne verticale à 2,45 GHz
    ax.axvline(
        f_cible_ghz, color="#e74c3c", linestyle="--", linewidth=2,
        label=f"Magnétron {f_cible_ghz:.2f} GHz",
    )

    # Bande de tolérance
    ax.axvspan(
        f_cible_ghz - delta_ghz, f_cible_ghz + delta_ghz,
        alpha=0.08, color="#e74c3c",
    )

    # Annotations des fréquences
    for barre, f in zip(barres, freqs):
        ax.text(
            f + 0.03, barre.get_y() + barre.get_height() / 2,
            f"{f:.2f} GHz", va="center", fontsize=8,
        )

    ax.set_xlabel("Fréquence (GHz)", fontsize=12)
    ax.set_title(titre, fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=10)
    ax.set_xlim(0, max(freqs) + 0.5)
    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


def plot_champ_cavite(
    r: np.ndarray,
    theta: np.ndarray,
    E_z: np.ndarray,
    m: int,
    n: int,
    p: int,
    a: float,
    titre: str | None = None,
    sauvegarde: str | None = None,
) -> plt.Figure:
    """Visualise le champ E_z(r, θ) d'un mode TM_{mnp} en coupe transversale.

    Affiche la distribution spatiale du champ électrique axial dans le plan
    perpendiculaire à l'axe de la cavité cylindrique.

    Args:
        r: Grille de coordonnées radiales (1D ou 2D meshgrid).
        theta: Grille de coordonnées angulaires (1D ou 2D meshgrid).
        E_z: Champ électrique axial E_z(r, θ), 2D.
        m: Indice azimutal du mode.
        n: Indice radial du mode.
        p: Indice axial du mode.
        a: Rayon de la cavité en mètres.
        titre: Titre personnalisé (auto-généré si None).
        sauvegarde: Chemin de fichier pour sauvegarder.

    Returns:
        Figure matplotlib.
    """
    if titre is None:
        titre = f"Mode TM$_{{{m}{n}{p}}}$ — Champ $E_z(r, \\theta)$"

    # Conversion en cartésien pour l'affichage
    if r.ndim == 1:
        R, Theta = np.meshgrid(r, theta)
    else:
        R, Theta = r, theta

    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- Panneau 1 : carte de couleur ---
    vmax = np.max(np.abs(E_z))
    im = axes[0].pcolormesh(
        X * 1e3, Y * 1e3, E_z,
        cmap="RdBu_r", shading="gouraud",
        vmin=-vmax, vmax=vmax,
    )
    # Contour de la cavité
    cercle = plt.Circle(
        (0, 0), a * 1e3, fill=False,
        edgecolor="black", linewidth=2, linestyle="--",
    )
    axes[0].add_patch(cercle)
    axes[0].set_aspect("equal")
    axes[0].set_xlabel("x (mm)")
    axes[0].set_ylabel("y (mm)")
    axes[0].set_title(titre)
    fig.colorbar(im, ax=axes[0], label="$E_z$ (normalisé)", shrink=0.8)

    # --- Panneau 2 : coupe radiale à θ=0 ---
    if theta.ndim == 1:
        idx_theta = np.argmin(np.abs(theta))
        r_coupe = r
        Ez_coupe = E_z[idx_theta, :]
    else:
        idx_theta = np.argmin(np.abs(theta[:, 0]))
        r_coupe = r[idx_theta, :]
        Ez_coupe = E_z[idx_theta, :]

    axes[1].plot(r_coupe * 1e3, Ez_coupe, "b-", linewidth=2)
    axes[1].axhline(0, color="gray", linestyle=":", linewidth=0.8)
    axes[1].axvline(a * 1e3, color="black", linestyle="--", linewidth=1.5,
                     label="Paroi ($r = a$)")
    axes[1].set_xlabel("r (mm)")
    axes[1].set_ylabel("$E_z$ (normalisé)")
    axes[1].set_title("Coupe radiale à θ = 0°")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3 — Profil plasma et indice de réfraction
# ═══════════════════════════════════════════════════════════════════════

def plot_profil_plasma(
    x: np.ndarray,
    y: np.ndarray,
    n_e: np.ndarray,
    n_refraction: np.ndarray,
    contour_chambre: float | None = None,
    titre: str = "Profil du plasma — Densité et indice de réfraction",
    sauvegarde: str | None = None,
) -> plt.Figure:
    """Visualise la densité électronique et l'indice de réfraction du plasma.

    Affiche deux panneaux côte à côte :
    - Gauche : carte de n_e(x, y) avec contour de la densité critique.
    - Droite : carte de n(x, y) avec zones de coupure (n=0).

    Args:
        x: Coordonnées x en mètres (2D meshgrid).
        y: Coordonnées y en mètres (2D meshgrid).
        n_e: Densité électronique (m⁻³), 2D.
        n_refraction: Indice de réfraction, 2D.
        contour_chambre: Rayon de la chambre en mètres (pour dessiner le cercle).
        titre: Titre global de la figure.
        sauvegarde: Chemin de fichier pour sauvegarder.

    Returns:
        Figure matplotlib.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # --- Panneau 1 : densité électronique ---
    im1 = axes[0].pcolormesh(
        x * 1e3, y * 1e3, n_e,
        cmap="inferno", shading="gouraud",
    )
    fig.colorbar(im1, ax=axes[0], label="$n_e$ (m⁻³)", shrink=0.8)
    axes[0].set_xlabel("x (mm)")
    axes[0].set_ylabel("y (mm)")
    axes[0].set_title("Densité électronique $n_e(x, y)$")
    axes[0].set_aspect("equal")

    # Contour de la densité critique (n_e,c ≈ 7,4×10¹⁶ m⁻³ pour 2,45 GHz)
    n_e_critique = 7.4e16
    try:
        cs = axes[0].contour(
            x * 1e3, y * 1e3, n_e,
            levels=[n_e_critique],
            colors=["cyan"], linewidths=2, linestyles="--",
        )
        axes[0].clabel(cs, fmt="$n_{e,c}$", fontsize=9)
    except ValueError:
        pass  # pas de contour si n_e ne traverse pas n_e,c

    # --- Panneau 2 : indice de réfraction ---
    im2 = axes[1].pcolormesh(
        x * 1e3, y * 1e3, n_refraction,
        cmap="coolwarm", shading="gouraud",
        vmin=-0.5, vmax=1.5,
    )
    fig.colorbar(im2, ax=axes[1], label="Indice de réfraction $n$", shrink=0.8)
    axes[1].set_xlabel("x (mm)")
    axes[1].set_ylabel("y (mm)")
    axes[1].set_title("Indice de réfraction $n(x, y)$")
    axes[1].set_aspect("equal")

    # Contour n=0 (coupure plasma)
    try:
        cs2 = axes[1].contour(
            x * 1e3, y * 1e3, n_refraction,
            levels=[0.0], colors=["black"], linewidths=2,
        )
        axes[1].clabel(cs2, fmt="$n=0$", fontsize=9)
    except ValueError:
        pass

    # Contour de la chambre (optionnel)
    if contour_chambre is not None:
        for ax in axes:
            cercle = plt.Circle(
                (0, 0), contour_chambre * 1e3,
                fill=False, edgecolor="white", linewidth=2, linestyle="--",
            )
            ax.add_patch(cercle)

    fig.suptitle(titre, fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4 — Potentiel quantique et gradient de force
# ═══════════════════════════════════════════════════════════════════════

def plot_potentiel_quantique(
    x: np.ndarray,
    y: np.ndarray,
    Q: np.ndarray,
    grad_Qx: np.ndarray | None = None,
    grad_Qy: np.ndarray | None = None,
    contour_chambre: float | None = None,
    titre: str = "Potentiel quantique $Q(x, y)$",
    sauvegarde: str | None = None,
) -> plt.Figure:
    """Visualise le potentiel quantique Q et son gradient −∇Q (force bohmienne).

    Args:
        x: Coordonnées x (2D meshgrid), en mètres.
        y: Coordonnées y (2D meshgrid), en mètres.
        Q: Potentiel quantique Q(x, y), 2D.
        grad_Qx: Composante x de ∇Q (optionnel, pour afficher les flèches).
        grad_Qy: Composante y de ∇Q (optionnel).
        contour_chambre: Rayon de la chambre en mètres.
        titre: Titre du graphique.
        sauvegarde: Chemin de fichier pour sauvegarder.

    Returns:
        Figure matplotlib.
    """
    n_panels = 2 if grad_Qx is not None else 1
    fig, axes = plt.subplots(1, n_panels, figsize=(7 * n_panels, 6))
    if n_panels == 1:
        axes = [axes]

    # --- Panneau 1 : carte de Q ---
    vmax = np.nanpercentile(np.abs(Q), 98)
    if vmax == 0:
        vmax = 1.0
    im = axes[0].pcolormesh(
        x * 1e3, y * 1e3, Q,
        cmap="viridis", shading="gouraud",
        vmin=-vmax, vmax=vmax,
    )
    fig.colorbar(im, ax=axes[0], label="$Q$ (unités normalisées)", shrink=0.8)
    axes[0].set_xlabel("x (mm)")
    axes[0].set_ylabel("y (mm)")
    axes[0].set_title("Potentiel quantique $Q(x, y)$")
    axes[0].set_aspect("equal")

    # --- Panneau 2 : champ de vecteurs −∇Q (force bohmienne) ---
    if grad_Qx is not None and grad_Qy is not None:
        # Sous-échantillonnage pour la lisibilité des flèches
        pas = max(1, x.shape[0] // 20)
        x_s = x[::pas, ::pas] * 1e3
        y_s = y[::pas, ::pas] * 1e3
        Fx = -grad_Qx[::pas, ::pas]  # F = −∇Q
        Fy = -grad_Qy[::pas, ::pas]

        norme_F = np.sqrt(Fx**2 + Fy**2)
        norme_max = np.nanpercentile(norme_F, 95)
        if norme_max == 0:
            norme_max = 1.0

        # Fond : norme de la force
        im2 = axes[1].pcolormesh(
            x * 1e3, y * 1e3, np.sqrt(grad_Qx**2 + grad_Qy**2),
            cmap="hot", shading="gouraud",
        )
        fig.colorbar(im2, ax=axes[1], label="$|\\nabla Q|$", shrink=0.8)

        # Flèches de force
        axes[1].quiver(
            x_s, y_s, Fx, Fy,
            color="cyan", alpha=0.8,
            scale=norme_max * 25, width=0.003,
        )

        axes[1].set_xlabel("x (mm)")
        axes[1].set_ylabel("y (mm)")
        axes[1].set_title("Force bohmienne $\\vec{F}_Q = -\\nabla Q$")
        axes[1].set_aspect("equal")

    # Contour de la chambre
    if contour_chambre is not None:
        for ax in axes:
            cercle = plt.Circle(
                (0, 0), contour_chambre * 1e3,
                fill=False, edgecolor="white", linewidth=2, linestyle="--",
            )
            ax.add_patch(cercle)

    fig.suptitle(titre, fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5 — Trajectoires bohmiennes
# ═══════════════════════════════════════════════════════════════════════

def plot_trajectoires_bohm(
    trajectoires: list[np.ndarray],
    x: np.ndarray | None = None,
    y: np.ndarray | None = None,
    fond: np.ndarray | None = None,
    fond_label: str = "$|\\psi|^2$",
    fond_cmap: str = "Blues",
    titre: str = "Trajectoires bohmiennes",
    sauvegarde: str | None = None,
) -> plt.Figure:
    """Affiche des trajectoires bohmiennes sur un fond de densité de probabilité.

    Chaque trajectoire est un array (N_pas, 2) avec les colonnes [x, y].

    Args:
        trajectoires: Liste d'arrays (N, 2) représentant les trajectoires.
        x: Grille x pour le fond (2D meshgrid, optionnel).
        y: Grille y pour le fond (2D meshgrid, optionnel).
        fond: Champ scalaire 2D à afficher en fond (ex : |ψ|², Q).
        fond_label: Étiquette de la colorbar du fond.
        fond_cmap: Palette de couleurs pour le fond.
        titre: Titre du graphique.
        sauvegarde: Chemin de fichier pour sauvegarder.

    Returns:
        Figure matplotlib.
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    # Fond optionnel
    if fond is not None and x is not None and y is not None:
        im = ax.pcolormesh(
            x, y, fond,
            cmap=fond_cmap, shading="gouraud", alpha=0.6,
        )
        fig.colorbar(im, ax=ax, label=fond_label, shrink=0.8)

    # Trajectoires avec gradient de couleur temporel
    cmap_traj = cm.get_cmap("plasma")
    for i, traj in enumerate(trajectoires):
        couleur = cmap_traj(i / max(len(trajectoires) - 1, 1))
        ax.plot(
            traj[:, 0], traj[:, 1],
            "-", color=couleur, linewidth=0.8, alpha=0.7,
        )
        # Point de départ
        ax.plot(traj[0, 0], traj[0, 1], "o", color=couleur, markersize=4)
        # Point d'arrivée
        ax.plot(traj[-1, 0], traj[-1, 1], "s", color=couleur, markersize=3)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(titre, fontsize=14, fontweight="bold")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)

    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6 — Comparaison des forces
# ═══════════════════════════════════════════════════════════════════════

def plot_force_comparaison(
    forces: dict[str, float],
    titre: str = "Comparaison des forces — Pression de radiation vs force bohmienne",
    sauvegarde: str | None = None,
) -> plt.Figure:
    """Diagramme en barres comparant les différentes contributions à la force.

    Args:
        forces: Dict {nom: valeur_en_newtons}. Ex: {'F_rad': 3.3e-6, 'F_Q': 1e-5}.
        titre: Titre du graphique.
        sauvegarde: Chemin de fichier pour sauvegarder.

    Returns:
        Figure matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    noms = list(forces.keys())
    valeurs = [forces[n] * 1e6 for n in noms]  # conversion en µN

    couleurs = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f39c12"]
    barres = ax.bar(
        noms, valeurs,
        color=couleurs[:len(noms)], edgecolor="white", width=0.5,
    )

    # Annotations
    for barre, v in zip(barres, valeurs):
        ax.text(
            barre.get_x() + barre.get_width() / 2, barre.get_height() + 0.1,
            f"{v:.2f} µN", ha="center", fontsize=11, fontweight="bold",
        )

    ax.set_ylabel("Force (µN)", fontsize=12)
    ax.set_title(titre, fontsize=13, fontweight="bold")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()

    if sauvegarde:
        fig.savefig(sauvegarde, dpi=150, bbox_inches="tight")
        print(f"  💾 Figure sauvegardée → {sauvegarde}")

    return fig
