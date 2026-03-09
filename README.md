# 🔬 Bohemian Lab

**Expérimentations en physique quantique** — simulation, computing & visualisation.

## Structure

```
notebooks/      — Jupyter : exploration interactive
experiments/    — Expériences reproductibles (scripts autonomes)
src/            — Modules réutilisables (circuits, états, mesures)
data/           — Résultats et jeux de données générés
docs/           — Notes théoriques et références
```

## Axes d'exploration

- **Simulation d'états quantiques** (qubits, portes, intrication)
- **Algorithmes quantiques** (Grover, Shor, VQE, QAOA...)
- **Informatique quantique** via Qiskit / PennyLane
- **Visualisation** (sphère de Bloch, diagrammes de circuits)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Références

- [Qiskit Textbook](https://qiskit.org/learn/)
- [PennyLane Demos](https://pennylane.ai/qml/demonstrations/)
- [Quantum Computing: An Applied Approach — Hidary](https://link.springer.com/book/10.1007/978-3-030-83274-2)
