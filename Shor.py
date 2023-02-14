from qiskit.quantum_info import *
from qiskit import *
import re
import matplotlib.pyplot as plt
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram
from qiskit.circuit.library.standard_gates import ZGate
from qiskit.circuit.library.standard_gates import YGate

print('\nShor Code')
print('----------------')

backend = Aer.get_backend('aer_simulator')

#create circuit
q = QuantumRegister(17,'q')
c = ClassicalRegister(17,'c')
cir = QuantumCircuit(q,c)


# Encodes the qubit in a three-qubit entangled state
cir.cx(q[0],q[3])
cir.cx(q[0],q[6])

cir.barrier()
#add Hadamard
cir.h([0])
cir.h([3])
cir.h([6])
cir.barrier()
#first block
cir.cx(q[0],q[1])
cir.cx(q[0],q[2])
cir.barrier()
#second block
cir.cx(q[3],q[4])
cir.cx(q[3],q[5])
cir.barrier()
#third block
cir.cx(q[6],q[7])
cir.cx(q[6],q[8])
cir.barrier()

cliff = random_clifford(8)
cq= cliff.to_circuit()
circuit= cir.compose(cq)
#add error
#circuit.u2(180, 90, q[1])
#circuit.t(q[4])
#circuit.z(q[7])
circuit.barrier()
#####syndrom measurement
circuit.h([9])
circuit.h([10])
circuit.h([11])
circuit.h([12])
circuit.h([13])
circuit.h([14])
circuit.h([15])
circuit.h([16])
circuit.barrier()
#X0X1X2X3X4X5
circuit.cx(q[9], q[0])
circuit.cx(q[9], q[1])
circuit.cx(q[9], q[2])
circuit.cx(q[9], q[3])
circuit.cx(q[9], q[4])
circuit.cx(q[9], q[5])
circuit.barrier()
#X3X4X5X6X7X8
circuit.cx(q[10], q[3])
circuit.cx(q[10], q[4])
circuit.cx(q[10], q[5])
circuit.cx(q[10], q[6])
circuit.cx(q[10], q[7])
circuit.cx(q[10], q[8])
circuit.barrier()
#Z0Z1
circuit.cz(q[11],q[0])
circuit.cz(q[11],q[1])
circuit.barrier()
#Z1Z2
circuit.cz(q[12],q[1])
circuit.cz(q[12],q[2])
circuit.barrier()
#Z3Z4
circuit.cz(q[13],q[3])
circuit.cz(q[13],q[4])
circuit.barrier()
#Z4Z5
circuit.cz(q[14],q[4])
circuit.cz(q[14],q[5])
circuit.barrier()
#Z6Z7
circuit.cz(q[15],q[6])
circuit.cz(q[15],q[7])
circuit.barrier()
#Z7Z8
circuit.cz(q[16],q[7])
circuit.cz(q[16],q[8])
circuit.barrier()
circuit.h([9])
circuit.h([10])
circuit.h([11])
circuit.h([12])
circuit.h([13])
circuit.h([14])
circuit.h([15])
circuit.h([16])
circuit.barrier()
##measurement
#X
circuit.measure(q[9], c[16])
circuit.measure(q[10], c[15])
circuit.barrier()
#Z
circuit.measure(q[11], c[14])
circuit.measure(q[12], c[13])
circuit.measure(q[13], c[12])
circuit.measure(q[14], c[11])
circuit.measure(q[15], c[10])
circuit.measure(q[16], c[9])
circuit.barrier()

####error correction

#phase flip correction
circuit.barrier()
circuit.cz(q[9],q[0])
circuit.cz(q[9],q[1])
circuit.cz(q[9],q[2])
circuit.barrier()
circuit.cz(q[10],q[6])
circuit.cz(q[10],q[7])
circuit.cz(q[10],q[8])
circuit.barrier()
c3z_gate = ZGate().control(2)
circuit.append(c3z_gate, [10,9,0])
circuit.append(c3z_gate, [10,9,1])
circuit.append(c3z_gate, [10,9,2])
circuit.append(c3z_gate, [10,9,3])
circuit.append(c3z_gate, [10,9,4])
circuit.append(c3z_gate, [10,9,5])
circuit.append(c3z_gate, [10,9,6])
circuit.append(c3z_gate, [10,9,7])
circuit.append(c3z_gate, [10,9,8])

circuit.barrier()
#first block bit flip
circuit.cx(q[11],q[0])
circuit.cx(q[12],q[2])
circuit.barrier()
circuit.ccx(q[12],q[11],q[0])
circuit.ccx(q[12],q[11],q[1])
circuit.ccx(q[12],q[11],q[2])
circuit.barrier()
#second block bit flip
circuit.cx(q[13],q[3])
circuit.cx(q[14],q[5])
circuit.barrier()
circuit.ccx(q[14],q[13],q[3])
circuit.ccx(q[14],q[13],q[4])
circuit.ccx(q[14],q[13],q[5])
circuit.barrier()
#third block bit flip
circuit.cx(q[15],q[6])
circuit.cx(q[16],q[8])
circuit.barrier()
circuit.ccx(q[16],q[15],q[6])
circuit.ccx(q[16],q[15],q[7])
circuit.ccx(q[16],q[15],q[8])
circuit.barrier()
####decoding
#first block
circuit.cx(q[0],q[2])
circuit.cx(q[0],q[1])
circuit.barrier()
#second block
circuit.cx(q[3],q[5])
circuit.cx(q[3],q[4])
circuit.barrier()
#third block
circuit.cx(q[6],q[8])
circuit.cx(q[6],q[7])

circuit.barrier()
#add Hadamard
circuit.h([0])
circuit.h([3])
circuit.h([6])
circuit.barrier()
circuit.cx(q[0],q[6])
circuit.cx(q[0],q[3])
circuit.barrier()
#faulty bit measure
circuit.measure(q[0], c[8])
circuit.measure(q[1], c[7])
circuit.measure(q[2], c[6])
circuit.measure(q[3], c[5])
circuit.measure(q[4], c[4])
circuit.measure(q[5], c[3])
circuit.measure(q[6], c[2])
circuit.measure(q[7], c[1])
circuit.measure(q[8], c[0])

job = execute(circuit, backend , shots=1000, memory=True)
job_monitor(job)
counts = job.result().get_counts()

print("\nShore code")
print("----------------------")
print(counts)


#circuit.draw(output='mpl', plot_barriers= False)
#plt.show()

result = [(key, value) for key, value in counts.items() if key.endswith("000000000")]
sum  = [sum(value for key, value in counts.items() if key.endswith("000000000"))]
print(sum)
print(result)
print(len(counts.items()))
