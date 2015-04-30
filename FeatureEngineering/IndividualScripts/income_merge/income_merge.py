import pandas as pd
import numpy as np
projects = pd.read_csv('/Users/greta/Downloads/projects_modified.csv', dtype = {'school_zip': np.str_})
projects.shape
projects2 = projects
projects.loc[:,'school_zip'].head(100)

incomes =  pd.read_csv('medInc_byZip.csv', dtype = {'med_inc': np.float64, 'zip': np.str_})
incomes.shape

# PERFORM MERGE
projects = pd.merge(projects, incomes, left_on = 'school_zip', right_on = 'zip', how='left')
projects.shape # right dimensions!

projects[['school_zip', 'zip']].head(10) # They match!

projects = projects.drop('zip', 1)
# PROBLEMS: MISSING 'MEDIAN INCOMES' FOR CERTAIN ZIP CODES (MISSING INCOMES FOR ~1100 ZIP CODES)

