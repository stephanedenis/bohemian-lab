"""
Expérience 005 — Circuits quantiques et accumulation de phase.

Simule l'accumulation de phase dans le plasma en utilisant des circuits
quantiques (Qiskit + fallback PennyLane), avec une analogie directe entre
les portes de phase et la physique de la cavité.

Analogie circuit quantique ↔ physique du plasma :
    ┌──────────────────────────┬───────────────────────────────────────┐
    │ Circuit quantique         │ Physique du plasma                    │
    ├──────────────────────────┼───────────────────────────────────────┤
    │ Porte H (Hadamard)       │ Création de l'onde pilote (ψ = R·e^iS)│
    │ Porte Rz(φ)              │ Accumulation de phase dans le plasma  │
    │ Phase φ                  │ S = ∫ n(r) × (ω/c) dl               │
    │ Amplitude |α|, |β|      │ Amplitude R de l'onde                 │
    │ Mesure                   │ Effondrement → sélection trajectoire  │
    │ 2 qubits intriqués       │ Corrélations non-locales de Q         │
    │ Circuit paramétrisé      │ Contrôle de n_e par pression/puissance│
    └──────────────────────────┴───────────────────────────────────────┘

    Dans le formalisme de la sphère de Bloch :
    - La latitude (θ) correspond au rapport R₀/R₁ (amplitude relative)
    - La longitude (φ) correspond à la phase S — c'est le paramètre
      que le plasma modifie.
    - Appliquer Rz(φ) revient à tourner le vecteur de Bloch autour de
      l'axe z d'un angle φ, modifiant la phase relative entre |0⟩ et |1⟩.

Scénarios :
    1. Phase unique — Un qubit avec Rz(φ) : visualisation sur Bloch.
    2. Balayage de phase — φ de 0 à 2π : probabilités vs phase.
    3. Double qubit — Intrication + phases locales : corrélations.
    4. Circuit paramétrisé — Analogie avec le contrôle PID du plasma.
    5. Gradient de phase — Circuit multi-qubit simulant le ∇S spatial.

Sorties :
    - Sphères de Bloch pour chaque phase.
    - Courbe P(|1⟩) vs φ.
    - Matrices de densité et corrélations.
    - Données dans data/simulations/005_*.csv et .npy.

Références :
    [1] Nielsen & Chuang (2000). Quantum Computation and Quantum Information.
    [2] Bohm, D. (1952). Physical Review, 85(2), 166–193.
    [3] Qiskit Textbook — https://qiskit.org/textbook
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.viz import statevector_to_bloch


# ═══════════════════════════════════════════════════════════════════════
# Détection du backend : Qiskit ou PennyLane
# ═══════════════════════════════════════════════════════════════════════

QISKIT_DISPONIBLE: bool = False
PENNYLANE_DISPONIBLE: bool = False

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    from qiskit_aer import AerSimulator
    QISKIT_DISPONIBLE = True
except ImportError:
    pass

try:
    import pennylane as qml
    PENNYLANE_DISPONIBLE = True
except ImportError:
    pass


# ═══════════════════════════════════════════════════════════════════════
# Scénario 1 : Phase unique — Rz(φ) sur un qubit
# ═══════════════════════════════════════════════════════════════════════

def scenario_phase_unique(phi: float = np.pi / 3) -> dict:
    """Applique une phase Rz(φ) à un qubit en superposition.

    Circuit :  |0⟩ ─── H ─── Rz(φ) ─── Mesure

    L'état après Rz(φ) est :
        |ψ⟩ = (e^{-iφ/2}|0⟩ + e^{iφ/2}|1⟩) / √2

    La phase φ est l'analogue de la phase accumulée S dans le plasma.
    Sur la sphère de Bloch, c'est une rotation autour de l'axe z.

    Args:
        phi: Phase appliquée (rad).

    Returns:
        Dict avec statevector, coordonnées Bloch, probabilités.
    """
    if QISKIT_DISPONIBLE:
        qc = QuantumCircuit(1)
        qc.h(0)          # |0⟩ → |+⟩
        qc.rz(phi, 0)    # Rotation de phase

        sv = Statevector.from_instruction(qc)
        probs = sv.probabilities_dict()
        bloch = statevector_to_bloch(sv.data)

        return {
            "statevector": sv.data,
            "bloch": bloch,
            "probs": probs,
            "phi": phi,
            "backend": "qiskit",
        }

    elif PENNYLANE_DISPONIBLE:
        dev = qml.device("default.qubit", wires=1)

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            qml.RZ(phi, wires=0)
            return qml.state()

        sv = circuit()
        bloch = statevector_to_bloch(np.array(sv))
        p0 = float(np.abs(sv[0])**2)
        p1 = float(np.abs(sv[1])**2)

        return {
            "statevector": np.array(sv),
            "bloch": bloch,
            "probs": {"0": p0, "1": p1},
            "phi": phi,
            "backend": "pennylane",
        }

    else:
        raise ImportError("Ni Qiskit ni PennyLane n'est installé.")


# ═══════════════════════════════════════════════════════════════════════
# Scénario 2 : Balayage de phase — P(|1⟩) vs φ
# ═══════════════════════════════════════════════════════════════════════

def scenario_balayage_phase(
    n_points: int = 50,
    shots: int = 1024,
) -> dict:
    """Balaye la phase φ de 0 à 2π et mesure P(|1⟩) pour chaque valeur.

    Circuit :  |0⟩ ─── H ─── Rz(φ) ─── H ─── Mesure

    La deuxième porte H convertit la phase en amplitude mesurable.
    Sans la 2e H, P(|1⟩) = 0.5 ∀ φ (la phase seule n'est pas observable
    sans interférence). Avec la 2e H :

        P(|1⟩) = sin²(φ/2)

    C'est l'analogue d'un interféromètre de Ramsey :
    - 1er H = séparation du faisceau (création de superposition)
    - Rz(φ) = accumulation de phase dans le milieu (plasma)
    - 2e H = recombinaison (interférence)
    - Mesure = détection

    Cette courbe sinusoïdale est la « signature » de la phase
    accumulée, directement analogue à ce que mesurerait un
    interféromètre optique traversant le plasma.

    Args:
        n_points: Nombre de valeurs de φ à scanner.
        shots: Nombre de tirs par mesure.

    Returns:
        Dict avec phases, probs_theoriques, probs_mesurees.
    """
    phases = np.linspace(0, 2 * np.pi, n_points)
    probs_theo = np.sin(phases / 2)**2
    probs_mes = np.zeros(n_points)

    if QISKIT_DISPONIBLE:
        sim = AerSimulator()
        for i, phi in enumerate(phases):
            qc = QuantumCircuit(1, 1)
            qc.h(0)
            qc.rz(phi, 0)
            qc.h(0)
            qc.measure(0, 0)

            job = sim.run(qc, shots=shots)
            counts = job.result().get_counts()
            probs_mes[i] = counts.get("1", 0) / shots

        backend_nom = "qiskit"

    elif PENNYLANE_DISPONIBLE:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def circuit(phi):
            qml.Hadamard(wires=0)
            qml.RZ(phi, wires=0)
            qml.Hadamard(wires=0)
            return qml.expval(qml.PauliZ(0))

        for i, phi in enumerate(phases):
            expval_z = float(circuit(phi))
            probs_mes[i] = (1 - expval_z) / 2  # P(|1⟩) = (1 - ⟨Z⟩)/2

        backend_nom = "pennylane"

    else:
        probs_mes = probs_theo.copy()
        backend_nom = "analytique"

    return {
        "phases": phases,
        "probs_theoriques": probs_theo,
        "probs_mesurees": probs_mes,
        "shots": shots,
        "backend": backend_nom,
    }


# ═══════════════════════════════════════════════════════════════════════
# Scénario 3 : Intrication + phases locales
# ═══════════════════════════════════════════════════════════════════════

def scenario_intrication_phase(
    phi_1: float = np.pi / 4,
    phi_2: float = np.pi / 2,
    shots: int = 2048,
) -> dict:
    """Deux qubits intriqués avec des phases locales différentes.

    Circuit :
        |0⟩ ─── H ─── ●── Rz(φ₁) ─── Mesure
                       │
        |0⟩ ─────── X ── Rz(φ₂) ─── Mesure

    L'état de Bell |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 est créé, puis chaque
    qubit reçoit une phase locale différente (φ₁ et φ₂).

    Dans l'interprétation bohmienne, l'intrication signifie que le
    potentiel quantique Q dépend des positions des DEUX particules
    simultanément — c'est la non-localité. Un changement de phase sur
    le qubit 1 affecte instantanément les corrélations avec le qubit 2.

    Cette simulation explore comment les corrélations changent quand
    on modifie les « phases plasma » indépendamment sur chaque qubit.

    Args:
        phi_1: Phase appliquée au qubit 1 (rad).
        phi_2: Phase appliquée au qubit 2 (rad).
        shots: Nombre de tirs.

    Returns:
        Dict avec statevector, probs, concurrence.
    """
    if QISKIT_DISPONIBLE:
        qc = QuantumCircuit(2, 2)
        qc.h(0)              # Superposition qubit 0
        qc.cx(0, 1)          # Intrication : |Φ⁺⟩
        qc.rz(phi_1, 0)      # Phase locale qubit 0
        qc.rz(phi_2, 1)      # Phase locale qubit 1
        qc.measure([0, 1], [0, 1])

        # Statevector (sans mesure)
        qc_sv = QuantumCircuit(2)
        qc_sv.h(0)
        qc_sv.cx(0, 1)
        qc_sv.rz(phi_1, 0)
        qc_sv.rz(phi_2, 1)
        sv = Statevector.from_instruction(qc_sv)

        # Mesure statistique
        sim = AerSimulator()
        job = sim.run(qc, shots=shots)
        counts = job.result().get_counts()

        # Probabilités
        probs = {k: v / shots for k, v in counts.items()}

        return {
            "statevector": sv.data,
            "probs": probs,
            "phi_1": phi_1,
            "phi_2": phi_2,
            "backend": "qiskit",
        }

    elif PENNYLANE_DISPONIBLE:
        dev = qml.device("default.qubit", wires=2, shots=shots)

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            qml.RZ(phi_1, wires=0)
            qml.RZ(phi_2, wires=1)
            return qml.probs(wires=[0, 1])

        probs_array = circuit()
        labels = ["00", "01", "10", "11"]
        probs = {l: float(p) for l, p in zip(labels, probs_array)}

        # Statevector exact
        dev_exact = qml.device("default.qubit", wires=2)

        @qml.qnode(dev_exact)
        def circuit_sv():
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            qml.RZ(phi_1, wires=0)
            qml.RZ(phi_2, wires=1)
            return qml.state()

        sv = np.array(circuit_sv())

        return {
            "statevector": sv,
            "probs": probs,
            "phi_1": phi_1,
            "phi_2": phi_2,
            "backend": "pennylane",
        }

    else:
        raise ImportError("Ni Qiskit ni PennyLane n'est installé.")


# ═══════════════════════════════════════════════════════════════════════
# Scénario 4 : Circuit paramétrisé — analogie contrôle PID
# ═══════════════════════════════════════════════════════════════════════

def scenario_circuit_parametrise(
    n_couches: int = 4,
    n_points: int = 30,
) -> dict:
    """Circuit paramétrisé multi-couche simulant le contrôle de phase.

    Circuit (n_couches couches) :
        |0⟩ ── [Ry(θ_k) ── Rz(φ_k)] × n_couches ── Mesure

    Chaque couche ajoute une rotation :
    - Ry(θ) modifie l'amplitude (analogue : puissance du magnétron)
    - Rz(φ) modifie la phase (analogue : densité du plasma)

    On balaye les paramètres (θ, φ) pour cartographier l'espace
    des configurations accessibles — c'est l'analogue de l'espace
    (pression, puissance) du contrôle PID du plasma.

    Le « paysage de coût » résultant montre les combinaisons optimales
    de paramètres, similaire à la recherche du point de fonctionnement
    optimal f_p = 2,45 GHz.

    Args:
        n_couches: Nombre de couches Ry-Rz.
        n_points: Résolution de la grille de paramètres.

    Returns:
        Dict avec grilles theta, phi, et carte d'expectation.
    """
    thetas = np.linspace(0, np.pi, n_points)
    phis = np.linspace(0, 2 * np.pi, n_points)
    paysage = np.zeros((n_points, n_points))

    if QISKIT_DISPONIBLE:
        for i, theta in enumerate(thetas):
            for j, phi in enumerate(phis):
                qc = QuantumCircuit(1)
                for _ in range(n_couches):
                    qc.ry(theta, 0)
                    qc.rz(phi, 0)
                sv = Statevector.from_instruction(qc)
                # P(|1⟩) = |⟨1|ψ⟩|²
                paysage[i, j] = float(np.abs(sv.data[1])**2)

    elif PENNYLANE_DISPONIBLE:
        dev = qml.device("default.qubit", wires=1)

        @qml.qnode(dev)
        def circuit(theta, phi):
            for _ in range(n_couches):
                qml.RY(theta, wires=0)
                qml.RZ(phi, wires=0)
            return qml.expval(qml.PauliZ(0))

        for i, theta in enumerate(thetas):
            for j, phi in enumerate(phis):
                expval_z = float(circuit(theta, phi))
                paysage[i, j] = (1 - expval_z) / 2

    else:
        # Modèle analytique approximatif
        Theta, Phi = np.meshgrid(thetas, phis, indexing="ij")
        paysage = np.sin(n_couches * Theta / 2)**2

    return {
        "thetas": thetas,
        "phis": phis,
        "paysage": paysage,
        "n_couches": n_couches,
    }


# ═══════════════════════════════════════════════════════════════════════
# Scénario 5 : Gradient de phase multi-qubit
# ═══════════════════════════════════════════════════════════════════════

def scenario_gradient_phase(
    n_qubits: int = 8,
    shots: int = 2048,
) -> dict:
    """Circuit multi-qubit avec un gradient de phase spatial.

    Chaque qubit reçoit une phase φ_k = 2π × k / n_qubits, simulant
    un gradient de phase ∇S le long d'une ligne de 8 points — analogie
    avec les 8 tubes Nixie IN-13 disposés en octogone dans la cavité.

    Circuit :
        |0⟩_k ── H ── Rz(φ_k) ── H ── Mesure   pour k = 0, …, n-1

    Les probabilités P(|1⟩)_k = sin²(φ_k/2) varient spatialement,
    créant un « pattern d'interférence » linéaire. C'est l'analogue
    numérique de la cartographie Nixie du gradient de densité plasma.

    Args:
        n_qubits: Nombre de qubits (= nombre de capteurs Nixie).
        shots: Nombre de tirs par qubit.

    Returns:
        Dict avec phases, probabilités, positions angulaires.
    """
    # Phases assignées à chaque qubit (gradient linéaire en θ)
    angles_nixie = np.linspace(0, 2 * np.pi, n_qubits, endpoint=False)
    phases = np.linspace(0, 2 * np.pi, n_qubits, endpoint=False)

    # Probabilités théoriques
    probs_theo = np.sin(phases / 2)**2

    # Simulation
    probs_mes = np.zeros(n_qubits)

    if QISKIT_DISPONIBLE:
        sim = AerSimulator()
        for k in range(n_qubits):
            qc = QuantumCircuit(1, 1)
            qc.h(0)
            qc.rz(phases[k], 0)
            qc.h(0)
            qc.measure(0, 0)
            job = sim.run(qc, shots=shots)
            counts = job.result().get_counts()
            probs_mes[k] = counts.get("1", 0) / shots

    elif PENNYLANE_DISPONIBLE:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def circuit(phi):
            qml.Hadamard(wires=0)
            qml.RZ(phi, wires=0)
            qml.Hadamard(wires=0)
            return qml.expval(qml.PauliZ(0))

        for k in range(n_qubits):
            expval = float(circuit(phases[k]))
            probs_mes[k] = (1 - expval) / 2

    else:
        probs_mes = probs_theo + np.random.normal(0, 0.02, n_qubits)

    return {
        "n_qubits": n_qubits,
        "angles_nixie": angles_nixie,
        "phases": phases,
        "probs_theoriques": probs_theo,
        "probs_mesurees": probs_mes,
    }


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée principal
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Expérience 005 — Circuits quantiques et phase plasma    ║")
    print("║  Analogie : portes Rz ↔ accumulation de phase dans le    ║")
    print("║  plasma — interféromètre de Ramsey quantique             ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    backend = "qiskit" if QISKIT_DISPONIBLE else (
        "pennylane" if PENNYLANE_DISPONIBLE else "analytique"
    )
    print(f"  Backend utilisé : {backend}\n")

    # ── Scénario 1 : Phase unique ────────────────────────────────────
    print("▶ Scénario 1 — Phase unique Rz(φ) sur un qubit")

    phases_demo = [0, np.pi/6, np.pi/3, np.pi/2, np.pi, 3*np.pi/2]
    fig1, axes1 = plt.subplots(2, 3, figsize=(15, 10))

    for ax, phi in zip(axes1.flat, phases_demo):
        resultat = scenario_phase_unique(phi)
        bx, by, bz = resultat["bloch"]

        # Dessin simplifié de la sphère de Bloch (projection)
        cercle = plt.Circle((0, 0), 1, fill=False, color="gray",
                            linestyle="--", linewidth=0.8)
        ax.add_patch(cercle)
        ax.arrow(0, 0, bx * 0.9, by * 0.9,
                 head_width=0.06, head_length=0.04,
                 fc="#e74c3c", ec="#c0392b", linewidth=2)
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect("equal")
        ax.axhline(0, color="gray", linewidth=0.3)
        ax.axvline(0, color="gray", linewidth=0.3)
        ax.set_title(
            f"$\\phi$ = {phi:.2f} rad ({np.degrees(phi):.0f}°)\n"
            f"Bloch: ({bx:.2f}, {by:.2f}, {bz:.2f})",
            fontsize=10,
        )
        ax.set_xlabel("x (Bloch)")
        ax.set_ylabel("y (Bloch)")
        ax.grid(True, alpha=0.2)

    fig1.suptitle(
        "Scénario 1 — Rotation de phase Rz(φ) sur la sphère de Bloch\n"
        "Projection x-y : la longitude correspond à la phase S accumulée dans le plasma",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()
    fig1.savefig("data/simulations/005_phase_unique_bloch.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/simulations/005_phase_unique_bloch.png")

    # ── Scénario 2 : Balayage de phase ──────────────────────────────
    print("\n▶ Scénario 2 — Balayage de phase (interféromètre de Ramsey)")

    balayage = scenario_balayage_phase(n_points=60, shots=2048)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(
        balayage["phases"] / np.pi, balayage["probs_theoriques"],
        "b-", linewidth=2, label="Théorique : $\\sin^2(\\phi/2)$",
    )
    ax2.plot(
        balayage["phases"] / np.pi, balayage["probs_mesurees"],
        "ro", markersize=4, alpha=0.7,
        label=f"Mesuré ({balayage['shots']} shots, {balayage['backend']})",
    )

    # Annotations physiques
    ax2.axvline(0.5, color="green", linestyle=":", alpha=0.5)
    ax2.text(0.52, 0.5, "φ = π/2\n(phase π/2\ndans le plasma)",
             fontsize=8, color="green")
    ax2.axvline(1.0, color="orange", linestyle=":", alpha=0.5)
    ax2.text(1.02, 0.85, "φ = π\n(inversion\ncomplète)",
             fontsize=8, color="orange")

    ax2.set_xlabel("Phase $\\phi$ / π", fontsize=12)
    ax2.set_ylabel("$P(|1\\rangle)$", fontsize=12)
    ax2.set_title(
        "Interféromètre de Ramsey : H — Rz(φ) — H — Mesure\n"
        "Analogie : phase accumulée par l'onde RF traversant le plasma",
        fontsize=13, fontweight="bold",
    )
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 2)
    ax2.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    fig2.savefig("data/simulations/005_balayage_phase.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/simulations/005_balayage_phase.png")

    # ── Scénario 3 : Intrication + phases ───────────────────────────
    print("\n▶ Scénario 3 — Intrication Bell + phases locales")

    # Scanner les corrélations pour plusieurs combinaisons de phases
    n_scan = 20
    phis_1 = np.linspace(0, 2 * np.pi, n_scan)
    phis_2 = np.linspace(0, 2 * np.pi, n_scan)
    correlations = np.zeros((n_scan, n_scan))

    print("    Scan des corrélations (φ₁ × φ₂)…")
    for i, p1 in enumerate(phis_1):
        for j, p2 in enumerate(phis_2):
            res = scenario_intrication_phase(p1, p2, shots=512)
            # Corrélation = P(00) + P(11) − P(01) − P(10)
            p = res["probs"]
            corr = (
                p.get("00", 0) + p.get("11", 0)
                - p.get("01", 0) - p.get("10", 0)
            )
            correlations[i, j] = corr

    fig3, ax3 = plt.subplots(figsize=(8, 7))
    im3 = ax3.pcolormesh(
        phis_1 / np.pi, phis_2 / np.pi, correlations.T,
        cmap="RdBu_r", shading="gouraud", vmin=-1, vmax=1,
    )
    fig3.colorbar(im3, ax=ax3, label="Corrélation $C = P_{00}+P_{11}-P_{01}-P_{10}$")
    ax3.set_xlabel("Phase qubit 1 : $\\phi_1$ / π", fontsize=12)
    ax3.set_ylabel("Phase qubit 2 : $\\phi_2$ / π", fontsize=12)
    ax3.set_title(
        "Corrélations quantiques — Bell + Rz local\n"
        "Analogie : non-localité du potentiel quantique Q",
        fontsize=13, fontweight="bold",
    )
    ax3.set_aspect("equal")
    plt.tight_layout()
    fig3.savefig("data/simulations/005_correlations_bell.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/simulations/005_correlations_bell.png")

    # ── Scénario 4 : Circuit paramétrisé ────────────────────────────
    print("\n▶ Scénario 4 — Paysage de coût (analogie espace pression-puissance)")

    paysage = scenario_circuit_parametrise(n_couches=4, n_points=40)

    fig4, ax4 = plt.subplots(figsize=(9, 7))
    im4 = ax4.pcolormesh(
        paysage["phis"] / np.pi, paysage["thetas"] / np.pi,
        paysage["paysage"],
        cmap="viridis", shading="gouraud",
    )
    fig4.colorbar(im4, ax=ax4, label="$P(|1\\rangle)$")
    ax4.set_xlabel(
        "Phase $\\phi$ / π\n(↔ densité plasma → pression de vapeur)", fontsize=11,
    )
    ax4.set_ylabel(
        "Amplitude $\\theta$ / π\n(↔ amplitude onde → puissance magnétron)", fontsize=11,
    )
    ax4.set_title(
        f"Paysage de coût — Circuit paramétrisé ({paysage['n_couches']} couches)\n"
        "Analogie : espace de contrôle (pression, puissance) du plasma",
        fontsize=13, fontweight="bold",
    )

    # Marquer le point de fonctionnement optimal (P(1) ≈ cible)
    cible = 0.5  # 50% — point de sensibilité maximale
    cs = ax4.contour(
        paysage["phis"] / np.pi, paysage["thetas"] / np.pi,
        paysage["paysage"],
        levels=[cible], colors=["red"], linewidths=2,
    )
    ax4.clabel(cs, fmt=f"P = {cible:.1f}", fontsize=9)

    plt.tight_layout()
    fig4.savefig("data/simulations/005_paysage_parametrise.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/simulations/005_paysage_parametrise.png")

    # ── Scénario 5 : Gradient de phase multi-qubit ──────────────────
    print("\n▶ Scénario 5 — Gradient de phase spatial (8 qubits = 8 Nixie)")

    gradient = scenario_gradient_phase(n_qubits=8, shots=4096)

    fig5, axes5 = plt.subplots(1, 2, figsize=(14, 5))

    # Panneau 1 : histogramme linéaire
    x_pos = np.arange(gradient["n_qubits"])
    axes5[0].bar(
        x_pos - 0.15, gradient["probs_theoriques"],
        width=0.3, color="#3498db", label="Théorique",
    )
    axes5[0].bar(
        x_pos + 0.15, gradient["probs_mesurees"],
        width=0.3, color="#e74c3c", alpha=0.7, label="Mesuré",
    )
    axes5[0].set_xlabel("Qubit (= position Nixie)", fontsize=11)
    axes5[0].set_ylabel("$P(|1\\rangle) = \\sin^2(\\phi_k/2)$", fontsize=11)
    axes5[0].set_title("Gradient de phase — réponse par qubit")
    axes5[0].set_xticks(x_pos)
    axes5[0].set_xticklabels(
        [f"Nixie {k}\n({np.degrees(a):.0f}°)"
         for k, a in enumerate(gradient["angles_nixie"])],
        fontsize=8,
    )
    axes5[0].legend()
    axes5[0].grid(True, axis="y", alpha=0.3)

    # Panneau 2 : vue polaire (octogone Nixie)
    ax_pol = fig5.add_axes([0.58, 0.1, 0.38, 0.8], polar=True)

    angles = gradient["angles_nixie"]
    # Fermer le polygone
    angles_ferme = np.append(angles, angles[0])
    probs_ferme = np.append(gradient["probs_mesurees"], gradient["probs_mesurees"][0])
    theo_ferme = np.append(gradient["probs_theoriques"], gradient["probs_theoriques"][0])

    ax_pol.plot(angles_ferme, theo_ferme, "b--", linewidth=1.5, label="Théorique")
    ax_pol.fill(angles_ferme, probs_ferme, alpha=0.3, color="red")
    ax_pol.plot(angles_ferme, probs_ferme, "r-o", markersize=6, label="Mesuré")

    ax_pol.set_title(
        "Vue octogonale — Cartographie Nixie\n"
        "(signal ∝ gradient de phase ∇S)",
        fontsize=11, pad=15,
    )
    ax_pol.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.3, 1.1))
    ax_pol.set_rlabel_position(0)

    # Remplacer les étiquettes axiales (pas nécessaire, mais plus clair)
    axes5[1].set_visible(False)

    fig5.suptitle(
        "Scénario 5 — Gradient de phase multi-qubit\n"
        "Analogie: 8 capteurs Nixie IN-13 cartographiant ∇n_e autour de la cavité",
        fontsize=13, fontweight="bold",
    )
    fig5.subplots_adjust(top=0.85, wspace=0.3)
    fig5.savefig("data/simulations/005_gradient_nixie.png", dpi=150, bbox_inches="tight")
    print("  💾 Figure sauvegardée → data/simulations/005_gradient_nixie.png")

    # ── Sauvegarde des données ──────────────────────────────────────
    print("\n▶ Sauvegarde des données numériques…")
    import csv

    # Balayage de phase
    with open("data/simulations/005_balayage_phase.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["phi_rad", "phi_deg", "P1_theorique", "P1_mesuree"])
        for phi, pt, pm in zip(
            balayage["phases"],
            balayage["probs_theoriques"],
            balayage["probs_mesurees"],
        ):
            writer.writerow([f"{phi:.6f}", f"{np.degrees(phi):.2f}",
                             f"{pt:.6f}", f"{pm:.6f}"])
    print("  💾 Balayage de phase → data/simulations/005_balayage_phase.csv")

    # Corrélations Bell
    np.save("data/simulations/005_correlations_bell.npy", correlations)
    print("  💾 Corrélations Bell → data/simulations/005_correlations_bell.npy")

    # Gradient Nixie
    with open("data/simulations/005_gradient_nixie.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["qubit", "angle_deg", "phase_rad",
                         "P1_theorique", "P1_mesuree"])
        for k in range(gradient["n_qubits"]):
            writer.writerow([
                k,
                f"{np.degrees(gradient['angles_nixie'][k]):.1f}",
                f"{gradient['phases'][k]:.6f}",
                f"{gradient['probs_theoriques'][k]:.6f}",
                f"{gradient['probs_mesurees'][k]:.6f}",
            ])
    print("  💾 Gradient Nixie → data/simulations/005_gradient_nixie.csv")

    # Paysage paramétrisé
    np.save("data/simulations/005_paysage_parametrise.npy", paysage["paysage"])
    print("  💾 Paysage paramétrisé → data/simulations/005_paysage_parametrise.npy")

    # ── Résumé ──────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  RÉSUMÉ — Expérience 005")
    print("═" * 60)
    print(f"""
  Backend utilisé : {backend}

  5 scénarios simulés :

  1. Phase unique Rz(φ) :
     → 6 états sur la sphère de Bloch.
     La longitude = phase S accumulée dans le plasma.

  2. Balayage de phase (interféromètre de Ramsey) :
     → P(|1⟩) = sin²(φ/2) — courbe d'interférence.
     Analogie : interféromètre optique traversant le plasma.

  3. Intrication Bell + phases locales :
     → Carte de corrélations C(φ₁, φ₂).
     Analogie : non-localité du potentiel quantique Q.

  4. Circuit paramétrisé (4 couches) :
     → Paysage de coût P(θ, φ).
     Analogie : espace de contrôle (pression, puissance) du PID.

  5. Gradient de phase multi-qubit (8 qubits) :
     → Cartographie octogonale des probabilités.
     Analogie directe : 8 tubes Nixie IN-13 mesurant ∇n_e.

  Lien avec la théorie :
     La phase φ du circuit ↔ S = ∫ n(r)·(ω/c)·dl dans le plasma.
     La porte Rz(φ) est l'opérateur de translation de phase,
     exactement ce que le plasma fait à l'onde RF du magnétron.
     Le gradient de phase ∇S → force de guidage v = ∇S/m (Bohm).
""")

    print("✅ Expérience 005 terminée.\n")
    plt.show()
