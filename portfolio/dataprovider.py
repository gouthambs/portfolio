from pandas.io.data import DataReader
import pandas as pd
import numpy as np
from common import PortfolioError

class ISecurityDataProvider(object):
    """
    The base security data provider interface.
    Things like security look up can go here.
    """
    def get_riskfree_rate(self,startdate,enddate,freq="M",maturity='1M'):
        raise PortfolioError("Method not implemented!")
        
        
class IStockDataProvider(ISecurityDataProvider):
    """
    The base Stock data provider interface.
    Things like returns, fundamental data, reference data go here.
    """
    def __init__(self): 
        pass
    
    def get_total_returns(self,identifier,startdate,enddate,freq='M'):
        """
        The function prototype for 
        """
        raise PortfolioError("Method not implemented!")
        


#class LimitedSizeDict(OrderedDict):
#  def __init__(self, *args, **kwds):
#    self.size_limit = kwds.pop("size_limit", None)
#    OrderedDict.__init__(self, *args, **kwds)
#    self._check_size_limit()

# def __setitem__(self, key, value):
#    OrderedDict.__setitem__(self, key, value)
#    self._check_size_limit()

#  def _check_size_limit(self):
#    if self.size_limit is not None:
#      while len(self) > self.size_limit:
#        self.popitem(last=False)
        
class StockDataProvider(IStockDataProvider):
    _cacheindxlist = set(["^GSPC","^NDX"])
    _cacheindxdata = {}
    _cacherfrate = None
    #RetCache(dict):
    #    def __missing__(self,key):
    #        self[key]
    #_cacheret   
    
    def __init__(self): pass
    
    def get_total_returns(self,identifier,startdate,enddate,freq='M'):
        """
        This function fetches the returns for the given ticker over a certain
        interval with a certain frequency
        Parameters
        ----------
        identifier  : string
                      the identifier or ticker that we need to fetch the 
        startdate   : datetime.date 
                      the start date for time series
        enddate     : datetime.date
                      end date for the time series
        freq        : char
                      'M' denotes monthly; if not, we get daily frequency
        """
        #ret = np.array([])
        grabdata = False
        ccheindx = True
        try:
            if identifier in self.__class__._cacheindxlist: # check if cached
                data = self.__class__._cacheindxdata.get(identifier)
                if data is None :
                    grabdata = True
                elif (startdate<data[0] or enddate>data[1]):
                    grabdata = True
            else:
                grabdata = True
                ccheindx = False
            if grabdata:
                data = DataReader(identifier, 'yahoo', startdate, enddate)
                if ccheindx: #if it should be cached
                    self.__class__._cacheindxdata[identifier] = \
                        (startdate,enddate,data)
            else:
                cacheval    = self.__class__._cacheindxdata[identifier]
                data        = cacheval[2]       
                    
                
            if freq=='M':
                dsmp = data[startdate:enddate].resample('M',how='last')
            else:
                dsmp = data[startdate:enddate]
            dsmp["Returns"] = dsmp["Adj Close"]/dsmp["Adj Close"].shift(1)-1
        except :
            raise PortfolioError("Cannot fetch stock total returns for "+identifier)
        return dsmp
        
    def get_riskfree_rate(self,startdate,enddate,freq="M",maturity='1M'):
        """
        Rates from FRED
        http://research.stlouisfed.org/fred2/categories/116
        """
        rfcache = self.__class__._cacherfrate
        grabdata = False
        if rfcache == None:
            grabdata = True
        elif rfcache[0]< startdate or rfcache[1] > enddate:
            grabdata = True
             
        if grabdata:
            dt          = DataReader('DTB4WK',"fred", startdate,enddate)
            dt.columns  = ['RFRate']
            dt.fillna(method='backfill',inplace=True)
            rfcache     = (startdate,enddate,dt)
            self.__class__._cacherfrate= rfcache
        else:
            dt          = rfcache[2]
        
        dsm     = dt[startdate:enddate].resample('M')
        return dsm
        
        
        
        
        