import requests
import json
import pandas as pd
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# prepare to collect the data
fips_dict = {"site_name": [], "fips": [], "statecd": [], "countycd": []}

# get the input data from the csv file
with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/phillips_us_sites.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    for row in reader:
        print(".", end="")
        site_name = row[0]
        latitude = row[1]
        longitude = row[2]

        # call the API
        url = "https://geo.fcc.gov/api/census/block/find"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "format": "json",
        }

        response = requests.get(url, params)

        # give the site a county or None
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            new_fips = response_dict["County"]["FIPS"]
            fips_dict["site_name"].append(site_name)
            fips_dict["fips"].append(new_fips)
            fips_dict["statecd"].append(str(new_fips[:2]))
            fips_dict["countycd"].append(str(new_fips[2:]).lstrip('0'))
        else:
            print(f"\nError on site {site_name}: {response.text}")

# turn it all into a dataframe
fips = pd.DataFrame(fips_dict)

fips.to_csv(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/phillips_sites_fips.csv', index=False)