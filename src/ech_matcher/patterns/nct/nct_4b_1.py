from copy import copy
from ...graph import Circuit, Gate

def nct_4b_1() -> Circuit:
    """

        q_0: ───────■─────────■──
                    │         │
        q_1: ──■────┼────■────┼──
               │    │    │    │
        q_2: ──■────■────■────■──
             ┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐
        q_3: ┤ X ├┤ X ├┤ X ├┤ X ├
             └───┘└───┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_123 = Gate('x', {1: 1, 2: 1}, 3)
    ccx_023 = Gate('x', {0: 1, 2: 1}, 3)
    cir = Circuit(4, [ccx_123, ccx_023, copy(ccx_123), copy(ccx_023)])
    return cir
