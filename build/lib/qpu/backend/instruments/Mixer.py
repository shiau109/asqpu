
from abc import ABCMeta, abstractmethod
from qpu.backend.instruments.vir_device import VDevice_abc
from typing import Tuple

class IQMixer_abc ( VDevice_abc, metaclass=ABCMeta ):
    """The abstract class as a template for all instrument with Mixer function."""
    @abstractmethod
    def __init__( self, id ):
        self.id = id
    @abstractmethod
    def get_CalibrationParas ( self ):
        """ Get the calibration value for the IQ mixer."""
        return NotImplemented
    @abstractmethod
    def get_IFfreq ( self )->float:
        """ Get the IF frequency value for the IQ mixer."""
        return NotImplemented
    @property
    def IF_device ( self ):
        """ Get the 2 devices linking to this IQ mixer."""
        return self._IF_device
    @IF_device.setter
    def IF_device ( self, value:tuple ):
        """ 
        Get the 2 devices linking to this mixer.
        The value[0] for I, [1] for Q
        """
        self._IF_device = value

    @property
    def func_type( self ):
        """ This type need 2 DAC devices and 1 LO device."""
        return "IQMixer"

    @property
    def IFfreq( self )->float:
        """ IF freq."""
        return self._IFfreq
    @IFfreq.setter
    def IFfreq( self, value:float ):
        self._IFfreq = value

class DummyIQMixer ( IQMixer_abc ):
    """The class is used to offline testing."""
    def __init__ ( self, id ):
        self.id = id
        self.IFfreq = 0.079
    def get_CalibrationParas( self, value=(1,90,0,0) )->Tuple[float,float,float,float]:
        """Get fake calibration parameters, the value always (1,90,0,0)."""
        return value
    def get_IFfreq( self )->float:
        """Get IF freq."""
        return self.IFfreq



