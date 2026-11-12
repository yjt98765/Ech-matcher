from ech_matcher.graph import Gate, to_H_Graph
from ech_matcher.match import check_convex
from ech_matcher.patterns.nct.nct_5a_2 import nct_5a_2

def test_check_null():
    gate = Gate('x', {1:1}, 0)
    assert check_convex([], gate)

def test_nct_5a_2():
    cir = nct_5a_2()
    graph = to_H_Graph(cir)
    assert not check_convex(graph.gates[2:4], graph.gates[0])
