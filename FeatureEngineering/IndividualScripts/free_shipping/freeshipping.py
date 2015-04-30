import pandas as pd 
import numpy as np

projects = pd.read_csv('/Users/stephaniekim/Desktop/wise/ipython/projects_modified.csv')

shipping = projects.loc[:,['vendor_shipping_charges']]


# if shipping_charges = 0 , 1
# if shipping_charges > 0 , 0

shipping[shipping == 0] = -1

shipping[shipping > 0] = 0

shipping[shipping == -1] = 1

# if we want to change NA to 0
# shippingfill = shipping.fillna(value=0)