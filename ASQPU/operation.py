from pulse_generator.pulse import Pulse, Waveform
from physicalChannel import PhysicalChannel
from typing import List

class Operation():
    """
    Store the name of the operation and pulses to form it. 
    """

    def __init__ ( self ):
        self._name = None
        self._t0 = 0
        self._pulse = None
        self._waveform = None
        self._physicalChannel = None
    @property
    def name ( self )->str:
        """ The name of the operation"""
        return self._name
    @name.setter
    def name ( self, value:str ):
        self._name = value



class OperationLib ():

    def __init__ ( self ):

        self.physicalChannels = [] # All Used channel
        self._operationList = []
        

    def get_OperationsName ( self )->List[str]:    
        nameList = []
        for op in self.operationList:
            nameList.append(op.name)
        return nameList

    def isExist_Operaion ( self, name:str )->bool:
        return name in self.get_OperationsName()
        
    def add_operation ( self, operation:Operation ):
        nameList = self.get_OperationsName()
        if operation.name not in nameList:
            self._operationList.append( operation )



    def get_operation ( self, name:str )->Operation:
        """ Get operation by name"""
        nameList = self.get_OperationsName()
        operation_idx = nameList.index(name)
        return self._operationList[operation_idx]

def create_operation ( name:str, phyCh:list, pulse:List[Pulse] ):
    """
    phyCh: physicalChannels
    """
    if len(phyCh) == len(pulse):
        newOp = Operation()
        newOp.name = name
        newOp.physicalChannels = phyCh
        newOp.pulse = pulse
    return newOp