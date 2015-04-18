# coding: utf-8

import pandas as pd 
import numpy as np
import matplotlib as plt

pwd()

projects = pd.read_csv('Documents/wise/opendata_projects.csv')

projects.shape

# Function to count the number of days between start_date and complete_date
from dateutil.parser import parse
import math
def dayCount(date0, date1):
    if isinstance(date0, float) or isinstance(date1, float):
        return 'NA'
    try:
        delta = parse(date0) - parse(date1)
    except Exception, e:
        print date1, type(date1), date0, type(date0)
        raise e
    return delta


# Apply dayCount function over dataframe
def dateCalc(row):
    return dayCount(row['date_completed'], row['date_posted'])
dateDiff = projects.apply(dateCalc, 1)

dtc = pd.DataFrame({'days_to_completion': pd.Series(dateDiff)})


# Add the dataframe containing dayCounts to projects dataframe
total = pd.concat([projects, dtc], axis = 1)

# Narrow down raw data to include only variables of interest
varsOfInt = total.loc[:,['school_state','funding_status','poverty_level',                           'primary_focus_area','primary_focus_subject',                            'grade_level','total_price_excluding_optional_support',                            'date_posted','date_completed','days_to_completion']]


# Subset to include only funded projects
fundedProjects = varsOfInt[varsOfInt.funding_status == 'completed']

fundedProjects.columns
varsOfInt.columns

# Get column of school state for all projects, and for funded projects

states = total['school_state']
states_funded = fundedProjects[['school_state','days_to_completion']]

# Get project funding percent by state

total_states_count = states.value_counts()
funded_states_count = states_funded['school_state'].value_counts()
funding_pct_by_state = funded_states_count/total_states_count

# Get average days to completion for each state

st = pd.DataFrame({'counts': pd.Series(total_states_count)})
fps = pd.DataFrame({'funding_percent': pd.Series(funding_pct_by_state)})
st_counts_pct = pd.concat([st, fps], axis = 1)

# Write st_counts_pct, fundedProjecst to csv

st_counts_pct.to_csv("states.csv")
fundedProjects.to_csv("funded.csv")


