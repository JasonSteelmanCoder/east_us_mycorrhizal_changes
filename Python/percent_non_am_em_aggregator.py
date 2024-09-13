import os
from dotenv import load_dotenv
import csv
import pandas as pd

load_dotenv()

county_data = pd.read_csv(f"C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/percent_non_am_em_basal_area.csv")

print(county_data)

t1_mean = (county_data['other_basal_area_t1'].sum() / county_data['total_basal_area_t1'].sum()) * 100
t2_mean = (county_data['other_basal_area_t2'].sum() / county_data['total_basal_area_t2'].sum()) * 100

print(f"mean percent non am/em at T1: {t1_mean}")
print(f"mean percent non am/em at T2: {t2_mean}")