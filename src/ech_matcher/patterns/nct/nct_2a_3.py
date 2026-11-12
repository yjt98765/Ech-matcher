from copy import copy
from ...graph import Circuit, Gate

def nct_2a_3() -> Circuit:
    """

        q_0: ──■────■──
               │    │
        q_1: ──■────■──
             ┌─┴─┐┌─┴─┐
        q_2: ┤ X ├┤ X ├
             └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cir = Circuit(3, [ccx_012, copy(ccx_012)])
    return cir
