"""

This program connects to the PostgreSQL database, pulls down data from the east_us_tree, 
east_us_cond, east_us_plot, and ref_species tables, then processes the data to find AM dominance at T1 
and T2, as well as the difference between them. It outputs its findings to a csv file.

For this program to work, you need to have the tree, plot, and cond tables for each state, and 
the ref_species table downloaded from the FIA database. Those then need to be put into a 
local postgres database. The state-by-state cond and tree tables will need to be merged 
into east_us_tree, east_us_plot, and east_us_cond tables respectively.

This program accesses details for connecting to the database through a .env file. 

"""

# import libraries for connecting to database and getting details from .env file
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

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
    GROUP BY statecd, unitcd, countycd
""")

counties = cursor.fetchall()

counties_data = []

count = 0

for county_row in counties:
    statecd = county_row[0]
    unitcd = county_row[1]
    countycd = county_row[2]

    # print for monitoring reasons
    count += 1
    print(f'Processing {statecd}  {unitcd}  {countycd}. Count: {count}')

    # 
    cursor.execute(f"""

        WITH plots AS (
          WITH observations_of_plots AS (
            WITH obs_of_trees_in_county AS (
              -- grab all observations of trees in the county
              SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 5) as basal_area, east_us_tree.spcd, ref_species.association
              FROM east_us_tree 
              LEFT JOIN ref_species
              ON east_us_tree.spcd = ref_species.spcd
              LEFT JOIN east_us_cond
              ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND east_us_tree.plot = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
              WHERE 

              east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1

              east_us_tree.statecd = {statecd} AND  
              east_us_tree.unitcd = {unitcd} AND
              east_us_tree.countycd = {countycd} AND 

              east_us_cond.stdorgcd = 0 AND	-- exclude timberland
              east_us_tree.statuscd = 1			-- only count live trees

              ORDER BY statecd, unitcd, countycd, plot, subp, tree
            )
            -- grab each observation of a plot, aggregating tree measurements from that observation
            SELECT 
              invyr, 
              statecd, 
              unitcd, 
              countycd, 
              plot, 
              SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) AS am_bas_area_t1,
              SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END) AS em_bas_area_t1,
              SUM(basal_area) AS total_bas_area_t1,
              CASE WHEN (SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) + SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END)) = 0 THEN 0 ELSE SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END)::double precision / (SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) + SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END))::double precision END AS am_dom_t1
            FROM obs_of_trees_in_county
            GROUP BY invyr, statecd, unitcd, countycd, plot
            ORDER BY statecd, unitcd, countycd, plot
          )
          -- grab each plot, averaging am_dom's where there are multiple years
          SELECT statecd, unitcd, countycd, plot, AVG(am_dom_t1) AS am_dom_t1
          FROM observations_of_plots
          GROUP BY statecd, unitcd, countycd, plot
          ORDER BY statecd, unitcd, countycd, plot
        )
        -- grab the county, averaging the am_dom of the plots in it
        SELECT 
          statecd, 
          unitcd, 
          countycd, 
          AVG(am_dom_t1) AS am_dom_t1,
          COALESCE(stddev(am_dom_t1)::double precision, 0) / sqrt(count(am_dom_t1))::double precision AS standard_error
        FROM plots
        GROUP BY statecd, unitcd, countycd

    """)

    t1_county_stats = cursor.fetchall()

    # print(t1_county_stats[0])

    cursor.execute(f"""

        WITH plots AS (
          WITH observations_of_plots AS (
            WITH obs_of_trees_in_county AS (
              -- grab all observations of trees in the county
              SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 5) as basal_area, east_us_tree.spcd, ref_species.association
              FROM east_us_tree 
              LEFT JOIN ref_species
              ON east_us_tree.spcd = ref_species.spcd
              LEFT JOIN east_us_cond
              ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND east_us_tree.plot = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
              WHERE 

              east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND										-- at T2

              east_us_tree.statecd = {statecd} AND  
              east_us_tree.unitcd = {unitcd} AND
              east_us_tree.countycd = {countycd} AND 

              east_us_cond.stdorgcd = 0 AND	-- exclude timberland
              east_us_tree.statuscd = 1			-- only count live trees

              ORDER BY statecd, unitcd, countycd, plot, subp, tree
            )
            -- grab each observation of a plot, aggregating tree measurements from that observation
            SELECT 
              invyr, 
              statecd, 
              unitcd, 
              countycd, 
              plot, 
              SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) AS am_bas_area_t2,
              SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END) AS em_bas_area_t2,
              SUM(basal_area) AS total_bas_area_t2,
              CASE WHEN (SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) + SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END)) = 0 THEN 0 ELSE SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END)::double precision / (SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END) + SUM(CASE WHEN association = 'EM' THEN basal_area ELSE 0 END))::double precision END AS am_dom_t2
            FROM obs_of_trees_in_county
            GROUP BY invyr, statecd, unitcd, countycd, plot
            ORDER BY statecd, unitcd, countycd, plot
          )
          -- grab each plot, averaging am_dom's where there are multiple years
          SELECT statecd, unitcd, countycd, plot, AVG(am_dom_t2) AS am_dom_t2
          FROM observations_of_plots
          GROUP BY statecd, unitcd, countycd, plot
          ORDER BY statecd, unitcd, countycd, plot
        )
        -- grab the county, averaging the am_dom of the plots in it
        SELECT 
          statecd, 
          unitcd, 
          countycd, 
          AVG(am_dom_t2) AS am_dom_t2,
          COALESCE(stddev(am_dom_t2)::double precision, 0) / sqrt(count(am_dom_t2))::double precision AS standard_error
        FROM plots
        GROUP BY statecd, unitcd, countycd

    """)

    t2_county_stats = cursor.fetchall()

    # print(t2_county_stats[0])

    if len(t1_county_stats) > 0 and len(t2_county_stats) > 0:       # if there are no stats for t1 or no stats for t2, then the county is not added to the output.
        single_county_stats = []
        single_county_stats.extend(t1_county_stats[0])
        single_county_stats.extend([t2_county_stats[0][3], t2_county_stats[0][4]])
        single_county_stats.append(t2_county_stats[0][3] - t1_county_stats[0][3])       # calculate dif_am_dom
        # print(single_county_stats)
        counties_data.append(single_county_stats)

output_df = pd.DataFrame(counties_data, columns=["statecd", "unitcd", "countycd", "am_dom_t1", "std_err_t1", "am_dom_t2", "std_err_t2", "dif_am_dom"])
output_df.to_csv(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_am_dominance_excluding.csv", index=False)

# clean up
cursor.close()
connection.close()