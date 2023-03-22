# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import os
import zipfile
import datetime

#Get a list of dates for which drought data are available (every 7 days starting 20220104)
start_date = datetime.date(2022, 1, 4)
end_date = datetime.date(2025, 12, 31)

date_list = []
current_date = start_date

while current_date <= end_date:
    date_list.append(current_date.strftime("%Y%m%d"))
    current_date += datetime.timedelta(days=7)

#Convert list to numeric
date_list = [eval(i) for i in date_list]
    
######Calculate dates 90 and 365 days ago
# Get today's date
today = datetime.date.today()

# Subtract 90 days
import datetime

# Get today's date
today = datetime.date.today()

# Calculate the date 90 days ago
delta = datetime.timedelta(days=90)
days_ago_90 = today - delta

# Format the date as YYYYMMDD
days90 = int(days_ago_90.strftime('%Y%m%d'))

# Calculate the date 365 days ago
delta = datetime.timedelta(days=365)
days_ago_365 = today - delta

# Format the date as YYYYMMDD
days365 = int(days_ago_365.strftime('%Y%m%d'))


########## Calculate closest date to 90 and 180 days ago
    
def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
     
#### Driver code
print("90 days ago was:", days90)
data90 = closest(date_list, days90)
print("Closest data to 90 days ago is:", data90)
print("365 days ago was:", days365)
data365 = closest(date_list, days365)
print("Closest data to 365 days ago is:", data365)

#Create url variables
url = 'https://droughtmonitor.unl.edu/data/shapefiles_m/USDM_current_M.zip'
url2 = url.replace('current', str(data90))
url3 = url.replace('current', str(data365))

########## Download the current data from the URL

response = requests.get(url)

with open('USDM_current_M.zip', 'wb') as f:
    f.write(response.content)

# Set up the ArcGIS Pro project and geodatabase
project = arcpy.mp.ArcGISProject('CURRENT')
map_view = project.activeView
gdb_name = 'USDM_data.gdb'
gdb_path = os.path.join(os.path.dirname(project.filePath), gdb_name)
if not arcpy.Exists(gdb_path):
    arcpy.management.CreateFileGDB(os.path.dirname(project.filePath), gdb_name)

# Extract the shapefile from the downloaded ZIP file
zipfile.ZipFile('USDM_current_M.zip').extractall('.')

# Import the shapefile into the geodatabase
shp_path = './USDM_current_M/dm_export.shp'
if arcpy.Exists(shp_path):
    arcpy.management.FeatureClassToFeatureClass(shp_path, gdb_path, 'USDM')

######### This section currently not working.#############
# Create a feature layer from the imported shapefile
fc_path = f'{gdb_path}/USDM'
if arcpy.Exists(fc_path):
    layer_name = 'USDM'
    arcpy.MakeFeatureLayer_management(fc_path, layer_name)
    layer = map_view.map.addLayer(layer_name).layer
    map_view.camera.setExtent(layer.getExtent())
    arcpy.RefreshActiveView()

##########################################################    


# Pull data from three months ago into ArcGIS
response2 = requests.get(url2)    
filename2 = str('USDM_'+str(data90)+'_M.zip')

with open(filename2, 'wb') as f:
    f.write(response2.content)
    
# Extract the shapefile from the downloaded ZIP file
zipfile.ZipFile(filename2).extractall('.')

# Import the shapefile into the geodatabase
shp_path = str('./'+filename2+'/dm_export.shp')
if arcpy.Exists(shp_path):
    arcpy.management.FeatureClassToFeatureClass(shp_path, gdb_path, 'USDM_3month')

    
# Pull data from 1 year ago into ArcGIS
response3 = requests.get(url3)    
filename3 = str('USDM_'+str(data365)+'_M.zip')

with open(filename3, 'wb') as f:
    f.write(response3.content)
    
# Extract the shapefile from the downloaded ZIP file
zipfile.ZipFile(filename3).extractall('.')

# Import the shapefile into the geodatabase
shp_path = str('./'+filename3+'/dm_export.shp')
if arcpy.Exists(shp_path):
    arcpy.management.FeatureClassToFeatureClass(shp_path, gdb_path, 'USDM_1year')
