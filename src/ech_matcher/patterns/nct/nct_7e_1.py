from copy import copy
from ...graph import Circuit, Gate

def nct_7e_1() -> Circuit:
    """

             ┌───┐                    ┌───┐
        q_0: ┤ X ├──■─────────■────■──┤ X ├──■──
             └───┘┌─┴─┐       │  ┌─┴─┐└───┘  │
        q_1: ─────┤ X ├───────┼──┤ X ├───────┼──
                  └─┬─┘┌───┐┌─┴─┐└─┬─┘     ┌─┴─┐
        q_2: ───────■──┤ X ├┤ X ├──■───────┤ X ├
                       └───┘└───┘          └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    x_0 = Gate('x', {}, 0)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    x_2 = Gate('x', {}, 2)
    cx_02 = Gate('x', {0: 1}, 2)
    cir = Circuit(3, [x_0, ccx_021, x_2, cx_02, copy(ccx_021), copy(x_0), copy(cx_02)])
    return cir
