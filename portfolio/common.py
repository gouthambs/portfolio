# -*- coding: utf-8 -*-



class PortfolioError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self,value):
        return repr(self.value)
