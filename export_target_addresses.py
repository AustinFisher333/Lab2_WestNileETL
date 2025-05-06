

import arcpy
import os

def export_addresses_to_csv():
    """
    Exports selected addresses from the 'Target_Addresses' feature class to a CSV file.

    Specifically, this function filters the addresses using a definition query
    (Join_Count = 1), meaning the address intersects with the spray zone defined
    in the 'final_analysis' layer. The result is exported as a CSV file for external use.

    Parameters:
    None

    Returns:
    None
    Output:
        - CSV file located at:
          C:/Users/valen/Documents/ArcGIS/GIS305/GeoSpatial Programming/westnileoutbreak/target_addresses.csv
    """
    try:
        # Set workspace
        gdb_path = r"C:\Users\valen\Documents\ArcGIS\GIS305\GeoSpatial Programming\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.gdb"
        arcpy.env.workspace = gdb_path
        arcpy.env.overwriteOutput = True

        input_table = "Target_Addresses"
        temp_layer = "Target_Addresses_Layer"
        csv_output_path = r"C:\Users\valen\Documents\ArcGIS\GIS305\GeoSpatial Programming\westnileoutbreak\target_addresses.csv"

        # Make layer and apply definition query
        arcpy.management.MakeFeatureLayer(input_table, temp_layer, "Join_Count = 1")
        arcpy.conversion.TableToTable(temp_layer, os.path.dirname(csv_output_path), os.path.basename(csv_output_path).replace(".csv", ""))
        print(f"✅ Exported to CSV at:\n{csv_output_path}")

    except Exception as e:
        print(f"❌ Error exporting addresses: {e}")


if __name__ == "__main__":
    export_addresses_to_csv()
