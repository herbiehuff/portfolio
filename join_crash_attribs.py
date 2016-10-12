# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 13:31:10 2016
# this function joins crash attributes to the sections files (the intersection
# file and the segment file) using the crash file with section IDs
@author: herbie
"""
#%%
# import necessary packages
import pandas as pd
import matplotlib.pyplot as plt
import time

now = time.strftime("%m%d")

#filepath for working from home on mac
working_folder = '/Users/herbie/Dropbox/Bicycle Crash Risk/python/'

#filepath for working on Lewis Center PC
#working_folder = '\\\\164.67.121.62\\BCRP\\Dataset'

# MAKE SURE THESE ARE THE CORRECTLY IDENTIFIED FILES IN THE WORKING FOLDER!
#SEG_FILE_PATH = working_folder + '\\Dataset_Int_061716_v01.xlsx'
#INT_FILE_PATH = working_folder + '\\Dataset_Seg_061716_v01.xlsx'
#CRASH_FILE_PATH = working_folder + '\\Crashes_Sections_06172016.xlsx'

SEG_FILE_PATH = working_folder + 'Dataset/Dataset_Seg_061716_v01.xlsx'
INT_FILE_PATH = working_folder + 'Dataset/Dataset_Int_061716_v01.xlsx'
CRASH_FILE_PATH = working_folder + 'Dataset/crashes_ALL_070116.xlsx'

SEG_OUTPUT_FILE = SEG_FILE_PATH[:-5] + 'Crashes.xlsx'
INT_OUTPUT_FILE = INT_FILE_PATH[:-5] + 'Crashes.xlsx'


segs = pd.read_excel(SEG_FILE_PATH)
ints = pd.read_excel(INT_FILE_PATH)
crashes = pd.read_excel(CRASH_FILE_PATH)

#%%

# this line produces the crash count by section - its a df
# second line cleans up the name for the join
count = crashes.groupby('Section_ID').agg('count')['OBJECTID']
count.name = 'Crash_count'

# this line produces the mean severity - its a series
crashsev = crashes['CRASHSEV'].groupby(crashes['Section_ID']).agg('mean')

# these lines counts the crashes that have night times - each is a series
time300 = crashes[crashes['TIMECAT'] == 300].groupby('Section_ID').agg('count')['TIMECAT']
time300.name = 'TIME300'
time2400 = crashes[crashes['TIMECAT'] == 2400].groupby('Section_ID').agg('count')['TIMECAT']
time2400.name = 'TIME2400'

# killed and injured
# you could use pedinj, bicinj, and vehinj = INJURED - sum of pedinj and bicinj
# but this is just using overall killed and injured fields
# this is a series
killed = crashes['KILLED'].groupby(crashes['Section_ID']).agg('sum')
injured = crashes['INJURED'].groupby(crashes['Section_ID']).agg('sum')


# nothing for parties yet. could get demographic info from that
# but it is a different table and a bit more work to get at

# write all the above series to one data frame with common Section_ID,
# summing the night counts
all = pd.concat([count,crashsev,time300,time2400,killed,injured],axis=1)
all['NIGHT']=all[['TIME300','TIME2400']].sum(axis=1)


# then join

segs = segs.join(all, on='Section_ID')
ints = ints.join(all, on='Section_ID')

# write output file
segs.to_excel(SEG_OUTPUT_FILE)
ints.to_excel(INT_OUTPUT_FILE)




