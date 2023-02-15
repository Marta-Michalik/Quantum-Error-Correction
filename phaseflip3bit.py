from qiskit.tools.monitor import job_monitor
from qiskit.quantum_info import *
from qiskit import *
import re
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit.circuit.library.standard_gates import ZGate
from qiskit.circuit.library.standard_gates import HGate
from qiskit.providers.aer.noise import *
print('\nPhase Flip Code')
print('----------------')

backend = Aer.get_backend('aer_simulator')

#create circuit

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')
cir = QuantumCircuit(q,c)

# Encodes the qubit in a three-qubit entangled state
cir.cx(q[0],q[1])
cir.cx(q[0],q[2])
cir.h(q[0])
cir.h(q[1])
cir.h(q[2])
cir.barrier()
#phase error
#circuit.z(q[0])
cliff = random_clifford(3)
cq= cliff.to_circuit()
circuit= cir.compose(cq)
circuit.barrier()
#syndrom measure
circuit.h(q[3])
circuit.h(q[4])
circuit.barrier()

circuit.cx(q[3],q[0])
circuit.cx(q[3],q[1])
circuit.cx(q[4],q[1])
circuit.cx(q[4],q[2])
circuit.barrier()
circuit.h(q[3])
circuit.h(q[4])
circuit.barrier()

circuit.measure(q[3], c[0])
circuit.measure(q[4], c[1])
circuit.barrier()
#error corrrection
circuit.cz(q[3],q[0])
circuit.cz(q[4],q[2])
circuit.barrier()
c3z_gate = ZGate().control(2)
circuit.append(c3z_gate, [4,3,0])
circuit.append(c3z_gate, [4,3,1])
circuit.append(c3z_gate, [4,3,2])
circuit.barrier()
#decoding
circuit.h(q[0])
circuit.h(q[1])
circuit.h(q[2])
circuit.barrier()
circuit.cx(q[0],q[2])
circuit.cx(q[0],q[1])
circuit.barrier()
circuit.measure(q[0], c[4])
circuit.measure(q[1], c[3])
circuit.measure(q[2], c[2])




job = execute(circuit, backend, shots=1000)
job_monitor(job)
counts = job.result().get_counts()

print("\nPhase flip code with error")
print("----------------------")
print(counts)
regex = r'000'
results = [[v,k] for k, v in counts.items() if re.match(regex, k)]
sum  = [sum(v for k, v in counts.items() if re.match(regex, k))]
print(results)
print(sum)
circuit.draw(output='mpl',plot_barriers= False)
plt.show()
plot_histogram(counts)
plt.show()
print(cliff)