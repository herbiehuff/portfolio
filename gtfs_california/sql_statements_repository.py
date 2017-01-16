
# how many unique routes?
MY_SQL_STATEMENT = '''
SELECT route_short_name, route_long_name, route_type FROM routes
    '''
COLUMN_NAMES = ['route_short_name','route_long_name','route_type']

# select trip count at stops
MY_SQL_STATEMENT = '''
        SELECT COUNT(stop_times.stop_id), stop_times.stop_id, stop_lat, stop_lon
        FROM stop_times, trips, calendar, stops
        WHERE calendar.monday = 1 AND calendar.service_id = trips.service_id
            AND trips.trip_id = stop_times.trip_id
            AND stops.stop_id = stop_times.stop_id
        GROUP BY stop_times.stop_id
        '''
COLUMN_NAMES = ['trip_id_count','stop_id','stop_lat','stop_lon']

# count number of monday trips per agency
MY_SQL_STATEMENT = '''
SELECT COUNT(*) as monday_trips FROM
(
SELECT trips.trip_id, calendar.service_id
FROM trips, calendar
WHERE calendar.monday = 1 AND calendar.service_id = trips.service_id
);
'''
COLUMN_NAMES = ['monday_trips']

# grab everything in the transfer table for the agencies that have it
MY_SQL_STATEMENT = '''
SELECT from_stop_id, to_stop_id, transfer_type, min_transfer_time
FROM transfers
'''
COLUMN_NAMES = ['from_stop_id', 'to_stop_id', 'transfer_type', 'min_transfer_time']

# grab everything in the fare_attributes table for the agencies that have it
MY_SQL_STATEMENT = '''
SELECT fare_id, price, currency_type, payment_method, transfers, transfer_duration
FROM fare_attributes
'''
COLUMN_NAMES = ['fare_id', 'price', 'currency_type',
'payment_method', 'transfers', 'transfer_duration']
