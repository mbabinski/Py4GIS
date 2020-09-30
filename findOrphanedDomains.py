# findOrphanedDomains.py
# author: Micah Babinski
# source: https://community.esri.com/thread/199961-finding-orphaned-domains-in-a-geodatabase
# description: Identifies domains that are not applied
# limitation: This does not account for subtypes! Only for use in geodatabases
# where subtypes are not applied

# import required modules
import arcpy, os

# get the SDE connection as a variable
sdeConnection = arcpy.GetParameterAsText(0) # or hard-code it

# create an empty list that we'll populate with the orphaned domains
orphanedDomains = []

# create an empty list that we'll populate with all the domains in your workspace
allDomains = []

# create an empty list that we'll populate with the applied (non-orphaned) domains in your workspace
appliedDomains = []

# define a function to list the domain names applied to a table or FC
def ListAppliedDomains(table): # could also be a feature class
    """
    Returns a list of domain names applied in the FC or table
    """
    # create empty list of domain names
    appliedDomains = []

    # add any applied domains to the list
    for f in arcpy.ListFields(table):
        if f.domain != "":
            appliedDomains.append(f.domain)

    return appliedDomains


# list the domain objects in your SDE workspace
domainObjects = arcpy.da.ListDomains(sdeConnection)
print("Your SDE workspace has {} domains.".format(str(len(domainObjects))))

# add the names to the list
for domain in domainObjects:
    allDomains.append(domain.name)

# clean up the list of domain objects now that we are done with it
del domainObjects

# list all the feature classes and tables in your SDE workspace
allFcsAndTables = []
walk = arcpy.da.Walk(sdeConnection, datatype=["FeatureClass", "Table"])
for dirpath, dirname, filenames in walk:
    for filename in filenames:
        allFcsAndTables.append(os.path.join(dirpath, filename))

# clean up the walk object
del walk

# go through the tables and feature classes and populate the list of applied domains
for item in allFcsAndTables:
    usedDomains = ListAppliedDomains(item)
    for d in usedDomains:
        appliedDomains.append(d)

# populate the list of orphaned domains based on the 'all domains' that are not in applied domains
for item in allDomains:
    if item not in appliedDomains:
        orphanedDomains.append(item)

# report the result
print("The following domains are not in use in your workspace!")
for item in orphanedDomains:
    print(item)
