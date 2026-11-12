from copy import copy

from ...graph import Circuit, Gate


def nct_9c_8() -> Circuit:
    """
    Template 9c_8:

    .. code-block:: text

        q_0: ──■─────────■────■─────────■──────────────■──
             ┌─┴─┐     ┌─┴─┐┌─┴─┐     ┌─┴─┐          ┌─┴─┐
        q_1: ┤ X ├──■──┤ X ├┤ X ├─────┤ X ├──■───────┤ X ├
             └─┬─┘┌─┴─┐└───┘└─┬─┘┌───┐└─┬─┘┌─┴─┐┌───┐└─┬─┘
        q_2: ──■──┤ X ├───────■──┤ X ├──■──┤ X ├┤ X ├──■──
                  └───┘          └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cx_12 = Gate('x', {1: 1}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    x_2 = Gate('x', {}, 2)
    return Circuit(
        3,
        [
            ccx_021,
            cx_12,
            cx_01,
            copy(ccx_021),
            x_2,
            copy(ccx_021),
            copy(cx_12),
            copy(x_2),
            copy(ccx_021),
        ],
    )
