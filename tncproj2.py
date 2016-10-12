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

MY_GOOGLE_MAPS_API_KEY = '!insert your API key here!'

# --- functions ---
# should GetStationCoords and GetTazCoords be revised so they take arguments?

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

    gmaps = googlemaps.Client(key=MY_GOOGLE_MAPS_API_KEY)
    dists = np.zeros([len(origins),len(dests)])
    times = np.zeros([len(origins),len(dests)])

    k_index = 0
    for k in origins:
        l_index = 0
        for l in dests:
            dmresult = gmaps.distance_matrix(k,l) # input a tuple
            dist = dmresult['rows'][0]['elements'][0]['distance']['value']
            time = dmresult['rows'][0]['elements'][0]['duration']['value']
            dists[k_index,l_index]=dist
            times[k_index,l_index]=time
            l_index = l_index+1
        k_index = k_index+1
    return dists, times

def main():
    stationcoords = GetStationCoords(RAIL_STOPS)
    tazcoords = GetTazCoords(TAZ_CENTROIDS)
    # dists, times = CallGmapsDistanceMatrix(stationcoords,tazcoords)
    # for testing, only first 25 origins and dests
    dists, times = CallGmapsDistanceMatrix(tazcoords[:25],stationcoords[:18])
    return dists, times

if __name__ == '__main__':
    dists, times = main()
