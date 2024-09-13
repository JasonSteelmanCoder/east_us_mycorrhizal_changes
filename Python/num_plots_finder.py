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
    WHERE plot_status_cd = 1            -- exclude non-forest plots
    GROUP BY statecd, unitcd, countycd
""")

counties = cursor.fetchall()

counties_data = []

count = 0

total_plots_t1 = 0
total_plots_t2 = 0

for county_row in counties:
    statecd = county_row[0]
    unitcd = county_row[1]
    countycd = county_row[2]

    # print for monitoring reasons
    count += 1
    print(f'Processing {statecd}  {unitcd}  {countycd}. Count: {count}')

    cursor.execute(f"""

        -- get all plots for a county at t1

        WITH observations_of_plots AS (
          WITH obs_of_trees_in_county AS (
            -- grab all observations of trees in the county
            SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 5) as basal_area, east_us_tree.spcd, ref_species.association
            FROM east_us_tree 
            LEFT JOIN ref_species
            ON east_us_tree.spcd = ref_species.spcd
            LEFT JOIN east_us_cond
            ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
            WHERE 
  
            east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1
  
            east_us_tree.statecd = {statecd} AND  
            east_us_tree.unitcd = {unitcd} AND
            east_us_tree.countycd = {countycd} AND 
  
            (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
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
            SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END)::double precision / SUM(basal_area)::double precision AS am_dom_t1
          FROM obs_of_trees_in_county
          GROUP BY invyr, statecd, unitcd, countycd, plot
          ORDER BY statecd, unitcd, countycd, plot
        )
        -- grab each plot, averaging am_dom's where there are multiple years
        SELECT statecd, unitcd, countycd, plot, AVG(am_dom_t1) AS am_dom_t1
        FROM observations_of_plots
        GROUP BY statecd, unitcd, countycd, plot
        ORDER BY statecd, unitcd, countycd, plot

    """)

    plots_in_county_t1 = cursor.fetchall()

    # print(len(plots_in_county_t1))

    total_plots_t1 += len(plots_in_county_t1)

    cursor.execute(f"""

        -- get all plots for a county at t2

        WITH observations_of_plots AS (
            WITH obs_of_trees_in_county AS (
                -- grab all observations of trees in the county
                SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 5) as basal_area, east_us_tree.spcd, ref_species.association
                FROM east_us_tree 
                LEFT JOIN ref_species
                ON east_us_tree.spcd = ref_species.spcd
                LEFT JOIN east_us_cond
                ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
                WHERE 

                east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND										-- at T2

                east_us_tree.statecd = {statecd} AND  
                east_us_tree.unitcd = {unitcd} AND
                east_us_tree.countycd = {countycd} AND 

                (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
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
                SUM(CASE WHEN association = 'AM' THEN basal_area ELSE 0 END)::double precision / SUM(basal_area)::double precision AS am_dom_t2
            FROM obs_of_trees_in_county
            GROUP BY invyr, statecd, unitcd, countycd, plot
            ORDER BY statecd, unitcd, countycd, plot
        )
        -- grab each plot, averaging am_dom's where there are multiple years
        SELECT statecd, unitcd, countycd, plot, AVG(am_dom_t2) AS am_dom_t2
        FROM observations_of_plots
        GROUP BY statecd, unitcd, countycd, plot
        ORDER BY statecd, unitcd, countycd, plot

    """)

    plots_in_county_t2 = cursor.fetchall()

    # print(len(plots_in_county_t2))

    total_plots_t2 += len(plots_in_county_t2)

print(f'total plots t1: {total_plots_t1}')
print(f'total plots t2: {total_plots_t2}')