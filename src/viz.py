"""
Utilitaires de visualisation quantique.

Usage:
    from src.viz import bloch_sphere, plot_statevector
"""
import numpy as np


def statevector_to_bloch(statevector: np.ndarray) -> tuple[float, float, float]:
    """Convertit un statevector |ψ⟩ en coordonnées (x, y, z) sur la sphère de Bloch."""
    alpha, beta = statevector[0], statevector[1]
    x = 2 * (alpha.conj() * beta).real
    y = 2 * (alpha.conj() * beta).imag
    z = abs(alpha) ** 2 - abs(beta) ** 2
    return x, y, z


def bloch_sphere(statevector: np.ndarray, title: str = "État quantique") -> None:
    """Affiche l'état d'un qubit sur la sphère de Bloch (matplotlib)."""
    try:
        from qiskit.visualization import plot_bloch_vector
        x, y, z = statevector_to_bloch(statevector)
        return plot_bloch_vector([x, y, z], title=title)
    except ImportError:
        raise ImportError("qiskit requis : pip install qiskit")
