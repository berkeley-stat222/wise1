import pandas as pd
import numpy as np

outside_dat =  pd.read_csv('outside_dat.csv', dtype = {'zip': np.str_, 'med_inc': np.float64, 'pop': np.float64, 'party': np.str_})

# PERFORM MERGE
projects = pd.merge(projects, outside_dat, left_on = 'school_zip', right_on = 'zip', how='left')
projects = projects.drop('zip', 1)

