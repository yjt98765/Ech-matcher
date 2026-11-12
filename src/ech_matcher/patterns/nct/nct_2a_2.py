from copy import copy
from ...graph import Circuit, Gate

def nct_2a_2() -> Circuit:
    """

        q_0: ──■────■──
             ┌─┴─┐┌─┴─┐
        q_1: ┤ X ├┤ X ├
             └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    cir = Circuit(2, [cx_01, copy(cx_01)])
    return cir
