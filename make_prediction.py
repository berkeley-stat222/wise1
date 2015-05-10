#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The code does the following:
     1. Take in argument from command line (project ID)
     2. Queries API to get data for the proj_id [RUSSELL CODE]
     3. Transforms API data to same featurized format used in model building [RUSSELL CODE]
     4. Loads in finalized random-forest model
     5. Makes predictions from finalized model
     6. Spits out predictions in JSON format
    
'''

# # -------------------------------------------- # # 
# #  STEP 1: Take in arg from command line/user  # #
# # -------------------------------------------- # #

import argparse
import sys

proj_id=sys.argv[1:][0] # I believe we will only be passing one arg: project ID.
                        # The [0] used to ignore other args passed through the command line
#print(proj_id) # this outputs to command line. proof it's working

# # -------------------------------------------------- # # 
# #  STEP 2 & 3: Query API, featurize and format data  # #
# # -------------------------------------------------- # #

''' RUSSELL WILL INPUT HIS EDITED api_calls.py HERE 
make sure to use the proj_id from above
return(api_final_dat)
'''


# # -------------------------------------------------- # # 
# #  STEP 4, 5 & 6: Load model, make preds, return preds   # #
# # -------------------------------------------------- # #

# Syntax may need to change here
m = load_model("model.rf") 
preds = m.predict(api_final_dat) # api_final_dat is the dataframe row created in steps 2 and 3
return preds # is this the right format that we want? JSON format?
