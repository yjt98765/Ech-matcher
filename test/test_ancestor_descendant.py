from ech_matcher.graph import (
    Circuit,
    Gate,
    to_H_Graph,
)
from ech_matcher.match import opt_with_patterns
from ech_matcher.patterns.nct.nct_5a_2 import nct_5a_2
from ech_matcher.patterns.nct.nct_5a_3 import nct_5a_3


def test_calculate_ancestor_decendant_tracks_non_commuting_gates_in_order():
    first = Gate("x", {}, 0)
    unrelated = Gate("x", {}, 1)
    last = Gate("z", {}, 0)
    graph = to_H_Graph(Circuit(2, [first, unrelated, last]))

    graph.calculate_ancestor_decendant()

    assert first.ancestors == 0
    assert first.descendants == 1 << 2
    assert unrelated.ancestors == 0
    assert unrelated.descendants == 0
    assert last.ancestors == 1 << 0
    assert last.descendants == 0


def test_calculate_ancestor_decendant_replaces_stale_relationships():
    first = Gate("x", {}, 0)
    last = Gate("x", {}, 1)
    graph = to_H_Graph(Circuit(2, [first, last]))
    first.ancestors = 1 << 1
    last.descendants = 1 << 0

    graph.calculate_ancestor_decendant()

    assert first.ancestors == 0
    assert first.descendants == 0
    assert last.ancestors == 0
    assert last.descendants == 0


def test_calculate_ancestor_decendant_does_not_compare_across_a_blocker():
    first = Gate("x", {}, 0)
    middle = Gate("z", {}, 0)
    last = Gate("x", {}, 0)
    graph = to_H_Graph(Circuit(1, [first, middle, last]))

    graph.calculate_ancestor_decendant()

    assert first.ancestors == 0
    assert first.descendants == 0b110
    assert middle.ancestors == 1 << 0
    assert middle.descendants == 1 << 2
    assert last.ancestors == 0b011
    assert last.descendants == 0


def test_calculate_ancestor_decendant_blocked_by_a_cnot():
    first = Gate("x", {}, 0)
    middle = Gate("x", {0: 1}, 1)
    last = Gate("z", {}, 1)
    graph = to_H_Graph(Circuit(2, [first, middle, last]))

    graph.calculate_ancestor_decendant()

    assert first.ancestors == 0
    assert first.descendants == 0b110
    assert middle.ancestors == 1 << 0
    assert middle.descendants == 1 << 2
    assert last.ancestors == 0b011
    assert last.descendants == 0


def test_calculate_ancestor_decendant_nct_5a_3():
    pattern = nct_5a_3()
    graph = to_H_Graph(pattern)

    graph.calculate_ancestor_decendant()

    gates = graph.gates
    assert gates[0].ancestors == 0
    assert gates[0].descendants == 0b1110
    assert gates[1].ancestors == 0b00001
    assert gates[1].descendants == 0b01100
    assert gates[2].ancestors == 0b00011
    assert gates[2].descendants == 0b01000
    assert gates[3].ancestors == 0b00111
    assert gates[3].descendants == 0
    assert gates[4].ancestors == 0
    assert gates[4].descendants == 0

