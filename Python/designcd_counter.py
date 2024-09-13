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

design_instances = {}

for county_row in counties:
    statecd = county_row[0]
    unitcd = county_row[1]
    countycd = county_row[2]

    # print for monitoring reasons
    count += 1
    print(f'Processing {statecd}  {unitcd}  {countycd}. Count: {count}')

    cursor.execute(f"""

        -- get all plot-observations for a county at t1, along with their designcd's

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
          -- grab each observation of a plot, along with its designcd
          SELECT 
            -- east_us_plot.invyr, 
            -- east_us_plot.statecd, 
            -- east_us_plot.unitcd, 
            -- east_us_plot.countycd, 
            -- east_us_plot.plot,
          	east_us_plot.designcd
          FROM obs_of_trees_in_county
          JOIN east_us_plot
          ON east_us_plot.invyr = obs_of_trees_in_county.invyr
          	AND east_us_plot.statecd = obs_of_trees_in_county.statecd
          	AND east_us_plot.unitcd = obs_of_trees_in_county.unitcd
          	AND east_us_plot.countycd = obs_of_trees_in_county.countycd
          	AND east_us_plot.plot = obs_of_trees_in_county.plot::text
          GROUP BY east_us_plot.invyr, east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot, east_us_plot.designcd
          ORDER BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot

    """)

    designs_in_county_t1 = cursor.fetchall()

    for design in designs_in_county_t1:
        if str(design[0]) in design_instances:
            design_instances[str(design[0])] += 1
        else:
            design_instances[str(design[0])] = 1

    cursor.execute(f"""

        -- get all plot-observations for a county at t2, along with their designcd's 

          WITH obs_of_trees_in_county AS (
            -- grab all observations of trees in the county
            SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 5) as basal_area, east_us_tree.spcd, ref_species.association
            FROM east_us_tree 
            LEFT JOIN ref_species
            ON east_us_tree.spcd = ref_species.spcd
            LEFT JOIN east_us_cond
            ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
            WHERE 
  
            east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2022 AND										-- at T2
  
            east_us_tree.statecd = {statecd} AND  
            east_us_tree.unitcd = {unitcd} AND
            east_us_tree.countycd = {countycd} AND 
  
            (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
            east_us_tree.statuscd = 1			-- only count live trees
  
            ORDER BY statecd, unitcd, countycd, plot, subp, tree
          )
          -- grab each observation of a plot, along with its designcd
          SELECT 
            -- east_us_plot.invyr, 
            -- east_us_plot.statecd, 
            -- east_us_plot.unitcd, 
            -- east_us_plot.countycd, 
            -- east_us_plot.plot,
          	east_us_plot.designcd
          FROM obs_of_trees_in_county
          JOIN east_us_plot
          ON east_us_plot.invyr = obs_of_trees_in_county.invyr
          	AND east_us_plot.statecd = obs_of_trees_in_county.statecd
          	AND east_us_plot.unitcd = obs_of_trees_in_county.unitcd
          	AND east_us_plot.countycd = obs_of_trees_in_county.countycd
          	AND east_us_plot.plot = obs_of_trees_in_county.plot::text
          GROUP BY east_us_plot.invyr, east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot, east_us_plot.designcd
          ORDER BY east_us_plot.statecd, east_us_plot.unitcd, east_us_plot.countycd, east_us_plot.plot

    """)

    designs_in_county_t2 = cursor.fetchall()

    for design in designs_in_county_t2:
        if str(design[0]) in design_instances:
            design_instances[str(design[0])] += 1
        else:
            design_instances[str(design[0])] = 1

print(design_instances)