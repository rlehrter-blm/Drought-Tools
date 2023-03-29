import arcpy

# set the workspace to the geodatabase that contains the feature classes
arcpy.env.workspace = r"C:\data\my_geodatabase.gdb"

# create a list of feature classes in the geodatabase
feature_classes = arcpy.ListFeatureClasses()

# define the new spatial reference
new_sr = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")

# loop through the feature classes and reproject each one to the new spatial reference
for feature_class in feature_classes:
    # define the current spatial reference of the feature class
    current_sr = arcpy.Describe(feature_class).spatialReference
    
    # check if the current spatial reference is the same as the new spatial reference
    if current_sr.name != new_sr.name:
        # if not, reproject the feature class
        arcpy.management.Project(feature_class, f"{feature_class}_WMAS", new_sr)
