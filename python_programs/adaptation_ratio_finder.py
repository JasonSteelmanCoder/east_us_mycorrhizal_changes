"""

This program connects to the PostgreSQL database, pulls down data from the east_us_tree, 
ref_species, and fire_adaptation tables. It outputs its findings to a csv file.

For this program to work, you need to have the tree table for each state compiled into one 
east_us_tree table.

This program accesses details for connecting to the database through a .env file. 


"""

# import libraries for connecting to database and getting details from .env file
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# start building the output by inserting the column titles of the output csv
output_contents = "statecd,countycd,adapted_area,intolerant_area,pct_adapted,excluded_bas_area,pct_area_excluded,am_area,em_area,pct_em,not_counted_area,pct_not_counted,region\n"

# connect to the database using details from the .env file
connection = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

# query east_us_plot to get every county in the eastern US
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

    # print for monitoring reasons
    count += 1
    print(f'Processing {statecd}  {unitcd}  {countycd}. Count: {count}')

    cursor.execute(f"""
        WITH trees AS (
            SELECT 
                east_us_tree.statecd AS statecd,
                east_us_tree.countycd AS countycd,
                east_us_tree.spcd AS spcd,
                fire_classification,
                ROUND(((PI() * (east_us_tree.dia::DECIMAL * 2.54 / 2) ^ 2) / 10000)::DECIMAL, 2) AS basal_area,
                ref_species.association
            FROM east_us_tree
            LEFT JOIN fire_adaptation
                ON east_us_tree.spcd = fire_adaptation.spcd
            LEFT JOIN ref_species
            ON ref_species.spcd = east_us_tree.spcd
            WHERE 
                east_us_tree.statecd = {statecd} 
                AND east_us_tree.countycd = {countycd}
        )
        SELECT 
            trees.statecd, 
        trees.countycd,
            COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) AS adapted_area,
            COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0) AS intolerant_area,
            -- note that pct_adapted is the percent of trees belonging to the 75 selected species that are adapted
            ROUND(COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) / (COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) + COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0)) * 100, 1) AS pct_adapted,
            COALESCE(SUM(CASE WHEN fire_classification IS NULL THEN basal_area END), 0) AS excluded_bas_area,  
            ROUND((SUM(CASE WHEN fire_classification IS NULL THEN basal_area END) / (SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END) + SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END) + SUM(CASE WHEN fire_classification IS NULL THEN basal_area END))) * 100, 2) AS pct_area_excluded,
            ROUND(COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + 0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) AS am_area,
            ROUND(COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + 0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) AS em_area,
            -- note that pct_em is the percent of trees belonging to the 75 selected species that are Ectomycorrhizal
            ROUND(((COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + (0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))) / (COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) + COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))) * 100, 1) AS pct_em,
            -- not_counted_area is the basal area of trees that are not part of the 75 species, plus ericoid sourwood trees
            COALESCE(SUM(CASE WHEN fire_classification IS NULL OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') THEN basal_area END), 0) AS not_counted_area,
            -- pct_not_counted is the not_counted_area as a percent of the total basal area in the county, including all species, association types, and fire adaptation types
            ROUND((COALESCE(SUM(CASE WHEN fire_classification IS NULL OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') THEN basal_area END), 0) / (COALESCE(SUM(CASE WHEN fire_classification IS NULL OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') THEN basal_area END), 0) + ROUND(COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) + ROUND(COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0), 2) + COALESCE(ROUND(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 2), 0))) * 100 , 2) AS pct_not_counted,
            east_us_region.region_id AS region
        FROM trees
        LEFT JOIN east_us_region
        ON east_us_region.statecd = trees.statecd AND east_us_region.countycd = trees.countycd  
        GROUP BY trees.statecd, trees.countycd, east_us_region.region_id;
    """)

    rows = cursor.fetchall()

    row_length = len(rows[0])

    # write the query results to output_contents
    for county_row in rows:            # (note that there is only one row per SQL query)
        for i in range(row_length - 1):
            if county_row[i] == 'None':
                output_contents += ','
            else:
                output_contents += f'{county_row[i]},'
        output_contents += f'{county_row[-1]}\n'

# once all county rows have been added to output_contents, write contents to a csv file
# note that this implementation gets part of the path from a .env file
# replace the path with the location where you want your csv file stored on your computer
with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/adaptation_by_county.csv", "w") as output_file:
    output_file.write(output_contents)

# clean up
cursor.close()
connection.close()