import arcpy
from etl.GSheetsEtl import GSheetsEtl
import yaml

def setup():
    with open("config/wnvoutbreak.yaml") as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
        return config_dict

def etl():
    print("🚀 Starting ETL process...")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

if __name__ == "__main__":
    global config_dict
    config_dict = setup()
    etl()

    # Run your spatial join afterward
    arcpy.env.workspace = config_dict.get("destination")
    arcpy.env.overwriteOutput = True

    target_features = "Addresses"
    join_features = "Intersect_Buffered_Layers"
    output_feature_class = "Addresses_At_Risk"

    arcpy.analysis.SpatialJoin(
        target_features,
        join_features,
        output_feature_class,
        "JOIN_ONE_TO_ONE",
        "KEEP_COMMON",
        match_option="INTERSECT"
    )

    print(f"✅ Spatial Join complete. At-risk addresses saved to: {output_feature_class}")

    # Count result addresses
    count = int(arcpy.management.GetCount(output_feature_class)[0])
    print(f"📌 Number of addresses within the area of concern: {count}")
