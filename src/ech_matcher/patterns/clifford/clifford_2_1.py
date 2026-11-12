from copy import copy
from ...graph import Circuit, Gate

def clifford_2_1() -> Circuit:
    """

        q_0: ─■──■─
              │  │
        q_1: ─■──■─

    Returns:
        Circuit: template as a quantum circuit.
    """
    cz_01 = Gate('z', {0: 1}, 1)
    cir = Circuit(2, [cz_01, copy(cz_01)])
    return cir
