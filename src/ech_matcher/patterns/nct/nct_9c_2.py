from copy import copy
from ...graph import Circuit, Gate

def nct_9c_2() -> Circuit:
    """

        q_0: ───────■────■──────────────■────■─────────■──
             ┌───┐  │  ┌─┴─┐┌───┐     ┌─┴─┐  │       ┌─┴─┐
        q_1: ┤ X ├──■──┤ X ├┤ X ├─────┤ X ├──■───────┤ X ├
             └─┬─┘┌─┴─┐└───┘└─┬─┘┌───┐└─┬─┘┌─┴─┐┌───┐└─┬─┘
        q_2: ──■──┤ X ├───────■──┤ X ├──■──┤ X ├┤ X ├──■──
                  └───┘          └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_21 = Gate('x', {2: 1}, 1)
    cx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    x_2 = Gate('x', {}, 2)
    cx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cir = Circuit(3, [cx_21, cx_012, cx_01, copy(cx_21), x_2, copy(cx_021), copy(cx_012), copy(x_2), cx_021])
    return cir
