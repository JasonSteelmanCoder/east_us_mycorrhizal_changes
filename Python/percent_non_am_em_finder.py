

# import libraries for connecting to database and getting details from .env file
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# start building the output by inserting the column titles of the output csv
output_contents = "total_basal_area_t1,other_basal_area_t1,percent_non_am_em_t1,total_basal_area_t2,other_basal_area_t2,percent_non_am_em_t2\n"

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
        WITH t1 
        AS (
            WITH association_basal_areas
            AS (
                WITH county_trees
                AS (
                    SELECT east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.invyr, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
                    FROM east_us_tree 
                    LEFT JOIN ref_species
                    ON east_us_tree.spcd = ref_species.spcd
                    LEFT JOIN east_us_cond
                    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot
                    WHERE 

                    east_us_tree.invyr > 1979 AND east_us_tree.invyr < 1999 AND										-- at T1

                    east_us_tree.statecd = {statecd} AND  
                    east_us_tree.countycd = {countycd} AND 
                    
                    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland
                    east_us_tree.statuscd = 1			-- only count live trees

                    ORDER BY association ASC
                )
                SELECT association, SUM(basal_area) AS basal_area_for_county
                FROM county_trees
                GROUP BY association
            )
            SELECT  
            sum(basal_area_for_county) AS total_basal_area_t1,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS am_basal_area_t1,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS em_basal_area_t1,
            sum(basal_area_for_county) - (ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) + ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2)) AS other_basal_area_t1,
            ROW_NUMBER() OVER() AS rownum
            FROM association_basal_areas
        ), 

        t2 AS (
            WITH association_basal_areas
            AS (
                WITH county_trees
                    AS (
                    SELECT east_us_tree.statecd, east_us_tree.unitcd, east_us_tree.countycd, east_us_tree.invyr, tree, round(east_us_tree.dia::decimal * 2.54, 1) as dia_cm, round(((PI() * (east_us_tree.dia::decimal * 2.54 / 2) ^ 2) / 10000)::decimal, 2) as basal_area, east_us_tree.spcd, ref_species.association
                    FROM east_us_tree 
                    LEFT JOIN ref_species
                    ON east_us_tree.spcd = ref_species.spcd
                    LEFT JOIN east_us_cond
                    ON east_us_tree.statecd = east_us_cond.statecd AND east_us_tree.unitcd = east_us_cond.unitcd AND east_us_tree.countycd = east_us_cond.countycd AND CAST(east_us_tree.plot AS text) = east_us_cond.plot

                    WHERE 

                    east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023 AND									-- at T2

                    east_us_tree.statecd = {statecd} AND  
                    east_us_tree.countycd = {countycd} AND

                    (east_us_cond.industrialcd_fiadb IS NULL OR east_us_cond.industrialcd_fiadb = 0) AND	-- exclude timberland            
                    east_us_tree.statuscd = 1			-- only count live trees            

                    ORDER BY association ASC
                )
                SELECT association, SUM(basal_area) AS basal_area_for_county
                FROM county_trees
                GROUP BY association
            )
            SELECT  
            sum(basal_area_for_county) AS total_basal_area_t2,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS am_basal_area_t2,
            ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) AS em_basal_area_t2,
            SUM(basal_area_for_county) - (ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2) + ROUND((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'EM') + COALESCE(((SELECT basal_area_for_county FROM association_basal_areas WHERE association = 'AM-EM')::DECIMAL / 2), 0), 2)) AS other_basal_area_t2,
            ROW_NUMBER() OVER() AS rownum
            FROM association_basal_areas
        )
        SELECT 
            total_basal_area_t1, 
            other_basal_area_t1,
            ROUND((other_basal_area_t1 / total_basal_area_t1) * 100, 2) AS percent_non_am_em_t1,
            total_basal_area_t2, 
            other_basal_area_t2,
            ROUND((other_basal_area_t2 / total_basal_area_t2) * 100, 2) AS percent_non_am_em_t2
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
with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/percent_non_am_em_basal_area.csv", "w") as output_file:
    output_file.write(output_contents)

# clean up
cursor.close()
connection.close()