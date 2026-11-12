import copy
import itertools
from typing import Dict, List
import numpy as np
from .graph import *

best_matched_nodes: Dict[Node_P, Node_P] = {} 
best_matched_gates: Dict[Gate, Gate] = {} 
best_matched_qubits: Dict[int, int] = {}
best_cost: int = 0

def print_matched_nodes(matched_nodes: Dict[Node_P, Node_P]) -> str:
    res = "matched_nodes={"
    for tn, cn in matched_nodes.items():
        res += f"{tn.qubit}: {cn.qubit}, "
    res += "}"
    return res

def match(
        cir: H_Graph,
        pattern: H_Graph,
        cost_dict: Dict[tuple[str, int], int],
        matched_nodes: Dict[Node_P, Node_P] = {},
        matched_gates: Dict[Gate, Gate] = {}, 
        matched_qubits: Dict[int, int] = {},
        cost: int = 0,
        pindex: int = 0,
    ) -> None:
    """Match a pattern graph to a circuit graph.

    Args:
        cir (H_Graph): The circuit graph to match against.
        pattern (H_Graph): The pattern graph to match.
        cost_dict (Dict[tuple[str, int], int]): A dictionary mapping gate types and qubit indices to their associated costs.
        matched_nodes (Dict[Node_P, Node_P], optional): A dictionary mapping nodes in the pattern graph to nodes in the circuit graph. Defaults to {}.
        matched_gates (Dict[Gate, Gate], optional): A dictionary mapping gates in the pattern graph to gates in the circuit graph. Defaults to {}.
        matched_qubits (Dict[int, int], optional): A dictionary mapping qubit indices in the pattern graph to qubit indices in the circuit graph. Defaults to {}.
        cost (int, optional): The cost of the current matching. Defaults to 0.
        pindex (int, optional): The index of the current gate in the pattern graph being matched. Defaults to 0.
    """
    global best_matched_nodes, best_matched_gates, best_matched_qubits, best_cost
    # print(f"{pindex=}, {matched_qubits=}, {matched_gates=}")

    # Do not allow matching from the second half
    plen = len(pattern.gates)
    plen_half = plen // 2
    if pindex == plen_half and not matched_gates:
        return

    # Only allow half of the template to be matched in a sliding window
    last_try_index = next(iter(matched_gates)).index + plen_half if matched_gates else plen_half
    if pindex == last_try_index:
        if cost > best_cost:
            best_matched_nodes = matched_nodes.copy()
            best_matched_gates = matched_gates.copy()
            best_matched_qubits = matched_qubits.copy()
            best_cost = cost
        return

    # Early return if the current matched gate count plus the remaining gates in the pattern is less than the best cost
    max_possible_cost = calculate_cost(list(matched_gates.keys()) + pattern.gates[pindex:last_try_index], cost_dict)
    if max_possible_cost <= best_cost:
        # print(f"{len(matched_gates)=}, {len(pattern.gates)=}")
        return

    # Make sure current gate forms a valid subcircuit with the previously matched gates
    tgate = pattern.gates[pindex]
    if check_convex(matched_gates.keys(), tgate):

        # Try to match the current gate in the pattern graph to each gate in the circuit graph
        candidates = gen_candidates(matched_nodes, matched_gates, matched_qubits, tgate)
        added_cost = cost_dict[(tgate.name, len(tgate.q_c))]
        # print(f"{pindex=}, {candidates=}")

        for candidate in candidates:
            matched_gates_n = matched_gates.copy()
            matched_qubits_n = matched_qubits.copy()
            matched_nodes_n = matched_nodes.copy()
            new_cost = cost + added_cost

            # Add matched gate to dictionaries
            matched_gates_n[tgate] = candidate
            if tgate.q_t != -1:
                matched_qubits_n[tgate.q_t] = candidate.q_t
                map_nodes(matched_nodes_n, tgate.q_t, candidate.q_t, tgate, candidate)
            free_qubits_t = []
            free_qubits_c = set(candidate.q_c.keys())
            for tq in tgate.q_c:
                if tq in matched_qubits_n:
                    cq = matched_qubits_n[tq]
                    free_qubits_c.remove(cq)
                    map_nodes(matched_nodes_n, tq, cq, tgate, candidate)
                else:
                    free_qubits_t.append(tq)
            assert len(free_qubits_t) == len(free_qubits_c)

            # Recursively call match with the next gate in the pattern graph
            for p in itertools.permutations(free_qubits_c):
                for tq, cq in zip(free_qubits_t, p):
                    matched_qubits_n[tq] = cq
                    map_nodes(matched_nodes_n, tq, cq, tgate, candidate)
                match(cir, pattern, cost_dict, matched_nodes_n, matched_gates_n, matched_qubits_n, new_cost, pindex + 1)

    # Skip current gate
    match(cir, pattern, cost_dict, matched_nodes, matched_gates, matched_qubits, cost, pindex + 1)

