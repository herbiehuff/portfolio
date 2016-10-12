# 9.27.2016

from osgeo import ogr
import pandas as pd
import numpy as np
import googlemaps

# ---- inputs ----
# can later write something to accommodate switching os's (linux and mac)

# mac at home
# geodata_path = '/Users/herbie/Dropbox/TNCGrandChallenges/geodata/'

# linux at work
geodata_path = '/home/lewiscenter/Dropbox/TNCGrandChallenges/geodata/'

TRANSIT_STOPS = geodata_path + 'AllExclusiveROW.kml'
TAZ_CENTROIDS = geodata_path + 'tier1centroids.kml'

#old key
# MY_GOOGLE_MAPS_API_KEY = 'AIzaSyAXlUfqZJS82XKQW2pguP7uTiFJo1U9p8c'
# MY_GOOGLE_MAPS_API_KEY = 'AIzaSyARfq5SY8fTDo6MlVk6h5iZFeJDzBxGF1I' #herbiehuff@g.ucla.edu key
MY_GOOGLE_MAPS_API_KEY = 'AIzaSyCBzm6aULHqIwaVzLnigyFPnd4h65dv58A' #lewiscenter key

# --- functions ---
# should GetStationCoords and GetTazCoords be revised so they take arguments?
# if yes it needs like this in main()
# stationcoords = GetStationCoords(RAIL_STOPS)

def GetCoordsFromGTFS(input_txt):
    # input is the stops.txt from a GTFS file directory
    # returns a list of 2-tuples (lat,lon)
    stops_df = pd.read_csv(input_txt)
    lats = list(rail_stops['stop_lat'])
    lons = list(rail_stops['stop_lon'])
    coords = zip(lats,lons)
    return coords

def GetCoordsFromKml(input_kml):
    # kml input
    # returns a list of 2-tuples (lat,lon)
    ds = ogr.Open(input_kml)
    xcoords = []
    ycoords = []
    lyr = ds.GetLayer(0)
    for feat in lyr:
        pt = feat.geometry()
        x = pt.GetX()
        y = pt.GetY()
        xcoords.append(x)
        ycoords.append(y)
    coords = zip(ycoords,xcoords)
    return coords

def CrowFliesFilter(input_kml, target_kml, buffer_radius):
    # to reduce calls to google maps api, we filter by a crow flies threshold
    # buffer_radius is the threshold distance (in what units)
    # output_kml is all the features within buffer_radius distance of target_kml
    return output_kml

def CallGmapsDistanceMatrix(origins,dests):
    # origins and dests are lists of 2-tuples (lat,lon)
    # call google maps api distance_matrix

    # new idea: no chunks. call one pair at a time.
    # gives me more control over not repeating pairs
    gmaps = googlemaps.Client(key=MY_GOOGLE_MAPS_API_KEY)
    #dists = []
    #times = []
    dists = np.zeros([len(origins),len(dests)])
    times = np.zeros([len(origins),len(dests)])

    # instead of k_index counters, tried to use k_index = origins.index(k)
    # but it seems like it failed to index a bunch of times.
    # unknown why. rounding error?
    k_index = 0
    for k in origins:
        l_index = 0
        for l in dests:
            dmresult = gmaps.distance_matrix(k,l) # input a tuple
            dist = dmresult['rows'][0]['elements'][0]['distance']['value']
            time = dmresult['rows'][0]['elements'][0]['duration']['value']
            #dists.append(dist)
            #times.append(time)
            dists[k_index,l_index]=dist
            times[k_index,l_index]=time
            l_index = l_index+1
        k_index = k_index+1
    return dists, times

def AssignGmapsResultsToColumns(fieldname,resultarray):
    pass
    # find minimum and index value at minimum (to ID closest feature)
    # can also use pandas to return minimum index value and store this too
    return

# can write a function to filter by distance threshold or time threshold

def main():
    stationcoords = GetStationCoords(RAIL_STOPS)
    tazcoords = GetTazCoords(TAZ_CENTROIDS)
    # dists, times = CallGmapsDistanceMatrix(stationcoords,tazcoords)
    # for testing, only first 25 origins and dests
    dists, times = CallGmapsDistanceMatrix(tazcoords[:25],stationcoords[:18])
    return dists, times

if __name__ == '__main__':
    #main()
    dists, times = main()
