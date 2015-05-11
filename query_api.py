from __future__ import division
from urllib2 import urlopen
import numpy as np
import pandas as pd
import json
import sys

"""
Assumes donation_counts.csv, outside_dat.csv and
query_api.py are all in the same folder
"""
donations = pd.read_csv('donations_counts.csv')
outside_dat =  pd.read_csv('outside_dat.csv',
                           dtype = {'school_zip': np.str_, 'med_inc': np.float64,\
                                    'pop': np.float64, 'party': np.str_})

# a few lookup tables
"""
the following list of top 49 city, states was constructed by:

from collections import Counter
Counter(test['city_state_cat']).keys()

and then removing 'Other'
"""
top_city_state = ['Charlotte, NC', 'Tucson, AZ', 'Tulsa, OK',
                  'Milwaukee, WI', 'Seattle, WA', 'San Antonio, TX',
                  'Newark, NJ', 'New York, NY', 'Winston Salem, NC',
                  'Saint Louis, MO', 'Detroit, MI', 'Richmond, VA',
                  'Baltimore, MD', 'Indianapolis, IN', 'Staten Island, NY',
                  'Sacramento, CA', 'Durham, NC', 'Bronx, NY',
                  'Dallas, TX', 'Tampa, FL', 'Las Vegas, NV',
                  'Washington, DC', 'Van Nuys, CA', 'Richmond, CA',
                  'Oakland, CA', 'Los Angeles, CA', 'Austin, TX',
                  'Oklahoma City, OK', 'Atlanta, GA', 'San Jose, CA',
                  'San Francisco, CA', 'Miami, FL', 'Bridgeport, CT',
                  'Anaheim, CA', 'Memphis, TN', 'Philadelphia, PA',
                  'New Orleans, LA', 'Louisville, KY', 'Denver, CO',
                  'Brooklyn, NY', 'Phoenix, AZ', 'Chicago, IL',
                  'Fort Worth, TX', 'San Diego, CA', 'Bakersfield, CA',
                  'Portland, OR', 'Joplin, MO', 'Houston, TX', 'Orlando, FL']

"""
the following lookup table was built by:

from collections import Counter
x = [x[0] for x in Counter(test['primary_focus_subject']).most_common()]
y = [y[0] for y in Counter(test['scaled_interest_par_sub']).most_common()]
sub_interest_dict = dict(zip(x, y))

and then copying and pasting. Similarly for pov_interest_dict.
Should I pickle instead of copying and pasting?
"""
sub_interest_dict = {np.nan: 5.7427204567211509e-05,
                     'Applied Sciences': 0.046910901426980053,
                     'Character Education': 0.011734209594511109,
                     'Civics & Government': 0.004503308399487903,
                     'College & Career Prep': 0.0089410822293279311,
                     'Community Service': 0.0027847007712426398,
                     'ESL': 0.012527814969187872,
                     'Early Development': 0.018895469981275802,
                     'Economics': 0.0031494696411866856,
                     'Environmental Science': 0.041058586686500816,
                     'Extracurricular': 0.0044112279435957096,
                     'Foreign Languages': 0.0086835485407214408,
                     'Gym & Fitness': 0.010195240246769564,
                     'Health & Life Science': 0.037509555650384836,
                     'Health & Wellness': 0.013788715992077571,
                     'History & Geography': 0.024063208266852952,
                     'Literacy': 0.2898423422134363,
                     'Literature & Writing': 0.12423840541970035,
                     'Mathematics': 0.11526493598853993,
                     'Music': 0.051238013697982497,
                     'Nutrition': 0.0021274501290110691,
                     'Other': 0.010846548586201168,
                     'Parent Involvement': 0.0010599115648126695,
                     'Performing Arts': 0.019826055987753846,
                     'Social Sciences': 0.012042106653145562,
                     'Special Needs': 0.071217593377488869,
                     'Sports': 0.0069608265970106708,
                     'Visual Arts': 0.052359097335636214}

