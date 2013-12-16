

# Portfolio class.
class Portfolio(object):
    '''
    The base portfolio class. This can be used to accumulate a bunch of
    securities and analyse them.
    '''
    def __init__(self): 
        self._securities = []
    
    def add_security(self,security):
        self._securities.append(security)
    
  
class BuyHoldPortfolio(Portfolio):
    def __init__(self):pass
    
 