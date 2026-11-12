from copy import copy
from ...graph import Circuit, Gate

def nct_7b_1() -> Circuit:
    """

             ┌───┐                    ┌───┐
        q_0: ┤ X ├──■─────────■────■──┤ X ├──■──
             └───┘┌─┴─┐       │  ┌─┴─┐└───┘  │
        q_1: ─────┤ X ├──■────■──┤ X ├───────■──
                  └───┘┌─┴─┐┌─┴─┐└───┘     ┌─┴─┐
        q_2: ──────────┤ X ├┤ X ├──────────┤ X ├
                       └───┘└───┘          └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    x_0 = Gate('x', {}, 0)
    cx_01 = Gate('x', {0: 1}, 1)
    cx_12 = Gate('x', {1: 1}, 2)
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cir = Circuit(3, [x_0, cx_01, cx_12, ccx_012, copy(cx_01), copy(x_0), copy(ccx_012)])
    return cir
