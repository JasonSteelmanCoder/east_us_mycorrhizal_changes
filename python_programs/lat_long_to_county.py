import requests
import json
import pandas as pd

# choose your variables
site_name = "EHFenced1"
latitude = "42.44318871"
longitude = "-76.40273319"

# prepare to collect the data
fips_dict = {"site_name": [], "fips": []}

# connect to the API
url = "https://geo.fcc.gov/api/census/block/find"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "format": "json",
}

response = requests.get(url, params)

# put the site name in the dictionary
fips_dict["site_name"].append(site_name)

# give the site a county or None
if response.status_code == 200:
    response_dict = json.loads(response.text)
    fips_dict["fips"].append(response_dict["County"]["FIPS"])
else:
    print(f"Error on site {site_name}: {response.text}")
    fips_dict["fips"].append(None)

# turn it all into a dataframe
fips = pd.DataFrame(fips_dict)

print('\n')
print(fips)
