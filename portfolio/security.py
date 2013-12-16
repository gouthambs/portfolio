
class Security(object):
    
    def __init__(self,security_type=None):
        # reference data as a dictionary
        self.refdata    = {"security_type":security_type}   
        
    
        

class Stock(Security):
    _dataprovider = None
    def __init__(self,symbol,benchmark="^GSPC"):
        super(Stock,self).__init__(security_type="stock")
        self.refdata["identifier"]  = symbol 
        self._benchmark             = benchmark        
    
    @classmethod
    def set_data_provider(cls,data_provider):
        """
        This method can be used to implement
        """
        cls._dataprovider = data_provider




