# faherty wants to identify which of its customers live within a 45 mile radius
# of the stores.

import pandas as pd

# input: a file with customers and their addresses
CUSTOMER_FILE = 'customers_export_09-21-2016.csv'


cust = pd.read_csv(CUSTOMER_FILE, dtype={'Zip':str})

cust_zipcodes = cust.groupby('Zip').count()
cust['Zip']= cust['Zip'].astype(str)

def cleanzip(string):
    if '-' in string:
        string = string[0:5]
    if len(string) == 3:
        string = '00'+string
    if len(string) == 4:
        string = '0'+string
    return string

cust['Zip'] = cust['Zip'].apply(cleanzip)

cust_ts = cust[['Total Spent','Zip']]
output = cust_ts.groupby(cust['Zip']).count()
output.to_csv('zip_count.csv')

# This allows me to generate a 'near table' in ArcGIS.
# I join 'zip_count.csv' to the Census ZCTA shapefile and select only the features
# with customers in them.
# I then input into the Near tool: 1) those features and 2) the Faherty stores
# The output is a 'near table' where each row is a zip code with customers in it,
# and the column 'NEAR_FID' indicates the closest store, and the column
# NEAR_DIST is the distance to that store.

cust_near = pd.read_csv('customers_near_table.txt')

cust_out = cust.merge(cust_near,how='left',on='Zip')
cust_out.to_csv('cust_with_near.csv')
