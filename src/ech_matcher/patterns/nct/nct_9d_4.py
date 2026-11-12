from copy import copy

from ...graph import Circuit, Gate


def nct_9d_4() -> Circuit:
    """
    Template 9d_4:

    .. code-block:: text

        q_0: ───────■─────────■──────────────■────────────
                    │  ┌───┐  │       ┌───┐  │       ┌───┐
        q_1: ──■────┼──┤ X ├──┼────■──┤ X ├──┼────■──┤ X ├
             ┌─┴─┐┌─┴─┐└─┬─┘┌─┴─┐┌─┴─┐└─┬─┘┌─┴─┐┌─┴─┐└─┬─┘
        q_2: ┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──┤ X ├┤ X ├──■──
             └───┘└───┘     └───┘└───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_12 = Gate('x', {1: 1}, 2)
    cx_02 = Gate('x', {0: 1}, 2)
    cx_21 = Gate('x', {2: 1}, 1)
    return Circuit(
        3,
        [
            cx_12,
            cx_02,
            cx_21,
            copy(cx_02),
            copy(cx_12),
            copy(cx_21),
            copy(cx_02),
            copy(cx_12),
            copy(cx_21),
        ],
    )
