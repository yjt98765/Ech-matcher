from copy import copy
from ...graph import Circuit, Gate

def nct_7c_1() -> Circuit:
    """

             ┌───┐                    ┌───┐
        q_0: ┤ X ├──■─────────■────■──┤ X ├──■──
             └───┘┌─┴─┐       │  ┌─┴─┐└───┘  │
        q_1: ─────┤ X ├──■────■──┤ X ├───────■──
                  └─┬─┘┌─┴─┐┌─┴─┐└─┬─┘     ┌─┴─┐
        q_2: ───────■──┤ X ├┤ X ├──■───────┤ X ├
                       └───┘└───┘          └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    x_0 = Gate('x', {}, 0)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cx_12 = Gate('x', {1: 1}, 2)
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cir = Circuit(3, [x_0, ccx_021, cx_12, ccx_012, copy(ccx_021), copy(x_0), copy(ccx_012)])
    return cir
