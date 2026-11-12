import os
import time
import sys
from quipper_to_circuit import parse_quipper_to_circuit
from ech_matcher.match import opt_a_circuit, opt_with_patterns
from ech_matcher.patterns.nct.nct_5a_3 import nct_5a_3
from ech_matcher.patterns.registry import get_all_patterns


from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import TemplateOptimization

ONLY_ECH = len(sys.argv) > 1

template = nct_5a_3()
templates = [template.to_qis_cir()]
templ_opt = TemplateOptimization(templates, heuristics_qubits_param=[1])
pm = PassManager(templ_opt)

if ONLY_ECH:
    print("name", "gates", "qubits", "Hgates", "HTime", "Hgates2", "HTime2", sep="\t")
else:
    print("name", "gates", "qubits", "Qgates", "QTime", "Hgates", "HTime", "Hgates2", "HTime2", sep="\t")

# Set the directory containing the Quipper files
QUIPPER_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

all_templates = get_all_patterns()

for fname in sorted(os.listdir(QUIPPER_DIR)):
    src_path = os.path.join(QUIPPER_DIR, fname)
    cir = parse_quipper_to_circuit(src_path)
    qc = cir.to_qis_cir()
    original_gates = qc.size()

    t_start = time.time()
    old_gates = len(cir.data)
    cir_opt = opt_a_circuit(cir, template)
    hgraph_time = time.time() - t_start
    hgraph_gates = len(cir_opt.data)

    t_start = time.time()
    cir_opt2 = opt_with_patterns(cir, all_templates)
    hgraph_time2 = time.time() - t_start
    hgraph_gates2 = len(cir_opt2.data)

    if ONLY_ECH:
        print(fname, original_gates, qc.num_qubits, hgraph_gates, f"{hgraph_time:.3f}", hgraph_gates2, f"{hgraph_time2:.3f}", sep="\t", flush=True)
    else:
        t_start = time.time()
        fixed = False
        while not fixed:
            old_gates = qc.size()
            qc = pm.run(qc)
            fixed = qc.size() == old_gates
        qiskit_time = time.time() - t_start
        qiskit_gates = qc.size()
        print(fname, original_gates, qc.num_qubits, qiskit_gates, f"{qiskit_time:.3f}", hgraph_gates, f"{hgraph_time:.3f}", hgraph_gates2, f"{hgraph_time2:.3f}", sep="\t", flush=True)
