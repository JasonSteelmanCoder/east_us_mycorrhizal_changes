"""

This program connects to the database. It pulls all of the counties in the eastern US from 
the east_us_plot table. Then, for each county, it uses the east_us_cond table to find all 
of the instances where a plot was reported to have fire damage in that county during the 
study period (1980 to 2022).

For this program to work, you need to have the plot, and cond tables for each state 
downloaded from the FIA database. Those then need to be put into a local postgres database. 
The state-by-state plot and cond tables will need to be merged into east_us_plot, and 
east_us_cond tables respectively.

This program accesses details for connecting to the database through a .env file. 

"""

# import libraries to help us connect to the database and access the .env file
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# start the output contents by inserting the titles of each column in the output csv
output_contents = "statecd,unitcd,countycd,burnedplots\n"

# Connect to the database using details from the .env file
# On your local computer, you can replace the os.getenv() calls with the details of your 
# own database
connection = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

# from the east_us_plot table, get the details of every county in the eastern US
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

    # print for monitoring purposes
    count += 1
    print(f'Processing {statecd}  {unitcd}  {countycd}. Count: {count}')

    # count all instances where fire damage was reported on a plot in the county between 1980 and 2022 
    cursor.execute(f"""
        SELECT  east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, COUNT(east_us_plot.invyr) AS burnedplots
        FROM east_us_cond 
        LEFT JOIN east_us_plot
        ON east_us_cond.plt_cn = east_us_plot.cn
        WHERE 
            east_us_plot.statecd = {statecd} AND east_us_plot.countycd = {countycd} AND
            east_us_plot.invyr > 1998 AND east_us_plot.invyr < 2023 AND
            (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND
            (dstrbcd1 = 30 OR dstrbcd1 = 31 OR dstrbcd1 = 32
            or dstrbcd2 = 30  OR dstrbcd2 = 31 OR dstrbcd2 = 32
            or dstrbcd3 = 30  OR dstrbcd3 = 31 OR dstrbcd3 = 32 )
        GROUP BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd;
    """)

    rows = cursor.fetchall()

    # write the counties to output_contents
    if not rows:                        # no plots in the county had fire reported between 1980 and 2022 
        output_contents += f'{statecd},{unitcd},{countycd},0\n'

    else:
        for county_row in rows:            # (there is only one row per SQL query)
            output_contents += f'{statecd},{unitcd},{countycd},'
            output_contents += str(county_row[3])
            output_contents += '\n' 

# write output_contents to a csv file
# replace the path with the location where you want the csv file to be written on your computer
with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_fire_occurreces.csv", "w") as output_file:
    output_file.write(output_contents)

# clean up
cursor.close()
connection.close()