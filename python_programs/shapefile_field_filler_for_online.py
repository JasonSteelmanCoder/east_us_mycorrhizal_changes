import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv
import os

load_dotenv()

csv_file_path = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_percents_and_ratios_by_plot.csv'
df = pd.read_csv(csv_file_path)

# cast some parts of csv df to text to preserve "None"

# remove the diff column from csv df


shapefile_path = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_shapefile/east_us_shapefile.shp'
gdf = gpd.read_file(shapefile_path)

gdf["STATEFP"] = gdf["STATEFP"].astype(int)     # cast STATEFP to allow comparison with statecd
gdf["COUNTYFP"] = gdf["COUNTYFP"].astype(int)

gdf = gdf.merge(df, left_on=["STATEFP", "COUNTYFP"], right_on=["statecd", "countycd"], how="left")

# DEBUGGING
# print(gdf[["STATEFP", "COUNTYFP"]].head())
# print(df[["statecd", "countycd"]].head())

gdf.to_file(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_shapefile_online.shp')