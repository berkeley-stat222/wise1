import pandas as pd
import re
import nltk, string
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk import FreqDist
from operator import itemgetter
import numpy as np
from __future__ import division
from pandas import *

#Subjects
#Missing Values
#projects = pd.read_csv("projects_modified.csv")
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
projects_merged = pd.merge(projects, df, left_on = 'primary_focus_subject', right_on='primary_focus_subject', how='left')


#Poverty
#No Missing Values
poverty = projects['poverty_level']
poverty = poverty.unique()
poverty.sort()

num_donors_pov = projects.groupby(['poverty_level']).sum()['num_donors']
poverty_size = projects.groupby('poverty_level').size()
poverty_prop = poverty_size / total_size
scaled_interest_par_pov = (num_donors_pov/total_donors)**2 /poverty_prop


df = pd.DataFrame({'poverty_level': poverty, 'scaled_interest_par_pov' : scaled_interest_par_pov.values})
projects_merged = pd.merge(projects_merged, df, left_on = 'poverty_level', right_on='poverty_level', how='left')
projects_merged = projects_merged.drop('Unnamed: 0', 1)

#Return missing value to NaN
projects = projects_merged.replace('Missing', np.nan)