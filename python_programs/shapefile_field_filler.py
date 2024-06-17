"""
This program adds data from a csv file into a shapefile as fields on the layer.

Replace the paths of the input csv, the input shapefile, and the output shapefile to match 
the desired locations on your computer.

"""

import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv
import os

load_dotenv()

# read in the input csv file
csv_file_path = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_percents_and_ratios_by_plot.csv'
df = pd.read_csv(csv_file_path)

# read in the input shapefile
shapefile_path = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_shapefile/east_us_shapefile.shp'
gdf = gpd.read_file(shapefile_path)

gdf["STATEFP"] = gdf["STATEFP"].astype(int)     # cast STATEFP to allow comparison with statecd
gdf["COUNTYFP"] = gdf["COUNTYFP"].astype(int)

gdf = gdf.merge(df, left_on=["STATEFP", "COUNTYFP"], right_on=["statecd", "countycd"], how="left")

# output a new shapefile including the data from the input csv file as fields
gdf.to_file(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_shapefile.shp')