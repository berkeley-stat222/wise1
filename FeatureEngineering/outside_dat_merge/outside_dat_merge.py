import pandas as pd
import numpy as np

# import projects data, or take it in
# projects = pd.read_csv('/Users/greta/Downloads/projects_modified.csv', dtype = {'school_zip': np.str_})
projects.shape
projects.loc[:,'school_zip'].head(20)

outside_dat =  pd.read_csv('outside_dat.csv', dtype = {'zip': np.str_, 'med_inc': np.float64, 'pop': np.float64, 'party': np.str_})
outside_dat.shape

# PERFORM MERGE
projects = pd.merge(projects, outside_dat, left_on = 'school_zip', right_on = 'zip', how='left')
projects.shape # right dimensions!

projects[['school_zip', 'zip']].head(10) # They match!

projects = projects.drop('zip', 1)
# PROBLEMS: SOME MISSING DATA FROM OUTSIDE MERGE!!

