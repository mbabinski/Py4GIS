# relationshipClassUtils.py
# author: Micah Babinski
# description: Contains useful functions for working with relationship classes in ArcGIS

# import required modules
import arcpy, os

def GetWorkspace(inputFeatureClass):
    """
    Returns the workspace which contains the input feature class
    """
    path = arcpy.Describe(inputFeatureClass).path
    if arcpy.Describe(path).dataType in ("Workspace", "Folder"):
        workspace = path
    else:
        workspace = arcpy.Describe(path).path

    return workspace


def hasRelatedTables(inputTable):
    """
    Returns true if the input table participates in a relationship class
    """
    if arcpy.Describe(inputTable).relationshipClassNames != []:
        return True
    else:
        return False


def GetRelatedTableInfo(inputTable):
    """
    Returns a dictionary of relationship class info
    """
    relTableInfo = {}
    workspace = GetWorkspace(inputTable)
    if hasRelatedTables(inputTable):
        relClasses = arcpy.Describe(inputTable).relationshipClassNames
        for rc in relClasses:
            relClassProps = arcpy.Describe(os.path.join(workspace, rc))
            if os.path.join(workspace, relClassProps.originClassNames[0]) == inputTable:
                isTopLevel = True
            else:
                isTopLevel = False
            relTableInfo[relClasses.index(rc)] = {"IsTopLevel": isTopLevel,
                                                  "RelClassName": rc,
                                                  "ParentTable": os.path.join(workspace, relClassProps.originClassNames[0]),
                                                  "ChildTable": os.path.join(workspace, relClassProps.destinationClassNames[0]),
                                                  "PrimaryKey": [k[0] for k in relClassProps.originClassKeys if k[1] == "OriginPrimary"][0],
                                                  "ForeignKey": [k[0] for k in relClassProps.originClassKeys if k[1] == "OriginForeign"][0],
                                                  "IsAttachment": relClassProps.isAttachmentRelationship,
                                                  "Cardinality": relClassProps.cardinality}

        return relTableInfo

    else:
        return {}


def ListRelatedTables(inputTable, excludeAttachments = False):
    """
    List all feature classes and tables that participate in a relationship
    class with an input table or feature class
    """
    if not hasRelatedTables(inputTable):
        return None
    
    relatedTables = []
    relTableInfo = GetRelatedTableInfo(inputTable)
    if excludeAttachments:
        for item in relTableInfo:
            if not relTableInfo[item]["IsAttachment"]:
                relatedTables.append(relTableInfo[item]["ParentTable"])
                relatedTables.append(relTableInfo[item]["ChildTable"])
    else:
        for item in relTableInfo:
            relatedTables.append(relTableInfo[item]["ParentTable"])
            relatedTables.append(relTableInfo[item]["ChildTable"])

    relatedTables = list(set(relatedTables))
    if inputTable in relatedTables:
        relatedTables.remove(inputTable)

    return relatedTables