def map_nodes(
        matched_nodes: Dict[Node_P, Node_P],
        tq: int,
        cq: int,
        tgate: Gate,
        cgate: Gate,
    ):
    tnode = tgate.nodes[tq]
    cnode = cgate.nodes[cq]
    matched_nodes[tnode] = cnode
    if (
        tgate.is_node_start[tq]
        and cgate.is_node_start[cq]
        and tnode.predecessor.predecessor is not None
        and cnode.predecessor.predecessor is not None
        and tnode.predecessor.is_commutable(cnode.predecessor)
    ):
        matched_nodes[tnode.predecessor] = cnode.predecessor
    if (
        tgate.is_node_end[tq]
        and cgate.is_node_end[cq]
        and tnode.successor.successor is not None
        and cnode.successor.successor is not None
        and tnode.successor.is_commutable(cnode.successor)
    ):
        matched_nodes[tnode.successor] = cnode.successor

def unmatch_qc_num(matched_qubits, tgate: Gate) -> int:
    """Count the number of unmatched control qubits in the pattern gate."""
    return sum(1 for tq in tgate.q_c if tq not in matched_qubits)

def gen_candidates(
        matched_nodes: Dict[Node_P, Node_P],
        matched_gates: Dict[Gate, Gate],
        matched_qubits: Dict[int, int],
        tgate: Gate
    ) -> List[Gate]:
    """Generate candidate gates in the circuit graph that can match the current gate in the pattern graph.

    Args:
        cir (H_Graph): The circuit graph to match against.
        matched_nodes (Dict[Node_P, Node_P]): A dictionary mapping nodes in the pattern graph to nodes in the circuit graph.
        matched_gates (Dict[Gate, Gate]): A dictionary mapping gates in the pattern graph to gates in the circuit graph.
        matched_qubits (Dict[int, int]): A dictionary mapping qubit indices in the pattern graph to qubit indices in the circuit graph.
        tgate (Gate): The current gate in the pattern graph being matched.

    Returns:
        List[Gate]: A list of candidate gates in the circuit graph that can match the current gate in the pattern graph.
    """
    candidates = []
    checked_gates = set(matched_gates.values())
    matched_cqubits = matched_qubits.values()
    matched_cnodes = matched_nodes.values()
    for node in tgate.nodes.values():
        if node in matched_nodes:
            matched_node = matched_nodes[node]
            for gate in matched_node.gates:
                if gate in checked_gates:
                    continue
                # print(f"checking {gate=}")
                checked_gates.add(gate)
                if (
                    # Validate the candidate gate against the current pattern gate
                    gate.name == tgate.name
                    and ('p' not in gate.name or np.allclose(gate.para, tgate.para))
                    and len(gate.q_c) == len(tgate.q_c)
                    and unmatch_qc_num(matched_qubits, tgate) == unmatch_qc_num(matched_cqubits, gate)
                    and (
                        (tgate.q_t not in matched_qubits and gate.q_t not in matched_cqubits)
                        or tgate.q_t in matched_qubits and matched_qubits[tgate.q_t] == gate.q_t
                    )
                    and (
                        tgate.q_t == -1
                        or (tgate.nodes[tgate.q_t] not in matched_nodes and gate.nodes[gate.q_t] not in matched_cnodes)
                        or tgate.nodes[tgate.q_t] in matched_nodes and matched_nodes[tgate.nodes[tgate.q_t]] == gate.nodes[gate.q_t]
                    )
                ):
                    # Check if the qubits match
                    qubit_match = True
                    for tq, v in tgate.q_c.items():
                        if tq in matched_qubits:
                            cq = matched_qubits[tq]
                            if cq not in gate.q_c or v != gate.q_c[cq]:
                                qubit_match = False
                                break

                            tnode = tgate.nodes[tq]
                            if (
                                tnode in matched_nodes and matched_nodes[tnode] != gate.nodes[cq]
                                or tnode not in matched_nodes and gate.nodes[cq] in matched_cnodes
                            ):
                                qubit_match = False
                                break
                    if qubit_match and check_convex(matched_gates.values(), gate):
                        candidates.append(gate)
    return candidates


