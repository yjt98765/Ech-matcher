from copy import copy
from ...graph import Circuit, Gate

def nct_4a_1() -> Circuit:
    """

        q_0: ───────■─────────■──
                    │         │
        q_1: ──■────┼────■────┼──
               │    │    │    │
        q_2: ──■────■────■────■──
               │  ┌─┴─┐  │  ┌─┴─┐
        q_3: ──┼──┤ X ├──┼──┤ X ├
             ┌─┴─┐└───┘┌─┴─┐└───┘
        q_4: ┤ X ├─────┤ X ├─────
             └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_124 = Gate('x', {1: 1, 2: 1}, 4)
    ccx_023 = Gate('x', {0: 1, 2: 1}, 3)
    cir = Circuit(5, [ccx_124, ccx_023, copy(ccx_124), copy(ccx_023)])
    return cir
