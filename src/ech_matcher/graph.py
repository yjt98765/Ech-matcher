import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
import networkx as nx
#import matplotlib.pyplot as plt
import itertools
import copy
from typing import Dict, Iterable, List, Set

PHASE_GATES = ['p', 'z', 's', 'sdg', 't', 'tdg']

class Gate:
    def __init__(
        self,
        name='',
        q_c: Dict[int, int] | None = None,
        q_t=0,
        para: float | np.ndarray | None = None,
    ):
        q_c = {} if q_c is None else q_c.copy()
        para = np.eye(2) if para is None else para

        # Name of the gate
        self.name = name

        # The control dictionary. Values are the control qubit states (0 or 1)
        self.q_c = q_c

        # The target qubit. -1 for Phase gates
        self.q_t = q_t

        # Record the nodes that this gate is associated with on each qubit line
        self.nodes: Dict[int, Node_P] = {}
        self.is_node_start: Dict[int, bool] = {}
        self.is_node_end: Dict[int, bool] = {}

        # The bitset of the gates that cannot commute with this gate
        self.ancestors: int = 0
        self.descendants: int = 0

        # The index in the circuit's gate list
        self.index: int = -1

        X = np.array([[0,1],[1,0]])
        if 'x' in name:
            self.para = X
        elif 'p' in name:
            if type(para) == float:
                self.para = np.array([[1,0],[0,np.exp(1j*para)]])
            else:
                self.para = para
        elif 'h' in name:
            self.para = np.array([[1,1],[1,-1]]) / np.sqrt(2)
        elif 'z' in name:
            self.para = np.array([[1, 0], [0, -1]])
        elif name == 's':
            self.para = np.array([[1,0],[0,np.exp(1j*np.pi/2)]])
        elif name == 'sdg':
            self.para = np.array([[1,0],[0,np.exp(-1j*np.pi/2)]])
        elif name == 't':
            self.para = np.array([[1,0],[0,np.exp(1j*np.pi/4)]])
        elif name == 'tdg':
            self.para = np.array([[1,0],[0,np.exp(-1j*np.pi/4)]])
        else:
            self.para=para

        if name in PHASE_GATES and q_t != -1:
            self.q_c[q_t] = 1
            self.q_t = -1

        if 'u' in name:
            if np.allclose(para,X):
                self.name = 'x'
                self.para = X
            elif abs(para[0][1])<1e-10 and abs(para[1][0])<1e-10:
                self.name = 'p'
        if np.allclose(self.para,np.eye(2)):
            self.name = 'p'
            self.q_c={}
            self.q_t = 0
 
    __eq__ = object.__eq__

    def f_eq(self,other):
        return self.q_c==other.q_c and self.q_t == other.q_t and np.allclose(self.para,other.para)
        
    def __str__(self):
        dict_str = '('+", ".join([f"{key}: {value}" for key, value in self.q_c.items()])+')'
        return str((self.name,dict_str,self.q_t,self.para))

    def __repr__(self) -> str:
        dict_str = '(' + ", ".join([f"{key}: {value}" for key, value in self.q_c.items()]) + ')'
        return str((self.name, dict_str, self.q_t, self.index))

    __hash__ = object.__hash__

    def to_cir(self,n):
        cir = QuantumCircuit(n)
        q_c = self.q_c.copy()
        if self.name in PHASE_GATES:
            q_t, _ = q_c.popitem()
        else:
            q_t = self.q_t
        if 'p' in self.name:
            theta = np.angle(self.para[1][1])
            if np.isclose(theta, np.pi):
                cir.z(q_t)
            elif np.isclose(theta, np.pi/2):
                cir.s(q_t)
            elif np.isclose(theta, -np.pi/2):
                cir.sdg(q_t)
            elif np.isclose(theta, np.pi/4):
                cir.t(q_t)
            elif np.isclose(theta, -np.pi/4):
                cir.tdg(q_t)
            else:
                cir.p(theta, q_t)
        elif 'x' in self.name:
            cir.x(self.q_t)
        elif 'u' in self.name:
            if np.allclose(self.para, np.array([[1, 1], [1, -1]]) / np.sqrt(2)):
                cir.h(self.q_t)
            else:
                u3 = UnitaryGate(self.para)
                cir.append(u3, [self.q_t])
        elif 'h' in self.name:
            cir.h(self.q_t)
        elif 'z' in self.name:
            cir.z(q_t)
        elif self.name == 's':
            cir.s(q_t)
        elif self.name == 'sdg':
            cir.sdg(q_t)
        elif self.name == 't':
            cir.t(q_t)
        elif self.name == 'tdg':
            cir.tdg(q_t)
        else:
            raise ValueError(f"Unrecognized gate: {self.name}")
        if len(q_c)>0:
            cir_new = QuantumCircuit(n)
            sorted_q_c = dict(sorted(q_c.items(), reverse=True))
            ctrl_cond = ''
            new_qubits = []
            for k in sorted_q_c:
                ctrl_cond+=str(sorted_q_c[k]) 
                new_qubits.append(k)
            new_qubits.append(q_t)
            # print(ctrl_cond,new_qubits)
            for instruction in cir.data:
                g = instruction.operation
                cg = g.control(len(q_c),ctrl_state=''.join(reversed(ctrl_cond)))
                cir_new.append(cg,new_qubits)
                return cir_new
        return cir

