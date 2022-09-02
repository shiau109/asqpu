from physics_model.complex_system import SingleReadableTransmon
from typing import List, Tuple
import sys
from pulse_signal.digital_mixer import upConversion_IQ
from pulse_signal.waveform import Waveform
from abc import ABC, abstractproperty, abstractmethod
from numpy import ndarray

class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    #deviceTypes = ["DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"]
    

    def __init__( self, name:str ):
        self.name = name
        self.devices = {}
        self.port = None
        #self.pulse_sequence = []
        self._idle_value = 0

    def __contains__( self )->str:
        return self.name

    def __eq__( self, other )->str:
        if isinstance(other, PhysicalChannel):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False
        
    # @property
    # def devices( self )->List[VDevice_abc]:
    #     """
    #     A list include devices that this channel used.
    #     """
    #     return self._devices
    # @devices.setter
    # def devices( self, value:List[VDevice_abc] ):
    #     self._devices = value

    # @property
    # def pulse_sequence( self )->List[Pulse]:
    #     """
    #     The output pulse sequence of this channel.
    #     """
    #     return self._pulse_sequence
    # @pulse_sequence.setter
    # def pulse_sequence( self, value:List[Pulse] ):
    #     self._pulse_sequence = value

    # @property
    # def idle_value( self )->float:
    #     """
    #     The default output value of this channel.
    #     """
    #     return self._idle_value
    # @idle_value.setter
    # def idle_value( self, value:float ):
    #     self._idle_value = value


    def register_device( self, virdtype:str, name:str ):
        """
        Register the device 'name' with virtual device type 'virdtype' in to this physicalChannel\n
        """
        if name not in self.devices[virdtype]:
            self.devices[virdtype].append(name)
        else:
            print(f"Device '{name}' is already registered.")

    
    # def get_devicesID( self, virdtype:str=None )->str:
    #     """
    #     Find the device name
    #     """
    #     IDList = []
    #     for f_type in self.devices.keys():
    #         for d in self.devices[f_type]:
    #             if deviceTypes == None or d.func_type == deviceTypes:
    #                 IDList.append(d.id)
    #         return IDList
    
    
    # def get_dt( self ):
    #     dt = []
    #     for d in self.devices["DAC"]:
    #         if isinstance(d, DAC_abc):
    #             dt.append(d.get_TimeResolution())
    #     if dt.count(dt[0]) == len(dt):
    #         return dt[0]
    #     else:
    #         raise ValueError("dt are not the same.")

    # def to_waveform_channel( self, dt:float )->Waveform:
    #     new_waveform = Waveform( 0, dt )
    #     for p in self.pulse_sequence:
    #         new_t0 = dt*new_waveform.Y.shape[-1]
    #         new_waveform.append( p.generate_signal( new_t0, dt ))

    #     return new_waveform

class WaveformChannel( ABC, PhysicalChannel ):
    def __init__( self, name:str, dt:float=1. ):
        super().__init__( name )
        # self.devices = {
        #     "DAC":[]
        # }
        self.dt = dt

    @abstractmethod
    def dac_output( self, dt:float=None )->dict:
        pass
         

class DACChannel( WaveformChannel ):
    def __init__( self, name:str, dt:float=1. ):
        super().__init__( name )
        # self.devices = {
        #     "DAC":[]
        # }
        self.dt = dt

    def dac_output( self, signal:ndarray, dt:float=None )->dict:
        if dt == None:
            dt = self.dt
        signal = {}
        new_waveform = Waveform( 0, dt, signal )

        dac_id = self.devices["DAC"][0]
        signal[dac_id] = new_waveform
        return signal

class UpConversionChannel( WaveformChannel ):
    def __init__( self, id:str ):
        super().__init__( id )
        # self.devices = {
        #     "DAC":[],
        #     "ADC":[],
        #     "SG":[],
        #     "IQMixer":[]
        # }
    def dac_output( self, signalRF:ndarray, dt:float=None, freqIF:float=None, IQMixer:Tuple=None )->dict:
        if dt == None:
            dt = self.dt
        signalIQ = {}

        signal_I, signal_Q = upConversion_IQ( signalRF, dt, freqIF, IQMixer )


        dac_id_I = self.devices["DAC"][0]
        dac_id_Q = self.devices["DAC"][1]
        signalIQ[dac_id_I] = signal_I
        signalIQ[dac_id_Q] = signal_Q
        return signalIQ


# class DownConversionChannel( PhysicalChannel ):
#     def __init__( id:str ):
#         super().__init__( id )

#     def get_dt( self ):
#         dt = []
#         for d in self.devices:
#             if isinstance(d, DAC_abc):
#                 dt.append(d.get_TimeResolution())
#         if dt.count(dt[0]) == len(dt):
#             return dt[0]
#         else:
#             raise ValueError("dt are not the same.")
