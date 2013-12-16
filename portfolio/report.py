# -*- coding: utf-8 -*-
from engine import TimeSeriesCalculationEngine
from common import PortfolioError
from pandas import DataFrame

class Report(object):
    """
    Base Report class for future extension
    """
    pass


class HoldingsReport(Report):
    def __init__(self, portfolio,reportdate):
        self.portfolio  = portfolio
        self.reportdate = reportdate
        self.report     = None
    
    def calculate(self):
        data=[self._engine_factory(sec).calculate(self.reportdate) for sec \
                in  self.portfolio._securities] 
        df = DataFrame(data)
        cols = ['Identifier','Beta','Alpha','SharpeRatio','Volatility',\
            'Momentum']        
        self.report = df[cols]
    def get_report(self):
        return self.report
        
    def _engine_factory(self,security):
        security_type = security.refdata["security_type"]
        eng_fact = {
            "stock": TimeSeriesCalculationEngine(security)
        
        }
        eng = eng_fact.get(security_type)
        if (eng==None):
            raise PortfolioError("HoldingsReport has unknown engine for \
                    security type %s"%security_type)
        return eng