class Circuit:
    def __init__(self, num_qubits=1, data: List[Gate] | None = None):
        self.num_qubits = num_qubits
        self.data = [] if data is None else list(data)

    def gates_num(self):
        return len(self.data)

    def __str__(self):
        s = str(self.num_qubits) + ', ['
        for g in self.data:
            s += repr(g)
            s+=','
        s+=']'
        return s      

    def to_qis_cir(self):
        cir = QuantumCircuit(self.num_qubits)
        for g in self.data:
            cir=cir&g.to_cir(self.num_qubits)
        return cir

def are_parallel(v1, v2):
    ad = v1[0] * v2[1] - v1[1] * v2[0]
    return abs(ad) < 1e-10

def are_perpendicular(v1, v2):
    # 计算点积
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    return abs(dot_product) < 1e-10

class Node_P:
    def __init__(self, qubit: int):
        self.qubit = qubit
        self.successor: None | Node_P = None
        self.predecessor: None | Node_P = None
        self.gates: Set[Gate] = set()
        self.eig_direction: np.ndarray = np.array([1,0])

    __hash__ = object.__hash__

    def is_commutable(self,other):
        v1 = self.eig_direction
        v2 = other.eig_direction
        return (
            abs(v1[0] * v2[1] - v1[1] * v2[0]) < 1e-10
            or abs(v1[0] * v2[0] + v1[1] * v2[1]) < 1e-10
        )

    def __repr__(self) -> str:
        return f"({self.qubit}, {self.gates}, {self.eig_direction})"


