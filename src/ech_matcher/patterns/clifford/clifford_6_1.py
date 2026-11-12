from copy import copy

from ...graph import Circuit, Gate


def clifford_6_1() -> Circuit:
    """
    Clifford template 6_1:

     .. code-block:: text

             ┌───┐     ┌───┐┌───┐
        q_0: ┤ H ├──■──┤ H ├┤ X ├
             ├───┤┌─┴─┐├───┤└─┬─┘
        q_1: ┤ H ├┤ X ├┤ H ├──■──
             └───┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    h_0 = Gate('h', {}, 0)
    h_1 = Gate('h', {}, 1)
    cx_01 = Gate('x', {0: 1}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    return Circuit(2, [h_0, h_1, cx_01, copy(h_0), copy(h_1), cx_10])
