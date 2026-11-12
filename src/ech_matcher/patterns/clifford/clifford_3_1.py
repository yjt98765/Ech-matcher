from copy import copy

from ...graph import Circuit, Gate


def clifford_3_1() -> Circuit:
    """
    Clifford template 3_1:

    .. code-block:: text

             ┌───┐┌───┐┌───┐
        q_0: ┤ S ├┤ S ├┤ Z ├
             └───┘└───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    s_0 = Gate('s', {}, 0)
    z_0 = Gate('z', {}, 0)
    return Circuit(1, [s_0, copy(s_0), z_0])
