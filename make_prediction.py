"""
The code does the following:
    1. Take in argument from command line (project ID)
    2. Queries API to get data for the proj_id
    3. Transforms API data to same featurized format used in model building
    4. Loads a pre-trained random-forest model
    5. Makes predictions from this model
    6. Returns a confidence score of the project being fully funded
       within 30 days
"""

from __future__ import division
from urllib2 import urlopen
import numpy as np
import pandas as pd
import json
import sys
import string
import WiseGamma
from WiseGamma import DataSet, Model
import GammaLL

# read in external data
donations = pd.read_csv('donations_counts.csv')
outside_dat =  pd.read_csv('outside_dat.csv',
                           dtype = {'school_zip': np.str_, 'med_inc': np.float64,\
                                    'pop': np.float64, 'party': np.str_})


# a few lookup tables
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

    row_dict = {'school_latitude': proj['latitude'],
                'school_longitude': proj['longitude'],
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
                'years_since_2000': float(proj['expirationDate'].split('-')[0]) - 2000,
                'scaled_interest_par_sub': sub_interest_dict[subject],
                'scaled_interest_par_pov': pov_interest_dict[poverty],
                'city_state_counts': ???,
                'Google_query': ???,
                'med_inc': outsideline.iloc[0]['med_inc'],
                'pop': outsideline.iloc[0]['pop'],
                'party': outsideline.iloc[0]['party']}

    return pd.DataFrame(row_dict, index=[0])


def query_api(proj_id):
    """
    Args:   project ID of the project to be queried
            from the donorschoose API

    Output: A pandas dataframe consisting of a single line that featurizes
            the API data into the same form as the data used to train the 
            model so that we can predict on this new line.
    """
    if len(proj_id) != 7 or not proj_id.isdigit():
        raise ValueError('The project ID should be a 7 digit number.')

    dc_apikey = '80g5fqgy8nd2'
    url_string = 'http://api.donorschoose.org/common/json_feed.html?id='\
                 + proj_id + '&APIKey=' + dc_apikey
    query = urlopen(url_string)
    projects_json = json.load(query)

    if not projects_json['proposals']:
        raise ValueError('Invalid project ID.')

    return parse(projects_json['proposals'][0])


def load_model(model_file):
    """
    A workaround to load a pre-trained WiseGamma random forest model because
    WiseGamma.Model.load is not available in the current version
    """
    return WiseGamma.Model(GammaLL.load_model_from_file(model_file, ""))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: python query_api.py <project ID number>"
        exit(-1)

    newline_df = query_api(sys.argv[1])
    """
    Write data frame out to csv, without the index and then read in as a
    WiseGamma.DataSet object. This is a workaround since the current
    version of WiseGamma does not have the appropriate pandas support.
    """
    newline_df.to_csv('temp.csv', index=FALSE)
    newline_ds = DataSet.load('temp.csv')


    trained_model = load_model("<model>") #FIXME: fill in name of the model file
    pred = trained_model.probs(newline_ds)

    """ Version 2 (not currently available)  
    pred = trained_model.probs(newline_df)
    """

    print pred['Yes'].values

