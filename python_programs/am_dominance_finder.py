"""



"""

# import libraries for connecting to database and getting details from .env file
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# start building the output by inserting the column titles of the output csv
output_contents = "statecd,unitcd,countycd,tot_bas_t1,ambasar_t1,embasar_t1,am_dom_t1,tot_bas_t2,ambasar_t2,embasar_t2,am_dom_t2,dif_am_dom\n"

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

    # check every tree in a county for AM/EM association, and sum all AM basal area and EM basal area
    # find AM dominance by county by dividing the AM area by the total AM and EM area
    # trees that are both AM and EM have half of their basal area counted as AM and the other half as AM
    # do this process once for T1 and again for T2
    # finally, select all of the values that should go into the output csv
    cursor.execute(f"""
        
        -- get the AM dom measurement for each plot in the county at T1
        WITH plots AS (
            WITH trees AS (
                WITH min_year_of_plot AS (
                    -- find the earliest year of observation for each plot
                    SELECT MIN(invyr), east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot
                    FROM east_us_plot
                    WHERE east_us_plot.invyr > 1979 AND east_us_plot.invyr < 1999
                    GROUP BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot
                    ORDER BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot, min
                )
                -- grab all of the trees in the county that are part of a first observation
                SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 3) as basal_area, east_us_tree.spcd, ref_species.association
                FROM east_us_tree 
                LEFT JOIN ref_species
                ON east_us_tree.spcd = ref_species.spcd
                LEFT JOIN east_us_cond
                ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
                JOIN min_year_of_plot
                ON east_us_tree.invyr = min_year_of_plot.min AND east_us_tree.statecd = min_year_of_plot.statecd AND east_us_tree.unitcd = min_year_of_plot.unitcd AND east_us_tree.countycd = min_year_of_plot.countycd AND east_us_tree.plot::text = min_year_of_plot.plot::text 
                WHERE 

                east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1

                east_us_tree.statecd = {statecd} AND  
                east_us_tree.unitcd = {unitcd} AND
                east_us_tree.countycd = {countycd} AND 

                (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
                east_us_tree.statuscd = 1			-- only count live trees

                ORDER BY statecd, unitcd, countycd, plot, subp, tree
            )
            -- grab plots and their associated AM and EM basal_areas
            SELECT 
                statecd, 
                unitcd, 
                countycd, 
                plot, 
                SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) AS am_basal_area, 
                SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END) AS em_basal_area, 
                SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END)::DOUBLE PRECISION / (SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) + SUM(CASE WHEN association != 'AM' THEN basal_area ELSE 0 END))::DOUBLE PRECISION AS am_dom
            FROM trees
            GROUP BY statecd, unitcd, countycd, plot
        )
        -- grab the county's average am dom, over all of its plots
        SELECT statecd, unitcd, countycd, AVG(am_dom) AS am_dom_t1
        FROM plots
        GROUP BY statecd, unitcd, countycd
        ORDER BY statecd, unitcd, countycd

    """)


    rows = cursor.fetchall()

    row_length = len(rows[0])

    # write the query results to output_contents
    for county_row in rows:            # (there is only one row per SQL query)
        output_contents += f'{statecd},{unitcd},{countycd},'
        for i in range(row_length - 1):
            if county_row[i] == 'None':
                output_contents += ','
            else:
                output_contents += f'{county_row[i]},'
        output_contents += f'{county_row[-1]}\n'

# once all county rows have been added to output_contents, write contents to a csv file
# note that this implementation gets part of the path from a .env file
# replace the path with the location where you want your csv file stored on your computer
with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_am_dominance.csv", "w") as output_file:
    output_file.write(output_contents)

# clean up
cursor.close()
connection.close()