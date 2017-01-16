'''
loops through the sqlite dbs produced by draft_gtfsdb_loop.py
runs a sql query defined by MY_SQL_STATEMENT
column names need to be specified as well in COLUMN_NAMES
always adds an 'agency' column with the name of the db the result came from
creates a single txt / csv
'''

import os
import sqlite3
from sqlite3 import Error
from gtfsdb_loop import create_connection
import pandas as pd


PROJECTDIR = '/home/lc/Dropbox/gtfs_caltrans'
SQL_DB_FOLDER = os.path.join(PROJECTDIR,'ca-gtfs-feeds','sqlite_output2','')
CSV_OUTPUT = os.path.join(PROJECTDIR, 'test1-15.csv')

# grab everything in the fare_attributes table for the agencies that have it
MY_SQL_STATEMENT = '''
SELECT fare_id, price, currency_type, payment_method, transfers, transfer_duration
FROM fare_attributes
'''
COLUMN_NAMES = ['fare_id', 'price', 'currency_type',
'payment_method', 'transfers', 'transfer_duration']

def run_sql(conn,sql_statement):
    try:
        c = conn.cursor()
        c.execute(sql_statement)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)

def put_sqlresult_in_df(sql_result):
    sqlresult_as_series = [pd.Series(tup, index=COLUMN_NAMES)
     for tup in sql_result]
    df = pd.DataFrame(sqlresult_as_series)
    return df

def run_and_concat_all(db_gen):
    masterdf = pd.DataFrame() # a blank df
    for db in db_gen:
        conn = create_connection(db)
        db_name = os.path.basename(db)
        sql_result = run_sql(conn,MY_SQL_STATEMENT) # result is a list of tuples
        if not sql_result:
            print 'sql result is empty for %s' %(db_name)
        else:
            print 'fetched %d rows with %d fields from %s' \
            %(len(sql_result), len(sql_result[0]),db_name)
            df = put_sqlresult_in_df(sql_result)
            df['agency'] = db_name
            masterdf = pd.concat([masterdf, df])
        conn.close()
    return masterdf

def main():
    db_path_list = [SQL_DB_FOLDER + f for f in os.listdir(SQL_DB_FOLDER)]
    db_gen = (f for f in db_path_list if f[-3:] == '.db')
    masterdf = run_and_concat_all(db_gen)
    return masterdf

if __name__ == '__main__':
    masterdf = main()
    #masterdf.to_csv(CSV_OUTPUT)
