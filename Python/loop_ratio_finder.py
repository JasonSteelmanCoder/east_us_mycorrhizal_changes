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
        WITH t1 
        AS (
            WITH association_basal_areas
            AS (
                WITH county_trees
                AS (
                    WITH min_year_of_tree AS (
                        SELECT MIN(east_us_tree.invyr), east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree
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

                        GROUP BY east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree
                        ORDER BY east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree
                    )
                    SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, east_us_tree.tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
                    FROM east_us_tree 
                    LEFT JOIN ref_species
                    ON east_us_tree.spcd = ref_species.spcd
                    LEFT JOIN east_us_cond
                    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = CAST(east_us_cond.plot AS text) AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
                    JOIN min_year_of_tree
                    ON east_us_tree.statecd = min_year_of_tree.statecd AND east_us_tree.unitcd = min_year_of_tree.unitcd AND east_us_tree.countycd = min_year_of_tree.countycd AND CAST(east_us_tree.plot AS text) = CAST(min_year_of_tree.plot AS text) AND CAST(east_us_tree.subp AS text) = CAST(min_year_of_tree.subp AS text) AND east_us_tree.tree = min_year_of_tree.tree AND east_us_tree.invyr = min_year_of_tree.min
                    WHERE 
                                        
                    east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1
                                        
                    east_us_tree.statecd = {statecd} AND  
                    east_us_tree.unitcd = {unitcd} AND
                    east_us_tree.countycd = {countycd} AND 
                                        
                    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
                    east_us_tree.statuscd = 1			-- only count live trees
                                        
                    ORDER BY statecd, unitcd, countycd, plot, subp, tree
                )
                SELECT association, SUM(basal_area) AS basal_area_for_county
                FROM county_trees
                GROUP BY association
            )
            SELECT  
            sum(basal_area_for_county) AS total_basal_area_t1,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS am_basal_area_t1,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS em_basal_area_t1,
            COALESCE(round(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0)) / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM'), 0))::decimal, 2), CASE WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) THEN 0 WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) THEN NULL ELSE 1 END) AS am_dominance_t1,
            ROW_NUMBER() OVER() AS rownum
            FROM association_basal_areas
        ), 

        t2 AS (
            WITH association_basal_areas
            AS (
                WITH county_trees
                AS (
                    WITH max_year_of_tree AS (
                        SELECT MAX(east_us_tree.invyr), east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree
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

                        GROUP BY east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree
                        ORDER BY east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, tree
                    )
                    SELECT east_us_tree.invyr, east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.plot, east_us_tree.subp, east_us_tree.tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
                    FROM east_us_tree 
                    LEFT JOIN ref_species
                    ON east_us_tree.spcd = ref_species.spcd
                    LEFT JOIN east_us_cond
                    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = CAST(east_us_cond.plot AS text) AND east_us_tree.invyr = east_us_cond.invyr AND east_us_tree.condid = east_us_cond.condid
                    JOIN max_year_of_tree
                    ON east_us_tree.statecd = max_year_of_tree.statecd AND east_us_tree.unitcd = max_year_of_tree.unitcd AND east_us_tree.countycd = max_year_of_tree.countycd AND CAST(east_us_tree.plot AS text) = CAST(max_year_of_tree.plot AS text) AND CAST(east_us_tree.subp AS text) = CAST(max_year_of_tree.subp AS text) AND east_us_tree.tree = max_year_of_tree.tree AND east_us_tree.invyr = max_year_of_tree.max
                    WHERE 
                                        
                    east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND										-- at T2
                                        
                    east_us_tree.statecd = {statecd} AND  
                    east_us_tree.unitcd = {unitcd} AND
                    east_us_tree.countycd = {countycd} AND 
                                        
                    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
                    east_us_tree.statuscd = 1			-- only count live trees
                                        
                    ORDER BY statecd, unitcd, countycd, plot, subp, tree

                )
                SELECT association, SUM(basal_area) AS basal_area_for_county
                FROM county_trees
                GROUP BY association
            )
            SELECT  
            sum(basal_area_for_county) AS total_trees_t2,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS am_basal_area_t2,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS em_basal_area_t2,
            COALESCE(round(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0)) / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM'), 0))::decimal, 2), CASE WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) THEN 0 WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) THEN NULL ELSE 1 END) AS am_dominance_t2,
            ROW_NUMBER() OVER() AS rownum
            FROM association_basal_areas
        )
        SELECT 
            total_basal_area_t1, 
            am_basal_area_t1, 
            em_basal_area_t1, 
            am_dominance_t1, 
            total_trees_t2, 
            am_basal_area_t2, 
            em_basal_area_t2, 
            am_dominance_t2,
            round(am_dominance_t2::decimal - am_dominance_t1::decimal, 2) difference_in_am_dominance
        FROM t1
        LEFT JOIN t2
        ON true;
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