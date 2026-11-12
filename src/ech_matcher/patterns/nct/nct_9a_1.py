from copy import copy

from ...graph import Circuit, Gate


def nct_9a_1() -> Circuit:
    """
    Template 9a_1:

    .. code-block:: text

             ┌───┐     ┌───┐          ┌───┐
        q_0: ┤ X ├──■──┤ X ├──■────■──┤ X ├──■──
             └─┬─┘┌─┴─┐└─┬─┘┌─┴─┐┌─┴─┐└─┬─┘┌─┴─┐
        q_1: ──■──┤ X ├──■──┤ X ├┤ X ├──■──┤ X ├
                  └─┬─┘  │  ├───┤└─┬─┘┌───┐└─┬─┘
        q_2: ───────■────■──┤ X ├──■──┤ X ├──■──
                            └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_10 = Gate('x', {1: 1}, 0)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    ccx_120 = Gate('x', {1: 1, 2: 1}, 0)
    x_2 = Gate('x', {}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    return Circuit(
        3,
        [
            cx_10,
            ccx_021,
            ccx_120,
            x_2,
            cx_01,
            copy(ccx_021),
            copy(cx_10),
            copy(x_2),
            copy(ccx_021),
        ],
    )
