from copy import copy

from ...graph import Circuit, Gate


def nct_9d_9() -> Circuit:
    """
    Template 9d_9:

    .. code-block:: text

        q_0: ──■────■────■─────────■────■─────────■────■──
               │    │  ┌─┴─┐       │  ┌─┴─┐       │  ┌─┴─┐
        q_1: ──■────┼──┤ X ├───────■──┤ X ├───────■──┤ X ├
             ┌─┴─┐┌─┴─┐└─┬─┘┌───┐┌─┴─┐└─┬─┘┌───┐┌─┴─┐└─┬─┘
        q_2: ┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──
             └───┘└───┘     └───┘└───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cx_02 = Gate('x', {0: 1}, 2)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    x_2 = Gate('x', {}, 2)
    return Circuit(
        3,
        [
            ccx_012,
            cx_02,
            ccx_021,
            x_2,
            copy(ccx_012),
            copy(ccx_021),
            copy(x_2),
            copy(ccx_012),
            copy(ccx_021),
        ],
    )
