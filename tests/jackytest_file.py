from cProfile import label
from qpu.backend.circuit.api import base_circuit_from_str
from qpu.backend.circuit.circuit_builder import CircuitBuilder
from physics_model.complex_system import SingleReadableTransmon
import matplotlib.pyplot as plt
from pandas import DataFrame

from numpy import pi

import ast


fo = open("./tests/specification.txt", "r")
spec = fo.read()
fo.close()

cirBuilder = CircuitBuilder( base_circuit_from_str(spec) )

cirBuilder.add_element( "q1", "rxy", [pi,0] )
cirBuilder.add_element( "q2", "rxy", [pi,0] )
cirBuilder.add_element( "q2", "rxy", [pi,0] )
cirBuilder.add_element( "q2", "rxy", [pi,pi/2] )
cirBuilder.add_element( "q1", "rxy", [pi/2,0] )
cirBuilder.add_element( "q1", "rz", [pi/2] )
cirBuilder.add_element( "q2", "rz", [pi] )

channel_output = cirBuilder.to_waveform_channel(0.001)

fig, ax = plt.subplots(2,1,sharex=True)

for chid in channel_output.keys():
    ax[0].plot(channel_output[chid].get_xAxis(),channel_output[chid].Y,label=chid)
ax[0].legend()

dac_output = cirBuilder.to_waveform_dac()

for dac_id in dac_output.keys():
    ax[1].plot(dac_output[dac_id].get_xAxis(),dac_output[dac_id].Y,label=dac_id)
ax[1].legend()

plt.show()