class H_Graph:
    def __init__(self, num_qubits = 1):
        self.num_qubits = num_qubits
        self.start_nodes: Dict[int, Node_P] = {}
        """The start_nodes are dummy nodes.

        The successor of a start_node is the first real node in the graph.
        """

        self.end_nodes: Dict[int, Node_P] = {}
        """The end_nodes are dummy nodes"""

        self.gates: List[Gate] = []

    def __repr__(self) -> str:
        res = f"H_Graph{{num_qubits={self.num_qubits}, gates={self.gates}, nodes="
        for i in range(self.num_qubits):
            res += f"\n{i}:"
            node = self.start_nodes[i].successor
            nodes_str = []
            while node.successor is not None:
                nodes_str.append(str(node))
                node = node.successor
            res += ' -> '.join(nodes_str)
        res += "\n}"
        return res

    def to_graph(self):
        temp_node = copy.copy(self.start_nodes)
        G = nx.Graph()
        pos = [0]*self.num_qubits
        is_end = False
        while(not is_end):
            is_end = True
            for k in range(self.num_qubits):
                if temp_node[k]!=None:
                    is_end = False
            for k in range(self.num_qubits):
                if temp_node[k]==None:
                    continue
                G.add_node(temp_node[k],label = (k,pos[k]))
                if temp_node[k]!=self.start_nodes[k]:
                    G.add_edge(temp_node[k],temp_node[k].predecessor)
                    for g in temp_node[k].gates:
                        if len(g.nodes)>1:
                            for (a,b) in itertools.combinations(g.nodes.values(), 2):
                                if a in G.nodes() and b in G.nodes:
                                    G.add_edge(a,b)
                temp_node[k] = temp_node[k].successor
                pos[k]=pos[k]+1
        # G2 = G.to_graph()
        # nx.draw(G2,with_labels = True,labels={node: data['label'] for node, data in G2.nodes(data=True)})                
        return G

    def validate(self) -> None:
        shown = set()
        for k in range(self.num_qubits):
            if k not in self.start_nodes or k not in self.end_nodes:
                raise ValueError(f"Node {k} is missing in start or end nodes.")
            node = self.start_nodes[k].successor
            pre_node = self.start_nodes[k]
            while node.successor:
                if node.predecessor != pre_node:
                    raise ValueError(f"Node {node} has incorrect predecessor.")
                shown.add(node)
                for g in node.gates:
                    if g not in self.gates:
                        raise ValueError(f"Gate {repr(g)} is not in the graph's gates.")
                    if k not in g.nodes:
                        raise ValueError(f"Node {k} is not in the gate {g}.")
                pre_node = node
                node = node.successor
            if node is not self.end_nodes[k] or node.successor is not None:
                raise ValueError(f"Node {k} does not end at the expected end node.")
        for gate in self.gates:
            nq = len(gate.q_c) + (gate.q_t != -1)
            if len(gate.nodes) != nq:
                raise ValueError(f"Gate {gate} does not have the correct number of nodes.")
            for node in gate.nodes.values():
                if gate not in node.gates:
                    raise ValueError(f"Gate {gate} is not listed in node {node}'s gates.")

    def local_commute(self, g1: Gate, g2: Gate) -> bool:
        """Check whether two ADJACENT gates commute with each other in the H_Graph."""
        common_qubits = g1.nodes.keys() & g2.nodes.keys()
        if not common_qubits:
            return True
        for qubit in common_qubits:
            if g1.nodes[qubit] is not g2.nodes[qubit]:
                return False
        return True

    def calculate_ancestor_decendant(self) -> None:
        """Calculate the ancestors and descendants for each gate in the H_Graph.

        Ancestors and descendants are the transitive closure of local
        noncommutation dependencies before and after each gate, respectively.
        Bit ``i`` in either integer identifies ``G.gates[i]``.
        """
        gates = self.gates

        for gate in gates:
            ancestors = 0
            for node in gate.nodes.values():
                for gate2 in node.predecessor.gates:
                    ancestors |= gate2.ancestors | (1 << gate2.index)
            gate.ancestors = ancestors

        for gate in reversed(gates):
            descendants = 0
            for node in gate.nodes.values():
                for gate2 in node.successor.gates:
                    descendants |= gate2.descendants | (1 << gate2.index)
            gate.descendants = descendants

        node_gate_sets = {}
        for qubit in range(self.num_qubits):
            node = self.start_nodes[qubit].successor
            while node.successor is not None:
                gate_set = 0
                for gate in node.gates:
                    gate_set |= 1 << gate.index
                node_gate_sets[node] = gate_set
                node = node.successor

        for gate in gates:
            gate.is_node_start = {}
            gate.is_node_end = {}
            for qubit, node in gate.nodes.items():
                gate_set = node_gate_sets[node]
                gate.is_node_start[qubit] = gate.ancestors & gate_set == 0
                gate.is_node_end[qubit] = gate.descendants & gate_set == 0

def get_controlled_circuit2(cir,cond = {0:1},add_qubits_num = 0):
    cir.num_qubits += add_qubits_num
    new_data = []
    for g in cir.data:
        for c in cond:
            g.q_c[c]=cond[c]
    return cir

# g = Gate('x',{},0)
# c = Circuit(2,[g])
# c.to_cir().draw('mpl')
# c2 = get_controlled_circuit2(c,{2:0,1:1},1)
# c.to_cir().draw('mpl')

