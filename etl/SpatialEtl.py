class SpatialEtl:
    def __init__(self, config_dict):
        self.config_dict = config_dict

    def extract(self):
        print(f"Extracting data from {self.config_dict.get('remote_url')} to {self.config_dict.get('proj_dir')}")

        import requests
        r = requests.get(self.config_dict.get("remote_url"))
        r.encoding = "utf-8"
        data = r.text

        with open(f"{self.config_dict.get('proj_dir')}/addresses.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        print(f"Transforming {self.config_dict.get('data_format')}")

        import csv

        transformed_path = f"{self.config_dict.get('proj_dir')}/new_addresses.csv"
        source_path = f"{self.config_dict.get('proj_dir')}/addresses.csv"

        transformed_file = open(transformed_path, "w")
        transformed_file.write("X,Y,Type\n")

        with open(source_path, "r") as partial_file:
            csv_dict = csv.DictReader(partial_file, delimiter=",")
            for row in csv_dict:
                address = row["Street Address"] + ", Boulder CO"
                print(address)

                geocode_url = (
                    self.config_dict.get("geocoder_prefix_url")
                    + address
                    + self.config_dict.get("geocoder_suffix_url")
                )

                r = requests.get(geocode_url)
                resp_dict = r.json()

                x = resp_dict["result"]["addressMatches"][0]["coordinates"]["x"]
                y = resp_dict["result"]["addressMatches"][0]["coordinates"]["y"]

                transformed_file.write(f"{x},{y},Residential\n")

        transformed_file.close()

    def load(self):
        print(f"Loading data into {self.config_dict.get('destination')}")

        import arcpy
        arcpy.env.workspace = self.config_dict.get("destination")
        arcpy.env.overwriteOutput = True

        in_table = f"{self.config_dict.get('proj_dir')}/new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"

        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)
        print(arcpy.GetCount_management(out_feature_class))
