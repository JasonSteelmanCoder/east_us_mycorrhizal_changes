import geopandas as gpd
from dotenv import load_dotenv
import os

load_dotenv()

gdf = gpd.read_file(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/cb_2018_us_county_500k/cb_2018_us_county_500k.shp')

print(gdf.head)