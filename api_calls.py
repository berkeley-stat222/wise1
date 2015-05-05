from __future__ import division
from urllib2 import urlopen
import numpy as np
import pandas as pd
import json

dc_apikey = '80g5fqgy8nd2'

"""
I'm just using a simple query here to set up the JSON parsing
We will look for projects requesting funding for a specific resource type
From the donorschoose API documentation, the proposalTypes accepted are
    1 Books
    2 Technology
    3 Supplies
    4 Trips
    5 Visitors
    6 Other
There's also proposalTypeCombo documented but I have not tried
an API call with that option.
"""

resource_type = '1'
url_string = 'http://api.donorschoose.org/common/json_feed.html?proposalType='\
              + resource_type + '&APIKey=' + dc_apikey + '&showSynopsis=true'
query = urlopen(url_string)
projects_json = json.load(query)

"""
The projects_json object is a dictionary, we are interested in the list
projects_json['proposals'] (in this case of length 10 corresponding to
the 10 proposals returned)
"""

# Look at the first proposal
type(projects_json['proposals'][0])
projects_json['proposals'][0].keys()
projects_json['proposals'][0]
# Most items are string/float but a few are dictionaries themselves
# Extract school types
[x['name'] for x in projects_json['proposals'][0]['schoolTypes']]
# Extract teacher types
[x['name'] for x in projects_json['proposals'][0]['teacherTypes']]

for proj in projects_json['proposals']:
    print [x['name'] for x in proj['schoolTypes']]


#TODO: parse each project. I think it's easier to write a function to parse
#      each project, create a row of data and concatenate to a dataframe
#      (because some items in the project dictionary are also dictionaries
#      and we need to test for existence of teacher/school types as well as
#      make sure the column names are the same as in the train/test sets from
#      the CSV dumps.


donations = pd.read_csv('donations_counts.csv')
outside_dat =  pd.read_csv('outside_dat.csv',
                            dtype = {'zip': np.str_, 'med_inc': np.float64,\
                                     'pop': np.float64, 'party': np.str_})


def parse(proj):
    """
    Args:   Dictionary of content of project proposal from the donorschoose
            API request. This would be elements of the list
            result_json['proposals']

    Output: Row of a dataframe that can be concatenated to already existing
            dataframes (e.g. training and test sets from the CSV dumps) -
            the column names will match
    """

    school_types = [x['name'] for x in proj['schoolTypes']]
    teacher_types = [x['name'] for x in proj['teacherTypes']]

    if "Charter" in school_types:
        charter = 't'
    else:
        charter = 'f'

    if "Magnet" in school_types:
        magnet = 't'
    else:
        magnet = 'f'

    if "Year-round" in school_types:
        yr = 't'
    else:
        yr = 'f'

    if "New Leaders" in school_types:
        nlns = 't'
    else:
        nlns = 'f'

    if "Teach for America" in teacher_types:
        tfa = 't'
    else:
        tfa = 'f'

    if "NY Teaching Fellow" in teacher_types:
        nytf = 't'
    else:
        nytf = 'f'

    row_dict = {'school_metro': np.nan,
                'school_charter': charter,
                'school_magnet': magnet,
                'school_year_round': yr,
                'school_nlns': nlns,
                'teacher_prefix': proj['teacherName'].split()[0],
                'teacher_teach_for_america': tfa,
                'teacher_ny_teaching_fellow': nytf,
                'primary_focus_subject': proj['subject']['name'],
                'resource_type': proj['resource']['name'],
                'poverty_level': proj['povertyLevel'],
                'grade_level': proj['gradeLevel']['name'],
                'total_price_excluding_optional_support': float(proj['totalPrice']),
                'days_to_completion': np.nan,
                'days_open': np.nan,
                'funded_by_30': np.nan,
                'scaled_interest_par_sub': ???,
                'city_state': proj['city'] + ", " + proj['state'],
                'completion_rank': ???,
                'city_state_cat': ???,
                'donor_counts': ???,
                'med_inc': ???,
                'pop': ???,
                'party': ???,
                'train_test_label': np.nan}

    return pd.DataFrame(row_dict)


# TODO: find out how to convert unicode (returned in the json obejcts)
#       to regular python strings. This is a problem for the field
#       primary_focus_subject due to ampersands -  & becomes &amp;
