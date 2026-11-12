from copy import copy

from ...graph import Circuit, Gate


def clifford_8_2() -> Circuit:
    """
    Clifford template 8_2:

    .. code-block:: text

                             ┌───┐
        q_0: ──■─────────■───┤ S ├───■────────────
             ┌─┴─┐┌───┐┌─┴─┐┌┴───┴┐┌─┴─┐┌───┐┌───┐
        q_1: ┤ X ├┤ H ├┤ X ├┤ SDG ├┤ X ├┤ S ├┤ H ├
             └───┘└───┘└───┘└─────┘└───┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    h_1 = Gate('h', {}, 1)
    s_0 = Gate('s', {}, 0)
    sdg_1 = Gate('sdg', {}, 1)
    s_1 = Gate('s', {}, 1)
    return Circuit(
        2,
        [cx_01, h_1, copy(cx_01), s_0, sdg_1, copy(cx_01), s_1, copy(h_1)],
    )
