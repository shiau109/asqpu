from math import e
import qpu.backend.channel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
import numpy as np
import qpu.application as qapp

import qpu.backend.circuit 
import pulse_signal.common_Mathfunc as ps 
import qpu.backend.circuit.compiler as becc
import sys
sys.path.append("..")
from BECircuit_fromTestFile import get_test_bec
import matplotlib.pyplot as plt



mybec = get_test_bec()

for i in range(2):
    d_setting = qapp.get_SQRB_device_setting( mybec, 5  )


    #print(mybec.load_coeff(coeffs))


    dac_wf = d_setting["DAC"]
    print(d_setting)
    for dcategory in d_setting.keys():
        print(dcategory, d_setting[dcategory].keys())
    # Plot setting
    fig, ax = plt.subplots(1,1,sharex=True)

    # Compare signal and envelope
    for dacname in dac_wf.keys():
        if type(dac_wf[dacname]) != type(None):
            ax.plot( dac_wf[dacname], label=dacname )
    ax.legend()

    plt.show()