def append_gates_to_graph(G: H_Graph, gates: Iterable[Gate], end_nodes: Dict[int, Node_P]):
    """Append gates to an H_Graph at `end_nodes`

    Args:
        G: The H_Graph
        gate: The gates to be added
        end_nodes: The starting points of gate appending. It will be updated during the append process
    """
    for g in gates:
        g.nodes = {}
        for k in g.q_c:
            if (
                are_parallel(end_nodes[k].eig_direction, (1, 0))
                and end_nodes[k] != G.start_nodes[k]
            ):
                end_nodes[k].gates.add(g)
            else:
                node = Node_P(k)
                node.eig_direction=np.array([1,0])
                node.gates.add(g)
                end_nodes[k].successor = node
                node.predecessor = end_nodes[k]
                end_nodes[k] = node
            g.nodes[k] = end_nodes[k]

        k = g.q_t

        # Skip target qubit placeholder
        if k == -1:
            continue

        res = np.dot(g.para,end_nodes[k].eig_direction)
        if (
            are_parallel(res, end_nodes[k].eig_direction)
            and end_nodes[k] != G.start_nodes[k]
        ):
            end_nodes[k].gates.add(g)
        else:
            node = Node_P(k)
            if g.name == 'p':
                eig_v = np.array([1,0])
            elif g.name == 'x':
                eig_v = np.array([1,1])
            elif g.name == 'h':
                eig_v = np.array([np.cos(np.pi / 8), np.sin(np.pi / 8)])
            else:
                eig_va, eig_vc = np.linalg.eig(g.para)
                eig_v = eig_vc[0]
            node.eig_direction = eig_v
            node.gates.add(g)
            end_nodes[k].successor = node
            node.predecessor = end_nodes[k]
            end_nodes[k] = node
        g.nodes[k] = end_nodes[k]

def to_H_Graph(cir: Circuit) -> H_Graph:
    n=cir.num_qubits
    G = H_Graph(n)
    end_nodes: Dict[int, Node_P] = {}
    for k in range(n):
        node = Node_P(k)
        node.eig_direction=np.array([1,0])
        G.start_nodes[k] = node
        end_nodes[k] = node

    append_gates_to_graph(G, cir.data, end_nodes)
    G.gates = copy.copy(cir.data)

    for k in range(n):
        node = Node_P(k)
        node.eig_direction=np.array([1,0])
        G.end_nodes[k] = node
        end_nodes[k].successor = node
        node.predecessor = end_nodes[k]

    for index, g in enumerate(cir.data):
        g.index = index

    G.calculate_ancestor_decendant()
    return G

def H_Graph_to_Cir(G: H_Graph) -> Circuit:
    cir = Circuit(G.num_qubits, G.gates.copy())
    return cir

def gen_cir(name=None,qubit_num = 1,gate_num = 1,seed = None):
    from qiskit import QuantumCircuit
    import random
    cir=QuantumCircuit(qubit_num)
    if seed:
        random.seed(seed)
    if name=='Random_Clifford':
        gate_set = ['x','y','z','h','s','cx']
        
        for k in range(gate_num):
            g = gate_set[random.randint(0,len(gate_set)-1)]
            q = random.randint(0,qubit_num-1)
            if g=='cx':
                q2 = random.randint(0,qubit_num-1)
                while q2==q:
                    q2 = random.randint(0,qubit_num-1)
                eval('cir.'+g+str(tuple([q,q2])))
            else:
                eval('cir.'+g+str(tuple([q])))
                
        return cir
    
    if name=='Random_Clifford_T':
        gate_set = ['x','y','z','h','s','cx','t']
        
        for k in range(gate_num):
            g = gate_set[random.randint(0,len(gate_set)-1)]
            q = random.randint(0,qubit_num-1)
            if g=='cx':
                q2 = random.randint(0,qubit_num-1)
                while q2==q:
                    q2 = random.randint(0,qubit_num-1)
                eval('cir.'+g+str(tuple([q,q2])))
            else:
                eval('cir.'+g+str(tuple([q])))
                
        return cir   
        
    if name=='Random_Clifford_CCZ':
        gate_set = ['x','y','z','h','s','cx','t','ccz']
        
        for k in range(gate_num):
            g = gate_set[random.randint(0,len(gate_set)-1)]
            q = random.randint(0,qubit_num-1)
            if g=='cx':
                q2 = random.randint(0,qubit_num-1)
                while q2==q:
                    q2 = random.randint(0,qubit_num-1)
                eval('cir.'+g+str(tuple([q,q2])))
            elif g == 'ccz':
                if qubit_num>=3:
                    q = random.sample(range(0, qubit_num), 3)
                    cir.ccz(q[0],q[1],q[2])
            else:
                eval('cir.'+g+str(tuple([q])))
                
        return cir         

