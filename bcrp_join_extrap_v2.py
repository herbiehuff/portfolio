import numpy as np
import pandas as pd
import os
import time

# next step is to fix this installation / openpyxl error


# --- overview ----

# identify file paths for SEG and INT datasets to update

# read in SectionIDs and extrapolation columns from appropriate sheets of primary query results
# mostly a matter of ID'ing the right sheets and columns

# combine into a single data frame
# this automatically deals with sections that have query results from multiple relationships
# e.g. SEG_SEG__SEG_ADJ_INT

# groupby section ID and average

# and join to SEG and INT datasets

#--- end overview ---

# --- Identify file paths ----
working_folder = '/Users/herbie/Dropbox/Bicycle Crash Risk/python/'

INPUT_SEG_FILE_PATH = working_folder + 'Dataset/Dataset_Seg_061716_v01Crashesvols.xlsx'
INPUT_INT_FILE_PATH = working_folder + 'Dataset/Dataset_Int_061716_v01Crashesvols.xlsx'
EXTRAP_RESULTS_FOLDER_PATH = working_folder + 'extrapolated count volumes//' #Berkeley's results

file_suffix = 'extraps_' + time.strftime("%m%d%y")

OUTPUT_SEG_FILE_PATH = INPUT_SEG_FILE_PATH[:-5] + file_suffix + '.xlsx'
OUTPUT_INT_FILE_PATH = INPUT_INT_FILE_PATH[:-5] + file_suffix + '.xlsx'

#--- Deal with primary query results

# the correct sheet is always named like 'INT_INT'
# i had to manually fix this in the case of 'INT_ADJ_SEG'
# which had a 'RAW' sheet and an 'INT_ADJ_SEG' sheet
# create a dict with the query, sheetname, and columns

# primaries = ['Q_INT_ADJ_SEG_v3_UPDATED_20160616_Julia.xlsx',
# 'Q_SEG_ADJ_INT_v3_UPDATED_20160617_v2_Dave.xlsx',
# 'Q_SEG_ADJ_SEG_v3_UPDATED_20160617_Dave.xlsx',
# 'Q_SEG_SEG_v3_UPDATED_201601617_Dave.xlsx',
# 'Q_INT_INT_v3_UPDATED_20160617_Dave.xlsx']

def IDPrimariesCombos():
    berkeley_excels = [file for file in os.listdir(EXTRAP_RESULTS_FOLDER_PATH) if file[-5:] == '.xlsx']
    queryLabels = {}

    for i in berkeley_excels:
        full_path = EXTRAP_RESULTS_FOLDER_PATH+i
        end_of_query_name = i.find('v')-1
        query_label = i[2:end_of_query_name]
        queryLabels.update({query_label:i})

    primary_labels = ['INT_INT','INT_ADJ_SEG','SEG_SEG','SEG_ADJ_INT','SEG_ADJ_SEG']
    combo_labels = ['INT_INT__INT_ADJ_SEG', 'SEG_ADJ_SEG__SEG_ADJ_INT', 'SEG_SEG__SEG_ADJ_INT', 'SEG_SEG__SEG_ADJ_SEG']

    primaries = {k:v for k,v in queryLabels.iteritems() if k in primary_labels}
    combos = {k:v for k,v in queryLabels.iteritems() if k in combo_labels}
    return primaries, combos

def loadExtraps(primaries):
# this needs to only run through primaries
    extraps = {}
    for i in primaries.values():
        # maybe I don't need this beginning code anymore
        full_path = EXTRAP_RESULTS_FOLDER_PATH+i
        end_of_query_name = i.find('v')-1
        query_label = i[2:end_of_query_name]

        # find sheet with primary query name
        df = pd.read_excel(full_path,sheetname=query_label)
        this_result = {query_label:df}
        extraps.update(this_result)
    return extraps

def loadComboLookupIDs(combos):
    # this needs to run on combo files
    lookups = {}
    for i in combos.values():
        full_path = EXTRAP_RESULTS_FOLDER_PATH+i
        end_of_query_name = i.find('v')-1
        query_label = i[2:end_of_query_name]

        # find sheet with primary query name
        df = pd.read_excel(full_path,sheetname='LOOKUP')
        this_result = {query_label:df}
        lookups.update(this_result)
    return lookups

# now for each df in extraps, only keep the SectionID, daily bikes, and annual bikes
keepcols = ['Section_ID','section_id','24 hour count','Annual Bikes','24 Hour',
    '24 Hour Count','Annual Bike',]
def strip_columns(df):
    for col in df.columns:
        if col not in keepcols:
            df.drop(col, axis=1, inplace=True)
    return

def get_clean_df(extraps):
    # cleans up the data frames which are stored as values in a dict, extraps
    # transforms into one df with repeated Section_ID s
    for frametitle in extraps.keys():
        df = extraps[frametitle]
        strip_columns(df)
        df.columns = ['Section_ID','24 Hour Bikes','Annual Bikes'] # all dfs have 3 cols with slightly diff names
    extraps_df = pd.concat(extraps)
    # by putting in one data frame, deals with combos automatically
    return extraps_df

def get_means_by_section(extraps_df):
    extraps_df['Section_ID'] = extraps_df['Section_ID'].apply(abs)
    extraps_means = extraps_df.groupby('Section_ID').mean()
    return extraps_means # a df

def join_to_dataset(extraps_means):
    segs = pd.read_excel(INPUT_SEG_FILE_PATH)
    ints = pd.read_excel(INPUT_INT_FILE_PATH)
    segs_output = segs.merge(extraps_means, how='left', left_on='Section_ID', right_index = True)
    ints_output = ints.merge(extraps_means, how='left', left_on='Section_ID', right_index = True)
    return segs_output, ints_output

def setup_extraps():
   primaries, combos = IDPrimariesCombos()
   extraps = loadExtraps(primaries)
   lookups = loadComboLookupIDs(combos)
   extraps = get_clean_df(extraps)
   extraps_means = get_means_by_section(extraps)
   return extraps_means

if (__name__ == "__main__"):
   extraps_means = setup_extraps()

   segs_output, ints_output = join_to_dataset(extraps_means)

   segs_output.to_excel(OUTPUT_SEG_FILE_PATH)
   ints_output.to_excel(OUTPUT_INT_FILE_PATH)
