from copy import copy

from ...graph import Circuit, Gate


def nct_9c_7() -> Circuit:
    """
    Template 9c_7:

    .. code-block:: text

        q_0: ──■────■────■────■────■─────────■────■───────
             ┌─┴─┐  │  ┌─┴─┐┌─┴─┐  │  ┌───┐  │    │  ┌───┐
        q_1: ┤ X ├──■──┤ X ├┤ X ├──┼──┤ X ├──■────┼──┤ X ├
             └─┬─┘┌─┴─┐└───┘└─┬─┘┌─┴─┐└─┬─┘┌─┴─┐┌─┴─┐└─┬─┘
        q_2: ──■──┤ X ├───────■──┤ X ├──■──┤ X ├┤ X ├──■──
                  └───┘          └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    cx_02 = Gate('x', {0: 1}, 2)
    cx_21 = Gate('x', {2: 1}, 1)
    return Circuit(
        3,
        [
            ccx_021,
            ccx_012,
            cx_01,
            copy(ccx_021),
            cx_02,
            cx_21,
            copy(ccx_012),
            copy(cx_02),
            copy(cx_21),
        ],
    )
