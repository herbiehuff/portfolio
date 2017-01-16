'''
A quick utility to inventory the tables in a directory of GTFS feeds.
It loops through the .zip files and updates a dict with the count for each
table.
author: Herbie Huff
Dec. 2016
'''

import os
import zipfile

HOME = os.path.expanduser('~')
FOLDER_PATH = os.path.join(HOME,'Dropbox','gtfs_caltrans',
'ca-gtfs-feeds','input')

def main():
    # initialize a dict for the counts
    counts = {}
    # manually removing a few problem files and duplicates
    feedlist = os.listdir(FOLDER_PATH)
    feedlist.remove('San Carlos (PCJPB).zip')
    feedlist.remove('San Carlos PCJPB.zip')
    feedlist.remove('San Carlos (SamTrans).zip')
    feedlist.remove('Diamond Springs.zip')
    feedlist.remove('Vallejo-Solano.zip')
    feedlist.remove('Modesto.zip')
    feedlist.remove('TriDelta.zip')
    for file in feedlist:
        if os.path.splitext(file)[1] == '.zip':
            path = os.path.join(FOLDER_PATH,file)
            z = zipfile.ZipFile(path,'r')
            for name in [name for name in z.namelist() if os.path.splitext(name)[1] == '.txt']:
                tally = counts.get(name,0)
                counts[name] = tally + 1
                print 'found %s in %s; count is at %d' %(name, file, counts[name])
            z.close()
    return counts

counts = main()

if __name__ == '__main__':
    main()
