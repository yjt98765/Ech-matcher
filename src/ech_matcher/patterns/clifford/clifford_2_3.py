from copy import copy
from ...graph import Circuit, Gate

def clifford_2_3() -> Circuit:
    """

             ┌───┐┌───┐
        q_0: ┤ H ├┤ H ├
             └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    h_0 = Gate('h', {}, 0)
    cir = Circuit(1, [h_0, copy(h_0)])
    return cir
