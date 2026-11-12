from copy import copy

from ...graph import Circuit, Gate


def clifford_6_2() -> Circuit:
    """
    Clifford template 6_2:

     .. code-block:: text

             ┌───┐
        q_0: ┤ S ├──■───────────■───■─
             ├───┤┌─┴─┐┌─────┐┌─┴─┐ │
        q_1: ┤ S ├┤ X ├┤ SDG ├┤ X ├─■─
             └───┘└───┘└─────┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    s_0 = Gate('s', {}, 0)
    s_1 = Gate('s', {}, 1)
    cx_01 = Gate('x', {0: 1}, 1)
    sdg_1 = Gate('sdg', {}, 1)
    cz_01 = Gate('z', {0: 1}, 1)
    return Circuit(2, [s_0, s_1, cx_01, sdg_1, copy(cx_01), cz_01])