def check_convex(gates: Iterable[Gate], tgate: Gate) -> bool:
    """Check if the given gate forms a convex subcircuit with the previously matched gates.
    
    Args:
        gates: A collection of gates that form a valid subcircuit
        tgate: The gate to check for convexity

    Returns:
        bool: True if the gate forms a convex subcircuit, False otherwise
    """
    #print(f"{gates=}, {tgate=}")
    mask = 0
    ancestors = 0
    descendants = 0
    for gate in gates:
        mask |= 1 << gate.index
        ancestors |= gate.ancestors
        descendants |= gate.descendants

    #print(f"{ancestors=}, {descendants=}, {mask=}")
    res = (
        ancestors & tgate.descendants & ~mask == 0
        and descendants & tgate.ancestors & ~mask == 0
    )
    #print(f"{res=}")
    return res

def get_conjuage_gate(gate: Gate) -> Gate:
    if gate.name in "xyzh":
        return copy.copy(gate)
    name_map = {"s": "sdg", "sdg": "s", "t": "tdg", "tdg": "t"}
    new_name = name_map.get(gate.name, gate.name)
    conj = copy.copy(gate)
    conj.para = gate.para.T.conj()
    conj.name = new_name
    return conj

def get_conjugate_cir(
        pattern: Iterable[Gate],
        matched_gates: Dict[Gate, Gate],
        matched_qubits: Dict[int, int]
) -> List[Gate]:
    """Create the conjugate for the matched subcircuit"""
    # print(f"{pattern=}")
    gate_set = 0
    ancestors = 0
    for g in pattern:
        if g in matched_gates:
            gate_set |= 1 << g.index
            ancestors |= g.ancestors

    # Unmatch gates are pushed to the back unless they must be in the front
    front_gates = []
    back_gates = []
    for g in pattern:
        if g not in matched_gates:
            if (1 << g.index) & ancestors == 0:
                back_gates.append(g)
            else:
                front_gates.append(g)

    res = []
    for g in front_gates[::-1] + back_gates[::-1]:
        conj = get_conjuage_gate(g)
        if conj.q_t == -1:
            conj.q_t = -1
        else:
            conj.q_t = matched_qubits[conj.q_t]
        q_c = {}
        for q, v in conj.q_c.items():
            q_c[matched_qubits[q]] = v
        conj.q_c = q_c
        res.append(conj)
    return res

