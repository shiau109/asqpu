from qpu.backend.phychannel.physical_channel import PhysicalChannel, UpConversionChannel, DACChannel


def from_dict( channel:dict )->PhysicalChannel:
    category = channel["type"]
    name = channel["id"]
    if category == "upconversion":    
        PChObj = UpConversionChannel(name)
        DAC_id_IQ = channel["devices"]["DAC"]
        if len(DAC_id_IQ) == 2:
            PChObj.DAC_id_IQ = DAC_id_IQ
    elif category == "dir_output":    
        PChObj = DACChannel(name)
        PChObj.DAC_id = channel["devices"]["DAC"]
    else:
        print("channel category not defined")
        return None
    print("api",PChObj.name,type(PChObj))
    PChObj.port = channel["port"]
    return PChObj