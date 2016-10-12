# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 15:58:53 2016

@author: herbie
"""
import pandas as pd
import matplotlib.pyplot as plt
import time

working_folder = '/Users/herbie/Dropbox/GHGbikespython/'

INPUT_FILE = working_folder + 'all_current_intervals_07062016.xlsx'

#%%

df = pd.read_excel(INPUT_FILE)
locsbytype = df[['pk_location_id','bikewaytype','Date']]
latlongs = df[['pk_location_id','latitude', 'longitude','street1','street2','street3']]


# find rows that have the same location_id 
# and have bikewaytype changing from none or route to lane

# try this imperfect method:
# group by location_id, concatenate unique bikeway type, 
# then look for bikeroute, bikelane

# df['bikewaytype'].value_counts()
first = locsbytype.groupby('pk_location_id').agg('first')['bikewaytype']
last = locsbytype.groupby('pk_location_id').agg('last')['bikewaytype']

# generate a data frame with the first and last
my_dict = {'pk_location_id':first.index,'first':first.values,'last':last.values}
firstlastdf = pd.DataFrame(my_dict)

# look for first = none/route and last = bikelane
# vols = vols.loc[~((vols['section_id']==9725) &  (vols['source']=='SEG_ADJ_SEG'))]
change1 = firstlastdf.loc[(firstlastdf['first']=='none') & (firstlastdf['last']=='bikelane')]
change2 = firstlastdf.loc[(firstlastdf['first']=='bikeroute') & (firstlastdf['last']=='bikelane')]

# trying to merge the lat longs to this table.
# this isn't used currently
# change_1 = change1.merge(latlongs, on='pk_location_id')
# a better method would be to pivot this data 
# create a column with the month and the type
# identify the year of the change
# clean out fake changes like 'bikepath' to 'none'
