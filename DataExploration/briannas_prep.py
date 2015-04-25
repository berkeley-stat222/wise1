# coding: utf-8

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab

# Read in opendata_projects file
projects = pd.read_csv('Documents/wise/Data/opendata_projects.csv')

# Function to count the number of days between start_date and complete_date
from dateutil.parser import parse
import math

def day_count(date0, date1):
    if isinstance(date0, float) or isinstance(date1, float):
        return 'NA'
    try:
        delta = parse(date0) - parse(date1)
    except Exception, e:
        print date1, type(date1), date0, type(date0)
        raise e
    return delta

# Apply dayCount function over dataframe
def date_calc(row):
    return day_count(row['date_completed'], row['date_posted'])
date_diff = projects.apply(date_calc, 1)

# Create single vector dataframe of days to completion
days_to_comp = pd.DataFrame({'days_to_completion': pd.Series(dateDiff)})

# Subset opendata_projects to include only live projects
live_projects = projects[projects.funding_status == 'live']

# Add column of current date so we can count open days
live_projects['current_date'] = '2014-11-10'

# Apply dayCount over live projects
def date_calc2(row):
    return day_count(row['current_date'], row['date_posted'])
date_diff2 = live_projects.apply(date_calc2, 1)

# Create single vector dataframe of days to completion
days_live = pd.DataFrame({'days_open': pd.Series(dateDiff2)})

# Combine city, state into city_state variable in projects dataframe
projects["city_state"] = projects["school_city"] + ', ' + projects["school_state"]

# Add the dataframes containing days_to_completion and days_open to projects dataframe
projects = pd.concat([projects, days_to_comp, days_live], axis = 1)


