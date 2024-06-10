import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

output_contents = "statecd,unitcd,countycd,firedplots\n"

connection = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

cursor.execute(f"""
    SELECT statecd, unitcd, countycd 
    FROM east_us_plot 
    WHERE plot_status_cd = 1            -- exclude non-forest plots
    GROUP BY statecd, unitcd, countycd
""")

counties = cursor.fetchall()

count = 0

for county_row in counties:
    statecd = county_row[0]
    unitcd = county_row[1]
    countycd = county_row[2]

    count += 1
    print(f'Processing {statecd}  {unitcd}  {countycd}. Count: {count}')

    cursor.execute(f"""
        SELECT  east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, COUNT(east_us_plot.invyr) AS firedplots
        FROM east_us_cond 
        LEFT JOIN east_us_plot
        ON east_us_cond.plt_cn = east_us_plot.cn
        WHERE 
            east_us_plot.statecd = {statecd} AND east_us_plot.countycd = {countycd} AND
            east_us_plot.invyr > 1979 AND east_us_plot.invyr < 2023 AND
            (dstrbcd1 = 30 OR dstrbcd1 = 31 OR dstrbcd1 = 32
            or dstrbcd2 = 30  OR dstrbcd2 = 31 OR dstrbcd2 = 32
            or dstrbcd3 = 30  OR dstrbcd3 = 31 OR dstrbcd3 = 32 )
        GROUP BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd;
    """)


    rows = cursor.fetchall()

    if not rows:                        # no plots in the county had fire reported between 1980 and 2022 
        output_contents += f'{statecd},{unitcd},{countycd},0\n'

    else:
        for county_row in rows:            # (there is only one row per SQL query)
            output_contents += f'{statecd},{unitcd},{countycd},'
            output_contents += str(county_row[3])
            output_contents += '\n' 

with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_fire_occurreces.csv", "w") as output_file:
    output_file.write(output_contents)

cursor.close()
connection.close()