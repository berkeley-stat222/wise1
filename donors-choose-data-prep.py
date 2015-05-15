
# coding: utf-8

from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
import re
import string
from operator import itemgetter
from pandas import *

# # ---------------------------------------------------------------------------
# # Data Preparation
# # ---------------------------------------------------------------------------

# Global variables
state_rank_count = 50

# Read in opendata_projects file and donation_counts project file, google queries data, and outside_dat
projects = pd.read_csv('../Data/opendata_projects.csv', index_col = False)
donations = pd.read_csv('../Data/donations_counts.csv')
trends = pd.read_csv('../Data/google_queries.csv')
outside_dat =  pd.read_csv('../Data/outside_dat.csv', 
                           dtype = {'zip': np.str_, 'med_inc': np.float64, 'pop': np.float64, 
                                    'party': np.str_})

# Use "shipping cost" variable to created binary variable indicating whether a project has free shipping
shipping = pd.DataFrame(projects['vendor_shipping_charges'])
# if shipping_charges = 0 , t
# if shipping_charges > 0 , f
shipping[shipping == 0] = -1
shipping[shipping > 0] = 'No'
shipping[shipping == -1] = 'Yes'

shipping.columns.values[0]='free_shipping'

# Function to count the number of days between start_date and complete_date
from dateutil.parser import parse
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

# Function to count the number of years after 2000 in which a project was posted
def years_since_2000(date0):
    if isinstance(date0, float):
        return 'NaN'
    try:
        delta = parse(date0).year - 2000
        if delta < 0:
            delta = 'NaN'       
        elif delta == 0:
            delta = 1      
        else:
            delta = delta
    except Exception, e:
        print date0, type(date0)
        raise e
    return delta

# Apply years_since_2000 function over dataframe
def year_calc(row):
    return years_since_2000(row['date_posted'])
year_diff = projects.apply(year_calc, 1)

years_since_2000 = pd.DataFrame({'years_since_2000': pd.Series(year_diff)})

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

# Add the dataframes containing days_to_completion and days_open to projects dataframe
projects = pd.concat([projects, days_to_comp, days_live, shipping, years_since_2000], axis = 1)

# Consider all reallocated projects and all projects live for more than 30 days as not funded at all. Delete all remaining live projects (which have been live for less than 30 days)
projects.ix[projects.days_to_completion <= 30, 'funded_by_30'] = 'Yes'
projects.ix[projects.days_to_completion > 30, 'funded_by_30'] = 'No'
projects.ix[projects.funding_status=='reallocated', 'funded_by_30'] = 'No'
projects.ix[projects.days_open > 30, 'funded_by_30'] = 'No'

projects = projects[projects.funded_by_30.notnull()]

# Create donor interest parameters by subject and poverty level

# By SUBJECT
# Deal with missing values
index = np.where(projects['primary_focus_subject'].isnull())[0]
projects.loc[index, 'primary_focus_subject'] = 'Missing'
total_size = len(projects) 
total_donors = projects['num_donors'].sum()

subjects = projects['primary_focus_subject']
subjects = subjects.unique()
subjects.sort()

num_donors_sub = projects.groupby(['primary_focus_subject']).sum()['num_donors']
subjects_size = projects.groupby('primary_focus_subject').size()
subjects_prop = subjects_size / total_size
scaled_interest_par_sub = (num_donors_sub/total_donors)**2 /subjects_prop 

df = pd.DataFrame({'primary_focus_subject': subjects, 'scaled_interest_par_sub' : scaled_interest_par_sub.values})
projects = pd.merge(projects, df, left_on = 'primary_focus_subject', right_on='primary_focus_subject', how='left')

# By POVERTY LEVEL
# Deal with missing values
index = np.where(projects['poverty_level'].isnull())[0]
projects.loc[index, 'poverty_level'] = 'Missing'
total_size = len(projects) 
total_donors = projects['num_donors'].sum()

poverty = projects['poverty_level']
poverty = poverty.unique()
poverty.sort()

num_donors_pov = projects.groupby(['poverty_level']).sum()['num_donors']
poverty_size = projects.groupby('poverty_level').size()
poverty_prop = poverty_size / total_size
scaled_interest_par_pov = (num_donors_pov/total_donors)**2 /poverty_prop

df = pd.DataFrame({'poverty_level': poverty, 'scaled_interest_par_pov' : scaled_interest_par_pov.values})
projects = pd.merge(projects, df, left_on = 'poverty_level', right_on='poverty_level', how='left')

#Replace missing values as NaN
projects = projects.replace('Missing', np.nan)

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

