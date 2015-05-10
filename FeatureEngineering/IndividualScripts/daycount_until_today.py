import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab
from dateutil.parser import parse
import math
import time
import datetime

projects = pd.read_csv('/Users/stephaniekim/Desktop/Files/opendata_projects.csv')


# Bri's day_count function
def day_count(date0, date1):
    if isinstance(date0, float) or isinstance(date1, float):
        return 'NaN'
    try:
        delta = parse(date0) - parse(date1)
        delta = delta.days
        if delta < 0:
            delta = 'NaN'       
        elif delta == 0:
            delta = 1      
        else:
            delta = delta
    except Exception, e:
        print date1, type(date1), date0, type(date0)
        raise e
    return delta

# This function counts number of days until today
def date_calc(row):
    return day_count(datetime.date.today().isoformat(),row['date_posted'])

# Day counts until today
days_until_today = projects.apply(date_calc, 1)

# We want to give more weight to more recent projects
# This reverses the order
# Maybe multiply some number to this?
date_weight = 1./days_until_today