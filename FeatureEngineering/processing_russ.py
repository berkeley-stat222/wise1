import pandas as pd
from dateutil.parser import parse
from collections import Counter

"""
I'm reading in the modified version of opendata_projects.csv because
I need days_open and days_to_completion for this processing
Also, completed_30 is the response variable in the modified version,
except that it's coded numerically instead of categorically
"""

projects = pd.read_csv('projects_modified2.csv')


"""
Option 1: Consider all reallocated projects and all projects live for more
than 30 days as not funded at all. Delete all remaining live projects 
(which have been live for less than 30 days)
"""
projects.ix[projects.days_to_completion <= 30, 'funded_by_30'] = 'Yes'
projects.ix[projects.days_to_completion > 30, 'funded_by_30'] = 'No'
projects.ix[projects.funding_status=='reallocated', 'funded_by_30'] = 'No'
projects.ix[projects.days_open > 30, 'funded_by_30'] = 'No'

Counter(projects.funded_by_30)
projects = projects[projects.funded_by_30.notnull()]
projects.shape


"""
Option 2: Delete all reallocated projects and consider all projects live for
more than 30 days as not funded at all. Delete all remaining live projects 
(which have been live for less than 30 days)
"""
projects.ix[projects.days_to_completion <= 30, 'funded_by_30'] = 'Yes'
projects.ix[projects.days_to_completion > 30, 'funded_by_30'] = 'No'
projects.ix[projects.days_open > 30, 'funded_by_30'] = 'No'

Counter(projects.funded_by_30)
projects = projects[projects.funded_by_30.notnull()]
projects.shape


"""
Create test set (~20%) by selecting projects most recently posted.
Then create training (~60%) and validation (~20%) sets.
"""
# convert dates from strings to datetime objects
projects.date_posted = [parse(x) for x in projects.date_posted]





# some weirdness
def day_count(date0, date1):
    if isinstance(date0, float) or isinstance(date1, float):
        return 'NA'
    try:
        delta = parse(date0) - parse(date1)
    except Exception, e:
        print date1, type(date1), date0, type(date0)
        raise e
    return delta

expired_projects = projects[projects.funding_status == 'expired']
len(expired_projects)


def expiration_length(row):
    return day_count(row['date_expiration'], row['date_posted'])
foo = parse('04/22/93') - parse('03/21/03')
days_to_expiry = [x.days for x in expired_projects.apply(expiration_length,\
                  axis=1) if type(x) == type(foo)]
len([x for x in days_to_expiry if x > 0 and x < 30])   #2005
len([x for x in days_to_expiry if x < 0])              #135
len([x for x in days_to_expiry if x > 3000])           #32

