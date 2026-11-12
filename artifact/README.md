# Artifact for *Template Matching for Quantum Circuits Using Eigen-Cluster Hypergraphs*

This directory contains the scripts, benchmark circuits, and reference results
needed to reproduce the experiments in Section VI of the paper *Template
Matching for Quantum Circuits Using Eigen-Cluster Hypergraphs*.

All commands below must be run from the repository root, not from the
`artifact/` directory.

## Artifact contents

```text
artifact/
|-- README.md
|-- data/                 # Quipper benchmark circuits used in Section VI.B
|-- expected-results/     # Data and figure reported in the paper
`-- scripts/
    |-- fixed_circuit.py
    |-- plot_speed_up.py
    |-- quipper_to_circuit.py
    |-- random_circuit.py
    `-- scale_with_ngate.py
```

The reference results are:

| File | Paper result | Description |
| --- | --- | --- |
| `expected-results/random.dat` | Table II | Random-circuit gate counts and running times |
| `expected-results/fixed.dat` | Table III | Fixed-circuit gate counts and running times |
| `expected-results/speedup.png` | Figure 9 | Speed-up of ECH Matcher over Qiskit |
| `expected-results/scale.dat` | Figure 10 | Raw measurements used to construct the figure |
| `expected-results/scale.png` | Figure 10 | Figure included in the paper |

The files in `data/` are arithmetic circuits from Nam et al. [1], obtained
from the [`Arithmetic_and_Toffoli` directory of the original repository][nam-data].
They correspond to the files whose original names end in `_after_heavy`; that
suffix was removed here for brevity. The files use the Quipper text format and
are loaded by `scripts/quipper_to_circuit.py`. See the repository's
[`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) for provenance and the
current redistribution status.

## Requirements and setup

The artifact uses Python 3.13 and [uv](https://docs.astral.sh/uv/). The first
setup requires network access to download the locked dependencies.

```console
uv python install 3.13
uv sync --locked --extra artifact
```

This creates `.venv`, installs the local `ech_matcher` source tree and the
artifact plotting dependencies, and uses the exact dependency versions
recorded in `uv.lock`. Activate the environment before running the commands in
this guide.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Confirm the setup before starting a long experiment:

```console
python -c "import ech_matcher, qiskit; print('artifact environment ready')"
```

The remaining commands assume that this virtual environment is active.

## Quick smoke test

The following command runs only ECH Matcher on the four random circuits and
normally completes in seconds:

```console
python artifact/scripts/random_circuit.py ech
```

A successful run prints a tab-separated header followed by one row for each
input size (100, 300, 500, and 700 gates). The `ech` argument selects the
ECH-Matcher-only mode and skips the substantially slower Qiskit baselines.

## Section VI.A: random circuits (Table II)

Run the complete comparison with:

```console
python artifact/scripts/random_circuit.py
```

To save the tab-separated output:

```console
python artifact/scripts/random_circuit.py > reproduced-random.dat
```

The complete experiment evaluates ECH Matcher, Qiskit template matching, and
Qiskit template matching with its qubit heuristic. It can take approximately
three hours, depending on the machine. For the shorter ECH-only run, append
`ech` to either command.

The output columns are:

| Column | Meaning |
| --- | --- |
| `gates` | Number of gates in the generated input circuit |
| `nqubits` | Number of qubits in the input circuit |
| `gates_h`, `time_h` | Gate count and time for ECH Matcher |
| `gates_q`, `time_q` | Gate count and time for Qiskit template matching |
| `gates_qh`, `time_qh` | Gate count and time for Qiskit with its qubit heuristic |

Compare the output with `artifact/expected-results/random.dat`.

## Section VI.B: fixed circuits (Table III)

Run the complete comparison with:

```console
python artifact/scripts/fixed_circuit.py
```

To save the tab-separated output:

```console
python artifact/scripts/fixed_circuit.py > reproduced-fixed.dat
```

The script reads every circuit in `artifact/data/`. The complete experiment
can take approximately ten hours because Qiskit is applied repeatedly until
the circuit size stops changing. The shorter ECH-only mode is:

```console
python artifact/scripts/fixed_circuit.py ech
```

The common output columns are `name`, `gates`, and `qubits`, identifying the
benchmark and its original size. The remaining columns report gate count and
time for these configurations:

| Columns | Configuration |
| --- | --- |
| `Qgates`, `QTime` | Qiskit applied repeatedly until the gate count stabilizes; omitted in ECH-only mode |
| `Hgates`, `HTime` | ECH Matcher using the `nct_5a_3` template |
| `Hgates2`, `HTime2` | ECH Matcher using all registered templates |

Compare the output with `artifact/expected-results/fixed.dat`.

### Figure 9: speed-up over Qiskit

After producing the complete Table II and Table III results, generate Figure 9
from the two tab-separated data files:

```console
python artifact/scripts/plot_speed_up.py \
  --random-input reproduced-random.dat \
  --input reproduced-fixed.dat \
  --output reproduced-speedup.png
```

On Windows PowerShell, use backticks for line continuation or enter the command
on one line:

```powershell
python artifact/scripts/plot_speed_up.py --random-input reproduced-random.dat --input reproduced-fixed.dat --output reproduced-speedup.png
```

The figure plots `Qiskit time / ECH time` against the input gate count on
logarithmic axes. Circles denote random circuits and triangles denote fixed
arithmetic circuits; color indicates the number of qubits. Compare the result
with `artifact/expected-results/speedup.png`.

To reproduce the paper figure directly from the committed reference data
instead of rerunning the long experiments, use:

```console
python artifact/scripts/plot_speed_up.py --output reproduced-speedup.png
```

## Section VI.C: scalability (Figure 10)

Run the scalability experiment with:

```console
python artifact/scripts/scale_with_ngate.py --output reproduced-scale.png
```

To retain the raw measurements and save the plot:

```console
python artifact/scripts/scale_with_ngate.py --output reproduced-scale.png > reproduced-scale.dat
```

For each circuit size from 10 to 4,010 gates, the script generates 15
six-qubit circuits with fixed seeds. It prints the individual running times,
their mean and standard deviation, the mean optimized gate count, and the
coefficients of a quadratic fit. It saves the reproduced plot to the path
specified by `--output`; no graphical display is required.

Compare the measurements with `artifact/expected-results/scale.dat` and the
plot with `artifact/expected-results/scale.png`.

## Interpreting differences

The random-circuit experiments use fixed seeds, so the generated circuits and
their input gate counts are deterministic. With the committed code and the
dependency versions in `uv.lock`, optimized gate counts should normally match
the reference results. Small differences may occur across platforms or Python
versions because template matching uses heuristic choices and tie-breaking.

Running times are inherently machine-dependent and will vary with CPU
performance, operating system, background load, and system configuration.
Reviewers should compare gate counts directly, while evaluating timings and
speed-ups by their overall scale and qualitative trends rather than expecting
identical values.

## Reference

[1] Y. Nam, N. J. Ross, Y. Su, A. M. Childs, and D. Maslov, "Automated
optimization of large quantum circuits with continuous parameters," *npj
Quantum Information*, vol. 4, article 23, 2018.

[nam-data]: https://github.com/njross/optimizer/tree/master/Arithmetic_and_Toffoli
