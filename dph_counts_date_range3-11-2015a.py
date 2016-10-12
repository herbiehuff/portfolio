# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 18:01:32 2015

@author: herbie
"""

import os
#lewis center machine
#os.chdir('C:\\Users\\Huff\\Dropbox\\BCDCHouse UCLA\\DPH automatic counters\\QAQC')

#when at home
os.chdir('/Users/herbie/Dropbox/BCDCHouse UCLA/DPH automatic counters/QAQC')

#os.getcwd()

# import relevant modules using conventions in pandas documentation
import pandas as pd
import numpy as np

from datetime import datetime
from dateutil.parser import parse

xls = pd.ExcelFile('Test_Cudahy.xlsx')
mydata = xls.parse(index_col=None)
col_select = [[0, 2*i+1, 2*i+2] for i in range(0, 12)]
flows = (len(mydata.columns)-1)/2

dates = pd.ExcelFile('dates_test_cud2.xlsx')
dateref = dates.parse(index_col = 'Flow_id')

toReturn = pd.DataFrame()

for x in xrange(0,flows):
    # pull out a 'chunk' three columns: dates, the flow_id and the flows
    chunk = mydata.ix[:,col_select[x]]
    # reindex this by the dates
    chunkd = chunk.set_index('Date')
    # rename the columns
    chunkd.columns = ['Flow_id', 'Flow']
    # pull out the flow_id to use to reference valid ranges
    chunkflow = chunkd.ix[0,'Flow_id']
    # this fixes data type errors (e.g. flow 115.0)
    chunkflow = chunkflow.astype(np.int64)
    # reference flow_id valid ranges and select only valid rows
    valdate1 = dateref.ix[chunkflow,0]
    valdate2 = dateref.ix[chunkflow,1]
    valchunk = chunkd[valdate1:valdate2] 
    valchunkI = valchunk.reset_index()
    toReturn = pd.concat([toReturn,valchunkI])
    
toReturn.to_csv('new2.csv')



