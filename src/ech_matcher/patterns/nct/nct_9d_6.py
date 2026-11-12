from copy import copy

from ...graph import Circuit, Gate


def nct_9d_6() -> Circuit:
    """
    Template 9d_6:

    .. code-block:: text

        q_0: ──■────■──────────────■────■─────────■───────
               │    │  ┌───┐       │  ┌─┴─┐       │  ┌───┐
        q_1: ──■────┼──┤ X ├───────■──┤ X ├───────■──┤ X ├
             ┌─┴─┐┌─┴─┐└─┬─┘┌───┐┌─┴─┐└─┬─┘┌───┐┌─┴─┐└─┬─┘
        q_2: ┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──
             └───┘└───┘     └───┘└───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cx_02 = Gate('x', {0: 1}, 2)
    cx_21 = Gate('x', {2: 1}, 1)
    x_2 = Gate('x', {}, 2)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    return Circuit(
        3,
        [
            ccx_012,
            cx_02,
            cx_21,
            x_2,
            copy(ccx_012),
            ccx_021,
            copy(x_2),
            copy(ccx_012),
            copy(cx_21),
        ],
    )
