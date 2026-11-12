from copy import copy

from ...graph import Circuit, Gate


def clifford_4_4() -> Circuit:
    """
    Clifford template 4_4:

    .. code-block:: text

             ┌───┐   ┌─────┐
        q_0: ┤ S ├─■─┤ SDG ├─■─
             └───┘ │ └─────┘ │
        q_1: ──────■─────────■─

    Returns:
        Circuit: template as a quantum circuit.
    """
    s_0 = Gate('s', {}, 0)
    cz_01 = Gate('z', {0: 1}, 1)
    sdg_0 = Gate('sdg', {}, 0)
    return Circuit(2, [s_0, cz_01, sdg_0, copy(cz_01)])