pov_interest_dict = {'high poverty': 0.2494275125818487,
                     'highest poverty': 0.58440167076436256,
                     'low poverty': 0.02598288386748716,
                     'moderate poverty': 0.1404074103565012}


def parse(proj):
    """
    Args:   Dictionary of content of project proposal from the donorschoose
            API request. This would be elements of the list
            result_json['proposals']

    Output: Row of a dataframe that can be concatenated to already existing
            dataframes (e.g. training and test sets from the CSV dumps) -
            the column names will match
    """

    sch_types = [x['name'] for x in proj['schoolTypes']]
    tchr_types = [x['name'] for x in proj['teacherTypes']]

    """
    dict comprehension is probably cleaner so delete these soon.

    if "Charter" in sch_types:
        charter = 't'
    else:
        charter = 'f'

    if "Magnet" in sch_types:
        magnet = 't'
    else:
        magnet = 'f'

    if "Year-round" in sch_types:
        yr = 't'
    else:
        yr = 'f'

    if "New Leaders" in sch_types:
        nlns = 't'
    else:
        nlns = 'f'

    if "Teach for America" in tchr_types:
        tfa = 't'
    else:
        tfa = 'f'

    if "NY Teaching Fellow" in tchr_types:
        nytf = 't'
    else:
        nytf = 'f'
    """

    city_state = str(proj['city'] + ", " + proj['state'])
    if city_state in top_city_state:
        city_state_cat = city_state
    else:
        city_state_cat = 'Other'

    # gets line of outside_dat where school_zip matches the zip of input proj
    schzip = proj['zip'].split('-')[0]
    outsideline = outside_dat[outside_dat.school_zip == schzip]

    subject = proj['subject']['name']
    poverty = proj['povertyLevel'].lower()

    row_dict = {'school_metro': None,
                'school_charter': 't' if "Charter" in sch_types else 'f',
                'school_magnet': 't' if "Magnet" in sch_types else 'f',
                'school_year_round': 't' if "Year-round" in sch_types else 'f',
                'school_nlns': 't' if "New Leaders" in sch_types else 'f',
                'teacher_prefix': proj['teacherName'].split()[0],
                'teacher_teach_for_america': 't' if "Teach for America"\
                                                    in tchr_types else 'f',
                'teacher_ny_teaching_fellow': 't' if "NY Teaching Fellow"\
                                                     in tchr_types else 'f',
                'primary_focus_subject': subject,
                'resource_type': proj['resource']['name'],
                'poverty_level': poverty,
                'grade_level': proj['gradeLevel']['name'],
                'total_price_excluding_optional_support': float(proj['totalPrice']),
                'free_shipping': 't' if proj['freeShipping'] == "true" else 'f',
                'funded_by_30': None,
                'scaled_interest_par_sub': sub_interest_dict[subject],
                'scaled_interest_par_pov': pov_interest_dict[poverty],
                'city_state_cat': city_state_cat,
                'med_inc': outsideline.iloc[0]['med_inc'],
                'pop': outsideline.iloc[0]['pop'],
                'party': outsideline.iloc[0]['party']}

    return pd.DataFrame(row_dict, index=[0])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: python query_api.py <project ID number>"
        exit(-1)

    """
    Is it necessary to also check for appropriate projects IDs?
    I think it would have to be a 7 digit number. 
    However, when actually querying the donorschoose API, no errors
    are returned even if something nonsensical like id=a15*@djs54 is used.
    Projects are actually returned but I'm not sure how they're chosen.
    """

    dc_apikey = '80g5fqgy8nd2'
    url_string = 'http://api.donorschoose.org/common/json_feed.html?id='\
                 + sys.argv[1] + '&APIKey=' + dc_apikey
    query = urlopen(url_string)
    projects_json = json.load(query)

    newline = parse(projects_json['proposals'][0])
    # A couple tests:
    print type(newline)
    print newline.dtypes
    print newline.ix[0]


    # load the pretrained model here
    # predict and save the prediction
    # transfrom prediction to appropriate json and print
