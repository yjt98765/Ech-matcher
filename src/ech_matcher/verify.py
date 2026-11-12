from qiskit import QuantumCircuit

def basis_permutation(qc: QuantumCircuit):
    n = qc.num_qubits
    permutation = list(range(1 << n))
    qindex = {q: i for i, q in enumerate(qc.qubits)}

    for inst in qc.data:
        name = inst.operation.name
        qs = [qindex[q] for q in inst.qubits]
        masks = [1 << q for q in qs]

        if name == "x":
            permutation = [y ^ masks[0] for y in permutation]

        elif name == "cx":
            control, target = masks
            permutation = [
                y ^ target if y & control else y
                for y in permutation
            ]

        elif name == "ccx":
            control1, control2, target = masks
            permutation = [
                y ^ target if (y & control1) and (y & control2) else y
                for y in permutation
            ]

        elif name == "barrier":
            continue

        else:
            raise ValueError(f"Unsupported operation: {name}")

    return tuple(permutation)


def equivalent(circuit1, circuit2):
    return (
        circuit1.num_qubits == circuit2.num_qubits
        and basis_permutation(circuit1) == basis_permutation(circuit2)
    )
