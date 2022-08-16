from qpu.backend.component.q_component import QComponent
from qpu.backend.channel.physical_channel import PhysicalChannel
from qpu.backend.actions.basic_action import PhysicalAction
from qpu.backend.instruments.vir_device import VDevice_abc

from pandas import DataFrame
import abc
from typing import List, Tuple

from numpy import logical_and

class PhysicalCircuit():
    """
    紀錄元件specification與使用的channel
    """
    def __init__( self ):
        self._qubits = []
        self._channels = []
        self._actions = []        
        self._devices = []        

    def register_qubit( self, qubit:QComponent ):
        """
        
        Args:
            qubit: the type should be "PhysicalQubit"
        """
        if isinstance(qubit,QComponent):
           self._qubits.append(qubit)
        else:
            raise TypeError()

    def get_IDs_qubits( self )->str:
        idList = []
        for q in self.qubits:
            idList.append(q.id)
        return idList


    def get_qubit( self, id:str )->QComponent:
        """
        Get qubit by its ID.
        """
        for q in self.qubits:
            if q == id:
                return q
        return None


    def register_channel( self, channel:PhysicalChannel ):
        """
        
        Args:
            channel: the type should be "PhysicalChannel"
        """
        if isinstance(channel,PhysicalChannel):
           self._channels.append(channel)
        else:
            raise TypeError()

    def get_IDs_channel( self )->str:
        idList = []
        for ch in self.channels:
            idList.append(ch.id)
        return idList



    def get_channel( self, id:str )->PhysicalChannel:
        """
        Get channel by its ID.
        """
        for ch in self.channels:
            if ch == id:
                return ch
        return None


    def register_device( self, device:VDevice_abc ):
        """
        
        Args:
            device: the type should be "VDevice_abc"
        """
        if isinstance(device,VDevice_abc):
           self._devices.append(device)
        else:
            raise TypeError()
            
    def get_device( self, id:str )->VDevice_abc:
        """
        Get device by its ID.
        """
        for d in self.devices:
            if d == id:
                return d
    def get_deviceByType( self, type:str=None )->List[VDevice_abc]:
        """
        Get devices by type, default is all.
        """
        d_list = []
        for channel in self.channels:
            for device in channel.devices:
                if type == None:
                    d_list.append(device)
                elif type == device.func_type:
                    d_list.append(device)
        return d_list

    def get_IDs_devices( self, type:str=None )->List[str]:
        """
        Get devices id by type, default is all.
        """
        id_list = []
        for device in self.devices:
            if type == None:
                id_list.append(device.id)
            elif type == device.func_type:
                id_list.append(device.id)
        return id_list

    def get_channel_qPort( self, q_id:str, port:str )->PhysicalChannel:
        """
        Get channel by q_component id and port.
        """
        myfilter = self.qc_relation["q_id"]==q_id

        q_id_channels = self.qc_relation["channel_id"].loc[myfilter].to_list()
        related_channel_id = None
        for channel_id in q_id_channels:
            channel = self._get_channel_id(channel_id)
            if channel.port == port:
                related_channel_id = channel_id
        return self._get_channel_id(related_channel_id)

    def get_port( self, action_id:str )->str:
        """ Get port of the action used."""
        myfilter = self.qa_relation["action"] == action_id 
        port_type = self.qa_relation["port_type"].loc[myfilter].to_list()[0]

        return port_type
    def _get_channel_id( self, id:str )->PhysicalChannel:
        """
        Get channel by its ID.
        """
        for ch in self.channels:
            if ch == id:
                return ch
        return None

    def register_action( self, action:PhysicalAction ):
        """
        
        Args:
            action: the type should be "PhysicalAction"
        """
        if isinstance(action,PhysicalAction):
           self._actions.append(action)
        else:
            raise TypeError()

    def get_action( self, id:str )->PhysicalAction:
        """
        Get action by its ID.
        """
        for action in self.actions:
            if action == id:
                return action
        return None

    def get_IDs_actions( self )->str:
        idList = []
        for action in self.actions:
            idList.append(action.id)
        return idList



    @property
    def qubits( self )->List[QComponent]:
        return self._qubits
    @qubits.setter
    def qubits( self, value:List[QComponent]):
        self._qubits = value

    @property
    def devices( self )->List[VDevice_abc]:
        return self._devices
    @devices.setter
    def devices( self, value:List[VDevice_abc]):
        self._devices = value

    @property
    def channels( self )->List[PhysicalChannel]:
        return self._channels
    @channels.setter
    def channels( self, value:List[PhysicalChannel]):
        self._channels = value

    @property
    def actions( self )->List[PhysicalAction]:
        return self._actions
    @actions.setter
    def actions( self, value:List[PhysicalAction]):
        self._actions = value

    @property
    def qc_relation( self )->DataFrame:
        return self._qc_relation
    @qc_relation.setter
    def qc_relation( self, value:DataFrame):
        self._qc_relation = value

    @property
    def qa_relation( self )->DataFrame:
        return self._qa_relation
    @qa_relation.setter
    def qa_relation( self, value:DataFrame):
        self._qa_relation = value




