import sys
import time
from ech_matcher.graph import gen_cir2
from ech_matcher.match import opt_with_patterns
from ech_matcher.patterns.registry import get_all_nct_patterns
from ech_matcher.verify import equivalent

from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import TemplateOptimization


ONLY_ECH = len(sys.argv) > 1

patterns = get_all_nct_patterns()

# Qiskit template matching pass
templates = [pattern.to_qis_cir() for pattern in patterns]
templ_opt = TemplateOptimization(templates)
pm = PassManager(templ_opt)

templ_opt_with_heuristics = TemplateOptimization(templates, heuristics_qubits_param=[1])
pm_with_heuristics = PassManager(templ_opt_with_heuristics)

nqubit = 10

if ONLY_ECH:
    print("gates", "nqubits", "gates_h", "time_h", sep='\t')
else:
    print("gates", "nqubits", "gates_h", "time_h", "gates_q", "time_q", "gates_qh", "time_qh", sep='\t')

for size in range(100, 701, 200):
    cir = gen_cir2('Random_X_CX_CCX', nqubit, size, 42)

    t_start = time.time()
    cir_n = opt_with_patterns(cir, patterns)
    htime = time.time() - t_start
    hsize = cir_n.gates_num()

    # Only used for debugging, to check if the optimized circuit is equivalent to the original circuit
    # if not equivalent(cir.to_qis_cir(), cir_n.to_qis_cir()):
    #     print("Error")
    #     break

    if ONLY_ECH:
        print(size, nqubit, hsize, f"{htime:.3f}", sep='\t', flush=True)
    else:
        qc = cir.to_qis_cir()
        t_start = time.time()
        qc_opt = pm.run(qc)
        qtime = time.time() - t_start
        qsize = qc_opt.size()

        qc = cir.to_qis_cir()
        t_start = time.time()
        qc_opt = pm_with_heuristics.run(qc)
        qhtime = time.time() - t_start
        qhsize = qc_opt.size()
        print(size, nqubit, hsize, f"{htime:.3f}", qsize, f"{qtime:.3f}", qhsize, f"{qhtime:.3f}", sep='\t', flush=True)
