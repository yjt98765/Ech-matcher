# ECH Matcher

ECH Matcher is a Python library for template-based quantum-circuit
optimization. It represents circuits as eigen-cluster hypergraphs (ECHs), a
commutativity-aware structure that groups compatible gates while retaining
local qubit connectivity. The matcher uses that local structure to find
equivalent, lower-cost circuit fragments without enumerating every commuting
gate order.

The package provides an internal circuit model, built-in NCT and Clifford
identity templates, single- and multi-template optimizers, configurable gate
costs, and conversion of optimized circuits to Qiskit `QuantumCircuit`
objects.

## Installation

ECH Matcher requires Python 3.13 or later. Install it from a local clone with:

```console
python -m pip install .
```

For an editable development environment using
[uv](https://docs.astral.sh/uv/):

```console
uv python install 3.13
uv sync --locked
```

Activate the generated environment before running Python. On Windows
PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

## Quick start

The optimizer operates on `ech_matcher.graph.Circuit` objects. This example
matches the built-in identity template `X X` and removes both gates:

```python
from ech_matcher.graph import Circuit, Gate
from ech_matcher.match import opt_a_circuit
from ech_matcher.patterns.nct.nct_2a_1 import nct_2a_1

circuit = Circuit(
    num_qubits=1,
    data=[
        Gate("x", {}, 0),
        Gate("x", {}, 0),
    ],
)

optimized = opt_a_circuit(circuit, nct_2a_1())

print(f"{circuit.gates_num()} -> {optimized.gates_num()}")
qiskit_circuit = optimized.to_qis_cir()
```

The example prints `2 -> 0`. `Circuit.to_qis_cir()` converts the result to a
Qiskit `QuantumCircuit` for use with the rest of the Qiskit toolchain.

## Circuit model

A circuit is an ordered list of `Gate` objects:

```python
from ech_matcher.graph import Circuit, Gate

circuit = Circuit(
    3,
    [
        Gate("h", {}, 0),             # H on qubit 0
        Gate("x", {0: 1}, 1),         # CX: control 0, target 1
        Gate("x", {0: 1, 1: 1}, 2),   # CCX: controls 0 and 1, target 2
    ],
)
```

`Gate(name, controls, target, parameter)` uses a dictionary from control-qubit
indices to control states (`0` or `1`). The target is a qubit index. The
optional parameter stores a phase angle or a single-qubit unitary matrix when
required by the gate type.

ECH Matcher currently uses this internal `Circuit` representation as optimizer
input. It supports exporting to Qiskit, but does not provide a general
`QuantumCircuit`-to-`Circuit` converter as part of the public API.

## Using templates

### Built-in template sets

Use the registry to create fresh instances of the bundled templates:

```python
from ech_matcher.match import opt_with_patterns
from ech_matcher.patterns.registry import (
    get_all_nct_patterns,
    get_all_patterns,
)

nct_patterns = get_all_nct_patterns()
all_patterns = get_all_patterns()  # NCT and Clifford templates

optimized = opt_with_patterns(circuit, all_patterns)
```

`opt_with_patterns` tries templates in the supplied order and continues
rewriting the circuit as profitable matches are found. For one template, use
`opt_a_circuit(circuit, pattern)`.

### Custom templates

A template is a `Circuit` that implements the identity. The optimizer matches
a portion of the template and replaces it with the inverse of the remaining
portion when doing so lowers the configured cost. Custom templates therefore
use the same `Circuit` and `Gate` classes as input circuits.

```python
template = Circuit(
    1,
    [Gate("x", {}, 0), Gate("x", {}, 0)],
)

optimized = opt_a_circuit(circuit, template)
```

Only use templates whose complete circuit is equivalent to the identity.

## Cost model

Both optimization entry points accept an optional `cost_dict`. Keys are
`(gate_name, number_of_control_qubits)` tuples and values are positive integer
costs. Without a custom dictionary, ECH Matcher uses its built-in weighted gate
costs; for example, X, CX, and CCX have different default costs.

```python
unit_gate_costs = {
    ("x", 0): 1,
    ("x", 1): 1,
    ("x", 2): 1,
}

optimized = opt_with_patterns(
    circuit,
    get_all_nct_patterns(),
    cost_dict=unit_gate_costs,
)
```

The custom dictionary must define every gate/control-count combination used by
the selected templates and candidate matches.

## Equivalence checks

`ech_matcher.verify.equivalent` provides a lightweight functional-equivalence
check for small NCT circuits containing X, CX, CCX, and barriers:

```python
from ech_matcher.verify import equivalent

assert equivalent(circuit.to_qis_cir(), optimized.to_qis_cir())
```

The verifier enumerates the computational basis, so its cost grows
exponentially with the number of qubits. Use Qiskit's general verification
tools for larger circuits or other gate sets.

## Paper artifact

The scripts, benchmark circuits, reference data, and reproduction instructions
for the accompanying paper are kept separately in the
[artifact directory](artifact/README.md). They are not required for normal
library use.

## Development

Install the development dependencies, activate the environment, and run the
test suite from the repository root:

```console
uv sync --locked --extra dev
python -m pytest test
```

## License

ECH Matcher is released under the [MIT License](LICENSE). Third-party artifact
data is documented separately in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
and may be subject to different terms.
