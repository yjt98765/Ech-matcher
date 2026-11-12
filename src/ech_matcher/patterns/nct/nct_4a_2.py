from copy import copy
from ...graph import Circuit, Gate

def nct_4a_2() -> Circuit:
    """

        q_0: ──■─────────■───────
               │         │
        q_1: ──■────■────■────■──
               │  ┌─┴─┐  │  ┌─┴─┐
        q_2: ──┼──┤ X ├──┼──┤ X ├
             ┌─┴─┐└───┘┌─┴─┐└───┘
        q_3: ┤ X ├─────┤ X ├─────
             └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_013 = Gate('x', {0: 1, 1: 1}, 3)
    cx_12 = Gate('x', {1: 1}, 2)
    cir = Circuit(4, [ccx_013, cx_12, copy(ccx_013), copy(cx_12)])
    return cir
