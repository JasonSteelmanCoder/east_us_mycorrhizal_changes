import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

output_contents = "statecd,unitcd,countycd,tot_bas_t1,ambasar_t1,embasar_t1,am_dom_t1,tot_bas_t2,ambasar_t2,embasar_t2,am_dom_t2,dif_am_dom\n"

connection = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

cursor.execute(f"""
    SELECT statecd, unitcd, countycd FROM east_us_plot WHERE statecd = 34 AND unitcd = 1 AND countycd = 21 GROUP BY statecd, unitcd, countycd
""")

counties = cursor.fetchall()

for county_row in counties:
    statecd = county_row[0]
    unitcd = county_row[1]
    countycd = county_row[2]

    print(unitcd)

    cursor.execute(f"""
        WITH t1 
        AS (
        WITH association_basal_areas
        AS (
            WITH county_trees
            AS (
            SELECT east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, invyr, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
            FROM east_us_tree 
            LEFT JOIN ref_species
            ON east_us_tree.spcd = ref_species.spcd
            WHERE 

            east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1996 AND										-- at T1

            east_us_tree.statecd = {statecd} AND  
            east_us_tree.unitcd = {unitcd} AND
            east_us_tree.countycd = {countycd} AND 

            east_us_tree.statuscd = 1			-- only count live trees

            ORDER BY association ASC
            )
            SELECT association, SUM(basal_area) AS basal_area_for_county
            FROM county_trees
            GROUP BY association
        )
        SELECT  
        sum(basal_area_for_county) AS total_basal_area_t1,
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') AS am_basal_area_t1,
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') AS em_basal_area_t1,
        COALESCE(round((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM'))::decimal, 2), CASE WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) THEN 0 WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) THEN NULL ELSE 1 END) AS am_dominance_t1,
        ROW_NUMBER() OVER() AS rownum
        FROM association_basal_areas
        ), 

        t2 AS (
        WITH association_basal_areas
        AS (
            WITH county_trees
            AS (
            SELECT east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, invyr, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
            FROM east_us_tree 
            LEFT JOIN ref_species
            ON east_us_tree.spcd = ref_species.spcd
            WHERE 

            east_us_tree.invyr > 2017 AND east_us_tree.invyr < 2023 AND									-- at T2

            east_us_tree.statecd = {statecd} AND  
            east_us_tree.unitcd = {unitcd} AND
            east_us_tree.countycd = {countycd} AND
            
            east_us_tree.statuscd = 1			-- only count live trees

            ORDER BY association ASC
            )
            SELECT association, SUM(basal_area) AS basal_area_for_county
            FROM county_trees
            GROUP BY association
        )
        SELECT  
        sum(basal_area_for_county) AS total_trees_t2,
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') AS am_basal_area_t2,
        (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') AS em_basal_area_t2,
        COALESCE(round((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') / ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM'))::decimal, 2), CASE WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NOT NULL) THEN 0 WHEN ((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') IS NULL AND (SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') IS NULL) THEN NULL ELSE 1 END) AS am_dominance_t2,
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

    for county_row in rows:            # (there is only one row per SQL query)
        output_contents += f'{statecd},{unitcd},{countycd},'
        # print(county_row)
        for i in range(row_length - 1):
            output_contents += f'{county_row[i]},'
        output_contents += f'{county_row[-1]}\n'

with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/maine_percents_and_ratios_by_plot.csv", "w") as output_file:
    output_file.write(output_contents)

cursor.close()
connection.close()