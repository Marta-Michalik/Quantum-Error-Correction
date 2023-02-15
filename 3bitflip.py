from qiskit.quantum_info import *
from qiskit.tools.monitor import job_monitor
from qiskit import *
import re
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import qiskit.providers.aer.noise as noise
from qiskit.providers.aer.noise import *
print('\nBit Flip Code')
print('----------------')

backend = Aer.get_backend('aer_simulator')

#create circuit
q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')
cir = QuantumCircuit(q,c)
# Encodes the qubit in a three-qubit entangled state
cir.cx(q[0],q[1])
cir.cx(q[0],q[2])
cir.barrier()
cliff = random_clifford(3)
cq= cliff.to_circuit()
circuit= cir.compose(cq)
#simulate a bit flip error
#circuit.x(q[0])
circuit.barrier()
#syndrom measurement
circuit.cx(q[0],q[3])
circuit.cx(q[1],q[3])
circuit.cx(q[1],q[4])
circuit.cx(q[2],q[4])
circuit.barrier()
circuit.measure(q[3], c[0])
circuit.measure(q[4], c[1])
circuit.barrier()
#error correction

circuit.cx(q[3],q[0])
circuit.cx(q[4],q[2])
circuit.barrier()
circuit.ccx(q[4],q[3],q[0])
circuit.ccx(q[4],q[3],q[1])
circuit.ccx(q[4],q[3],q[2])
circuit.barrier()
#decoding
circuit.cx(q[0],q[2])
circuit.cx(q[0],q[1])
circuit.barrier()
#checking results
circuit.measure(q[0], c[4])
circuit.measure(q[1], c[3])
circuit.measure(q[2], c[2])

#####################################################

job = execute(circuit, backend, shots=1000, memory=True)
job_monitor(job)
counts = job.result().get_counts()

print("\nBit flip code with error")
print("----------------------")
print(counts)
regex = r'00\b'
results = [[v,k] for k, v in counts.items() if re.match(regex, k)]

print(results)
#circuit.draw(output='mpl', plot_barriers=False, scale= 0.20, vertical_compression = 'low')
#plt.show()

#plot_histogram(counts)
#plt.show()

result = [(key, value) for key, value in counts.items() if key.endswith("00")]
sum  = [sum(value for key, value in counts.items() if key.endswith("00"))]
print(sum)
print(result)