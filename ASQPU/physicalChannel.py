from physics_model.coupling_system import SingleReadableTransmon
import abc


class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    deviceTypes = ["DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"]
    roles = ["Control","Readout"]

    def __init__( self, id ):
        self.id = id
        #self.role = role
        self.coupled = []
        self.device = {}

    def register_device( self, deviceIDs:str, deviceType:str ):
        """
        Register the devise 'deviceIDs' with type 'deviceType' in to this physicalChannel\n
        'deviceType' arg = "DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"
        """
        #print(f"Add devices {deviceIDs} with type {deviceType} to physical channel {self.id}.")
        if deviceType in PhysicalChannel.deviceTypes:
            if deviceType not in self.device.keys():
                self.device[deviceType]=[]
                print(f"Device type {deviceType} didn't exist, creating now.")

            for dID in deviceIDs:
                if dID not in self.device[deviceType]:
                    self.device[deviceType].append(dID)
                    #print(f"Device {dID} is added successfully.")
                else:
                    print(f"Device {dID} is already registered.")
        else: 
            print(f"Can't recognize device type {deviceType}.")

class ABInstr( metaclass=abc.ABCMeta ):
    """ Abstract class for create virtual instrument with specific function."""
    @property
    @abc.abstractmethod
    def id ( self ):
        """ The id of the instrument. """
        return self._id
    @id.setter
    @abc.abstractmethod
    def id ( self, value:str ):
        self._id = value
    
class DAC (ABInstr):
    def __init__( self, id ):
        self.id = id

class PhysicalSingleTransmon():
    """
    This class is used for record information of a Qubit-Cavity coupling system.
    """
    def __init__ ( self, qid:str ):

        self.id = qid
        self.phyChIDList = []
        self.operationLib = None
        self._sensitivity_flux = None
        self._sensitivity_RF = None
        self.transmonProperties = SingleReadableTransmon()
        self.T1 = None

    @property
    def sensitivity_flux ( self )->float:
        """Unit in magnetic flux quantum per mA"""
        return self._sensitivity_flux
    @sensitivity_flux.setter
    def sensitivity_flux ( self, value:float ):
        self._sensitivity_flux = value

    @property
    def sensitivity_RF ( self )->float:
        """Intergation of V(t) per pi pulse, unit in V/ns"""
        return self.sensitivity_RF
    @sensitivity_RF.setter
    def sensitivity_RF ( self, value:float ):
        self.sensitivity_RF = value
        
    def isExist_PhysicalChannel( self, channelID:str ):
        if channelID in self.phyChIDList:
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def register_PhysicalChannel( self, phyChDict ):
        for phyCh in phyChDict.keys():
            if not self.isExist_PhysicalChannel(phyCh):
                #print(f"Assign physical channel {phyCh} to Qubit {self.id} successfully.")
                self.phyChIDList.append(phyCh)
            else:
                print(f"Physical channel {phyCh} is already in Qubit {self.id}.")

    
    def set_intrinsicProperties( self, properties ):
        self.intrinsicProperties.update(properties)

    

    def set_operationCondition( self, paras:dict ):
        opcTemp = {
            "fluxBias": None,
            "qubit_frequency": None, #GHz
            "readout_frequency": None, #GHz
            "state_determination": None,
            "readout_pulse":None,
            "x_gate":None,
        }
        opcTemp.update(paras)
        self.operationCondition = opcTemp

if __name__ == '__main__':
    a = DAC("cc")
    print(a.id)