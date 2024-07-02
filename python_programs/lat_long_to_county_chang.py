import requests
import json
import pandas as pd
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# prepare to collect the data
fips_dict = {"species": [], "fips": [], "statecd": [], "countycd": []}

# get the input data from the csv file
with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/Chang et al supplement.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    for row in reader:
        if row[1] != "Ontario":
            print(".", end="")
            species = row[0]
            latitude = row[2]
            longitude = row[3]

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
                if new_fips != None:
                    fips_dict["species"].append(species)
                    fips_dict["fips"].append(new_fips)
                    fips_dict["statecd"].append(str(new_fips[:2]).lstrip('0'))
                    fips_dict["countycd"].append(str(new_fips[2:]).lstrip('0'))
            else:
                print(f"\nFIP not found for {species}. \nReport: {response.text}")

# turn it all into a dataframe
fips = pd.DataFrame(fips_dict)

fips.to_csv(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/chang_fips.csv', index=False)