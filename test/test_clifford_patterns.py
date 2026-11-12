from importlib import import_module

import pytest
from qiskit.quantum_info import Operator


TEMPLATE_NAMES = [
    'clifford_2_1',
    'clifford_2_2',
    'clifford_2_3',
    'clifford_2_4',
    'clifford_3_1',
    'clifford_4_1',
    'clifford_4_2',
    'clifford_4_3',
    'clifford_4_4',
    'clifford_5_1',
    'clifford_6_1',
    'clifford_6_2',
    'clifford_6_3',
    'clifford_6_4',
    'clifford_6_5',
    'clifford_8_1',
    'clifford_8_2',
    'clifford_8_3',
]


def operation_signatures(circuit):
    qubit_indices = {qubit: index for index, qubit in enumerate(circuit.qubits)}
    signatures = []

    for instruction in circuit.data:
        name = instruction.operation.name
        qubits = tuple(qubit_indices[qubit] for qubit in instruction.qubits)
        if name == 'swap':
            first, second = qubits
            signatures.extend(
                [
                    ('cx', (first, second)),
                    ('cx', (second, first)),
                    ('cx', (first, second)),
                ]
            )
        else:
            signatures.append((name, qubits))

    return signatures


@pytest.mark.parametrize('template_name', TEMPLATE_NAMES)
def test_clifford_pattern_matches_qiskit(template_name):
    local_module = import_module(f'ech_matcher.patterns.clifford.{template_name}')
    qiskit_module = import_module(
        f'qiskit.circuit.library.templates.clifford.{template_name}'
    )

    local_circuit = getattr(local_module, template_name)().to_qis_cir()
    qiskit_circuit = getattr(qiskit_module, template_name)()

    assert operation_signatures(local_circuit) == operation_signatures(qiskit_circuit)
    assert Operator(local_circuit).equiv(Operator(qiskit_circuit))
