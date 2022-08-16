from qpu.backend.channel.physical_channel import PhysicalChannel, UpConversionChannel, DACChannel


def channel_from_dict( channel:dict ):
    channel_type = channel["type"]
    channel_id = channel["id"]
    if channel_type == "upconversion":    
        PChObj = UpConversionChannel(channel_id)
        DAC_id_IQ = channel["devices"]["DAC"]
        if len(DAC_id_IQ) == 2:
            PChObj.DAC_id_IQ = DAC_id_IQ
    elif channel_type == "dir_output":    
        PChObj = DACChannel(channel_id)
        PChObj.DAC_id = channel["devices"]["DAC"]
    else:
        PChObj = PhysicalChannel(channel_id)
    print("api",PChObj.id,type(PChObj))
    PChObj.port = channel["port"]
    return PChObj