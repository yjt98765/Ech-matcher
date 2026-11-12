from copy import copy

from ...graph import Circuit, Gate


def clifford_8_1() -> Circuit:
    """
    Clifford template 8_1:

    .. code-block:: text

                       ┌───┐ ┌───┐ ┌───┐┌─────┐
        q_0: ──■───────┤ X ├─┤ S ├─┤ X ├┤ SDG ├
             ┌─┴─┐┌───┐└─┬─┘┌┴───┴┐└─┬─┘└┬───┬┘
        q_1: ┤ X ├┤ H ├──■──┤ SDG ├──■───┤ H ├─
             └───┘└───┘     └─────┘      └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    h_1 = Gate('h', {}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    s_0 = Gate('s', {}, 0)
    sdg_1 = Gate('sdg', {}, 1)
    sdg_0 = Gate('sdg', {}, 0)
    return Circuit(
        2,
        [cx_01, h_1, cx_10, s_0, sdg_1, copy(cx_10), sdg_0, copy(h_1)],
    )
