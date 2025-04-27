import arcpy
import yaml
import logging
from etl.GSheetsEtl import GSheetsEtl

def setup():
    with open("config/wnvoutbreak.yaml") as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
        return config_dict

def etl():
    logging.info("🚀 Starting ETL process...")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

def main():
    logging.info("🧭 Starting Spatial Join...")
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

    logging.info(f"✅ Spatial Join complete. Saved to {output_feature_class}")

    count = int(arcpy.management.GetCount(output_feature_class)[0])
    logging.info(f"📌 Number of addresses within area of concern: {count}")

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        filename=f"{setup().get('proj_dir')}/wnvlog.log",
        filemode="w",
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Global config
    global config_dict
    config_dict = setup()

    # ETL + Spatial Join
    etl()
    main()
