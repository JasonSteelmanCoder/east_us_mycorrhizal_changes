import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

connection = psycopg2.connect(
    dbname = os.getenv('DBNAME'),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

cursor.execute("""

    WITH counting AS (
    SELECT statecd, unitcd, countycd, plot, subp, tree, COUNT(invyr) AS num_obs, MIN(invyr) AS obs_1_year, MAX(invyr) AS obs_2_year 
    FROM east_us_tree
    WHERE statuscd = 1					-- only accept live trees
    GROUP BY statecd, unitcd, countycd, plot, subp, tree 
    ORDER BY COUNT(invyr)
    )
    SELECT * 
    FROM counting
    WHERE num_obs > 1

""")

rows = cursor.fetchall()

# for row in rows: 
#   ...
cursor.execute(f"""

    SELECT east_us_cond.invyr, trtcd1, trtcd2, trtcd3 
    FROM east_us_cond 
    WHERE 
        east_us_cond.statecd = {rows[0][0]}
        AND east_us_cond.unitcd = {rows[0][1]}
        AND east_us_cond.countycd = {rows[0][2]}    
        AND east_us_cond.plot = {rows[0][3]}::text
    ORDER BY east_us_cond.invyr

""")

treatments = cursor.fetchall()

print(treatments)