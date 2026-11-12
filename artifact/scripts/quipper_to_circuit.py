import numpy as np
from ech_matcher.graph import Circuit, Gate
import os
import re

def parse_quipper_to_circuit(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    num_qubits = None
    gates = []
    for line in lines:
        line = line.strip()
        if line.startswith('Inputs:'):
            # Count number of Qbits
            num_qubits = len(re.findall(r'\d+:Qbit', line))
        elif line.startswith('QGate'):
            # Parse gate name
            m = re.match(r'QGate\["(\w+)"\]\((\d+)\)(.*)', line)
            if not m:
                m = re.match(r'QGate\["(\w+)"\]\*\((\d+)\)(.*)', line)  # For T*
            if m:
                name = m.group(1).lower()
                target = int(m.group(2))
                rest = m.group(3)
                # Controls
                q_c = {}
                ctrl_match = re.search(r'controls=\[(.*?)\]', rest)
                if ctrl_match:
                    for ctrl in ctrl_match.group(1).split(','):
                        ctrl = ctrl.strip()
                        if ctrl.startswith('+'):
                            q_c[int(ctrl[1:])] = 1
                        elif ctrl.startswith('-'):
                            q_c[int(ctrl[1:])] = 0
                        else:
                            raise ValueError(f"Unrecognized control format: {ctrl}")
                # Parameter for T/T*
                if name == 't':
                    name = 'p'
                    para = np.pi/4
                elif name == 's':
                    name = 'p'
                    para = np.pi/2
                elif name == 'z':
                    para = np.array([[1,0],[0,-1]])
                elif name == 'h':
                    para = np.sqrt(2)/2 * np.array([[1,1],[1,-1]])
                elif name == 'not':
                    para = np.array([[0,1],[1,0]])
                    name = 'x'
                else:
                    raise ValueError(f"Unrecognized gate name: {name}")
                if '*' in line:
                    if name == 'p':
                        para = -para
                    else:
                        raise ValueError(f"Unexpected '*' for non-parameterized gate: {name}")
                gates.append(Gate(name, q_c, target, para))
            else:
                raise ValueError(f"Unrecognized gate format: {line}")
        else:
            assert line.startswith('Outputs:'), f"Unrecognized line format: {line}"
    return Circuit(num_qubits, gates)
