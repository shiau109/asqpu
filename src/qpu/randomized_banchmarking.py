
from cProfile import label
from typing import List
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pulse_generator.pulse import Pulse
import numpy as np
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj, fock_dm
from qutip_qip.circuit import QubitCircuit, Gate, CircuitSimulator
from qutip_qip.device import ModelProcessor, Processor, Model
from qutip_qip.compiler import GateCompiler, Instruction
from qutip_qip.operations import gate_sequence_product


class MyModel(Model):
    """A custom Hamiltonian model with sigmax and sigmay control."""
    def get_control(self, label):
        """
        Get an available control Hamiltonian.
        For instance, sigmax control on the zeroth qubits is labeled "sx0".

        Args:
            label (str): The label of the Hamiltonian

        Returns:
            The Hamiltonian and target qubits as a tuple (qutip.Qobj, list).
        """
        targets = int(label[2:])
        if label[:2] == "sx":
            return 2 * np.pi * sigmax() / 2, [targets]
        elif label[:2] == "sy":
            return 2 * np.pi * sigmay() / 2, [targets]
        else:
            raise NotImplementError("Unknown control.")


class MyCompiler(GateCompiler):
    """Custom compiler for generating pulses from gates using the base class 
    GateCompiler.

    Args:
        num_qubits (int): The number of qubits in the processor
        params (dict): A dictionary of parameters for gate pulses such as
                       the pulse amplitude.
    """

    def __init__(self, num_qubits, params=None, args=None):
        super().__init__(num_qubits, params=params)
        self.params = params
        self.gate_compiler = {
            "RX": self.single_qubit_gate_compiler,
            "RY": self.single_qubit_gate_compiler,
        }
        self.args = {  # Default configuration
            "shape": "rectangular",
            "num_samples": None,
            "params": self.params,
        }
        self.args.update( args )
        print(args)

    def generate_pulse(self, gate, tlist, coeff):
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
            ("sx" + str(gate.targets[0]), coeff.real),
            ("sy" + str(gate.targets[0]), coeff.imag),
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
        
        pulse = Pulse()
        pulse = args["pulse"]
        # gate.arg_value is the rotation angle
        envelope = pulse.generate_envelope(0,args["dt"])
        coeff = envelope.Y
        # tlist = np.abs(gate.arg_value) / self.params["pulse_amplitude"]
        coeff *= gate.arg_value/np.pi
        if gate.name == "RX":
            return self.generate_pulse(gate, envelope.get_xAxis(), coeff)
        elif gate.name == "RY":
            return self.generate_pulse(gate, envelope.get_xAxis(), coeff)


"""
g_x = Gate("X", 0)
g_y = Gate("Y", 0)
g_z = Gate("Z", 0)
rg_z = Gate("RZ", 0, arg_value= np.pi)
g_nhz = Gate("RZ", 0, arg_value= np.pi/2)
"""


## Basic
## Pi
rg_i = Gate("RX", 0, arg_value= 0)
rg_x = Gate("RX", 0, arg_value= np.pi)
rg_y = Gate("RY", 0, arg_value= np.pi)
## Pi/2
rg_px2 = Gate("RX", 0, arg_value= +np.pi/2)
rg_py2 = Gate("RY", 0, arg_value= +np.pi/2)
rg_nx2 = Gate("RX", 0, arg_value= -np.pi/2)
rg_ny2 = Gate("RY", 0, arg_value= -np.pi/2)

## Decompose
## Pi
g_z = [rg_y,rg_x]
## Pi/2
g_phz = [rg_nx2,rg_py2,rg_px2]
g_nhz = [rg_nx2,rg_ny2,rg_px2]
## Had
g_hpxz = [rg_x,rg_ny2]
g_hnxz = [rg_x,rg_py2]
g_hpyz = [rg_y,rg_px2]
g_hnyz = [rg_y,rg_nx2]
g_hpxy = [rg_px2,rg_py2,rg_px2]
g_hnxy = [rg_nx2,rg_py2,rg_nx2]
## 2pi/3 
g_pc1 = [rg_py2,rg_px2]
g_pc2 = [rg_py2,rg_nx2]
g_pc4 = [rg_ny2,rg_px2]
g_pc3 = [rg_ny2,rg_nx2]

g_nc1 = [rg_nx2,rg_py2]
g_nc2 = [rg_px2,rg_py2]
g_nc4 = [rg_nx2,rg_ny2]
g_nc3 = [rg_px2,rg_ny2]





gates_set = [
    [rg_i],[rg_x],[rg_y],[rg_px2],[rg_nx2],[rg_py2],[rg_ny2],
    ## Pi
    g_z,
    ## Pi/2
    g_phz,g_nhz,
    ## Had
    g_hpxz,g_hnxz,g_hpyz,g_hnyz,g_hpxy,g_hnxy,
    ## 2pi/3 
    g_pc1,g_pc2,g_pc4,g_pc3,
    g_nc1,g_nc2,g_nc4,g_nc3
]

gate_set_num = len(gates_set)



