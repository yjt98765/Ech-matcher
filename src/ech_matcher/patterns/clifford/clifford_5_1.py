from copy import copy

from ...graph import Circuit, Gate


def clifford_5_1() -> Circuit:
    """
    Clifford template 5_1:

     .. code-block:: text

        q_0: ──■─────────■─────────■──
             ┌─┴─┐     ┌─┴─┐       │
        q_1: ┤ X ├──■──┤ X ├──■────┼──
             └───┘┌─┴─┐└───┘┌─┴─┐┌─┴─┐
        q_2: ─────┤ X ├─────┤ X ├┤ X ├
                  └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    cx_12 = Gate('x', {1: 1}, 2)
    cx_02 = Gate('x', {0: 1}, 2)
    return Circuit(3, [cx_01, cx_12, copy(cx_01), copy(cx_12), cx_02])
