from qpu.backend.instruments.Mixer import DummyIQMixer
from qpu.backend.instruments.DAC import DummyDAC
from qpu.backend.instruments.vir_device import VDevice_abc

def device_from_dict( device:dict )->VDevice_abc:
    device_type = device["type"] 
    device_id = device["id"]
    print(device)
    ##TODO check driver        
    if device_type == "DAC":
        deviceObj = []
        for i in range(device["sub_channel"]):
            deviceObj.append(DummyDAC(f"{device_id}-{i+1}")) 
        return deviceObj

    if device_type == "Mixer":
        deviceObj = [DummyIQMixer(device_id)]
        return deviceObj
