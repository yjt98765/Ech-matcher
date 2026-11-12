from copy import copy

from ...graph import Circuit, Gate


def clifford_8_3() -> Circuit:
    """
    Clifford template 8_3:

    .. code-block:: text

        q_0: ─────────────────■───────────────────────■──
             ┌───┐┌───┐┌───┐┌─┴─┐┌─────┐┌───┐┌─────┐┌─┴─┐
        q_1: ┤ S ├┤ H ├┤ S ├┤ X ├┤ SDG ├┤ H ├┤ SDG ├┤ X ├
             └───┘└───┘└───┘└───┘└─────┘└───┘└─────┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    s_1 = Gate('s', {}, 1)
    h_1 = Gate('h', {}, 1)
    cx_01 = Gate('x', {0: 1}, 1)
    sdg_1 = Gate('sdg', {}, 1)
    return Circuit(
        2,
        [s_1, h_1, copy(s_1), cx_01, sdg_1, copy(h_1), copy(sdg_1), copy(cx_01)],
    )