def replace_cir(
        cir_g: H_Graph,
        pattern_g: H_Graph,
        matched_gates: Dict[Gate, Gate],
        matched_qubits: Dict[int, int]
) -> H_Graph:
    # Determine the region that is affected by the replacement
    low_index = len(cir_g.gates)
    high_index = 0
    matched_gate_set = 0
    ancestors = 0
    descendants = 0
    matched_circuit_gates = set(matched_gates.values())
    for g in matched_circuit_gates:
        low_index = min(low_index, g.index)
        for node in g.nodes.values():
            for g2 in node.gates:
                high_index = max(high_index, g2.index)
        matched_gate_set |= 1 << g.index
        ancestors |= g.ancestors
        descendants |= g.descendants

    # Collect related nodes
    nodes_on_qubit: Dict[int, List[Node_P]] = {}
    for i in range(low_index, high_index + 1):
        g = cir_g.gates[i]
        for qubit, node in g.nodes.items():
            if qubit not in nodes_on_qubit:
                nodes_on_qubit[qubit] = [node]
            else:
                nodes_on_qubit[qubit].append(node)

    # Separate unmatched gates
    left_gates = []
    right_gates = []
    for i in range(low_index + 1, high_index + 1):
        g = cir_g.gates[i]
        if g in matched_circuit_gates:
            continue
        if (1 << g.index) & descendants == 0:
            left_gates.append(g)
            # assert(matched_gate_set & g.ancestors == 0)
        else:
            right_gates.append(g)
            # assert(matched_gate_set & g.descendants == 0)
            # assert((1 << g.index) & ancestors == 0)

    # Identify the left nodes of the replacement region
    left_nodes: Dict[int, Node_P] = {}
    to_remove = set(cir_g.gates[low_index: high_index + 1])
    for qubit, nodes in nodes_on_qubit.items():
        node = nodes[0]
        node.gates.difference_update(to_remove)
        if len(node.gates) != 0:
            left_nodes[qubit] = node
        else:
            left_nodes[qubit] = node.predecessor

    # Identify the right nodes of the replacement region
    right_nodes: Dict[int, Node_P] = {}
    for qubit, nodes in nodes_on_qubit.items():
        if nodes[0] is nodes[-1]:
            node = nodes[-1].successor
        else:
            node = nodes[-1]
        node.gates.difference_update(to_remove)
        if node.gates or node.successor is None:
            right_nodes[qubit] = node
        else:
            right_nodes[qubit] = node.successor
        # assert(right_nodes[qubit] is not None and f"{qubit=}")

    # Calculate the conjugate circuit and replace the matched gates
    start = next(iter(matched_gates)).index
    plen_half = len(pattern_g.gates) // 2
    conj_gates = get_conjugate_cir(pattern_g.gates[start: start+plen_half], matched_gates, matched_qubits)
    middle_gates = left_gates + conj_gates + right_gates
    # print(f"{left_gates=}, {conj_gates=}, {right_gates=}")
    append_gates_to_graph(cir_g, middle_gates, left_nodes)

    # Append the right part of the circuit
    for k, right_node in right_nodes.items():
        if not right_node.is_commutable(left_nodes[k]) or right_node.successor is None or left_nodes[k].predecessor is None:
            left_nodes[k].successor = right_node
            right_node.predecessor = left_nodes[k]
        else:
            # Merge right_node with left_node
            for g in right_node.gates:
                left_nodes[k].gates.add(g)
                g.nodes[k] = left_nodes[k]
            left_nodes[k].successor = right_node.successor
            right_node.successor.predecessor = left_nodes[k]
            right_node = left_nodes[k].successor

    # Generate new gate list
    cir_g.gates = cir_g.gates[:low_index] + middle_gates + cir_g.gates[high_index + 1:]
    for index, g in enumerate(cir_g.gates[low_index:]):
        g.index = index + low_index
    cir_g.calculate_ancestor_decendant()

    return cir_g

def calculate_cost(gates: Iterable[Gate], cost_dict: Dict[tuple[str, int], int]) -> int:
    """Calculate the cost of a list of gates based on a cost dictionary.

    Args:
        gates (Iterable[Gate]): The list of gates to calculate the cost for.
        cost_dict (Dict[tuple[str, int], int]): A dictionary mapping gate names and qubit counts to their respective costs.

    Returns:
        int: The total cost of the gates.
    """
    total_cost = 0
    for g in gates:
        key = (g.name, len(g.q_c))
        if key in cost_dict:
            total_cost += cost_dict[key]
        else:
            raise ValueError(f"Cost not defined for gate {g.name} with {len(g.q_c)} control qubits.")
    return total_cost

