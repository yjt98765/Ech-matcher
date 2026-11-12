from importlib import import_module

import pytest
from qiskit.quantum_info import Operator


NEW_TEMPLATE_NAMES = [
    'nct_9a_1',
    'nct_9c_1',
    'nct_9c_3',
    'nct_9c_4',
    'nct_9c_5',
    'nct_9c_6',
    'nct_9c_7',
    'nct_9c_8',
    'nct_9c_9',
    'nct_9c_10',
    'nct_9c_11',
    'nct_9c_12',
    'nct_9d_1',
    'nct_9d_2',
    'nct_9d_3',
    'nct_9d_4',
    'nct_9d_5',
    'nct_9d_6',
    'nct_9d_7',
    'nct_9d_8',
    'nct_9d_9',
    'nct_9d_10',
]


def operation_signatures(circuit):
    qubit_indices = {qubit: index for index, qubit in enumerate(circuit.qubits)}
    signatures = []
    for instruction in circuit.data:
        name = instruction.operation.name
        qubits = tuple(qubit_indices[qubit] for qubit in instruction.qubits)
        if name == 'ccx':
            qubits = (*sorted(qubits[:2]), qubits[2])
        signatures.append((name, qubits))
    return signatures


@pytest.mark.parametrize('template_name', NEW_TEMPLATE_NAMES)
def test_nct_pattern_matches_qiskit(template_name):
    local_module = import_module(f'ech_matcher.patterns.nct.{template_name}')
    qiskit_name = f'template_{template_name}'
    qiskit_module = import_module(
        f'qiskit.circuit.library.templates.nct.{qiskit_name}'
    )

    local_circuit = getattr(local_module, template_name)().to_qis_cir()
    qiskit_circuit = getattr(qiskit_module, qiskit_name)()

    assert operation_signatures(local_circuit) == operation_signatures(qiskit_circuit)
    assert Operator(local_circuit).equiv(Operator(qiskit_circuit))
