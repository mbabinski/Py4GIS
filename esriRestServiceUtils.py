# esriRestServiceUtils.py
# Author: Micah Babinski
# Date: 12/19/2016
# Description: Contains functions which support retrieving REST Service Directory Info

# import required modules
import urllib2, json

# ConnectToServer
def ConnectToServer(serverUrl):
    """
    Creates a live connection to a REST services directory
    """
    connectionUrl = serverUrl + "/?f=pjson"
    connection = json.loads(urllib2.urlopen(connectionUrl, '').read())

    return connection

# ListFolders
def ListFolders(serverUrl):
    """
    Returns a live list of folders contained within a certain services directory
    """
    connectionUrl = serverUrl + "/?f=pjson"
    serverConnection = json.loads(urllib2.urlopen(connectionUrl, '').read())
    if "folders" in serverConnection.keys():
        folders = serverConnection["folders"]
    else:
        folders = []

    return folders

# ListServicesByFolder
def ListServicesByFolder(serverUrl, folderName):
    """
    Returns a live list of services running in a given folder
    """
    connectionUrl = serverUrl + "/" + folderName + "/?f=pjson"
    serverConnection = json.loads(urllib2.urlopen(connectionUrl, '').read())
    services = serverConnection["services"]
    serviceList = []

    for service in services:
        serviceList.append("{} ({})".format(service["name"], service["type"]))

    return serviceList
   
    
# ListAllServices
def ListAllServices(serverUrl):
    """
    Lists all services contained within a REST service directory (includes subfolders)
    """
    # create empty list
    serviceList = []

    # connect to server root and add root services to service list
    connectionUrl = serverUrl + "/?f=pjson"
    serverConnection = json.loads(urllib2.urlopen(connectionUrl, '').read())
    rootServices = serverConnection["services"]
    for service in rootServices:
        serviceList.append("Root/{} ({})".format(service["name"], service["type"]))

    # list folders
    folders = ListFolders(serverUrl)

    # add the services in each list to the overall list
    for folder in folders:
        folderServices = ListServicesByFolder(serverUrl, folder)
        for service in folderServices:
            serviceList.append(service)

    # return the result
    return serviceList

# ListAllServicesByType
def ListAllServicesByType(serverUrl, serviceType):
    """
    Lists all services of a given type within a REST services directory
    Available Types:
        ImageServer
        GeometryServer
        FeatureServer
        MapServer
        GeoDataServer
        GPServer
        IndexGenerator
        SearchServer
        IndexingLauncher
    """
    # create empty list
    serviceList = []

    # connect to server root and add root services to service list
    connectionUrl = serverUrl + "/?f=pjson"
    serverConnection = json.loads(urllib2.urlopen(connectionUrl, '').read())
    rootServices = serverConnection["services"]
    for service in rootServices:
        if service["type"] == serviceType:
            serviceList.append("Root/{} ({})".format(service["name"], service["type"]))

    # list folders
    folders = ListFolders(serverUrl)

    # add the services in each list to the overall list
    for folder in folders:
        folderServices = ListServicesByFolder(serverUrl, folder)
        for service in folderServices:
            if service.split(" (")[1] == serviceType + ")":
                serviceList.append(service)

    return serviceList

# GetServiceCount
def GetServiceCount(serverUrl):
    """
    Returns an integer count of all services contained within a REST Service directory
    """
    return len(ListAllServices(serverUrl))

# GetServiceProperties
def GetServiceProperties(serverUrl, folderName, serviceName, serviceType):
    """
    Returns information about the service:
        Name
        Type
        Version Number
        Description
        Copyright
    """

    if folderName.upper() != "ROOT":
        connectionUrl = serverUrl + "/" + folderName + "/" + serviceName + "/" + serviceType + "/?f=pjson"
    else:
        connectionUrl = serverUrl + "/" + serviceName + "/" + serviceType + "/?f=pjson"

    serverConnection = json.loads(urllib2.urlopen(connectionUrl, '').read())

    if serviceType == "MapServer":
        properties = {"Name": serviceName,
                      "Type": serviceType,
                      "Version": serverConnection["currentVersion"],
                      "Description": serverConnection["serviceDescription"],
                      "Copyright": serverConnection["copyrightText"],
                      "Capabilities": serverConnection["capabilities"],
                      "Cached Map Service": serverConnection["singleFusedMapCache"]}
        
    if serviceType == "FeatureServer":
        properties = {"Name": serviceName,
                      "Type": serviceType,
                      "Version": serverConnection["currentVersion"],
                      "Description": serverConnection["serviceDescription"],
                      "Copyright": serverConnection["copyrightText"],
                      "Capabilities": serverConnection["capabilities"]}

    if serviceType == "ImageServer":
        properties = {"Name": serviceName,
                      "Type": serviceType,
                      "Version": serverConnection["currentVersion"],
                      "Description": serverConnection["serviceDescription"],
                      "Copyright": serverConnection["copyrightText"],
                      "Capabilities": serverConnection["capabilities"]}

    return properties