def decomposition( gates:List[Gate] )->Qobj:
    """
        
    Args:
        List : A list of qutip Gate object (qutip_qip.circuit.Gate). 
    
    Returns:
        Qobj (qutip.Qobj): An .
    """
    circuit = QubitCircuit(1)
    eff_op = qeye(2)
    name_seq = []
    for g in gates:
        circuit.add_gate(g)
        name_seq.append(g.name)
        g_qobj = g.get_compact_qobj()
        eff_op = g_qobj *eff_op
        # eff_op = circuit.run(qeye(2))
    return eff_op

def get_random_gateSeq( num_gates ):
    
    circuit = QubitCircuit(1)
    single_qubit = basis(2)
    total_op = qeye(2)
    for ind in np.random.randint(0, gate_set_num, num_gates):
        random_gate = gates_set[ind]
        eff_op = decomposition(random_gate)
        for g in random_gate:
            circuit.add_gate(g)
        #print(random_gate.name, random_gate.arg_value/np.pi)
        #print( eff_op )
        single_qubit = eff_op*single_qubit
        total_op = eff_op*total_op
            #print( total_op )
    return circuit.gates

def find_inv_gate( gates:List[Gate] ):
    """get inversed gate from input gates in clifford group.    
    Args:
        gates: list  A list of (qutip_qip.circuit.Gate) gate.
    
    Returns:
        list : A list of (qutip_qip.circuit.Gate) gate.
    """
    operation_eff = decomposition(gates)
    gate_inv = None
    for gate in gates_set:
        rev_op = operation_eff.inv()
        compared_op = decomposition(gate)
        for g_phase in [1,1j,-1,-1j]:
            if g_phase*rev_op == compared_op:
                gate_inv = gate
    return gate_inv

def find_inv_gate_state( state:List[Gate] ):
    """get inversed gate from input gates in clifford group.    
    Args:
        gates: list  A list of (qutip_qip.circuit.Gate) gate.
    
    Returns:
        list : A list of (qutip_qip.circuit.Gate) gate.
    """
    gate_inv = None
    for gate in gates_set:
        compared_op = decomposition(gate)
        final_state = compared_op*state
        if abs(abs(final_state[0][0][0])-1)<0.01:
            gate_inv = gate
    return gate_inv


def get_RBseq_envelope( dt, pulse:Pulse, num_gates ):
    myprocessor = ModelProcessor(model=MyModel(1))
    myprocessor.native_gates = ["RX","RY"]
    mycompiler = MyCompiler(1, args={"num_samples": 20,"pulse":pulse, "dt":dt})

    circuit_RB = QubitCircuit(1)
    circuit_RB.add_gates( get_random_gateSeq( num_gates ) )

    inv_gate = find_inv_gate(circuit_RB.gates)

    circuit_RB.add_gates(inv_gate)
    tlist, coeffs = myprocessor.load_circuit(circuit_RB, compiler=mycompiler)
    envelope = coeffs["sx0"]+1j*coeffs["sy0"]
    return tlist["sx0"], envelope

def test_1():
    myprocessor = ModelProcessor(model=MyModel(1))
    myprocessor.native_gates = ["RX","RY"]
    mycompiler = MyCompiler(1, args={"num_samples": 20})

    init_qubit = basis(2)
    circuit_RB = QubitCircuit(1)
    circuit_RB.add_gates( get_random_gateSeq( 10 ) )
    tlist_RB, coeffs_RB = myprocessor.load_circuit(circuit_RB, compiler=mycompiler)
    final_qubit = decomposition(circuit_RB.gates)*init_qubit
    print( "pulse length", len(circuit_RB.gates))
    print(decomposition(circuit_RB.gates), "RB seq---------------")

    print( final_qubit[0][0], "ground state before inverse---------------")

    inv_gate = find_inv_gate(circuit_RB.gates)
    #inv_gate = find_inv_gate_state(final_qubit)
    #print(inv_gate[0].get_compact_qobj()*decomposition(circuit_RB.gates), "total operation---------------")
    final_qubit = decomposition(inv_gate) *final_qubit
    print( final_qubit[0][0], "ground state")

    circuit_inv = QubitCircuit(1)
    circuit_inv.add_gates(inv_gate)
    tlist_inv, coeffs_inv = myprocessor.load_circuit(circuit_inv, compiler=mycompiler)
    plt.plot(tlist_RB["sx0"],coeffs_RB["sx0"],label="sx0")
    plt.plot(tlist_RB["sy0"],coeffs_RB["sy0"],label="sy0")
    plt.plot(tlist_RB["sx0"][-1]+tlist_inv["sx0"],coeffs_inv["sx0"],label="sx0")
    plt.plot(tlist_RB["sy0"][-1]+tlist_inv["sy0"],coeffs_inv["sy0"],label="sy0")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    from pulse_generator.pulse import get_Pulse_DRAG, convert_envtoIQ
    native_gate_pulse = get_Pulse_DRAG(20,(1,5,10,1),0,0)

    tlist, envelope = get_RBseq_envelope(1, native_gate_pulse, 10)

    fig, ax = plt.subplots(3,1,sharex=True)
    ax[0].plot(tlist,envelope.real,label="sx0")
    ax[0].plot(tlist,envelope.imag,label="sy0")

    sig_I, sig_Q = convert_envtoIQ(envelope, 0.079)
    
    ax[1].plot(tlist,sig_I,label="sig_I")
    ax[1].plot(tlist,sig_Q,label="sy0")
    plt.legend()
    plt.show()




