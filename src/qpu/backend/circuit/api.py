from qpu.backend.instruments.api import device_from_dict
from qpu.backend.channel.api import channel_from_dict
from qpu.backend.actions.api import action_from_dict

from qpu.backend.component.api import qComponent_from_dict
from qpu.backend.circuit.base_circuit import PhysicalCircuit
from pandas import DataFrame



def base_circuit_from_str( specification:str )->PhysicalCircuit:

    specification_list = specification.split("===")


    baseCir = PhysicalCircuit()
    q_component_list = eval(specification_list[2])
    for q in q_component_list:
        baseCir.register_qubit( qComponent_from_dict( q ) )

    device_list = eval(specification_list[4])
    for device in device_list:
        for deviceObj in device_from_dict(device):
            baseCir.register_device( deviceObj )



    channel_list = eval(specification_list[6])
    for ch_dict in channel_list:
        PChObj = channel_from_dict( ch_dict )
        for device_type in ch_dict["devices"].keys():
            devices = ch_dict["devices"][device_type]
            for devices_id in devices:
                if devices_id in baseCir.get_IDs_devices():
                    PChObj.register_device(baseCir.get_device(devices_id))
        PChObj.port = ch_dict["port"]
        baseCir.register_channel(PChObj)

    action_list = eval(specification_list[8])
    for a_dict in action_list:
        actionObj = action_from_dict(a_dict)
        baseCir.register_action(actionObj)

    qa_relation_dict = eval(specification_list[10])
    baseCir.qa_relation = DataFrame.from_dict(qa_relation_dict)


    qc_relation_dict = eval(specification_list[12])
    baseCir.qc_relation = DataFrame.from_dict(qc_relation_dict)
    return baseCir
