# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 17:08:42 2014

@author: herbie
"""
# this module takes the whole tims data file, keeps only relevant fields,
# selects crashes in SCAG and bike ped crashes,
# and outputs csv files organized by year of crash

# set working directory
import os

# when on Lewis Center machine

os.chdir('C:\\Users\\Huff\\Dropbox\\lcpython\\CSV_20140930')

# when on personal macbook
# os.chdir('/Users/herbie/Dropbox/lcpython/python/crash_data_project')
mydir = os.getcwd()

# import relevant modules using conventions in pandas documentation
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

# this get all data then delete blank rows approach has a long run time
# and produces a dtype / memory warning. it worked fine for the test files
# but needs some tweaking for the full file

# a chunker approach may bring down run time but i am not going to worry about this for now

#get data from csv
#nrows argument is only there for development. DELETE this for final test runs
# column 35 = 'POP'
# the dtype dict is there to improve run time also
# another possibility to investigate to improve run time eventually is HDF5 format
from pandas import read_csv
tims_csv = pd.read_csv('collisions_2003to2012.csv')

                       #dtype = {'LOCATION':object, 'CHPTYPE': object, 'POP': object})
print "total rows in file"
print len(tims_csv.index)

# delete blank rows - the code below looks for CASEID values equal to NaN
# and keeps only rows that have a valid CASEID
tims = tims_csv[np.isfinite(tims_csv['CASEID'])]
print "total crashes in file"
print len(tims.index)

# pare down dataset to only relevant fields
keepcol = ['CASEID','POINT_X','POINT_Y', 'YEAR_', 'LOCATION', 'CRASHSEV', 'VIOLCAT', 'KILLED', 'INJURED', 'PEDCOL', 'BICCOL', 'PEDKILL', 'PEDINJ', 'BICKILL', 'BICINJ', 'CITY', 'COUNTY', 'STATE', 'X_CHP', 'Y_CHP']
timsR = tims[keepcol]

# only keep crashes in SCAG counties
# isin method
SCAG = ['IMPERIAL', 'LOS ANGELES', 'ORANGE', 'RIVERSIDE', 'SAN BERNARDINO', 'VENTURA']
timsSCAG = timsR[timsR['COUNTY'].isin(SCAG)]
#print timsSCAG.head()
#print timsSCAG.tail()
print "crashes in SCAG counties: "
print len(timsSCAG.index)

# only keep crashes that are bike/ped
timsSCAG_BP = timsSCAG[(timsSCAG['PEDCOL'] == 'Y') | (timsSCAG['BICCOL'] == 'Y')]

#print timsSCAG_BP.head(20)
#print timsSCAG_BP.tail(20)
print "bike ped crashes in SCAG: "
print len(timsSCAG_BP)

# break down by year
# later, rewrite this as a for loop and think about the fact that the year will
# change each year so last_year should be an input to the final function
crash03 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2003]
print "2003 SCAG bike ped crashes: "
print len(crash03)
crash03.to_csv('crash03.csv')

crash04 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2004]
print "2004 SCAG bike ped crashes: "
print len(crash04)
crash04.to_csv('crash04.csv')

crash05 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2005]
print "2005 SCAG bike ped crashes: "
print len(crash05)
crash05.to_csv('crash05.csv')

crash06 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2006]
print "2006 SCAG bike ped crashes: "
print len(crash06)
crash06.to_csv('crash06.csv')

crash07 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2007]
print "2007 SCAG bike ped crashes: "
print len(crash07)
crash07.to_csv('crash07.csv')

crash08 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2008]
print "2008 SCAG bike ped crashes: "
print len(crash08)
crash08.to_csv('crash08.csv')

crash09 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2009]
print "2009 SCAG bike ped crashes: "
print len(crash09)
crash09.to_csv('crash09.csv')

crash10 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2010]
print "2010 SCAG bike ped crashes: "
print len(crash10)
crash10.to_csv('crash10.csv')

crash11 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2011]
print "2011 SCAG bike ped crashes: "
print len(crash11)
crash11.to_csv('crash11.csv')

crash12 = timsSCAG_BP[timsSCAG_BP['YEAR_'] == 2012]
print "2012 SCAG bike ped crashes: "
print len(crash12)
crash12.to_csv('crash12.csv')

#for x in range(2003,2012):
# change this later

# also note these files are bike and ped - need to break that up



