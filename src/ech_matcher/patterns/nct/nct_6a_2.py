from copy import copy
from ...graph import Circuit, Gate

def nct_6a_2() -> Circuit:
    """

        q_0: ──■────■────■────■────■────■──
               │  ┌─┴─┐  │  ┌─┴─┐  │  ┌─┴─┐
        q_1: ──■──┤ X ├──■──┤ X ├──■──┤ X ├
             ┌─┴─┐└─┬─┘┌─┴─┐└─┬─┘┌─┴─┐└─┬─┘
        q_2: ┤ X ├──■──┤ X ├──■──┤ X ├──■──
             └───┘     └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cir = Circuit(3, [ccx_012, ccx_021, copy(ccx_012), copy(ccx_021), copy(ccx_012), copy(ccx_021)])
    return cir
