from copy import copy

from ...graph import Circuit, Gate


def clifford_6_4() -> Circuit:
    """
    Clifford template 6_4:

    .. code-block:: text

        global phase: 7π/4
           ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
        q: ┤ S ├┤ H ├┤ S ├┤ H ├┤ S ├┤ H ├
           └───┘└───┘└───┘└───┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    s_0 = Gate('s', {}, 0)
    h_0 = Gate('h', {}, 0)
    return Circuit(1, [s_0, h_0, copy(s_0), copy(h_0), copy(s_0), copy(h_0)])
