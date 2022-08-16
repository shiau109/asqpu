# import sys,os
# sys.path.append(os.path.realpath(r".\instruments"))
# print(sys.path[-2],sys.path[-1])
from abc import ABC, abstractmethod
from qpu.backend.instruments.vir_device import VDevice_abc


class DAC_abc( VDevice_abc, ABC ):
    """The abstract class as a template for all instrument with DAC function."""
    @abstractmethod
    def __init__( self, id ):
        self.id = id
    
    @abstractmethod
    def get_TimeResolution ( self ):
        """ Get the time resolution of the instrument."""
        return NotImplemented

    @property
    def func_type( self )->str:
        return "DAC"

    # @property
    # def dt( self ):
    #     return self._dt
    # @dt.setter
    # def dt( self ):
    #     self._dt

        
class DummyDAC( DAC_abc ):
    """The class is used to offline testing."""
    def __init__ ( self, id ):
        self.id = id
    def get_TimeResolution( self ):
        """Get fake time resolution, the value always 1."""
        return 1
    def initialize ( self ):
        """Do nothing"""
        pass
try:
    from .lib import SDAWG as mySDAWG
except ImportError:
    print(f"module SDAWG can't import")
class SDAWG( DAC_abc ):
    def __init__ ( self, id:str ):
        self.id = id
        self._module = mySDAWG.Initiate( id )
    @property
    def module ( self ):
        return self._module

    def initialize ( self ):
        self._module = mySDAWG.Initiate()

    def get_TimeResolution( self )->float:
        """Get time resolution from SDAWG"""
        dt = mySDAWG.clock(self.module)
        return dt


try:
    import lib.TKAWG as myTKAWG
except:
    print(f"module myTKAWG can't import")
class TKAWG( DAC_abc ):
    def __init__ ( self, id ):
        
        self.id = id
    @property
    def module ( self ):
        return self._bench
    @module.setter
    def module ( self, value ):
        self._bench = value
    def initialize ( self ):
        self._bench = myTKAWG.Initiate()
    def get_TimeResolution( self )->float:
        """Get time resolution from SDAWG"""
        dt = self._bench.clock()
        return dt


if __name__ == '__main__':
    a = DummyDAC("cc")
    print(a.id)
    print(a.get_TimeResolution())