from ech_matcher.graph import to_H_Graph, Circuit, Gate
from ech_matcher.patterns.nct.nct_9c_2 import nct_9c_2

def test_x_z():
    x = Gate('x', {}, 0)
    z = Gate('z', {}, 0)
    cir = Circuit(1, [x, z])
    g = to_H_Graph(cir)
    n1 = g.start_nodes[0].successor
    n2 = n1.successor
    assert not n1.is_commutable(n2)

def test_x_control_qubit():
    x = Gate('x', {}, 0)
    cx = Gate('x', {0: 1}, 1)
    cir = Circuit(2, [x, cx])
    g = to_H_Graph(cir)
    n1 = g.start_nodes[0].successor
    n2 = n1.successor
    assert not n1.is_commutable(n2)

def test_is_first_gate_in_node():
    x = Gate('x', {}, 0)
    ccx = Gate('x', {0: 1, 1: 1}, 2)
    cx = Gate('x', {0: 1}, 1)
    cir = Circuit(3, [x, ccx, cx])
    to_H_Graph(cir)
    assert not cx.is_node_start[0]
    assert cx.is_node_start[1]
    assert ccx.is_node_start[0]

def test_is_first_gate_in_node2():
    """
                        ┌───┐
    q_0: ───────■───────┤ X ├
              ┌─┴─┐     └─┬─┘
    q_1: ─────┤ X ├───────■──
              └─┬─┘       │
    q_2: ───────┼─────────┼──
         ┌───┐  │         │
    q_3: ┤ X ├──■────■────■──
         └───┘     ┌─┴─┐
    q_4: ──────────┤ X ├─────
                   └───┘
    """
    x = Gate('x', {}, 3)
    ccx_031 = Gate('x', {0: 1, 3: 1}, 1)
    ccx_130 = Gate('x', {1: 1, 3: 1}, 0)
    cx = Gate('x', {3: 1}, 4)
    cir = Circuit(5, [x, ccx_031, cx, ccx_130])
    print(cir.to_qis_cir())
    to_H_Graph(cir)
    assert not ccx_130.is_node_start[3]
    assert ccx_031.is_node_start[3]
