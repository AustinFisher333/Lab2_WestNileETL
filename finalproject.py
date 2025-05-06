import arcpy

def set_spatial_reference(aprx):
    """
finalproject.py

Sets spatial reference and creates 'final_analysis' by erasing
sensitive zones (avoid_points_buf) from high-risk mosquito areas.

Author: Valen (Austin) Fisher
Date: May 2025
"""

    try:
        map_doc = aprx.listMaps()[0]
        state_plane_noco = arcpy.SpatialReference(102653)
        map_doc.spatialReference = state_plane_noco
        print("✅ Spatial reference set to NAD 1983 StatePlane Colorado North.")
    except Exception as e:
        print(f"❌ Error in set_spatial_reference: {e}")

def create_final_analysis():
    """Creates 'final_analysis' by erasing 'avoid_points_buf' from 'Intersect_Buffered_Layers'."""
    try:
        arcpy.env.workspace = r"C:\Users\valen\Documents\ArcGIS\GIS305\GeoSpatial Programming\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.gdb"
        arcpy.env.overwriteOutput = True

        input_layer = "Intersect_Buffered_Layers"
        erase_layer = "avoid_points_buf"
        output_layer = "final_analysis"

        arcpy.analysis.Erase(input_layer, erase_layer, output_layer)
        print("✅ Created 'final_analysis' layer.")
    except Exception as e:
        print(f"❌ Error in create_final_analysis: {e}")

def debug_list_layers(aprx):
    """Prints the names of all layers in the current map."""
    try:
        map_doc = aprx.listMaps()[0]
        layers = map_doc.listLayers()
        print("📋 Layers currently in the map:")
        for lyr in layers:
            print(" -", lyr.name)
    except Exception as e:
        print(f"❌ Error in debug_list_layers: {e}")

def apply_simple_renderer(aprx):
    """Apply a red fill with black outline and 50% transparency to 'final_analysis'."""
    try:
        map_doc = aprx.listMaps()[0]
        found = False

        for lyr in map_doc.listLayers():
            if lyr.name == "final_analysis" and lyr.isFeatureLayer:
                found = True
                sym = lyr.symbology
                sym.updateRenderer('SimpleRenderer')
                sym.renderer.symbol.applySymbolFromGallery("Red fill (50% transparency)")
                lyr.symbology = sym
                print("✅ Simple renderer applied to 'final_analysis' layer.")
                break

        if not found:
            print("⚠️ 'final_analysis' layer was not found as a feature layer.")

    except Exception as e:
        print(f"❌ Error in apply_simple_renderer: {e}")

# MAIN EXECUTION
if __name__ == "__main__":
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    set_spatial_reference(aprx)
    create_final_analysis()
    debug_list_layers(aprx)
    apply_simple_renderer(aprx)
