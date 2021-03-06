###################################
# QASM utility functions          #
# By Scott Pakin <pakin@lanl.gov> #
###################################

import qasm
import sys

# Define a function that maps from a symbol to a number, creating a
# new association if necessary.
def symbol_to_number(sym):
    global sym2num, next_sym_num
    try:
        return qasm.sym2num[sym]
    except KeyError:
        qasm.next_sym_num += 1
        qasm.sym2num[sym] = qasm.next_sym_num
        return qasm.next_sym_num

# Define a function to abort the program on an error.
def abend(str):
    sys.stderr.write("%s: %s\n" % (qasm.progname, str))
    sys.exit(1)

# Define a function that returns the topology of the chimera graph associated
# with a given solver.
def chimera_topology(solver):
    nominal_qubits = solver.properties["num_qubits"]
    couplers = solver.properties["couplers"]
    deltas = [abs(c1 - c2) for c1, c2 in couplers]
    delta_tallies = {d: 0 for d in deltas}
    for d in deltas:
        delta_tallies[d] += 1
        sorted_tallies = sorted(delta_tallies.items(), key=lambda dt: dt[1], reverse=True)
    L = sorted_tallies[0][0]
    M = sorted_tallies[1][0] // (2*L)
    N = (nominal_qubits + 2*L*M - 1) // (2*L*M)
    return L, M, N
