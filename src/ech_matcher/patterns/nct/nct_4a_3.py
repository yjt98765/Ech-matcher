from copy import copy
from ...graph import Circuit, Gate

def nct_4a_3() -> Circuit:
    """

        q_0: ──■────■────■────■──
               │  ┌─┴─┐  │  ┌─┴─┐
        q_1: ──┼──┤ X ├──┼──┤ X ├
             ┌─┴─┐└───┘┌─┴─┐└───┘
        q_2: ┤ X ├─────┤ X ├─────
             └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_02 = Gate('x', {0: 1}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    cir = Circuit(3, [cx_02, cx_01, copy(cx_02), copy(cx_01)])
    return cir
