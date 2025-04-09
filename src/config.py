import os

import yaml

if os.path.exists("config.yaml"):
    print("Config file found.")

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

DATASET_NAME = config["dataloader"]["dataset_name"]
DATASET_FILE = config["dataloader"]["dataset_file"]

COLUMNS_PIECHART = config["columns"]["piechart"]
COLUMNS_BARPLOT = config["columns"]["barplot"]
COLUMNS_GEOMAP = config["columns"]["geomap"]
COLUMNS_LINECHART = config["columns"]["linechart"]
COLUMNS_BENTBOXES = config["columns"]["bentoboxes"]
