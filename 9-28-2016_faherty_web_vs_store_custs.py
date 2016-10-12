# IPython log file

get_ipython().magic(u'pwd ')
get_ipython().magic(u'cd Dropbox/faherty')
get_ipython().magic(u'logstart 9-23-2016.py')
import pandas as pd
storecusts = pd.read_excel('springboard store customers.xlsx')
webcusts = pd.read_csv('shopify store customers.csv')
storecusts.columns
webcusts.columns
storecusts
#row 2 of store custs has the column names
storecusts[2,:]
storecusts.loc[2,:]
col_labels = list(storecusts.loc[2,:])
storecusts.rename(columns = col_labels)
storecusts.columns = col_labels
#that worked
storecusts
storecusts.head()
',''])
webcusts.head()
store_from_web = storecusts.merge(webcusts, how='left',on='Customer')
store_from_web = storecusts.merge(webcusts, how='left',on='')
laksjfl;kajsdf
store_from_web = storecusts.merge(
webcusts, how='left',on='Customer: Email', 'Email')
store_from_web = storecusts.merge(
webcusts, how='left',on=['Customer: Email', 'Email'])
storecusts.columns()
storecusts.columns
store_from_web = storecusts.merge(
webcusts, how='left',left_on='Customer: Email', right_on='Email')
store_from_web.head()
store_from_web.columns
store_from_web.to_csv('store_from_web_09-23-2016.csv')
webcusts.columns
storecusts.columns
store_from_web['Email']
store_from_web['Email' != NaN]
store_from_web[type('Email') is string]
store_from_web[type('Email') is str]
store_from_web[~('Email' is null)]
get_ipython().magic(u'logstop')
get_ipython().magic(u'logstate')
get_ipython().magic(u'logstart 9-28-2016')
# per Alex, want to flag email custs who have already come into the store
get_ipython().magic(u'pwd ')
get_ipython().magic(u'cpaste')
import pandas as pd
storecusts = pd.read_excel('springboard store customers.xlsx')
webcusts = pd.read_csv('shopify store customers.csv')
webcusts
storecusts
storecusts.columns
col_labels = list(storecusts.loc[2,:])
storecusts.rename(columns = col_labels)
storecusts.columns = col_labels
# that .rename does not work
storecusts.head()
#'Customer: Email' is the right column
# need to get rid of rows 0,1, and 2
storecusts.drop(storecusts.index[0:2],inplace=True)
storecusts.head()
storecusts.drop(storecusts.index[2],inplace=True)
storecusts.head()
storecusts.drop(storecusts.index[3],inplace=True)
storecusts.head()
# start over
storecusts = pd.read_excel('springboard store customers.xlsx')
storecusts.head()
ol_labels = list(storecusts.loc[2,:])
storecusts.columns = col_labels
storecusts.head()
storecusts.drop(storecusts.index[0:3],inplace=True)
storecusts.head()
# worked
webcusts.head()
# 'Email' in webcusts need to match 'Customer: Email' in storecusts
web_went_to_store = webcusts.merge(
storecusts, how='right', left_on = 'Email', \
right_on = 'Customer: Email')
web_went_to_store
# gives 61071 rows. not what I want. prob misunderstanding about right
#gives 61071 rows. not what we want
web_went_to_store = webcusts.merge(
storecusts, how='inner', left_on = 'Email', \
right_on = 'Customer: Email')
web_went_to_store
# 60665 rows?! not right
webcusts
webcusts.columns
webcusts['Email']
# new approach
webcusts['Email'].isin(storecusts['Customer: Email']
)
webcusts['already_went_to_store']=webcusts['Email'].isin(
)
webcusts['store_by_email'] = /
webcusts['store_by_email'] = webcusts['Email'].isin(storecusts['Customer: Email'])
sum(webcusts['store_by"email'])
sum(webcusts['store_by_email'])
storecusts
# a lot of matches
# maybe there are duplicates
sum(webcusts['store_by_email'])
# 781 matches
webcusts.head()
storecusts.head()
webcusts.to_csv('shopify store custs w springboard flag 09-28-2016.csv')
# upon inspection, every time email was blank, it matched!
webcusts.head()
# if Email is NaN, set store_by_email to False
# or maybe there is a setting in the isin method
# no
# there is not
# hmm can just do this easier in google sheets
# how bout filter where email has value and store_by_email is True
get_ipython().magic(u'logstate')
storecusts['Customer: Email']
# what if rewrite all of NaN in here to '0' then do the match?
storecusts['Customer: Email'].fillna(value = 0, inplace=True)
storecusts['Customer: Email']
webcusts['store_by_email'] = webcusts['Email'].isin(storecusts['Customer: Email'])
sum(webcusts['store_by"email'])
sum(webcusts['store_by_email'])
webcusts.to_csv('shopify store custs w springboard flag 09-28-2016.csv')
webcusts
quit()
