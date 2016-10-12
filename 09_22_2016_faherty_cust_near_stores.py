# IPython log file

get_ipython().magic(u'pwd ')
get_ipython().magic(u'cd .. ')
get_ipython().magic(u'ls ')
get_ipython().magic(u'cd Dropbox')
get_ipython().magic(u'cd faherty')
get_ipython().magic(u'logstart 09_22_2016.py')
get_ipython().magic(u'pwd ')
import pandas as pd
cust = pd.read_csv('customers_export_09-21-2016')
cust = pd.read_csv('customers_export_09-21-2016.csv')
type(cust)
cust.columns()
cust.columns
cust_zipcodes = cust.groupby('Zip').count()
cust_zipcodes
# necessary to clean up zip codes that are longer than 5 digits
for zip in cust['Zip']:
    if '-' in zip:
        zip = zip[0:5]
        
type(cust['Zip'])
cust['Zip'].dtype
cust = pd.read_csv('customers_export_09-21-2016.csv', dtype={'Zip':str})
cust['Zip'].dtype
cust['Zip'].astype(str)
for zip in cust['Zip']:
    if '-' in zip:
        zip = zip[0:5]
        
cust['Zip']= cust['Zip'].astype(str)
cust['Zip'].dtype
cust['Zip']
cust['Zip'][0]
type(cust['Zip'][0])
def cleanzip(string):
    if '-' in string:
        string = string[0:5]
        
cust['Zip'] = cust['Zip'].apply(cleanzip)
cust['Zip']
a = asdfasdf
a = 'asdfasdf'
a[0:5]
def cleanzip(string):
    if '-' in string:
        string = string[0:5]
    return string

cust = pd.read_csv('customers_export_09-21-2016.csv', dtype={'Zip':str})
cust['Zip'] = cust['Zip'].apply(cleanzip)
cust['Zip']= cust['Zip'].astype(str)
cust['Zip'] = cust['Zip'].apply(cleanzip)
cust['Zip']
cust['Zip'].count()
cust.groupby(cust['Zip']).count()
cust.columns
cust_ts = cust[['Total Spent','Zip']]
cust_ts.groupby(cust['Zip']).count()
output = cust_ts.groupby(cust['Zip']).count()
output.to_csv()
get_ipython().magic(u'pwd ')
output.to_csv('C:\\Users\\Lewis Center\\Dropbox\\faherty')
output.to_csv('C:\Users\Lewis Center\Dropbox\faherty')
output.to_csv('zip_count.csv')
def cleanzip(string):
    
    if '-' in string:
        string = string[0:5]
    if len(string) = 3:
        string = '00'+string
    if len(string) = 4:
        string = '0'+string
    return string
import cleanzip
cleanzip
from cleanzip import cleanzip
cleanzip('943-0451')
cleanzip('943')
s = 00111-2345
s.split('-')
s = '00111-2345'
s.split('-')
s.split('-')[0]
#now I have working cleanzip
cust = pd.read_csv('customers_export_09-21-2016.csv', dtype={'Zip':str})
cust['Zip']= cust['Zip'].astype(str)
cust['Zip'] = cust['Zip'].apply(cleanzip)
cust['Zip']
cust_ts = cust[['Total Spent','Zip']]
output = cust_ts.groupby(cust['Zip']).count()
output.to_csv('zip_count.csv')
output.head()
output.to_csv('zip_count.csv')
output.to_excel('zip_count.xls')
pd.read_csv('customers_near_table.txt')
cust_near = pd.read_csv('customers_near_table.txt')
type(cust_near_


)
type(cust_near)
type(cust)
cust.columns()
cust.columns
cust_out = cust.merge(cust_near,how='left')
cust_out.to_excel('cust_with_near.xls')
cust_out.to_excel('cust_with_near.xlsx')
cust_out.head()
cust_out
cust_out.to_csv('cust_with_near.csv')
cust_out = cust.merge(cust_near,how='left',left_on='Zip',right_on='Zip1')
cust_out.to_csv('cust_with_near.csv')
cust.columns
cust_near.columns
cust_out = cust.merge(cust_near,how='left',on='Zip')
cust_out
cust_out.to_csv('cust_with_near.csv')
# not working; getting a blank output where there should be a join
cust_near.head()
cust_near['Zip']
cust_near['Zip']= cust_near['Zip'].astype(str)
cust_near['Zip'] = cust_near['Zip'].apply(cleanzip)
cust_out = cust.merge(cust_near,how='left',on='Zip')
cust_out.to_csv('cust_with_near.csv')
quit()
