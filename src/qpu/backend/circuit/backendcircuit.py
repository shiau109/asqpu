from qpu.backend.component.q_component import QComponent
from qpu.backend.phychannel.physical_channel import PhysicalChannel
from qpu.backend.action.basic_action import PhysicalAction
from qpu.backend import phychannel
from pandas import DataFrame
import abc
from typing import List, Tuple, Union, Dict

from numpy import array, logical_and



def xy_control( coeffs_map, target_index ):
    sx_exist = False
    sy_exist = False
    for label in coeffs_map.keys():
        label_index = int(label[2:])
        label_action = label[:2]
        if label_index == target_index:
            match label_action:
                    case "sx":
                        sx_exist = True
                        sx_coeff = array(coeffs_map[label])
                    case "sy": 
                        sy_exist = True
                        sy_coeff = array(coeffs_map[label])
                    case _: pass
    if sx_exist and sy_exist:
        rf_envelop = sx_coeff +1j*sy_coeff
        return rf_envelop



class BackendCircuit():
    """
    紀錄元件specification與使用的channel
    """
    def __init__( self ):
        self._qComps = []
        self._channels = []
        self._actions = []        
        self._devices = []
        
        self.q_reg = None      

    def register_qComp( self, qcomp:QComponent ):
        """
        
        Args:
            qcomp: Quantum component
        """
        if isinstance(qcomp,QComponent):
           self._qComps.append(qcomp)
        else:
            raise TypeError()

    def get_IDs_qComps( self )->List[str]:
        idList = []
        for q in self._qComps:
            idList.append(q.id)
        return idList


    def get_qComp( self, name:str )->QComponent:
        """
        Get Quantum component by its ID.
        """
        for q in self._qComps:
            if q == name:
                return q
        return None


    def register_channel( self, info:Dict ):
        """
        
        Args:
            channel: the type should be "PhysicalChannel"
        """
        # if isinstance(info,PhysicalChannel):
        #    self._channels.append(info)
        if isinstance(info,Dict):
           new_channel = phychannel.from_dict(info)
           self._channels.append(new_channel)
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

    def get_devicesCMD( self )->dict:
        idList = []
        for action in self.actions:
            idList.append(action.id)
        return idList

    
    def load_coeff( self, coeffs_map:dict ):

        dac_output = {}
        
        for qi, qname in enumerate(self.q_reg["qubit"]):
            print(qname)
            phyCh = self.get_channel_qPort(qname,"xy")
            if phyCh != None:
                print(phyCh)
                envelope = xy_control(coeffs_map, qi)
                dac_output[phyCh.name] = phyCh.dac_output(envelope, 0.08)
        return dac_output


    # def to_instrPara():

    #     pass
    #     return





    @property
    def qubits( self )->List[QComponent]:
        return self._qubits
    @qubits.setter
    def qubits( self, value:List[QComponent]):
        self._qubits = value

    # @property
    # def devices( self )->List[VDevice_abc]:
    #     return self._devices
    # @devices.setter
    # def devices( self, value:List[VDevice_abc]):
    #     self._devices = value

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




    # def register_device( self, device ):
    #     """
        
    #     Args:
    #         device: the type should be "VDevice_abc"
    #     """
    #     if isinstance(device,VDevice_abc):
    #        self._devices.append(device)
    #     else:
    #         raise TypeError()
            
    # def get_device( self, id:str )->VDevice_abc:
    #     """
    #     Get device by its ID.
    #     """
    #     for d in self.devices:
    #         if d == id:
    #             return d
    # def get_deviceByType( self, type:str=None )->List[VDevice_abc]:
    #     """
    #     Get devices by type, default is all.
    #     """
    #     d_list = []
    #     for channel in self.channels:
    #         for device in channel.devices:
    #             if type == None:
    #                 d_list.append(device)
    #             elif type == device.func_type:
    #                 d_list.append(device)
    #     return d_list

    # def get_IDs_devices( self, type:str=None )->List[str]:
    #     """
    #     Get devices id by type, default is all.
    #     """
    #     id_list = []
    #     for device in self.devices:
    #         if type == None:
    #             id_list.append(device.id)
    #         elif type == device.func_type:
    #             id_list.append(device.id)
    #     return id_list



