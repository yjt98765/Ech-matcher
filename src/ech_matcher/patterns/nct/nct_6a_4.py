from copy import copy
from ...graph import Circuit, Gate

def nct_6a_4() -> Circuit:
    """

        q_0: ───────■──────────────■───────
                  ┌─┴─┐     ┌───┐  │  ┌───┐
        q_1: ──■──┤ X ├──■──┤ X ├──■──┤ X ├
             ┌─┴─┐└─┬─┘┌─┴─┐└─┬─┘┌─┴─┐└─┬─┘
        q_2: ┤ X ├──■──┤ X ├──■──┤ X ├──■──
             └───┘     └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_12 = Gate('x', {1: 1}, 2)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cx_21 = Gate('x', {2: 1}, 1)
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cir = Circuit(3, [cx_12, ccx_021, copy(cx_12), cx_21, ccx_012, copy(cx_21)])
    return cir
