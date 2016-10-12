# this is the final version from the test_12_10_2014b series of files

# Import system modules
import arcpy
import os

# Set local variables
# the r makes the backslashes work:
# "When an 'r' or 'R' prefix is present, a character following a backslash is included in the string without change, and all backslashes are left in the string."
# - https://docs.python.org/2/reference/lexical_analysis.html

workspace = r"C:\Users\Huff\Dropbox\lcpython\python\crash_data_project\GISFiles"
outWorkspace = r"C:\Users\Huff\Dropbox\lcpython\python\crash_data_project\GISFiles"

arcpy.env.overwriteOutput = True

# Want to join crashes to Census block groups and calculate the total crashes per block group
# os.path.join puts together its arguments into a new path

# i manually edit these two lines to run this file each time for each crYY.shp file
# or crYY_YY as the case may be
targetFeatures = os.path.join(workspace, "2010bg_scag.shp")
joinFeatures = os.path.join(workspace, "cr08_12.shp")

# output also manually edited each time. it is crbgYY or crbgYY_YY
output = os.path.join(outWorkspace, "crbg08_12.shp")

# Create a new fieldmappings and add the two input feature classes.
# addTable(table_dataset) specifies a table or feature class whose fields will be used to define the output fields
# here we are adding ALL the fields from both targetFeatures and joinFeatures as input fields, and
# arcpy automatically generates fieldmaps including output fields for each
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(targetFeatures)
fieldmappings.addTable(joinFeatures)

# now that all the fields are in as a mega list, we edit this list and mapping.
# each edit deals wtih a "fieldmap" which is an output field and the rules to make that output field

# first, the crash count.
# get the crash fieldmap. 'PEDCOL' has a Y in it if there was a ped crash.
# likewise 'BICCOL' has Y if bike crash

# how this works: gets the index by name, then gets the field map by calling that index
# Rename the field and pass the updated field object back into the field map

#ped
PcrFieldIndex = fieldmappings.findFieldMapIndex("PEDCOL")
fieldmapP = fieldmappings.getFieldMap(PcrFieldIndex)
outfieldP = fieldmapP.outputField
outfieldP.name = "PEDCOL_S"
outfieldP.aliasName = "PEDCOL_S"
fieldmapP.outputField = outfieldP
# Set the merge rule to sum and then replace the old fieldmap in the mappings object
# with the updated one
fieldmapP.mergeRule = "sum"
fieldmappings.replaceFieldMap(PcrFieldIndex, fieldmapP)

# Analogous process for BIC_CR,
BcrFieldIndex = fieldmappings.findFieldMapIndex("BICCOL")
fieldmapB = fieldmappings.getFieldMap(BcrFieldIndex)
outfieldB = fieldmapB.outputField
outfieldB.name = "BICCOL_S"
outfieldB.aliasName = "BICCOL_S"
fieldmapB.outputField = outfieldB
# Get the output field's properties as a field object
# outputField: an element of a field map

fieldmapB.mergeRule = "sum"
fieldmappings.replaceFieldMap(BcrFieldIndex, fieldmapB)

# Get sums of PEDKILL, PEDINJ, BICKILL, BICINJ
##sum_fields = ["PEDKILL","PEDINJ","BICKILL","BICINJ"]
##for x in count_fields:
##    i = fieldmappings.findFieldMapIndex(x)
##    map = fieldmappings.getFieldMap(i)
##    map.outputField = x + "_T"
##    map.mergeRule = "sum"
##    fieldmappings.replaceFieldMap(i,map)

#above is failed loop code. trying blunt force:

A_FieldIndex = fieldmappings.findFieldMapIndex("PEDKILL")
fieldmapA = fieldmappings.getFieldMap(A_FieldIndex)
outfield_A = fieldmapA.outputField
outfield_A.name = "PEDKILL_S"
outfield_A.aliasName = "PEDKILL_S"
fieldmapA.outputField = outfield_A
fieldmapA.mergeRule = "sum"
fieldmappings.replaceFieldMap(A_FieldIndex, fieldmapA)

C_FieldIndex = fieldmappings.findFieldMapIndex("PEDINJ")
fieldmapC = fieldmappings.getFieldMap(C_FieldIndex)
outfield_C = fieldmapC.outputField
outfield_C.name = "PEDINJ_S"
outfield_C.aliasName = "PEDINJ_S"
fieldmapC.outputField = outfield_C
fieldmapC.mergeRule = "sum"
fieldmappings.replaceFieldMap(C_FieldIndex, fieldmapC)

D_FieldIndex = fieldmappings.findFieldMapIndex("BICKILL")
fieldmapD = fieldmappings.getFieldMap(D_FieldIndex)
outfield_D = fieldmapD.outputField
outfield_D.name = "BICKILL_S"
outfield_D.aliasName = "BICKILL_S"
fieldmapD.outputField = outfield_D
fieldmapD.mergeRule = "sum"
fieldmappings.replaceFieldMap(D_FieldIndex, fieldmapD)

E_FieldIndex = fieldmappings.findFieldMapIndex("BICINJ")
fieldmapE = fieldmappings.getFieldMap(E_FieldIndex)
outfield_E = fieldmapE.outputField
outfield_E.name = "BICINJ_S"
outfield_E.aliasName = "BICINJ_S"
fieldmapE.outputField = outfield_E
fieldmapE.mergeRule = "sum"
fieldmappings.replaceFieldMap(E_FieldIndex, fieldmapE)

# Delete a bunch of fields we don't want to join from the field map
# Delete fields that are no longer applicable
# note: Having problems adding fields to this list. Later would be more ideal to delete more fields
# or to start with a partial table rather than ALL the fields
##del_fields = ["CASEID","POINT_X","POINT_Y","YEAR_","LOCATION","CITY","COUNTY","STATE"]
del_fields = ["STATE","COUNTY","CITY","LOCATION","YEAR_","POINT_Y","POINT_X","CASEID"]
list_del = []
for x in del_fields:
    list_del.append(fieldmappings.findFieldMapIndex(x))

for x in list_del:
    fieldmappings.removeFieldMap(x)



#Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, output, "#", "#", fieldmappings)

#print the fields of the Spatial Join output to check
my_fields = arcpy.ListFields(output)
for field in my_fields:
    print field.name

