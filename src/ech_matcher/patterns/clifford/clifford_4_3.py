from copy import copy

from ...graph import Circuit, Gate


def clifford_4_3() -> Circuit:
    """
    Clifford template 4_3:

    .. code-block:: text

             ┌───┐     ┌─────┐
        q_0: ┤ S ├──■──┤ SDG ├──■──
             └───┘┌─┴─┐└─────┘┌─┴─┐
        q_1: ─────┤ X ├───────┤ X ├
                  └───┘       └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    s_0 = Gate('s', {}, 0)
    cx_01 = Gate('x', {0: 1}, 1)
    sdg_0 = Gate('sdg', {}, 0)
    return Circuit(2, [s_0, cx_01, sdg_0, copy(cx_01)])
