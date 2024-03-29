# coding: utf-8

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab

# Global variables
state_rank_count = 50

# Read in opendata_projects file
projects = pd.read_csv('Documents/wise/Data/opendata_projects.csv')

# Read in donations by city_state
donations = pd.read_csv('Documents/wise/Data/donations_counts.csv')

# Using "shipping cost" variable to created binary variable indicating whether a project has free shipping
shipping = projects.loc[:,['vendor_shipping_charges']]

# if shipping_charges = 0 , 1
# if shipping_charges > 0 , 0
shipping[shipping == 0] = -1
shipping[shipping > 0] = 0
shipping[shipping == -1] = 1

# Function to count the number of days between start_date and complete_date
from dateutil.parser import parse
from collections import Counter
import math
import time

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

# Apply dayCount function over dataframe
def date_calc(row):
    return day_count(row['date_completed'], row['date_posted'])
date_diff = projects.apply(date_calc, 1)

# Create single vector dataframe of days to completion
days_to_comp = pd.DataFrame({'days_to_completion': pd.Series(date_diff)})

# Subset opendata_projects to include only live projects
live_projects = projects[projects.funding_status == 'live']

# Add column of current date so we can count open days
live_projects['current_date'] = '2014-11-10'

# Apply dayCount over live projects
def date_calc2(row):
    return day_count(row['current_date'], row['date_posted'])
date_diff2 = live_projects.apply(date_calc2, 1)

# Create single vector dataframe of days open. If project live fewer than 30 days, set days live to NA
days_live = pd.DataFrame({'days_open': pd.Series(date_diff2)})

"""
    Option 1: Consider all reallocated projects and all projects live for more
    than 30 days as not funded at all. Delete all remaining live projects
    (which have been live for less than 30 days)
    """
projects.ix[projects.days_to_completion <= 30, 'funded_by_30'] = 'Yes'
projects.ix[projects.days_to_completion > 30, 'funded_by_30'] = 'No'
projects.ix[projects.funding_status=='reallocated', 'funded_by_30'] = 'No'
projects.ix[projects.days_open > 30, 'funded_by_30'] = 'No'

projects = projects[projects.funded_by_30.notnull()]

# Combine city, state into city_state variable in projects dataframe
projects['city_state'] = projects['school_city'] + ', ' + projects['school_state']

# Get the count of the completed projects from each city_state
# and create levels from the top 50, and group all remaining into 51st category
comp = projects[projects.funding_status == 'completed']
counts = comp['city_state'].value_counts()
ranks = pd.DataFrame([x+1 for x in range(counts.shape[0])], columns = ['completion_rank'])
names = pd.DataFrame(counts.index, columns = ['city_state'])

ranks = pd.concat([names, ranks], axis = 1)
ranks['city_state_cat'] = ranks['city_state']

ranks['city_state_cat'][ranks.completion_rank > state_rank_count] = 'Other'

# Add the dataframes containing days_to_completion and days_open to projects dataframe
projects = pd.concat([projects, days_to_comp, days_live], axis = 1)

# Join the ranks table and projects table on the city_state column
projects = projects.merge(ranks, how = 'right', on = 'city_state')

# Join the donations table and projects table on the city_state column
projects = projects.merge(donations, how = 'right', on = 'city_state')

# Read in outside data
outside_dat =  pd.read_csv('outside_dat.csv', dtype = {'zip': np.str_, 'med_inc': np.float64, 'pop': np.float64, 'party': np.str_})

# PERFORM MERGE
projects = pd.merge(projects, outside_dat, left_on = 'school_zip', right_on = 'zip', how='left')
projects = projects.drop('zip', 1)

"""
    Create test set (~20%) by selecting projects posted from Nov 2013 onwards.
    Then create training (~60%) and validation (~20%) sets.
    """
# convert dates from strings to datetime objects
projects.date_posted = [parse(x) for x in projects.date_posted]

def split_train_test(date):
    if date.year == 2014 or (date.year == 2013 and (date.month == 11 or date.month == 12)):
        return 'Test'
    else:
        return 'Train'

projects['train_test_label'] = [split_train_test(x) for x in projects.date_posted]

train = projects[projects.train_test_label == 'Train']
test = projects[projects.train_test_label == 'Test']