from copy import copy
from ...graph import Circuit, Gate

def nct_5a_4() -> Circuit:
    """

                  ┌───┐     ┌───┐
        q_0: ──■──┤ X ├──■──┤ X ├
             ┌─┴─┐└───┘┌─┴─┐├───┤
        q_1: ┤ X ├─────┤ X ├┤ X ├
             └───┘     └───┘└───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    x_0 = Gate('x', {}, 0)
    x_1 = Gate('x', {}, 1)
    cir = Circuit(2, [cx_01, x_0, copy(cx_01), copy(x_0), x_1])
    return cir
