import numpy as np

from ech_matcher.graph import Circuit, Gate


def test_gate_default_controls_are_not_shared():
    Gate("z", q_t=2)

    assert Gate("x").q_c == {}


def test_gate_does_not_mutate_supplied_controls():
    controls = {0: 1}

    Gate("p", controls, 1, np.pi / 4)

    assert controls == {0: 1}


def test_circuit_default_data_is_not_shared():
    first = Circuit()
    second = Circuit()

    first.data.append(Gate("x"))

    assert second.data == []


def test_circuit_copies_supplied_gate_list():
    gates = [Gate("x")]
    circuit = Circuit(data=gates)

    gates.clear()

    assert circuit.gates_num() == 1
