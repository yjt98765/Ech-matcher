from copy import copy

from ...graph import Circuit, Gate


def clifford_4_1() -> Circuit:
    """
    Clifford template 4_1:

    .. code-block:: text

                  ┌───┐
        q_0: ──■──┤ X ├──■───X─
             ┌─┴─┐└─┬─┘┌─┴─┐ │
        q_1: ┤ X ├──■──┤ X ├─X─
             └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    return Circuit(
        2,
        [cx_01, cx_10, copy(cx_01), copy(cx_01), copy(cx_10), copy(cx_01)],
    )
