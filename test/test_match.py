import numpy as np
import time
from copy import copy
from qiskit.quantum_info import Operator
from ech_matcher.graph import Circuit, Gate, gen_cir2
from ech_matcher.match import opt_a_circuit, opt_with_patterns
from ech_matcher.patterns.clifford.clifford_6_2 import clifford_6_2
from ech_matcher.patterns.nct.nct_9c_2 import nct_9c_2
from ech_matcher.patterns.nct.nct_2a_2 import nct_2a_2
from ech_matcher.patterns.nct.nct_4a_1 import nct_4a_1
from ech_matcher.patterns.nct.nct_5a_1 import nct_5a_1
from ech_matcher.patterns.nct.nct_5a_2 import nct_5a_2
from ech_matcher.patterns.nct.nct_5a_3 import nct_5a_3
from ech_matcher.patterns.nct.nct_6a_1 import nct_6a_1
from ech_matcher.patterns.clifford.clifford_2_1 import clifford_2_1
from ech_matcher.patterns import clifford_2_3, clifford_3_1, nct_2a_1, clifford_8_1
from ech_matcher.verify import equivalent

def test_2cx_template():
    tm = nct_2a_2()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    cir = Circuit(2,[])
    cir.data = [Gate('x', {1:1}, 0), Gate('x', {1:1}, 0), Gate('x', {0:1}, 1), Gate('x', {0:1}, 1)]
    cir_q = cir.to_qis_cir()
    print(cir_q)

    cir_n = opt_a_circuit(cir, tm)
    assert len(cir_n.data) == 0

def test_2cx_4q_circuit():
    cir = Circuit(4,[])
    cir.data=[Gate('x',{0:1},1),Gate('x',{1:1},0),Gate('x',{0:1},1),Gate('x',{0:1},1),Gate('x',{1:1},0),Gate('x',{0:1},1)]
    cir.data+=[Gate('u',{},2,1/np.sqrt(2)*np.array([[1,1],[1,-1]])),Gate('x',{2:1},3),Gate('x',{3:1},2),Gate('x',{2:1},3)]

    tm = nct_2a_2()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    cir_q = cir.to_qis_cir()
    print(cir_q)
    # cir_q.draw('mpl')

    t_start = time.time()
    cir_n = opt_a_circuit(cir, tm)
    print(time.time()-t_start)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

def test_3q5g_template():
    tm = nct_5a_3()
    tm_q = tm.to_qis_cir()
    print(tm_q)
    # tm_q.draw('mpl')

    cir = Circuit(3,[])
    cir.data=[Gate('x',{0:1},1),Gate('x',{1:1},2),Gate('x',{0:1},2)]
    cir_q = cir.to_qis_cir()
    print(cir_q)
    # cir_q.draw('mpl')

    t_start = time.time()
    cir_n = opt_a_circuit(cir,tm)
    print(time.time()-t_start)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)

def test_nct_4a_1():
    tm = nct_4a_1()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    ccx_320 = Gate('x', {3: 1, 2: 1}, 0)
    ccx_421 = Gate('x', {4: 1, 2: 1}, 1)
    ccx_421_2 = Gate('x', {4: 1, 2: 1}, 1)
    cir = Circuit(5, [ccx_421, ccx_320, ccx_421_2])
    cir_q = cir.to_qis_cir()
    print(cir_q)

    cir_n = opt_a_circuit(cir, tm)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)

def test_nct_5a_1():
    tm = nct_5a_1()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    ccx_042 = Gate('x', {0: 1, 4: 1}, 2)
    cx_40 = Gate('x', {4: 1}, 0)
    cir = Circuit(5, [copy(cx_40), copy(ccx_042), copy(cx_40)])
    cir_q = cir.to_qis_cir()
    print(cir_q)

    cir_n = opt_a_circuit(cir, tm)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)

def test_nct_5a_1_wrap():
    tm = nct_5a_1()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    cx_42 = Gate('x', {4: 1}, 2)
    ccx_042 = Gate('x', {0: 1, 4: 1}, 2)
    cx_40 = Gate('x', {4: 1}, 0)
    cir = Circuit(5, [cx_42, ccx_042, cx_40])
    cir_q = cir.to_qis_cir()
    print(cir_q)

    cir_n = opt_a_circuit(cir, tm)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)

def test_nct_9c_2():
    tm = nct_9c_2()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    cx_21 = Gate('x', {2: 1}, 1)
    cx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    x_2 = Gate('x', {}, 2)
    cx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cir = Circuit(3, [cx_01, cx_21, x_2, cx_021, cx_012, copy(x_2)])
    cir_q = cir.to_qis_cir()
    print(cir_q)

    cir_n = opt_a_circuit(cir, tm)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)

