from abc import ABCMeta, abstractproperty 
#import SDAWG as mySDAWG


class VDevice_abc( metaclass=ABCMeta ):
    """ Abstract class for create new class with specific function."""
    @property
    def id ( self ):
        """ The id of the instrument. """
        return self._id
    @id.setter
    def id ( self, value:str ):
        self._id = value

    @property
    @abstractproperty
    def func_type( self )->str:
        """ The function type of the instrument. """
        return ""

    def __eq__( self, other ):
        if (isinstance(other, VDevice_abc)):
            return self.id == other.id
        if isinstance(other, str):
            return self.id == other
        return False

        
    def initialize ( self ):
        """Initalize the instrument."""
        return
    
