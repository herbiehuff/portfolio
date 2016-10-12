#import necessary packages
import pandas as pd
SURVEY_FILE_PATH = '//Users//herbie//Dropbox//GHGbikespython//Tier2SurveyOD.csv'
#SURVEY_FILE_PATH = '\Users\Lewis Center\Dropbox\GHGbikespython\Tier2Survey.csv'

# read tabular data in from google sheets
survey = pd.read_csv(SURVEY_FILE_PATH)

# a bunch of alternative subsets of the survey.

#recreational riders
survey = survey[survey['Q1_Purpose']== 'E']

# utilitarian riders
#survey = survey[~(survey['Q1_Purpose']== 'E')]

# physical separation
#CT = ['2nd','HarborBeryl','Pico6th','ResedaPlummer','SFVBikePath']
#survey = survey[survey['Location'].isin(CT)]

# striping only
#CT = ['2nd','HarborBeryl','Pico6th','ResedaPlummer','SFVBikePath']
#survey = survey[~(survey['Location'].isin(CT))]

#no Harbor Dr
#survey = survey[~(survey['Location']=='HarborBeryl')]

#utilitarian and mode choice WAS affected by facility
#survey = survey[~(survey['Q1_Purpose']== 'E')]
#survey = survey[survey['Q4b_tripinfluencetobike']=='Y']

#recreational and mode choice WAS affected by facility
#survey = survey[(survey['Q1_Purpose']== 'E')]
#survey = survey[survey['Q4b_tripinfluencetobike']=='Y']

#create a subset for each location
# for loop through locations

# get unique values for locations in a numpy array
locations = pd.unique(survey['Location'].values.ravel())

loc_list = []
for i in range (0, locations.size):
	loc_list.append(locations[i])

# create a dict with each location and the number of surveys at that location
# REVISE - A LESS VERBOSE WAY IS list(df) / list(series)

loc_count = {}
for i in range (0, locations.size):
	count = {locations[i]: len(survey[survey['Location']==loc_list[i]].index)}
	loc_count.update(count)

# most are recreational riders
# survey['Q1_Purpose'].value_counts()

# Y-70, N-63 say lane influenced their trip
# survey['Q4a_Laneinfluecedtrip'].value_counts()

# 120 of 145 say the would still take trip. 25 would not have.
# survey['Q4a_Stilltaketrip'].value_counts()

# for all the categorical columns, create a dict of dicts with their summmary stats
category_descriptives = {}

# select categorical columns:
catvars = survey[['Q1_Purpose','Q1_ifother','Q4a_Laneinfluecedtrip','Q4a_Stilltaketrip','Q4b_tripinfluencetobike','Q4bi_othermodeifinfluenced','Q4c_routeinfluence','Q4d_other','Q5_Vehicleavailable','Q6_otherbikelane','Q7_transit','Q8_safer','Q9_lanechangedhowyougetaround','Q9a_likelytotravelbybike','Q9aii_changedroute','Q9iii_changedmode','Q10_oftenbike','Q12_gender','Q13_Race/Ethnicity','Q13_ifother','Q14_income']]

for i in range(0,len(catvars.columns)):
	onevar_desc = {catvars.columns[i]: catvars.ix[:,i].value_counts()}
	category_descriptives.update(onevar_desc)

triplengthvars = survey[['Origin_dist','Destin_dist','Total_dist']]
triplengthvars = triplengthvars[~(triplengthvars['Total_dist']=='incomplete')]
triplengthvars['Total_dist'] = triplengthvars['Total_dist'].astype(float)

trip_length_mean = triplengthvars['Total_dist'].mean()
trip_length_median = triplengthvars['Total_dist'].median()
N_trip_length = triplengthvars['Total_dist'].count()
subset_N = survey['Date'].count()

	
# write output to CSVs? 