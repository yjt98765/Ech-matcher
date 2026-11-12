from copy import copy

from ...graph import Circuit, Gate


def nct_9c_1() -> Circuit:
    """
    Template 9c_1:

    .. code-block:: text

             ┌───┐     ┌───┐┌───┐     ┌───┐          ┌───┐
        q_0: ┤ X ├──■──┤ X ├┤ X ├─────┤ X ├──■───────┤ X ├
             └─┬─┘┌─┴─┐└───┘└─┬─┘┌───┐└─┬─┘┌─┴─┐┌───┐└─┬─┘
        q_1: ──■──┤ X ├───────■──┤ X ├──■──┤ X ├┤ X ├──■──
                  └───┘          └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_10 = Gate('x', {1: 1}, 0)
    cx_01 = Gate('x', {0: 1}, 1)
    x_0 = Gate('x', {}, 0)
    x_1 = Gate('x', {}, 1)
    return Circuit(
        2,
        [
            cx_10,
            cx_01,
            x_0,
            copy(cx_10),
            x_1,
            copy(cx_10),
            copy(cx_01),
            copy(x_1),
            copy(cx_10),
        ],
    )
