import numpy as np

from ech_matcher.graph import Circuit, Gate, to_H_Graph


def local_commute(g1: Gate, g2: Gate, num_qubits: int) -> bool:
    graph = to_H_Graph(Circuit(num_qubits, [g1, g2]))
    return graph.local_commute(g1, g2)


def test_local_commute_for_gates_on_disjoint_qubits():
    g1 = Gate("x", {}, 0)
    g2 = Gate("p", {}, 1, np.pi)

    assert local_commute(g1, g2, num_qubits=2)


def test_local_commute_when_all_common_qubits_share_nodes():
    g1 = Gate("x", {0: 1}, 1)
    g2 = Gate("x", {0: 1}, 1)

    assert local_commute(g1, g2, num_qubits=2)


def test_local_commute_when_common_qubit_nodes_are_different():
    g1 = Gate("x", {}, 0)
    g2 = Gate("p", {}, 0, np.pi)

    assert not local_commute(g1, g2, num_qubits=1)


def test_local_commute_when_z_with_control_qubit():
    g1 = Gate("x", {0: 1}, 1)
    g2 = Gate("p", {}, 0, np.pi)

    assert local_commute(g1, g2, num_qubits=2)


def test_local_commute_requires_every_common_qubit_to_share_a_node():
    controlled_x = Gate("x", {0: 1}, 1)
    controlled_z = Gate("p", {0: 1}, 1, np.pi)

    graph = to_H_Graph(Circuit(2, [controlled_x, controlled_z]))

    assert controlled_x.nodes[0] is controlled_z.nodes[0]
    assert controlled_x.nodes[1] is not controlled_z.nodes[1]
    assert not graph.local_commute(controlled_x, controlled_z)
