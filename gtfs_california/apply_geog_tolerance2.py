'''
given a pandas dataframe for all transit stops in ca
with lat, long columns,
identify the stops that are within a tolerance X of any other stop
that is *not* in the same agency as the original stop
'''
from haversine import haversine # package to calculate great circle distance from lat,lon
import pandas as pd
import numpy as np

df = pd.read_csv('allstops12-7-v2.csv')

df['lat_lon'] = df[['stop_lat','stop_lon']].apply(tuple,axis=1)
# ll_list = list(df['lat_lon'])
# N = len(ll_list) # this is N = 75,268 stops

for row1 in df.itertuples():
    min_lat = row1.stop_lat-.01 # search polygon: .01 x .01 decimal degrees
    max_lat = row1.stop_lat+.01
    min_lon = row1.stop_lon-.01
    max_lon = row1.stop_lon+.01
    candidates = df[(df['stop_lat']> min_lat) & (df['stop_lat']< max_lat)
    & (df['stop_lon']> min_lon) & (df['stop_lon']< max_lon)]
    print('created candidates for ', row1.Index)
    for row2 in candidates.itertuples():
        if haversine(row1.lat_lon,row2.lat_lon,miles=True) < .01 \
        and row1.agency_name != row2.agency_name:   #.01  miles
            df.ix[row1.Index,'interagency'] = True
            df.ix[row1.Index,'other_agency'] = row2.agency_name
            print('found interagency for',row1.Index)


inter = df[df['interagency']==True]
inter.to_csv('interagencystops12-7.csv')
