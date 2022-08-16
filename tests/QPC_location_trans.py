import sys
sys.path.append(r"E:\Jacky\Github\ASQPU\src")
sys.path.append(r"E:\Jacky\Github\pulse_generator")

from cProfile import label
from qpu.backend.circuit.api import to_deviceManager

from numpy import pi


fo = open("./tests/specification_deviceOnly.txt", "r")
spec = fo.read()
fo.close()

QPU_dict = to_deviceManager(spec,["DAC","SG"])

print(QPU_dict)