def preprocess_cost_dict(cost_dict: Dict[tuple[str, int], int] | None) -> Dict[tuple[str, int], int]:
    """Preprocess the cost dictionary to fit the special Gate definition of phase gates.

    Args:
        cost_dict: The original cost dictionary.

    Returns:
        Dict[tuple[str, int], int]: The preprocessed cost dictionary with default values for missing keys.
    """
    if cost_dict is None:
        # Return a default cost dictionary if none is provided
        return {
            ("x", 0): 1,
            ("x", 1): 2,
            ("x", 2): 21,
            ("x", 3): 96,
            ("x", 4): 312,
            ("y", 0): 1,
            ("y", 1): 4,
            ("z", 1): 1,
            ("z", 2): 4,
            ("h", 0): 1,
            ("h", 1): 8,
            ("s", 1): 1,
            ("sdg", 1): 1,
            ("t", 1): 1,
            ("tdg", 1): 1,
            ("p", 1): 1,
            ("u", 0): 1,
            ("u", 1): 10,
        }
    res = {}
    for (name, num_ctrl_qubits), value in cost_dict.items():
        if name in PHASE_GATES:
            res[(name, num_ctrl_qubits + 1)] = value
        else:
            res[(name, num_ctrl_qubits)] = value
    return res

def opt_with_patterns(
        cir: Circuit,
        patterns: list[Circuit],
        cost_dict: Dict[tuple[str, int], int] | None = None,
    ) -> Circuit:
    """Optimize ``cir`` with multiple patterns."""
    global best_matched_nodes, best_matched_gates, best_matched_qubits, best_cost
    # print(cir_g)

    cost_dict = preprocess_cost_dict(cost_dict)
    cir_g = to_H_Graph(cir)

    cost_thresholds = []
    pattern_gs = []
    for pattern in patterns:
        # print(f"pattern={pattern.data}")
        cost_threshold = calculate_cost(pattern.data, cost_dict) / 2
        cost_thresholds.append(cost_threshold)
        # Double the pattern to support wrap around matching
        copied_gates = [copy.copy(g) for g in pattern.data]
        pattern2 = Circuit(pattern.num_qubits, pattern.data + copied_gates)
        # print(pattern2.to_qis_cir())
        pattern_g = to_H_Graph(pattern2)
        pattern_gs.append(pattern_g)
        # print(pattern_g)

    idx = 0
    while idx < len(cir_g.gates):
        for pattern_g, cost_threshold in zip(pattern_gs, cost_thresholds):
            best_matched_nodes = {}
            best_matched_gates = {}
            best_matched_qubits = {}
            best_cost = 0
            gate = cir_g.gates[idx]
            node = gate.nodes[gate.q_t] if gate.q_t != -1 else next(iter(gate.nodes.values()))
            for qubit in range(pattern_g.num_qubits):
                pnode = pattern_g.start_nodes[qubit].successor
                while pnode.successor is not None:
                    if pnode.is_commutable(node):
                        match(cir_g, pattern_g, cost_dict, {pnode: node}, {}, {qubit: node.qubit}, 0)
                    pnode = pnode.successor

            cost = calculate_cost(best_matched_gates.values(), cost_dict)
            #print(f"{cost=}, {best_matched_gates=}")
            if cost > cost_threshold:
                # print(H_Graph_to_Cir(pattern_g).to_qis_cir())
                # print(f"{best_matched_gates=}")
                # print(print_matched_nodes(best_matched_nodes))
                cir_g = replace_cir(cir_g, pattern_g, best_matched_gates, best_matched_qubits)
                idx = max(0, idx - len(pattern_g.gates) // 2)
                # print(f"{idx=}")
                # print(cir_g)
                # print(H_Graph_to_Cir(cir_g).to_qis_cir())
                break
        else:
            idx += 1

    cir_n = H_Graph_to_Cir(cir_g)
    return cir_n

def opt_a_circuit(
        cir: Circuit,
        pattern: Circuit,
        cost_dict: Dict[tuple[str, int], int] | None = None,
    ):
    """Optimize ``cir`` with one pattern."""
    return opt_with_patterns(cir, [pattern], cost_dict)
