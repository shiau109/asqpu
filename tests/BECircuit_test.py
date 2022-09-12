import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.circuit import QubitCircuit, Gate
from qutip_qip.compiler import GateCompiler, Instruction
import numpy as np
import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.component as qcp
from pandas import DataFrame

def read_phych():
    fo = open("./tests/wiring.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    dict_list = eval(spec)
    channels = []
    for ch in dict_list:
        #print(ch)
        channels.append( pch.from_dict( ch ) )
    return channels


def read_qComp():
    fo = open("./tests/spec.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    dict_list = eval(spec)
    qComps = []
    for qc in dict_list:
        #print(ch)
        qComps.append( qcp.from_dict( qc ) )
    return qComps

def read_ChQcomp():
    fo = open("./tests/ChQComp_relation.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    read_dict = eval(spec)
    
    return DataFrame.from_dict(read_dict)

def read_QReg():
    fo = open("./tests/qRegister.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    read_dict = eval(spec)
    
    return read_dict


class MyCompiler(GateCompiler):
    """Custom compiler for generating pulses from gates using the base class 
    GateCompiler.

    Args:
        num_qubits (int): The number of qubits in the processor
        params (dict): A dictionary of parameters for gate pulses such as
                       the pulse amplitude.
    """

    def __init__(self, num_qubits, params):
        super().__init__(num_qubits, params=params)
        self.params = params
        self.gate_compiler = {
            "RX": self.single_qubit_gate_compiler,
            "RY": self.single_qubit_gate_compiler,
        }

    def generate_pulse(self, gate, tlist, coeff, phase=0.0):
        """Generates the pulses.

        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
            tlist (array): A list of times for the evolution.
            coeff (array): An array of coefficients for the gate pulses
            phase (float): The value of the phase for the gate.

        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.                                               
        """

        pulse_info = [
            # (control label, coeff)
            ("sx" + str(gate.targets[0]), np.cos(phase) * coeff),
            ("sy" + str(gate.targets[0]), np.sin(phase) * coeff),
        ]
        #print(tlist)
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]

    def single_qubit_gate_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """
        
        
        # gate.arg_value is the rotation angle
        coeff, tlist= self.generate_pulse_shape(
                "hann",  # Scipy Hann window
                10,  # 100 sampling point
                maximum= 1,
                area= 1,  # 1/2 becuase we use sigmax as the operator instead of sigmax/2
            )
        # tlist = np.abs(gate.arg_value) / self.params["pulse_amplitude"]
        coeff *= self.params["pulse_amplitude"] *gate.arg_value/np.pi
        if gate.name == "RX":
            return self.generate_pulse(gate, tlist, coeff, phase=0.0)
        elif gate.name == "RY":
            return self.generate_pulse(gate, tlist, coeff, phase=np.pi / 2)

#total_op = qeye(2)
num_qubits = 1

rg_x0 = Gate("RX", 0, arg_value= np.pi)
rg_y0 = Gate("RY", 0, arg_value= np.pi)
rg_x1 = Gate("RX", 1, arg_value= np.pi)
rg_y1 = Gate("RY", 1, arg_value= np.pi)

gates_set = [
    rg_x0, rg_x0, rg_y0, rg_y0, rg_x0
]
circuit = QubitCircuit(1)

single_qubit = basis(2, 0)
for gate in gates_set:
    circuit.add_gate(gate)
    print(gate.name)
    g_qobj = gate.get_compact_qobj()
    #print( g_qobj )
    #total_op *= g_qobj
#print( "Result" )
#print( total_op )

mycompiler = MyCompiler(num_qubits, {"pulse_amplitude": 0.02})
#print(mycompiler.gate_compiler)

# raw circuit
for gate in circuit.gates:
    print(gate.name, gate.get_compact_qobj())

# After transpile
# total_op = qeye(2)
# trans_QC = myprocessor.transpile(circuit)
# for gate in trans_QC.gates:
#     total_op *= gate.get_compact_qobj()
# print(total_op)

compiled_data = (mycompiler.compile(circuit))
tlist = compiled_data[0]
coeffs = compiled_data[1]
#print(coeffs)

# plt.plot(tlist["sx0"],coeffs["sx0"], label="sx0")
# plt.plot(tlist["sy0"],coeffs["sy0"], label="sy0")
# plt.legend()
# plt.show()


mybec = bec.BackendCircuit()
mybec._channels = read_phych()
mybec._qComps = read_qComp()
mybec.qc_relation = read_ChQcomp()
mybec.q_reg = read_QReg()

#print(mybec.load_coeff(coeffs))
dac_wf = mybec.load_coeff(coeffs)
# Plot setting
import matplotlib.pyplot as plt
fig, ax = plt.subplots(2,1,sharex=True)

# Compare signal and envelope
for cl in coeffs.keys():
    ax[0].plot( coeffs[cl], label=cl )
ax[0].legend()

# Compare signal and envelope
for ch_name in dac_wf.keys():
    for d_name in dac_wf[ch_name]:
        if type(dac_wf[ch_name][d_name]) != type(None):
            ax[1].plot( dac_wf[ch_name][d_name], label=f"{d_name}-{ch_name}" )
ax[1].legend()

plt.show()