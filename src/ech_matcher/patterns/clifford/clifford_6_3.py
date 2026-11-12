from copy import copy

from ...graph import Circuit, Gate


def clifford_6_3() -> Circuit:
    """
    Clifford template 6_3:

    .. code-block:: text

                   ┌───┐     ┌───┐
        q_0: ─X──■─┤ H ├──■──┤ X ├─────
              │  │ └───┘┌─┴─┐└─┬─┘┌───┐
        q_1: ─X──■──────┤ X ├──■──┤ H ├
                        └───┘     └───┘

    Returns:
        Circuit: template as a quantum circuit.
    """
    cx_01 = Gate('x', {0: 1}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    cz_01 = Gate('z', {0: 1}, 1)
    h_0 = Gate('h', {}, 0)
    h_1 = Gate('h', {}, 1)
    return Circuit(
        2,
        [
            cx_01,
            cx_10,
            copy(cx_01),
            cz_01,
            h_0,
            copy(cx_01),
            copy(cx_10),
            h_1,
        ],
    )
