from copy import copy

from ...graph import Circuit, Gate


def nct_9c_3() -> Circuit:
    """
    Template 9c_3:

    .. code-block:: text

        q_0: ───────■────────────────────────■────────────
             ┌───┐  │  ┌───┐┌───┐     ┌───┐  │       ┌───┐
        q_1: ┤ X ├──■──┤ X ├┤ X ├─────┤ X ├──■───────┤ X ├
             └─┬─┘┌─┴─┐└───┘└─┬─┘┌───┐└─┬─┘┌─┴─┐┌───┐└─┬─┘
        q_2: ──■──┤ X ├───────■──┤ X ├──■──┤ X ├┤ X ├──■──
                  └───┘          └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_21 = Gate('x', {2: 1}, 1)
    ccx_012 = Gate('x', {0: 1, 1: 1}, 2)
    x_1 = Gate('x', {}, 1)
    x_2 = Gate('x', {}, 2)
    return Circuit(
        3,
        [
            cx_21,
            ccx_012,
            x_1,
            copy(cx_21),
            x_2,
            copy(cx_21),
            copy(ccx_012),
            copy(x_2),
            copy(cx_21),
        ],
    )
