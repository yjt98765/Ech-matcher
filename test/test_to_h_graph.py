import numpy as np

from ech_matcher.graph import Circuit, Gate, to_H_Graph

def test_p_merge_with_controlled_x():
    g1 = Gate("x", {0: 1}, 1)
    g2 = Gate("p", {}, 0, np.pi)
    to_H_Graph(Circuit(2, [g1, g2]))
    assert g1.nodes[0] is g2.nodes[0]

def test_two_h_gates():
    g1 = Gate("h", {}, 0)
    g2 = Gate("h", {}, 0)
    to_H_Graph(Circuit(1, [g1, g2]))
    assert g1.nodes[0] is g2.nodes[0]
