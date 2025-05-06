import arcpy
import os

def spatial_join_and_filter(aprx):
    """
    Performs a spatial join between the 'Addresses' feature class and the 'final_analysis' layer.
    The result is stored as 'Target_Addresses' in the current geodatabase. After creating the output,
    this function adds the layer to the map and applies a definition query to show only those records
    where Join_Count = 1, indicating the address intersects with the spray zone.

    Parameters:
    aprx (arcpy.mp.ArcGISProject): The ArcGIS Pro project object to which the output layer will be added.

    Returns:
    None
    """
    try:
        arcpy.env.workspace = r"C:\Users\valen\Documents\ArcGIS\GIS305\GeoSpatial Programming\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.gdb"
        arcpy.env.overwriteOutput = True

        target = "Addresses"
        join_features = "final_analysis"
        output = "Target_Addresses"

        print("🔄 Running spatial join...")
        arcpy.analysis.SpatialJoin(target, join_features, output)
        print("✅ Created Target_Addresses with spatial join.")

        # Add layer to map
        map_doc = aprx.listMaps()[0]
        gdb_path = arcpy.env.workspace
        output_layer_path = os.path.join(gdb_path, output)
        map_doc.addDataFromPath(output_layer_path)
        print("🗺️  Added Target_Addresses layer to the map.")

        # Apply definition query
        for lyr in map_doc.listLayers():
            if lyr.name == "Target_Addresses":
                lyr.definitionQuery = "Join_Count = 1"
                print("✅ Applied definition query to Target_Addresses.")
                return
        print("⚠️ Target_Addresses layer still not found after adding.")
    except Exception as e:
        print(f"❌ Error in spatial_join_and_filter: {e}")


if __name__ == "__main__":
    aprx_path = os.path.normpath(
        r"C:/Users/valen/Documents/ArcGIS/GIS305/GeoSpatial Programming/westnileoutbreak/WestNileOutbreak/WestNileOutbreak.aprx"
    )
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    spatial_join_and_filter(aprx)
