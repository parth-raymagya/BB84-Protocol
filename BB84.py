import qiskit
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, BasicAer
from qiskit.tools.visualization import plot_histogram
n = 16
qr = QuantumRegister(n, name='qr')
cr = ClassicalRegister(n, name='cr')
alice = QuantumCircuit(qr, cr, name='Alice')
alice_key = np.random.randint(0, high=2**n)
alice_key = np.binary_repr(alice_key, n)
for index, digit in enumerate(alice_key):
    if digit == '1':
        alice.x(qr[index])
alice_table = []
for index in range(len(qr)):
    if 0.5 < np.random.random():
        alice.h(qr[index])
        alice_table.append('X')
    else:
        alice_table.append('Z')
def SendState(qc1, qc2, qc1_name):
    qs = qc1.qasm().split(sep=';')[4:-1]
    for index, instruction in enumerate(qs):
        qs[index] = instruction.lstrip()
    for instruction in qs:
        if instruction[0] == 'x':
            old_qr = int(instruction[5:-1])
            qc2.x(qr[old_qr])
        elif instruction[0] == 'h':
            old_qr = int(instruction[5:-1])
            qc2.h(qr[old_qr])
        elif instruction[0] == 'm':
            pass
        else:
            raise Exception('Unable to parse instruction')
bob = QuantumCircuit(qr, cr, name='Bob')
SendState(alice, bob, 'Alice')
bob_table = []
for index in range(len(qr)):
    if 0.5 < np.random.random():
        bob.h(qr[index])
        bob_table.append('X')
    else:
        bob_table.append('Z')
for index in range(len(qr)):
    bob.measure(qr[index], cr[index])
backend = BasicAer.get_backend('qasm_simulator')
result = execute(bob, backend=backend, shots=1).result()
plot_histogram(result.get_counts(bob))
bob_key = list(result.get_counts(bob))[0]
bob_key = bob_key[::-1]
keep = []
discard = []
for qubit, basis in enumerate(zip(alice_table, bob_table)):
    if basis[0] == basis[1]:
        print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0]))
        keep.append(qubit)
    else:
        print("Different choice for qubit: {}, Alice has {}, Bob has {}" .format(qubit, basis[0], basis[1]))
        discard.append(qubit)
acc = 0
for bit in zip(alice_key, bob_key):
    if bit[0] == bit[1]:
        acc += 1
print('Percentage of qubits to be discarded according to table comparison: ', len(keep)/n)
print('Measurement convergence by additional chance: ', acc/n)
new_alice_key = [alice_key[qubit] for qubit in keep]
new_bob_key = [bob_key[qubit] for qubit in keep]
acc = 0
for bit in zip(new_alice_key, new_bob_key):
    if bit[0] == bit[1]:
        acc += 1
print('Percentage of similarity between the keys: ', acc/len(new_alice_key))
if (acc//len(new_alice_key) == 1):
    print("Key exchange has been successfull")
    print("New Alice's key: ", new_alice_key)
    print("New Bob's key: ", new_bob_key)
else:
    print("Key exchange has been tampered! Check for eavesdropper or try again")
    print("New Alice's key is invalid: ", new_alice_key)
print("New Bob's key is invalid: ", new_bob_key)
eve = QuantumCircuit(qr, cr, name='Eve')
SendState(alice, eve, 'Alice')
eve_table = []
for index in range(len(qr)):
    if 0.5 < np.random.random():
        eve.h(qr[index])
        eve_table.append('X')
    else:
        eve_table.append('Z')
for index in range(len(qr)):
    eve.measure(qr[index], cr[index])
backend = BasicAer.get_backend('qasm_simulator')
result = execute(eve, backend=backend, shots=1).result()
eve_key = list(result.get_counts(eve))[0]
eve_key = eve_key[::-1]
for qubit, basis in enumerate(zip(alice_table, eve_table)):
    if basis[0] == basis[1]:
        print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0]))
    else:
        print("Different choice for qubit: {}, Alice has {}, Eve has {}" .format(qubit, basis[0], basis[1]))
        if eve_key[qubit] == alice_key[qubit]:
            eve.h(qr[qubit])
        else:
            if basis[0] == 'X' and basis[1] == 'Z':
                eve.h(qr[qubit])
                eve.x(qr[qubit])
            else:
                eve.x(qr[qubit])
                eve.h(qr[qubit])
SendState(eve, bob, 'Eve')
bob_table = []
for index in range(len(qr)):
    if 0.5 < np.random.random():
        bob.h(qr[index])
        bob_table.append('X')
    else:
        bob_table.append('Z')
for index in range(len(qr)):
    bob.measure(qr[index], cr[index])
result = execute(bob, backend=backend, shots=1).result()
plot_histogram(result.get_counts(bob))
bob_key = list(result.get_counts(bob))[0]
bob_key = bob_key[::-1]
keep = []
discard = []
for qubit, basis in enumerate(zip(alice_table, bob_table)):
    if basis[0] == basis[1]:
        print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0]))
        keep.append(qubit)
    else:
        print("Different choice for qubit: {}, Alice has {}, Bob has {}" .format(qubit, basis[0], basis[1]))
        discard.append(qubit)
acc = 0
for bit in zip(alice_key, bob_key):
    if bit[0] == bit[1]:
        acc += 1
print('\nPercentage of qubits to be discarded according to table comparison: ', len(keep)/n)
print('Measurement convergence by additional chance: ', acc/n)
new_alice_key = [alice_key[qubit] for qubit in keep]
new_bob_key = [bob_key[qubit] for qubit in keep]
acc = 0
for bit in zip(new_alice_key, new_bob_key):
    if bit[0] == bit[1]:
        acc += 1
print('\nPercentage of similarity between the keys: ', acc/len(new_alice_key))
if (acc//len(new_alice_key) == 1):
    print("\nKey exchange has been successfull")
    print("New Alice's key: ", new_alice_key)
    print("New Bob's key: ", new_bob_key)
else:
    print("\nKey exchange has been tampered! Check for eavesdropper or try again")
    print("New Alice's key is invalid: ", new_alice_key)
    print("New Bob's key is invalid: ", new_bob_key)



