from qpu.backend.component.q_component import QComponent
from qpu.backend.component.qubit.transmon import Transmon


def qComponent_from_dict( info:dict )->QComponent:
    if info["type"] == "qubit":
        qubitObj = Transmon(info["id"])
        qubitObj.transition_freq = info["freq_xy"]
        qubitObj.sensitivity_RF = info["coupling_xy"]
    else:
        qubitObj = QComponent(info["id"])
    return qubitObj