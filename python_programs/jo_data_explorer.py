import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/jo_data_recent/data/FPA_FOD_20221014.sqlite')

cursor = conn.cursor()

cursor.execute('''
    SELECT fips_code, count(fips_code) 
    FROM fires 
    WHERE UPPER(TRIM(state)) IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    group by fips_code
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
    # group by state

# GET FIRES REPORTED PER COUNTY
    # SELECT fips_code, count(fips_code) 
    # FROM fires 
    # WHERE UPPER(TRIM(state)) IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    # group by fips_code