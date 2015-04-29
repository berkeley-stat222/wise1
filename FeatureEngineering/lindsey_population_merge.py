import pandas as pd
import numpy as np
projects = pd.read_csv('/Users/Lindsey/Documents/Spring_2015/stat222/project5/data/projects_modified.csv', dtype = {'school_zip': np.str_})
projects.shape  # (771929, 47)
projects2 = projects
projects.loc[:,'school_zip'].head(100)

pops =  pd.read_csv('/Users/Lindsey/Documents/Spring_2015/stat222/project5/data/population_byZip.csv', dtype = {'population': np.float64, 'zip': np.str_})
pops.shape

# PERFORM MERGE
projects = pd.merge(projects, pops, left_on = 'school_zip', right_on = 'zip', how='left')
projects.shape # (772271, 49)
# I don't know why there are more rows after merging.
# I'll look up the data frame to find the problem.

projects = projects.drop('zip', 1)
# PROBLEMS: Missing population for some zip code.

# projects.to_csv('/Users/Lindsey/Documents/Spring_2015/stat222/project5/data/out.csv')
