import sqlite3
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

df = pd.DataFrame(columns=['fips', 'statecd', 'countycd', 'fire_reports'])

conn = sqlite3.connect(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/jo_data_recent/data/FPA_FOD_20221014.sqlite')

cursor = conn.cursor()

cursor.execute('''
    SELECT fips_code, count(fips_code) 
    FROM fires 
    WHERE UPPER(TRIM(state)) IN ('PA', 'NH', 'MD', 'IL', 'TN', 'OH', 'KY', 'NY', 'NJ', 'MI', 'MA', 'AL', 'MS', 'IN', 'WV', 'VT', 'FL', 'ME', 'SC', 'WI', 'VA', 'NC', 'CT', 'DE', 'RI', 'GA')
    GROUP BY fips_code
''')

rows = cursor.fetchall()

for row in rows[1:]:
    row_df = pd.DataFrame({'fips':[row[0]], 'statecd':[str(row[0])[:2].lstrip('0')], 'countycd':[str(row[0])[-3:].lstrip('0')], 'fire_reports':[row[1]]})
    df = pd.concat([df, row_df])
    print('.', end='')

conn.close()

print('\n')
print(df)

df.to_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/fires_reported_by_county.csv', index=False)
