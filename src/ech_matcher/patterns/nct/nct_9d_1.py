from copy import copy

from ...graph import Circuit, Gate


def nct_9d_1() -> Circuit:
    """
    Template 9d_1:

    .. code-block:: text

                       ┌───┐          ┌───┐          ┌───┐
        q_0: ──■───────┤ X ├───────■──┤ X ├───────■──┤ X ├
             ┌─┴─┐┌───┐└─┬─┘┌───┐┌─┴─┐└─┬─┘┌───┐┌─┴─┐└─┬─┘
        q_1: ┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──
             └───┘└───┘     └───┘└───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    x_1 = Gate('x', {}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    return Circuit(
        2,
        [
            cx_01,
            x_1,
            cx_10,
            copy(x_1),
            copy(cx_01),
            copy(cx_10),
            copy(x_1),
            copy(cx_01),
            copy(cx_10),
        ],
    )
