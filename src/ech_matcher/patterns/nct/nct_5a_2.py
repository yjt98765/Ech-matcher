from copy import copy
from ...graph import Circuit, Gate

def nct_5a_2() -> Circuit:
    """

        q_0: ──■─────────■─────────■──
               │  ┌───┐  │  ┌───┐  │
        q_1: ──■──┤ X ├──■──┤ X ├──┼──
             ┌─┴─┐└───┘┌─┴─┐└───┘┌─┴─┐
        q_2: ┤ X ├─────┤ X ├─────┤ X ├
             └───┘     └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    x_1 = Gate('x', {}, 1)
    cx_02 = Gate('x', {0: 1}, 2)
    cir = Circuit(3, [ccx_012, x_1, copy(ccx_012), copy(x_1), cx_02])
    return cir
