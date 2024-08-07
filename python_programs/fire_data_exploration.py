import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/fire_data_sqlite/Data/FPA_FOD_20221014.sqlite')

cursor = conn.cursor()

cursor.execute("SELECT * FROM fires LIMIT 1")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()