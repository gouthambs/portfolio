# -*- coding: utf-8 -*-
import numpy as np
from common import PortfolioError
import utils as qpu

class Engine(object):
    """
    Engine base class.
    """
    def __init__(self) : 
        pass
    
    def handle(self):
        pass
    
class TimeSeriesCalculationEngine(Engine):
    """ 
    Time series calculation engine is used for time series calculation
    analytics.
    """
    def __init__(self,security):
        self._security  = security
        self.reportdata = {"Identifier":security.refdata["identifier"]}
        self.dt         = 1./12.
    def _ts_calcs(self,df):
        df  = df.dropna()
        adj_stock_returns   = df["AdjReturns"].values
        adj_bnch_returns    = df["bnch_ret"].values
        if len(adj_stock_returns) == len(adj_bnch_returns):        
            covmat = np.cov(adj_stock_returns,adj_bnch_returns)
            beta    = covmat[0,1]/covmat[1,1] # OLS estimation
            st_mean = np.mean(adj_stock_returns)
            bn_mean = np.mean(adj_bnch_returns)
            alpha   = st_mean - beta*bn_mean
            sd      = np.std(adj_stock_returns)*np.sqrt(12)
            sharpe  = st_mean/sd
            lst12rt = 1+df["Returns"].tail(12).values
            mmntm   = 100.*(np.prod(lst12rt) - 1.) if len(lst12rt) == 12 \
                        else float('nan')
            self.reportdata["Alpha"]    = alpha*12*100 # annualized here
            self.reportdata["Beta"]     = beta
            self.reportdata["SharpeRatio"]  = sharpe*12
            self.reportdata["Volatility"]   = sd*100
            self.reportdata["Momentum"]     = mmntm
            
            #self.reportdata["alpha"] = 
        else:
            raise PortfolioError("Mismatch in the length of the return of stock and benchmark")
    def calculate(self,date):
        df  = self._fetch_returns(date)
        self._ts_calcs(df)
        return self.reportdata
        
    def _fetch_returns(self,date):
        dp          = self._security.__class__._dataprovider
        enddate     = qpu.shift_months(date,-1)
        enddate     = qpu.get_month_end(enddate)
        strtdate    = qpu.shift_years(enddate,-5)
        strtdate    = qpu.get_month_beg(strtdate)
        ticker      = self._security.refdata["identifier"]
        st_ret      = dp.get_total_returns(ticker,strtdate,enddate)
        # TODO : cache benchmark returns
        rf_rate     = dp.get_riskfree_rate(strtdate,enddate)        
        bn_ret      = dp.get_total_returns(self._security._benchmark,strtdate,enddate)
        st_ret["bnch_ret"] = bn_ret["Returns"]-rf_rate["RFRate"]*self.dt/100.
        st_ret["AdjReturns"]  = st_ret["Returns"]-rf_rate["RFRate"]*self.dt/100.
        
        return st_ret
        