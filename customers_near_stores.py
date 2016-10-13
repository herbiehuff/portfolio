# Faherty wants to identify which of its customers live within a 45 mile radius
# of its brick-and-mortar stores.
# This script takes in an export of the customers for whom Faherty has addresses
# and uses python and ArcGIS to append an ID with the closest store and the
# distance to that store.

# by Herbie Huff

import pandas as pd
import os

out_dir = os.getcwd()

# input: a file with customers and their addresses
source_dir = '/Users/herbie/Dropbox/faherty/'
CUSTOMER_FILE = source_dir + 'customers_export_09-21-2016.csv'

os.chdir(source_dir)
cust = pd.read_csv(CUSTOMER_FILE, dtype={'Zip':str})

# Zip code is sufficient to describe location - no need for further accuracy
cust_zipcodes = cust.groupby('Zip').count()
cust['Zip']= cust['Zip'].astype(str)

def cleanzip(zipcode):
    if '-' in zipcode:
        zipcode = zipcode[0:5]
    if len(zipcode) == 3:
        zipcode = '00'+zipcode
    if len(zipcode) == 4:
        zipcode = '0'+zipcode
    return zipcode

cust['Zip']= cust['Zip'].astype(str)
cust['Zip'] = cust['Zip'].apply(cleanzip)

cust_ts = cust[['Total Spent','Zip']]
output = cust_ts.groupby(cust['Zip']).count()
os.chdir(out_dir)
output.to_csv('zip_count.csv')

# This allows me to generate a 'near table' in ArcGIS.
# I join 'zip_count.csv' to the Census ZCTA shapefile and select only the features
# with customers in them.
# I then input into the Near tool: 1) those features and 2) the Faherty stores
# The output is a 'near table' where each row is a zip code with customers in it,
# and the column 'NEAR_FID' indicates the closest store, and the column
# NEAR_DIST is the distance to that store.

NEAR_TABLE = source_dir+'customers_near_table.txt'
cust_near = pd.read_csv(NEAR_TABLE)
cust_near['Zip']= cust_near['Zip'].astype(str)
cust_near['Zip'] = cust_near['Zip'].apply(cleanzip)

cust_out = cust.merge(cust_near,how='left',on='Zip')
cust_out.to_csv('cust_with_near.csv')
