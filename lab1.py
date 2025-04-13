import arcpy

# Set environment
arcpy.env.workspace = r"C:\Users\valen\Documents\ArcGIS\GIS305\GeoSpatial Programming\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.gdb"
arcpy.env.overwriteOutput = True

# Inputs
target_features = "Addresses"
join_features = "Intersect_Buffered_Layers"
output_feature_class = "Addresses_At_Risk"

# Spatial Join
arcpy.analysis.SpatialJoin(target_features, join_features, output_feature_class, "JOIN_ONE_TO_ONE", "KEEP_COMMON", match_option="INTERSECT")

print(f"Spatial Join complete. At-risk addresses saved to: {output_feature_class}")

# Count addresses within the area of concern (Extra Credit)
count = int(arcpy.management.GetCount(output_feature_class)[0])
print(f"Number of addresses within the area of concern: {count}")
