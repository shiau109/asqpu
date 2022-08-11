import numpy as np
from qpu.application.singleQ_CliffordRB import get_RB_pulseSeq
import matplotlib.pyplot as plt
from qpu.backend.circuit.api import base_circuit_from_str

fo = open("./tests/specification.txt", "r")
spec = fo.read()
fo.close()

# Input arg
qubit_id = "q1"
action_id = "rxy"
base_cir = base_circuit_from_str(spec)
port_type = "xy"

envelope, IQsignal = get_RB_pulseSeq(base_cir, qubit_id, action_id, port_type, 10)

tlist = np.array(range(len(envelope)))
fig, ax = plt.subplots(3,1,sharex=True)
ax[0].plot(tlist,envelope.real,label="sx0")
ax[0].plot(tlist,envelope.imag,label="sy0")

ax[1].plot(tlist,IQsignal.real,label="sig_I")
ax[1].plot(tlist,IQsignal.imag,label="sig_Q")
plt.legend()
plt.show()