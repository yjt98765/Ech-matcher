from copy import copy

from ...graph import Circuit, Gate


def clifford_4_2() -> Circuit:
    """
    Clifford template 4_2:

    .. code-block:: text

        q_0: ───────■────────■─
             ┌───┐┌─┴─┐┌───┐ │
        q_1: ┤ H ├┤ X ├┤ H ├─■─
             └───┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    h_1 = Gate('h', {}, 1)
    cx_01 = Gate('x', {0: 1}, 1)
    cz_01 = Gate('z', {0: 1}, 1)
    return Circuit(2, [h_1, cx_01, copy(h_1), cz_01])
