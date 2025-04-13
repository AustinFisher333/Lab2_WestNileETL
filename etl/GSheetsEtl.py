from etl.SpatialEtl import SpatialEtl
import requests
import arcpy
import csv

class GSheetsEtl(SpatialEtl):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def extract(self):
        print("📥 Extracting addresses from Google Form...")

        r = requests.get(self.config_dict.get("remote_url"))
        r.encoding = "utf-8"
        data = r.text

        with open(f"{self.config_dict.get('proj_dir')}/addresses.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        print("🔄 Geocoding addresses and writing new CSV...")

        transformed_path = f"{self.config_dict.get('proj_dir')}/new_addresses.csv"
        source_path = f"{self.config_dict.get('proj_dir')}/addresses.csv"

        with open(transformed_path, "w") as transformed_file:
            transformed_file.write("X,Y,Type\n")

            with open(source_path, "r") as partial_file:
                csv_dict = csv.DictReader(partial_file, delimiter=",")
                for row in csv_dict:
                    address = row["Address"] + ", Boulder CO"
                    print(f"Geocoding: {address}")

                    geocode_url = (
                            self.config_dict.get("geocoder_prefix_url")
                            + address
                            + self.config_dict.get("geocoder_suffix_url")
                    )

                    try:
                        r = requests.get(geocode_url, timeout=5)
                        r.raise_for_status()  # will raise for 4xx/5xx errors
                        resp_dict = r.json()

                        matches = resp_dict["result"]["addressMatches"]
                        if matches:
                            x = matches[0]["coordinates"]["x"]
                            y = matches[0]["coordinates"]["y"]
                            transformed_file.write(f"{x},{y},Residential\n")
                        else:
                            print(f"⚠️ No geocode match for: {address}")

                    except Exception as e:
                        print(f"❌ Failed to geocode {address}: {e}")

    def load(self):
        print("📍 Loading avoid points into GIS...")

        arcpy.env.workspace = self.config_dict.get("destination")
        arcpy.env.overwriteOutput = True

        in_table = f"{self.config_dict.get('proj_dir')}/new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"

        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)
        print(arcpy.GetCount_management(out_feature_class))

    def process(self):
        self.extract()
        self.transform()
        self.load()
