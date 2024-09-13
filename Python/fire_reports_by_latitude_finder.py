import sqlite3
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

results = []

conn = sqlite3.connect(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/jo_data_recent/data/FPA_FOD_20221014.sqlite')

cursor = conn.cursor()

cursor.execute('''
    SELECT latitude, longitude, discovery_date
    FROM fires 
    WHERE state IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    GROUP BY latitude, longitude, discovery_date
''')

rows = cursor.fetchall()

i = 0

for row in rows:
    date = datetime.strptime(row[2], '%m/%d/%Y')
    results.append([row[0], row[1], date])
    if i % 100 == 0:
        print('.', end='')
    i += 1

df = pd.DataFrame(results, columns=['latitude', 'longitude', 'discovery_date'])

conn.close()

df = df.sort_values(by="discovery_date")
df.to_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/fire_report_unique_lat_long_dates.csv', index=False)