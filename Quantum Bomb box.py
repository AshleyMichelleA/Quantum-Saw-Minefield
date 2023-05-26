#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Code for the basic bomb tester circuit to test if it is active or not . 
# We are using two qubits


from qiskit import QuantumCircuit


bomb_tester = QuantumCircuit(2) #QuantumCircuit object with 2 qubits named "Bomb tester"
bomb_tester.h(0)                # ".h"  for Hadamard gate to the first qubit (index 0)
bomb_tester.cx(0,1)             # ".cx" for CNOT gate with control qubit 0 and target qubit 1 //study more
bomb_tester.h(0)                # apply Hadamard gate to the first qubit again
bomb_tester.measure_all()       # measure both qubits
bomb_tester.draw(output='mpl')  # visualize the circuit using matplotlib

#IMAGE-DESCRIPTION

#What we have here is a hadmard gate for our beam splitter a CNOT gate for the bomb
# and then another hadmard gate


# In[3]:


#running the basic bomb tester circuit

from qiskit.providers.aer import QasmSimulator
simulator = QasmSimulator()
# Run the bomb_tester circuit on the simulator and specify the number of shots (i.e., repetitions) for the measurement
job = simulator.run(bomb_tester, shots=1000)
result = job.result()

# Extract the measurement counts from the result
counts = result.get_counts(bomb_tester)

from qiskit.visualization import plot_histogram
plot_histogram(counts)



# In[18]:


from qiskit import execute
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, CompleteMeasFitter)
cal_circuits, state_labels = complete_meas_cal(qr=bomb_tester.qregs[0], 
                                               circlabel='measurement_calibration')
cal_circuits[3].draw(output='mpl')


# In[16]:


len(cal_circuits)


# In[19]:


cal_job = execute(cal_circuits,
             backend=device,
             shots=8192,
             optimization_level=0)
#print(cal_job.job_id())
job_monitor(cal_job)
cal_results = cal_job.result()


# In[5]:


#quantum bomb tester using the quantum zeno effect

from qiskit.circuit import QuantumRegister, ClassicalRegister
import numpy as np
from qiskit.circuit.library import RXGate

cycles= 6 #chose number of times we want to pass our photon through the mystery box. The more, the better
theta= np.pi/cycles #The correct reflectivity of our beamsplitter is chose fpr the Zeno effect to work

#Create our Quantum Circuit

qr = QuantumRegister(2, 'q')
cr = ClassicalRegister(cycles, 'c')
zeno_tester = QuantumCircuit (qr, cr)

#Create a chain pf out variable beamsplitters and C-NOT bombs

for cycle in range(cycles-1):
                  zeno_tester.append(RXGate(theta), [qr[0]])
                  zeno_tester.cx(0,1)
                  zeno_tester.measure(qr[1],cr[cycle])
                  zeno_tester.reset(qr[1])
            
#Add a final beamsplitter
zeno_tester.append(RXGate(theta), [qr[0]])

#Measure our photon to predict whether there is a bomb , and a measure our bomb qubit to see if it exploded.
zeno_tester.measure(qr[0], cr[cycles-1])
zeno_tester.draw(output='mpl')




# In[6]:


zeno_job = simulator.run(zeno_tester, shots=1000)
zeno_result = zeno_job.result()
zeno_counts = zeno_result.get_counts(zeno_tester)

plot_histogram(zeno_counts)


# In[7]:


# Setting up the circuit for quantum minesweeper 

from qiskit.circuit.library import CCXGate

def q_sweeper(cycles) -> QuantumCircuit:
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(cycles+1, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    for cycle in range(cycles-1):
        qc.append(RXGate(theta), [qr[1]])
        qc.ccx(qr[0], qr[1], qr[2]) 
        qc.measure(qr[2],cr[cycle])
        if cycle < cycles-1:
            qc.reset(qr[2])
        
    qc.append(RXGate(theta), [qr[1]])
    qc.measure(qr[1],cr[cycles-1])
    qc.measure(qr[0],cr[cycles])
    return qc

successes = 0 # We will use this variable to track the number of successful predictions in a row
cycles = 8
theta = np.pi/cycles

zeno_circuit = q_sweeper(cycles)
zeno_circuit.draw(output='mpl')


# In[8]:


qsweeper_job = simulator.run(zeno_circuit, shots=1000)
qsweeper_result = qsweeper_job.result()
qsweeper_counts = qsweeper_result.get_counts(zeno_circuit)

plot_histogram(qsweeper_counts)


# In[9]:


# Game of quantum minesweeper 
qsweeper_job = simulator.run(zeno_circuit, shots=1)
qsweeper_result = qsweeper_job.result()
qsweeper_counts = qsweeper_result.get_counts(zeno_circuit)

result = sorted(qsweeper_counts.keys())[0]



for i in range(2,cycles): # Check that none of the 3rd to last bits have flipped to a 1 
    if int(result[i]) == 1:
        print("GAME OVER ")
        print("Your score was:") 
        print(successes)
        print(bomb)
        successes = 0
        explode = 1
        break
    else:
        explode = 0
        
        bomb = 7
    
if explode == 0:
    print("The qubit predicts...")
    if int(result[1]) == 0:
        print("Bomb present")
        Prediction = input("There are 8 bombs between you and the red door accross the hallway.Type 0 for no bomb, 1 for bomb.")
    else:
        print("No bomb")
        Prediction = input("There are 8 bombs between you and the red door accross the hallway.Type 0 for no bomb, 1 for bomb.")
        
    if Prediction == "0": 
        print("You predicted there is no bomb.")
    elif Prediction == "1":
        print("You predicted there is a bomb")
    else:
        print("Invalid prediction!")
       

    if Prediction == result[0]:
        print("Congratulations! You predicted correctly")
        successes += 1
       
    
    elif int(Prediction) == (int(result[0]) + 1) % 2:
        print("Uh oh! You predicted wrong. GAME OVER :")
        print("Your score was:") 
        print(successes)
        successes = 0
       
        
        
       
    else:
        print("Prediction was invalid, try again")
              
    
print("Jigsaw Game Score:")
print(successes)

    




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




