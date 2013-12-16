# -*- coding: utf-8 -*-
"""
Created on Sat Dec 07 13:54:19 2013

@author: Goutham
"""

import portfolio as pf
import datetime

p = pf.Portfolio()
p.add_security(pf.Stock('AAPL'))
p.add_security(pf.Stock('BRK-A'))

r = pf.HoldingsReport(p,datetime.date.today() )
r.calculate()
print r.get_report()