def gen_cir2(name=None,qubit_num = 1,gate_num = 1,seed = None) -> Circuit:
    import random
    cir=Circuit(qubit_num,[])
    if seed:
        random.seed(seed)
    if name=='Random_Clifford':
        gate_set = ['x','y','z','h','s','cx']
        
        for k in range(gate_num):
            g = gate_set[random.randint(0,len(gate_set)-1)]
            q = random.randint(0,qubit_num-1)
            if g=='cx':
                q2 = random.randint(0,qubit_num-1)
                while q2==q:
                    q2 = random.randint(0,qubit_num-1)
                # eval('cir.'+g+str(tuple([q,q2])))
                cir.data+=[Gate('x',{q:1},q2)]
            else:
                # eval('cir.'+g+str(tuple([q])))
                if g=='x':
                    cir.data+=[Gate('x',{},q)]
                if g=='y':
                    cir.data+=[Gate('u',{},q,np.array([[0,-1j],[1j,0]]))]
                if g=='z':
                    cir.data+=[Gate('p',{},q,np.pi)]
                if g=='s':
                    cir.data+=[Gate('p',{},q,np.pi/2)]
                if g=='h':
                    cir.data+=[Gate('u',{},q,np.sqrt(2)/2*np.array([[1,1],[1,-1]]))]                    
                    
        return cir
    
    elif name=='Random_Clifford_T':
        gate_set = ['x','y','z','h','s','cx','t']
        
        for k in range(gate_num):
            g = gate_set[random.randint(0,len(gate_set)-1)]
            q = random.randint(0,qubit_num-1)
            if g=='cx':
                q2 = random.randint(0,qubit_num-1)
                while q2==q:
                    q2 = random.randint(0,qubit_num-1)
                # eval('cir.'+g+str(tuple([q,q2])))
                cir.data+=[Gate('x',{q:1},q2)]
            else:
                # eval('cir.'+g+str(tuple([q])))
                if g=='x':
                    cir.data+=[Gate('x',{},q)]
                if g=='y':
                    cir.data+=[Gate('u',{},q,np.array([[0,-1j],[1j,0]]))]
                if g=='z':
                    cir.data+=[Gate('p',{},q,np.pi)]
                if g=='s':
                    cir.data+=[Gate('p',{},q,np.pi/2)]
                if g=='t':
                    cir.data+=[Gate('p',{},q,np.pi/4)]                    
                if g=='h':
                    cir.data+=[Gate('u',{},q,np.sqrt(2)/2*np.array([[1,1],[1,-1]]))]  
                
        return cir
        
    elif name == 'Random_X_CX_CCX':
        gate_set = ['x','cx','ccx']
        
        for k in range(gate_num):
            g = gate_set[random.randint(0,len(gate_set)-1)]
            if g=='x':
                q = random.sample(range(qubit_num), 1)
                cir.data+=[Gate('x',{},q[0])]
            if g=='cx':
                if qubit_num<2:
                    continue
                q = random.sample(range(qubit_num), 2)
                cir.data+=[Gate('x',{q[0]:1},q[1])]
            if g=='ccx':
                if qubit_num<3:
                    continue
                q = random.sample(range(qubit_num), 3)
                cir.data+=[Gate('x',{q[0]:1,q[1]:1},q[2])]
                
        return cir

    else:
        raise ValueError(f"Unrecognized name {name}")
