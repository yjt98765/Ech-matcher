from copy import copy

from ...graph import Circuit, Gate


def clifford_6_5() -> Circuit:
    """
    Clifford template 6_5:

    .. code-block:: text

                      ┌───┐
        q_0: ─■───■───┤ S ├───■───────
              │ ┌─┴─┐┌┴───┴┐┌─┴─┐┌───┐
        q_1: ─■─┤ X ├┤ SDG ├┤ X ├┤ S ├
                └───┘└─────┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cz_01 = Gate('z', {0: 1}, 1)
    cx_01 = Gate('x', {0: 1}, 1)
    s_0 = Gate('s', {}, 0)
    sdg_1 = Gate('sdg', {}, 1)
    s_1 = Gate('s', {}, 1)
    return Circuit(2, [cz_01, cx_01, s_0, sdg_1, copy(cx_01), s_1])
