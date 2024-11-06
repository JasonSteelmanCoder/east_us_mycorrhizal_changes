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
output_contents = "statecd,unitcd,countycd,adapted_area,intolerant_area,pct_adapted,excluded_bas_area,pct_area_excluded,am_area,em_area,pct_em,not_counted_area,pct_not_counted,region\n"

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

    cursor.execute(f"""

        WITH plots AS (
            WITH obs_of_plots AS (
                WITH obs_of_trees AS (
                    -- grab all observations of trees in the county (including those with null fire classifications, excluding those with null diameters)
                    SELECT 
                        east_us_tree.statecd AS statecd,
                        east_us_tree.unitcd AS unitcd,
                        east_us_tree.countycd AS countycd,
                        east_us_tree.plot AS plot,
                        east_us_tree.invyr AS invyr,
                        east_us_tree.spcd AS spcd,
                        fire_classification,
                        ROUND(((PI() * (east_us_tree.dia::DECIMAL * 2.54 / 2) ^ 2) / 10000)::DECIMAL, 4) AS basal_area,
                        ref_species.association
                    FROM east_us_tree
                    LEFT JOIN fire_adaptation								-- include species with null fire classifications (to allow calculation of excluded basal area)
                    ON east_us_tree.spcd = fire_adaptation.spcd
                    JOIN ref_species
                    ON ref_species.spcd = east_us_tree.spcd
                    JOIN east_us_cond euc
					ON 
						euc.plt_cn = east_us_tree.plt_cn
						AND euc.condid = east_us_tree.condid
                    WHERE 
                        east_us_tree.statecd = {statecd} 
                        AND east_us_tree.unitcd = {unitcd}
                        AND east_us_tree.countycd = {countycd}
                        AND east_us_tree.invyr > 2014 AND east_us_tree.invyr < 2023				-- at T2
                        AND east_us_tree.dia IS NOT NULL											-- trees must have diameters
                        AND euc.stdorgcd = 0                                                -- trees should be on natural conditions, not artificially regenerated ones
                )
                -- grab all observations of plots, summing AM and EM basal areas
                SELECT 
                    oot.statecd,
                    oot.unitcd,
                    oot.countycd,
                    oot.plot,
                    oot.invyr,
                    COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) AS adapted_area,
                    COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0) AS intolerant_area,
                    -- note that pct_adapted is the percent of trees belonging to the 75 selected species that are adapted
                    CASE
                        WHEN
                            COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) 
                            + 
                            COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0)
                            = 
                            0
                        THEN 
                            NULL
                        ELSE
                            ROUND(
                                COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) 
                                / 
                                (
                                    COALESCE(SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END), 0) 
                                    + 
                                    COALESCE(SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END), 0)
                                ) * 100
                                , 1
                            )
                    END 
                    AS pct_adapted,
                    COALESCE(SUM(CASE WHEN fire_classification IS NULL THEN basal_area END), 0) AS excluded_bas_area,  -- trees that are not part of the 75 species
                    COALESCE(
                        ROUND(
                            (
                                SUM(CASE WHEN fire_classification IS NULL THEN basal_area END) 
                                / 
                                (
                                    SUM(CASE WHEN fire_classification = 'adapted' THEN basal_area END) 
                                    + 
                                    SUM(CASE WHEN fire_classification = 'intolerant' THEN basal_area END) 
                                    + 
                                    SUM(CASE WHEN fire_classification IS NULL THEN basal_area END)
                                )
                            ) * 100
                            , 2
                        )
                        , 0
                    ) AS pct_area_excluded,
                    ROUND(
                        COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
                        + 
                        0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
                        , 4
                    ) AS am_area,
                    ROUND(
                        COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
                        + 
                        0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
                        , 4
                    ) AS em_area,
                    -- note that pct_em is the percent of trees belonging to the 75 selected species that are Ectomycorrhizal
                    CASE 
						WHEN 
							COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
							+
							COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
							+ 
							COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
							= 
							0
						THEN NULL
						ELSE
							ROUND(
		                        (
		                            (
		                                COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
		                                +
		                                (0.5 * COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0))
		                            ) 
		                            / 
		                            (
		                                COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
		                                +
		                                COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0) 
		                                + 
		                                COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
		                            )
								) * 100
								, 1
							)
					END AS pct_em,
                    -- not_counted_area is the basal area of trees that are not part of the 75 species, plus ericoid sourwood trees
                    COALESCE(
                        SUM(
                            CASE 
                                WHEN fire_classification IS NULL 
                                    OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') 
                                THEN basal_area 
                            END
                        )
                        , 0
                    ) AS not_counted_area,
                    -- pct_not_counted is the not_counted_area as a percent of the total basal area in the county, including all species, association types, and fire adaptation types
                    ROUND(
                        (
                            COALESCE(
                                SUM(
                                    CASE 
                                        WHEN fire_classification IS NULL 
                                            OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') 
                                        THEN basal_area 
                                    END
                                )
                                , 0
                            ) 
                            / 
                            (
                                COALESCE(
                                    SUM(
                                        CASE 
                                            WHEN fire_classification IS NULL 
                                                OR (association != 'AM' AND association != 'EM' AND association != 'AM-EM') 
                                            THEN basal_area 
                                        END
                                    )
                                    , 0
                                ) 
                                + 
                                COALESCE(SUM(CASE WHEN association = 'AM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
                                + 
                                COALESCE(SUM(CASE WHEN association = 'EM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
                                + 
                                COALESCE(SUM(CASE WHEN association = 'AM-EM' AND fire_classification IS NOT NULL THEN basal_area END), 0)
                            )
                        ) * 100 
                        , 2
                    ) AS pct_not_counted,
                    region_id
                FROM obs_of_trees oot
                JOIN east_us_region
                ON east_us_region.statecd = oot.statecd AND east_us_region.countycd = oot.countycd
                GROUP BY 
                    oot.statecd,
                    oot.unitcd,
                    oot.countycd,
                    oot.plot,
                    oot.invyr,
                    region_id
                ORDER BY 
                    oot.statecd,
                    oot.unitcd,
                    oot.countycd,
                    oot.plot,
                    oot.invyr
            )
            -- grab each plot, averaging the measurements from the plot's observations
            SELECT 
                oop.statecd,
                oop.unitcd,
                oop.countycd, 
                oop.plot,
                ROUND(AVG(oop.adapted_area), 4) AS adapted_area,
                ROUND(AVG(oop.intolerant_area), 4) AS intolerant_area,
                ROUND(AVG(oop.pct_adapted), 2) AS pct_adapted,
                ROUND(AVG(oop.excluded_bas_area), 4) AS excluded_bas_area,
                ROUND(AVG(oop.pct_area_excluded), 2) AS pct_area_excluded,
                ROUND(AVG(oop.am_area), 4) AS am_area,
                ROUND(AVG(oop.em_area), 4) AS em_area,
                ROUND(AVG(oop.pct_em), 2) AS pct_em,
                ROUND(AVG(oop.not_counted_area), 4) AS not_counted_area,
                ROUND(AVG(oop.pct_not_counted), 2) AS pct_not_counted,
                oop.region_id AS region
            FROM obs_of_plots oop
            GROUP BY 
                oop.statecd,
                oop.unitcd,
                oop.countycd, 
                oop.plot,
                oop.region_id
            ORDER BY 
                oop.statecd,
                oop.unitcd,
                oop.countycd, 
                oop.plot,
                oop.region_id
        )
        -- grab the county, averaging the measurements of each plot
        SELECT 
            statecd,
            unitcd, 
            countycd,
            ROUND(AVG(adapted_area), 4) adapted_area,
            ROUND(AVG(intolerant_area), 4) intolerant_area,
            ROUND(AVG(pct_adapted), 2) pct_adapted,
            ROUND(AVG(excluded_bas_area), 4) excluded_bas_area,
            ROUND(AVG(pct_area_excluded), 2) pct_area_excluded,
            ROUND(AVG(am_area), 4) am_area,
            ROUND(AVG(em_area), 4) em_area,
            ROUND(AVG(pct_em), 2) pct_em,
            ROUND(AVG(not_counted_area), 4) not_counted_area,
            ROUND(AVG(pct_not_counted), 2) pct_not_counted,
            region
        FROM plots
        GROUP BY 
            statecd,
            unitcd,
            countycd,
            region

    """)

    rows = cursor.fetchall()

    if len(rows) > 0:

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
with open(f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/adaptation_by_county_filtered.csv", "w") as output_file:
    output_file.write(output_contents)

# clean up
cursor.close()
connection.close()