def test_nct_9c_2_and_5a_2():
    #tm = [nct_9c_2(), nct_2a_2()]
    tm = [nct_9c_2(), nct_5a_2()]

    cx_21 = Gate('x', {2: 1}, 1)
    cx_012 = Gate('x', {0: 1, 1: 1}, 2)
    cx_01 = Gate('x', {0: 1}, 1)
    x_2 = Gate('x', {}, 2)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cir = Circuit(3, [copy(cx_21), copy(cx_012), cx_01, cx_21, x_2, ccx_021, cx_012, copy(ccx_021)])
    cir_q = cir.to_qis_cir()
    print(cir_q)

    cir_n = opt_with_patterns(cir, tm)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)
    assert cir_n.gates_num() == 2

def test_nct_5a_2_match_3_gates():
    tm = nct_5a_2()

    x_1 = Gate('x', {}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    cx_01 = Gate('x', {0: 1}, 1)
    x_2 = Gate('x', {}, 2)
    ccx_021 = Gate('x', {0: 1, 2: 1}, 1)
    cir = Circuit(3, [x_1, cx_10, cx_01, x_2, ccx_021])
    cir_q = cir.to_qis_cir()
    print("Input")
    print(cir_q)

    cir_n = opt_a_circuit(cir, tm)
    cir_n2 = cir_n.to_qis_cir()
    print(cir_n2)

    assert equivalent(cir_q, cir_n2)
    assert cir_n.gates_num() == 4

def test_nct_5a_2():
    cir = gen_cir2('Random_X_CX_CCX', 6, 20, seed=794)
    qc = cir.to_qis_cir()
    print("Input")
    print(qc)

    tm = nct_5a_2()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    fixed = False
    while not fixed:
        old_gates = len(cir.data)
        cir = opt_a_circuit(cir, tm)
        qc = cir.to_qis_cir()
        print(qc)
        fixed = len(cir.data) == old_gates
    cir_n2 = cir.to_qis_cir()
    print(cir_n2)
    assert equivalent(qc, cir_n2)


def test_nct_5a_3():
    cir = gen_cir2('Random_X_CX_CCX', 6, 136, seed=13607)
    qc = cir.to_qis_cir()
    print("Input")
    print(qc)

    tm = nct_5a_3()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    fixed = False
    while not fixed:
        old_gates = len(cir.data)
        cir = opt_a_circuit(cir, tm)
        qc = cir.to_qis_cir()
        print(qc)
        fixed = len(cir.data) == old_gates
    cir_n2 = cir.to_qis_cir()
    print(cir_n2)
    assert equivalent(qc, cir_n2)


def test_non_neighbor_nct_5a_3():
    cx_25 = Gate('x', {2: 1}, 5)
    cx_50 = Gate('x', {5: 1}, 0)
    ccx_013 = Gate('x', {0: 1, 1: 1}, 3)
    ccx_420 = Gate('x', {4: 1, 2: 1}, 0)
    cx_24 = Gate('x', {2: 1}, 4)
    cx_54 = Gate('x', {5: 1}, 4)
    cir = Circuit(6, [cx_25, cx_50, ccx_013, ccx_420, cx_24, cx_54])
    qc = cir.to_qis_cir()
    print("Input")
    print(qc)

    tm = nct_5a_3()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    cir_opt = opt_a_circuit(cir, tm)
    qc = cir_opt.to_qis_cir()
    print(qc)

    # Should not be optimized
    assert cir.gates_num() == cir_opt.gates_num()


def test_wrap_around():
    cir = Circuit(2, [Gate('h', {}, 1), Gate('z', {0 : 1}, 1), Gate('h', {}, 1)])
    template = Circuit(2, [Gate('h', {}, 1), Gate('x', {0 : 1}, 1), Gate('h', {}, 1), Gate('z', {0 : 1}, 1)])
    cir = opt_a_circuit(cir, template)
    qc = cir.to_qis_cir()
    print(qc)
    assert cir.gates_num() == 1


def test_no_replace_due_to_cost():
    cir = Circuit(2, [Gate('h', {}, 1), Gate('x', {0 : 1}, 1), Gate('h', {}, 1)])
    template = Circuit(2, [Gate('h', {}, 1), Gate('x', {0 : 1}, 1), Gate('h', {}, 1), Gate('z', {0 : 1}, 1)])
    cir = opt_a_circuit(cir, template)
    qc = cir.to_qis_cir()
    print(qc)
    assert cir.gates_num() == 3


def test_replace_with_user_defined_cost():
    cir = Circuit(2, [Gate('h', {}, 1), Gate('x', {0 : 1}, 1), Gate('h', {}, 1)])
    template = Circuit(2, [Gate('h', {}, 1), Gate('x', {0 : 1}, 1), Gate('h', {}, 1), Gate('z', {0 : 1}, 1)])
    cost_dict = {("x", 1): 1, ("h", 0): 1, ("z", 1): 1}
    cir = opt_a_circuit(cir, template, cost_dict=cost_dict)
    qc = cir.to_qis_cir()
    print(qc)
    assert cir.gates_num() == 1


def test_clifford_6_2_matches_s_and_sdg():
    s_0 = Gate('s', {}, 0)
    cx_01 = Gate('x', {0: 1}, 1)
    sdg_1 = Gate('sdg', {}, 1)
    cir = Circuit(2, [s_0, cx_01, sdg_1, copy(cx_01)])
    original = cir.to_qis_cir()
    print("Input")
    print(original)

    cir_opt = opt_a_circuit(cir, clifford_6_2())
    optimized = cir_opt.to_qis_cir()
    print(optimized)

    assert [instruction.operation.name for instruction in optimized.data] == ['sdg', 'cz']
    assert Operator(original).equiv(Operator(optimized))


def test_match_after_replace():
    cx_01 = Gate('x', {0: 1}, 1)
    cx_10 = Gate('x', {1: 1}, 0)
    cir = Circuit(2, [cx_01, cx_10, copy(cx_01), copy(cx_01), copy(cx_10), copy(cx_01), copy(cx_10), copy(cx_01)])
    qc = cir.to_qis_cir()
    print("Input")
    print(qc)

    template = nct_6a_1()
    cir_opt = opt_a_circuit(cir, template)
    qc = cir_opt.to_qis_cir()
    print(qc)
    assert cir_opt.gates_num() == 2

def test_nct_5a_2_997():
    cir = gen_cir2('Random_X_CX_CCX', 6, 20, seed=997)
    qc = cir.to_qis_cir()
    print("Input")
    print(qc)

    tm = nct_5a_2()
    tm_q = tm.to_qis_cir()
    print(tm_q)

    cir = opt_a_circuit(cir, tm)
    qc = cir.to_qis_cir()
    print(qc)

def test_switched_cz():
    cir = Circuit(2, [Gate('z', {0: 1}, 1), Gate('z', {1: 1}, 0)])
    tm = clifford_2_1()
    tm_q = tm.to_qis_cir()
    print(f"{tm.data=}")
    cir = opt_a_circuit(cir, tm)
    assert cir.gates_num() == 0

def test_ss_to_z():
    cir = Circuit(1, [Gate('s', {}, 0), Gate('s', {}, 0)])
    tm = clifford_3_1()
    cir = opt_a_circuit(cir, tm)
    assert cir.gates_num() == 1

def test_merge_leading_and_trailing_nodes():
    cir = Circuit(1, [Gate('h', {}, 0), Gate('x', {}, 0), Gate('x', {}, 0), Gate('h', {}, 0)])
    cir = opt_with_patterns(cir, [clifford_2_3(), nct_2a_1()])
    assert cir.gates_num() == 0

def test_remove_sdg_s():
    h_0 = Gate('h', {}, 0)
    h_1 = Gate('h', {}, 1)
    cir = Circuit(2, [h_1, h_0, Gate('sdg', {}, 1), Gate('x', {1: 1}, 0), Gate('s', {}, 1), copy(h_1), copy(h_0)])
    tm = Circuit(1, [Gate('sdg', {}, 0), Gate('s', {}, 0)])
    cir = opt_a_circuit(cir, tm)
    print(cir.to_qis_cir())
    assert cir.gates_num() == 5

def test_clifford_8_1():
    h_1 = Gate('h', {}, 1)
    cx_01 = Gate('x', {0: 1}, 1)
    cir = Circuit(2, [Gate('sdg', {}, 0), h_1, Gate('sdg', {}, 1), cx_01, Gate('s', {}, 1), copy(cx_01), copy(h_1), copy(cx_01)])
    print("Input")
    print(cir.to_qis_cir())
    tm = clifford_8_1()
    cir = opt_a_circuit(cir, tm)
    print(cir.to_qis_cir())
    assert cir.gates_num() == 8
