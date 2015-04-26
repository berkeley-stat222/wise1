import pandas as pd 
import numpy as np

projects_modified = pd.read_csv('/Users/stephaniekim/Desktop/wise/ipython/projects_modified.csv')

shipping = projects_modified.loc[:,['vendor_shipping_charges']]

shippingContents = shipping.vendor_shipping_charges

for i in range(shippingContents.shape[0]):
    if shippingContents[i] > 0:
        shippingContents[i] = 1

freeshipping = pd.DataFrame(shippingContents)