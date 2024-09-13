import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/jo_data_recent/data/FPA_FOD_20221014.sqlite')

cursor = conn.cursor()

cursor.execute('''
    SELECT NWCG_CAUSE_CLASSIFICATION, NWCG_GENERAL_CAUSE
    FROM fires 
    WHERE state IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    GROUP BY NWCG_CAUSE_CLASSIFICATION, NWCG_GENERAL_CAUSE
    ORDER BY NWCG_CAUSE_CLASSIFICATION, NWCG_GENERAL_CAUSE
''')

rows = cursor.fetchall()

for row in rows:
    print(f'{row}')

conn.close()


# GET COLUMN NAMES:
    # PRAGMA table_info(fires)

# GET FIRST ROW
    # SELECT * FROM fires LIMIT 1

# GET YEARS
    # SELECT fire_year, count(fire_year) FROM fires GROUP BY fire_year 

# GET FIRE COUNT BY STATE IN EAST
    # SELECT state, count(state) 
    # FROM fires 
    # WHERE UPPER(TRIM(state)) IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    # GROUP BY state

# GET FIRES REPORTED PER COUNTY
    # SELECT fips_code, count(fips_code) 
    # FROM fires 
    # WHERE UPPER(TRIM(state)) IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    # GROUP BY fips_code

# FIND DUPLICATE FIRES
    # SELECT latitude, longitude, fire_year, COUNT(fire_year) AS count
    # FROM fires 
    # WHERE state IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    # GROUP BY latitude, longitude, fire_year
    # ORDER BY count

# EXAMINE ONE EXAMPLE OF DUPLICATE FIRES
    # SELECT *
    # FROM fires 
    # WHERE latitude = '41.913769' AND longitude = '-71.908096'

# FIND DUPLICATES WHEN GROUPING BY DATE
    # SELECT latitude, longitude, discovery_date, COUNT(discovery_date) AS count
    # FROM fires 
    # WHERE state IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    # GROUP BY latitude, longitude, discovery_date
    # ORDER BY count

# EXAMINE ONE EXAMPLE OF A DUPLICATE WHEN GROUPING BY DATE
    # SELECT *
    # FROM fires 
    # WHERE latitude = '31.3955' AND longitude = '-82.8381' AND discovery_date = '12/14/1995'

# PUT INDEX ON fires
    # CREATE INDEX unique_fires
    # ON fires(latitude, longitude, discovery_date)