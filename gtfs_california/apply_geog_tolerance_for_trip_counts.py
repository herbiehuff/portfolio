'''
given a pandas dataframe for all transit stops in ca
with lat, long columns,
identify the stops that are within a tolerance X of any other stop
that is *not* in the same agency as the original stop
and sum the trip_counts across agencies
'''
from haversine import haversine # package to calculate great circle distance from lat,lon
import pandas as pd
import numpy as np

df = pd.read_csv('stopsbytrip12-9TEST.csv')
df['lat_lon'] = df[['stop_lat','stop_lon']].apply(tuple,axis=1)
MILES_TOL = .025 # this is about 150 feet

for row1 in df.itertuples():
    df.ix[row1.Index, 'trips_sum'] = df.ix[row1.Index, 'trip_id_count']
    df.ix[row1.Index, 'other_stops'] = 0
    min_lat = row1.stop_lat-.01 # search polygon: .01 x .01 decimal degrees
    max_lat = row1.stop_lat+.01
    min_lon = row1.stop_lon-.01
    max_lon = row1.stop_lon+.01
    candidates = df[(df['stop_lat']> min_lat) & (df['stop_lat']< max_lat)
    & (df['stop_lon']> min_lon) & (df['stop_lon']< max_lon)]
    print('created candidates for ', row1.Index)
    for row2 in candidates.itertuples():
        if haversine(row1.lat_lon,row2.lat_lon,miles=True) < MILES_TOL \
        and row1.agency != row2.agency:   #.01  miles
            df.ix[row1.Index,'interagency'] = True
            df.ix[row1.Index,'other_agency'] = row2.agency # better to change to concatenate them. this just takes the last one
            df.ix[row1.Index, 'other_stops'] = df.ix[row1.Index, 'other_stops'] + 1
            df.ix[row1.Index, 'trips_sum'] = df.ix[row1.Index, 'trips_sum'] + df.ix[row2.Index,'trip_id_count']
            print('found interagency for',row1.Index)


#inter = df[df['interagency']==True]
#inter.to_csv('interagencystops12-7.csv')