# Separate city_state into categories based on the counts of funded projects in each city_state. Thresholds include: 10 or fewer, 11 to 50, 51 to 100, 101 to 200, 201 to 500, and greater than 500. 
max_count = max(counts)
counts_cut = counts
counts_cut[(counts_cut>=1) & (counts_cut<=10)] = 1
counts_cut[(counts_cut>10) & (counts_cut<=50)] = 2
counts_cut[(counts_cut>50) & (counts_cut<=100)] = 3
counts_cut[(counts_cut>100) & (counts_cut<=200)] = 4
counts_cut[(counts_cut>200) & (counts_cut<=500)] = 5
counts_cut[(counts_cut>500) & (counts_cut<=max_count)] = 6

cut = pd.DataFrame(counts_cut.values, columns = ['city_state_counts'])
ranks = pd.concat([ranks, cut], axis = 1)

# Join the ranks table and projects table on the city_state columns
projects = projects.merge(ranks, how = 'right', on = 'city_state')

# Join the donations table and projects table on the city_state column
projects = projects.merge(donations, how = 'right', on = 'city_state')

# Function to process Google queries data
def date_conv(row):
    date = row.isocalendar()
    year_week = str(date[0]) + " " + str(date[1])
    return year_week

date_posted = pd.to_datetime(projects['date_posted'])
projects['year_week'] = date_posted.apply(date_conv, 1)

projects = pd.merge(projects, trends, on = 'year_week', how='left')

# Merge outside_data with projects
projects = projects.merge(outside_dat, on = 'school_zip', how='left')

# Drop last 20986 rows because those rows only have outside data
projects = projects.drop(projects.tail(20986).index)

#Function to remove projects posted prior to 2010
def sub_projects(date):
    if isinstance(date, float):
        return 'NaN'
    try:
        date = parse(date)
        year = date.year
    except Exception, e:
        print date, type(date)
        raise e
    if year >= 2010:
        return 'Keep'
    else: 
        return 'Drop'
    
projects['keep_drop'] = [sub_projects(x) for x in projects.date_posted]
projects = projects[projects.keep_drop == 'Keep']


# # ---------------------------------------------------------------------------
# # Generate test set / training set
# # ---------------------------------------------------------------------------

# Create test set (~20%) by selecting projects posted from Nov 2013 onwards. Then create training (~80%)
def split_train_test(date):
    if isinstance(date, float):
        return 'NaN'
    try:
        date = parse(date)
        day = date.day
        month = date.month
        year = date.year
    except Exception, e:
        print date, type(date)
        raise e
    #if year == 2014 or (year == 2013 and (month == 11 or month == 12)):
    if year == 2014 and month >= 4:
        return 'Test'
    else:
        return 'Train'

projects['train_test_label'] = [split_train_test(x) for x in projects.date_posted]
train = projects[projects.train_test_label == 'Train']
test = projects[projects.train_test_label == 'Test']

# Remove unnecessary columns from projects dataframe
# 
# Removed: _projectid, _teacher_acctid, _schoolid, school_ncesid, school_city, school_state, school_zip, school_district, school_county, school_kipp, school_charter_ready_promise, primary_focus_area, secondary_focus_area, sales_tax, payment_processing_charges, fulfillment_labor_materials, total_price_including_optional_support, students_reached, total_donations, num_donors, eligible_double_your_impact_match, eligible_almost_home_match, funding_status, date_posted, date_completed, date_thank_you_packet_mailed, date_expiration, secondary_focus_subject, city_state, vendor_shipping_charges, city_state_cat, keep_drop

drop_cols = ['_projectid', '_teacher_acctid', '_schoolid', 'school_ncesid', 'school_city', 'school_state', 'school_zip', 
             'school_district', 'school_county', 'school_kipp', 'school_charter_ready_promise', 'primary_focus_area', 
             'secondary_focus_area', 'completion_rank', 'sales_tax', 'payment_processing_charges', 'fulfillment_labor_materials', 
             'total_price_including_optional_support', 'students_reached', 'total_donations', 'num_donors', 'eligible_double_your_impact_match', 
             'eligible_almost_home_match', 'funding_status', 'date_posted', 'date_completed', 'date_thank_you_packet_mailed',
             'date_expiration', 'secondary_focus_subject', 'Unnamed: 0', 'city_state', 'donor_counts', 'days_open', 
             'days_to_completion', 'vendor_shipping_charges', 'city_state_cat', 'keep_drop', 'year_week']

projects = projects.drop(drop_cols, axis = 1)
train = train.drop(drop_cols, axis = 1)
test = test.drop(drop_cols, axis = 1)

# Write full dataset to csv
projects.to_csv('../Data/projects_prelim_data.csv', index = False)

# Drop train_test_label column from training and testing sets
drop_cols2 = ['train_test_label'] 
train = train.drop(drop_cols2, axis = 1)
test = test.drop(drop_cols2, axis = 1)

# Write separate training/testing sets to csvs
train.to_csv('../Data/training_set.csv', index = False)
test.to_csv('../Data/testing_set.csv', index = False)



