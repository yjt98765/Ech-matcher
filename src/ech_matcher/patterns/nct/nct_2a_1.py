from copy import copy
from ...graph import Circuit, Gate

def nct_2a_1() -> Circuit:
    """

             ┌───┐┌───┐
        q_0: ┤ X ├┤ X ├
             └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    x_0 = Gate('x', {}, 0)
    cir = Circuit(1, [x_0, copy(x_0)])
    return cir
