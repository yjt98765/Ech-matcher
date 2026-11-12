from copy import copy
from ...graph import Circuit, Gate

def nct_7d_1() -> Circuit:
    """

             ┌───┐                    ┌───┐
        q_0: ┤ X ├──■─────────■────■──┤ X ├──■──
             └─┬─┘┌─┴─┐       │  ┌─┴─┐└─┬─┘  │
        q_1: ──■──┤ X ├──■────■──┤ X ├──■────■──
                  └─┬─┘┌─┴─┐┌─┴─┐└─┬─┘     ┌─┴─┐
        q_2: ───────■──┤ X ├┤ X ├──■───────┤ X ├
                       └───┘└───┘          └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_10 = Gate('x', {1: 1}, 0)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cx_12 = Gate('x', {1: 1}, 2)
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cir = Circuit(3, [cx_10, ccx_021, cx_12, ccx_012, copy(ccx_021), copy(cx_10), copy(ccx_012)])
    return cir
