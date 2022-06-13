from physics_model.complex_system import SingleReadableTransmon
from qpu.backend.instruments.vir_device import VDevice_abc
from typing import List
from pulse_generator.pulse import Pulse, Waveform
from qpu.backend.instruments.DAC import DAC_abc

class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    deviceTypes = ["DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"]
    

    def __init__( self, id:str ):
        self.id = id
        self.devices = []
        self.port = None
        self.pulse_sequence = []
        self._idle_value = 0

    def __contains__( self )->str:
        return self.id

    def __eq__( self, other )->str:
        if isinstance(other, PhysicalChannel):
            return self.id == other.id
        if isinstance(other, str):
            return self.id == other
        return False
        
    @property
    def devices( self )->List[VDevice_abc]:
        """
        A list include devices that this channel used.
        """
        return self._devices
    @devices.setter
    def devices( self, value:List[VDevice_abc] ):
        self._devices = value

    @property
    def pulse_sequence( self )->List[Pulse]:
        """
        The output pulse sequence of this channel.
        """
        return self._pulse_sequence
    @pulse_sequence.setter
    def pulse_sequence( self, value:List[Pulse] ):
        self._pulse_sequence = value

    @property
    def idle_value( self )->float:
        """
        The default output value of this channel.
        """
        return self._idle_value
    @idle_value.setter
    def idle_value( self, value:float ):
        self._idle_value = value


    def register_device( self, device:VDevice_abc ):
        """
        Register the devise 'deviceIDs' with type 'deviceType' in to this physicalChannel\n
        'deviceType' arg = "DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"
        """
        #print(f"Add devices {deviceIDs} with type {deviceType} to physical channel {self.id}.")
        if isinstance(device, VDevice_abc):
            if device not in self.devices:
                self.devices.append(device)
                #print(f"Device {device.id} is added successfully.")
            else:
                print(f"Device {device.id} is already registered.")
        else: 
            print(f"Can't recognize instr.")
    
    def get_devicesID( self, deviceTypes:str=None )->str:
        IDList = []
        for d in self.devices:
            if deviceTypes == None or d.func_type == deviceTypes:
                IDList.append(d.id)
        return IDList
    
    
    def get_dt( self ):
        dt = []
        for d in self.devices:
            if isinstance(d, DAC_abc):
                dt.append(d.get_TimeResolution())
        if dt.count(dt[0]) == len(dt):
            return dt[0]
        else:
            raise ValueError("dt are not the same.")

    def to_waveform_channel( self, dt:float )->Waveform:
        new_waveform = Waveform( 0, dt )
        for p in self.pulse_sequence:
            new_t0 = dt*new_waveform.Y.shape[-1]
            new_waveform.append( p.generate_signal( new_t0, dt ))

        return new_waveform

class DACChannel( PhysicalChannel ):
    def __init__( self, id:str ):
        super().__init__( id )
        self.DAC_id = None


    def to_waveform_dac( self, dt:float=None )->dict:
        if dt == None:
            dt = self.get_dt()
        dac_waveform = {}
        new_waveform = Waveform( 0, dt )
        for p in self.pulse_sequence:
            new_t0 = dt*new_waveform.Y.shape[-1]
            appended_waveform = p.generate_signal( new_t0, dt )
            new_waveform.append( appended_waveform )

        dac_id = self.DAC_id[0]
        dac_waveform[dac_id] = new_waveform
        return dac_waveform

class UpConversionChannel( PhysicalChannel ):
    def __init__( self, id:str ):
        super().__init__( id )
        self.DAC_id_IQ = None
    
    def to_waveform_dac( self, dt:float=None )->dict:
        if dt == None:
            dt = self.get_dt()
        dac_waveform = {}
        new_waveform_I = Waveform( 0, dt )
        new_waveform_Q = Waveform( 0, dt )

        for p in self.pulse_sequence:
            new_t0 = dt*new_waveform_I.Y.shape[-1]
            appended_I, appended_Q = p.generate_IQSignal( new_t0, dt, 0.089 )
            new_waveform_I.append( appended_I )
            new_waveform_Q.append( appended_Q )

        dac_id_I = self.DAC_id_IQ[0]
        dac_id_Q = self.DAC_id_IQ[1]
        dac_waveform[dac_id_I] = new_waveform_I
        dac_waveform[dac_id_Q] = new_waveform_Q
        return dac_waveform

class DownConversionChannel( PhysicalChannel ):
    def __init__( id:str ):
        super().__init__( id )

    def get_dt( self ):
        dt = []
        for d in self.devices:
            if isinstance(d, DAC_abc):
                dt.append(d.get_TimeResolution())
        if dt.count(dt[0]) == len(dt):
            return dt[0]
        else:
            raise ValueError("dt are not the same.")
