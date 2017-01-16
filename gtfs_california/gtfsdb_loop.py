'''
Loops through a directory of gtfs feeds, each a .zip file.
Creates a blank sqlite db for each, then calls gtfsdb-load
to fill the sqlite db with the gtfs feed.
Creating a blank sqlite db may not be necessary, but seemed to help some
feeds get through.
'''
import os
import subprocess32
import sqlite3
from sqlite3 import Error

HOME = os.path.expanduser('~')
PROJECTDIR = os.path.join(HOME, 'Dropbox','gtfs_caltrans')
TESTFOLDER = os.path.join(PROJECTDIR,'ca-gtfs-feeds','new-12-7','')
OUTFOLDER = os.path.join(PROJECTDIR,'ca-gtfs-feeds','sqlite_output3','')

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_and_delete_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute('CREATE TABLE aTable(field1 int);')
        c.execute('DROP TABLE aTable;')
    except Error as e:
        print(e)

def main():
    for filename in os.listdir(TESTFOLDER):
        if os.path.splitext(filename)[1] == '.zip':
            # create a blank sqlite db
            dbfilepath = OUTFOLDER + filename[:-4] + '.db'
            conn = create_connection(dbfilepath)
            create_and_delete_table(conn)
            print 'created blank sql db for ' + filename

            # call gtfsdb-load on the zip file to the blank db
            db_url = 'sqlite:///' + OUTFOLDER + filename[:-4] + '.db'
            gtfsfilepath = TESTFOLDER + filename
            subprocess32.call(['gtfsdb-load', gtfsfilepath, '--database_url', db_url])
            print 'called gtfsdb-load on ' + filename

if __name__ == '__main__':
    main()
