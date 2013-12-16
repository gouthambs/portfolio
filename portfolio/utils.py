# -*- coding: utf-8 -*-

import calendar 
import datetime


def get_month_end(date):
    dayrange = calendar.monthrange(date.year,date.month)
    return date.replace(day=dayrange[1])
    
def get_month_beg(date):
    return date.replace(day=1)
    
def shift_years(from_date,num_years):
    num_years = (int)(num_years)
    try:
        return from_date.replace(year=from_date.year + num_years)
    except:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year+num_years)
                                 


def shift_months(from_date, num_months):
     month = from_date.month - 1 + num_months
     year = from_date.year + month / 12
     month = month % 12 + 1
     day = min(from_date.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)
    