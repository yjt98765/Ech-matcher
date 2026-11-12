from qiskit import QuantumCircuit
from qiskit.circuit.library.templates import template_nct_2a_2, template_nct_5a_1, template_nct_5a_2
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import TemplateOptimization
from ech_matcher.graph import gen_cir2

def test_6cx():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    print(qc)

    tm = TemplateOptimization([template_nct_2a_2()])
    pm = PassManager(tm)
    fixed = False
    while not fixed:
        old_gates = qc.size()
        qc = pm.run(qc)
        fixed = qc.size() == old_gates
    optimized_qc = pm.run(qc)
    print(optimized_qc)

def test_nct_5a_1():
    qc = QuantumCircuit(3)
    qc.cx(0, 2)
    qc.ccx(0, 1, 2)
    qc.cx(0, 1)
    print(qc)

    tm = TemplateOptimization([template_nct_5a_1()])
    pm = PassManager(tm)
    fixed = False
    while not fixed:
        old_gates = qc.size()
        qc = pm.run(qc)
        fixed = qc.size() == old_gates
    optimized_qc = pm.run(qc)
    print(optimized_qc)

cost_dict = {'x': 1, 'cx': 1, 'ccx': 1}

def test_nct_5a_2():
    cir = gen_cir2('Random_X_CX_CCX', 6, 20, seed=718)
    qc = cir.to_qis_cir()
    print(qc.size())
    print(qc)

    tm = TemplateOptimization([template_nct_5a_2()], user_cost_dict=cost_dict)
    pm = PassManager(tm)
    fixed = False
    while not fixed:
        old_gates = qc.size()
        qc = pm.run(qc)
        print(qc.size())
        print(qc)
        fixed = qc.size() == old_gates
    #print(qc)

def test_mutiple_replace():
    qc = template_nct_5a_2()
    qc.x(0)
    qc.ccx(0, 1, 2)
    qc.x(1)
    qc.ccx(0, 1, 2)
    qc.x(1)
    #qc.compose(template_nct_5a_2(), [0, 1, 2], inplace=True)
    print("Original:")
    print(qc)
    tm = TemplateOptimization([template_nct_5a_2()])
    pm = PassManager(tm)
    qc = pm.run(qc)
    print(qc.size())
