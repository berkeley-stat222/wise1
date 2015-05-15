import datetime

def date_conv(row):
    date = row.isocalendar()
    year_week = str(date[0]) + " " + str(date[1])
    return year_week

date_posted = pd.to_datetime(projects['date_posted'])
projects['year_week'] = date_posted.apply(date_conv, 1)

trends = pd.read_csv('google_queries.csv')
projects = pd.merge(projects, trends, on = 'year_week', how='left')

# ADD year_week to dropped columns!
drop_cols = [....., 'vendor_shipping_charges', 'year_week']
