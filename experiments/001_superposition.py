"""
Expérience 001 — Superposition et mesure d'un qubit.

Un circuit Hadamard simple : |0⟩ → H → |+⟩
On mesure la distribution statistique après N shots.
"""
import numpy as np


def run_qiskit(shots: int = 1024):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    qc = QuantumCircuit(1, 1)
    qc.h(0)          # superposition : |0⟩ → |+⟩ = (|0⟩ + |1⟩)/√2
    qc.measure(0, 0)

    sim = AerSimulator()
    job = sim.run(qc, shots=shots)
    counts = job.result().get_counts()

    print(f"Résultats ({shots} shots) :")
    for state, count in sorted(counts.items()):
        bar = "█" * int(count / shots * 40)
        print(f"  |{state}⟩  {count:5d}  {bar}")
    return counts


def run_pennylane(shots: int = 1024):
    import pennylane as qml

    dev = qml.device("default.qubit", wires=1, shots=shots)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))

    samples = circuit()
    zeros = int(np.sum(samples == 1))   # PauliZ: +1 = |0⟩, -1 = |1⟩
    ones  = shots - zeros

    print(f"Résultats PennyLane ({shots} shots) :")
    print(f"  |0⟩  {zeros:5d}  {'█' * int(zeros/shots*40)}")
    print(f"  |1⟩  {ones:5d}  {'█' * int(ones/shots*40)}")


if __name__ == "__main__":
    print("=== Expérience 001 : Superposition H|0⟩ ===\n")
    try:
        run_qiskit()
    except ImportError:
        print("(qiskit-aer non installé — tentative PennyLane)")
        run_pennylane()
