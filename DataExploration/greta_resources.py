import pandas as pd
resources = pd.read_csv('/Users/greta/Downloads/opendata_resources.csv')
import matplotlib.pyplot as plt

resources.columns
resources.head()

#resources.assign(total_price=resources['item_unit_price'] * resources['item_quantity'])
resources['total_price']= resources['item_unit_price'] * resources['item_quantity']

resources.loc[:,'total_price'].head()
resources["vendor_name"].value_counts()
resources["project_resource_type"].value_counts()
resources["item_name"].value_counts()

pd.pivot_table(resources, values='item_unit_price', index=['project_resource_type'])
resources.groupby("project_resource_type").mean()
resources['item_unit_price'].describe()

# bulk of data lies here
x = resources["item_unit_price"] < 200
y = resources["item_unit_price"]  > 0

# check out these outliers?
x10000 = resources["item_unit_price"] < 10000
xlarge = resources["item_unit_price"] > 50000
weird_sub = resources[xlarge]
data_bulk = resources[x & y]

#subsets by resource type
resources[x10000].shape
resources[xlarge].shape

# Make plots
resources["item_quantity"].hist(color="r", alpha=.5, bins=50)
plt.title("Histogram of Item Quantity Requested")
plt.ylabel("Count")
plt.xlabel("Item Quantity")
plt.show()

data_bulk["item_unit_price"].hist(color="r", alpha=.5, bins=50)
plt.title("Histogram of Item Unit Price (prices less than $200)")
plt.ylabel("Count")
plt.xlabel("Item Unit Price")
plt.show()

data_bulk[["item_unit_price", "project_resource_type"]].shape
data_bulk[["item_unit_price", "project_resource_type"]].boxplot(by='project_resource_type')
plt.ylim([-20,5000])
plt.show()

data_plot = resources[x10000 & y]
#pd.options.display.mpl_style = 'default'
data_plot[["item_unit_price", "project_resource_type"]].boxplot(by='project_resource_type')
plt.ylim([-20,10050])
plt.title("Item Unit Prices (<$10000) by Resource Type")
plt.xlabel('Resource Type')
plt.ylabel('Item Unit Price')
plt.show()

resources[(resources["item_unit_price"] < 2000) & y][["item_unit_price", "project_resource_type"]].boxplot(by='project_resource_type')
plt.ylim([-20,2050])
plt.title("Item Unit Prices (<$2000) by Resource Type")
plt.xlabel('Resource Type')
plt.ylabel('Item Unit Price')
plt.show()
