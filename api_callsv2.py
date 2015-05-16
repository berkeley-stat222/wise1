from __future__ import division
from urllib2 import urlopen
from collections import Counter
import numpy as np
import pandas as pd
import json
import requests
import ast

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
print projects_json['proposals'][0]
"""
# Most items are string/float but a few are dictionaries themselves
# Extract school types
[x['name'] for x in projects_json['proposals'][0]['schoolTypes']]
# Extract teacher types
[x['name'] for x in projects_json['proposals'][0]['teacherTypes']]

for pj in projects_json['proposals']:
    print [x['name'] for x in pj['schoolTypes']]
"""
# Note: KIPP is actually in the API.
#       Worth the effort to edit feature engineering script?

#TODO: parse each project. I think it's easier to write a function to parse
#      each project, create a row of data and concatenate to a dataframe
#      (because some items in the project dictionary are also dictionaries
#      and we need to test for existence of teacher/school types as well as
#      make sure the column names are the same as in the train/test sets from
#      the CSV dumps.


donations = pd.read_csv('donations_counts.csv')
outside_dat = pd.read_csv('outside_datmay16.csv',
                           dtype = {'school_zip': np.str_, 'med_inc': np.float64,\
                                    'pop': np.float64, 'party': np.str_})
top_city_state = ['Charlotte, NC', 'Tucson, AZ', 'Tulsa, OK', 'Milwaukee, WI',
                  'Seattle, WA', 'San Antonio, TX', 'Newark, NJ', 'New York, NY',
                  'Winston Salem, NC', 'Saint Louis, MO', 'Detroit, MI', 'Richmond, VA',
                  'Baltimore, MD', 'Indianapolis, IN', 'Staten Island, NY', 'Sacramento, CA',
                  'Durham, NC', 'Bronx, NY', 'Dallas, TX', 'Tampa, FL',
                  'Las Vegas, NV', 'Washington, DC', 'Van Nuys, CA', 'Richmond, CA',
                  'Oakland, CA', 'Los Angeles, CA', 'Austin, TX', 'Oklahoma City, OK',
                  'Atlanta, GA', 'San Jose, CA', 'San Francisco, CA', 'Miami, FL',
                  'Bridgeport, CT', 'Anaheim, CA', 'Memphis, TN', 'Philadelphia, PA',
                  'New Orleans, LA', 'Louisville, KY', 'Denver, CO', 'Brooklyn, NY',
                  'Phoenix, AZ', 'Chicago, IL', 'Fort Worth, TX', 'San Diego, CA',
                  'Bakersfield, CA', 'Portland, OR', 'Joplin, MO', 'Houston, TX',
                  'Orlando, FL']
    
# Retrieve Google Trends data; implemented inside the parse function
def retrieve_goog():
    html_base = u"http://www.google.com/trends/fetchComponent?q="
    q = u"donors+choose"
    query_type = u"&cid=TIMESERIES_GRAPH_0&export=3"
    full_query = html_base + q + query_type
    response = requests.get(full_query)
    split = response.text.split('setResponse(')
    if len(split)==1: # If you have reached your quota limit, return value is different
        q_count = None
    else:
        nice_dict = ast.literal_eval(split[1].rstrip()[:-2].replace('new Date', ''))
        # Ugly formatting (from Java)
        # Get most recent Google Trends count
        q_count_scaled = nice_dict['table']['rows'][-1]['c'][-1]['v']
        scale = 0.09854
        q_count = scale * q_count_scaled * 7 # unscale by top # of counts, convert to weekly
    return(q_count)

    
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
        
    citystate = str(proj['city'] + ", " + proj['state'])
    if citystate in top_city_state:
        citystatecat = citystate
    else:
        citystatecat = 'Other'
        
    # gets line of outside_dat where school_zip matches the zip in proj
    schzip = proj['zip'].split('-')[0]
    outsideline = outside_dat[outside_dat.school_zip == schzip]

    # retrieve info from google
    goog_search = retrieve_goog()
    
    row_dict = {'school_metro': None,
                'school_charter': charter,
                'school_magnet': magnet,
                'school_year_round': yr,
                'school_nlns': nlns,
                'teacher_prefix': proj['teacherName'].split()[0],
                'teacher_teach_for_america': tfa,
                'teacher_ny_teaching_fellow': nytf,
                'primary_focus_subject': proj['subject']['name'],
                'resource_type': proj['resource']['name'],
                'poverty_level': proj['povertyLevel'].lower(),
                'grade_level': proj['gradeLevel']['name'],
                'total_price_excluding_optional_support': float(proj['totalPrice']),
                'days_to_completion': None,
                'days_open': None,
                'funded_by_30': None,
                'scaled_interest_par_sub': '??',
                'city_state': citystate,
                'completion_rank': '??',
                'city_state_cat': citystatecat,
                'donor_counts': '??',
                'med_inc': outsideline.iloc[0]['med_inc'],
                'pop': outsideline.iloc[0]['pop'],
                'party': outsideline.iloc[0]['party'],
                'train_test_label': None,
                'Google_query': goog_search}
    return pd.DataFrame(row_dict, index=[0])


# TODO: find out how to convert unicode (returned in the json obejcts)
#       to regular python strings. This is a problem for the field
#       primary_focus_subject and possibly for teacher_prefix due to ampersands
#       & becomes &amp;


testparse = parse(projects_json['proposals'][0])
print type(testparse)
print testparse.ix[0]
