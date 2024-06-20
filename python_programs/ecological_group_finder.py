import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2

load_dotenv()


connection = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

# find if there are invasive species at all in each county
cursor.execute(f"""
    SELECT east_us_plot.statecd, east_us_plot.countycd, count(DISTINCT ecological_groups.ecological_group) > 0 AS has_invasives
    FROM east_us_plot
    LEFT JOIN worms_drake 
    ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
    LEFT JOIN ecological_groups
    ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
    GROUP BY east_us_plot.statecd, east_us_plot.countycd
    ORDER BY has_invasives;
""")

counties = cursor.fetchall()

output_1 = pd.DataFrame(counties, columns=["statecd", "countycd", "has_invasives"])

# find if there are EPIGEIC invasive species in each county
cursor.execute(f"""
    WITH 
    combos AS (
        -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal epigeic)
        SELECT 
            east_us_plot.statecd, 
            east_us_plot.countycd, 
            COALESCE(ecological_groups.ecological_group = 'Epigeic', false) AS is_epigeic_row
        FROM east_us_plot
        LEFT JOIN worms_drake 
        ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
        LEFT JOIN ecological_groups
        ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
        GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
        ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
    )
    SELECT statecd, countycd, BOOL_OR(is_epigeic_row) AS has_epigeic
    FROM combos
    GROUP BY statecd, countycd
    ORDER BY statecd, countycd;
""")

epigeics = cursor.fetchall()

epigeics_df = pd.DataFrame(epigeics, columns=["statecd", "countycd", "has_epigeics"])

output_2 = pd.merge(output_1, epigeics_df, on=['statecd', 'countycd'], how="left")

# find if there are ANECIC invasive species in each county
cursor.execute(f"""
    WITH 
    combos AS (
        -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal anecic)
        SELECT 
            east_us_plot.statecd, 
            east_us_plot.countycd, 
            ecological_groups.ecological_group,
            COALESCE(ecological_groups.ecological_group = 'Anecic', false) AS is_anecic_row
        FROM east_us_plot
        LEFT JOIN worms_drake 
        ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
        LEFT JOIN ecological_groups
        ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
        GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
        ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
    )
    SELECT statecd, countycd, BOOL_OR(is_anecic_row) AS has_anecic
    FROM combos
    GROUP BY statecd, countycd
    ORDER BY statecd, countycd;
""")

anecics = cursor.fetchall()

anecic_df = pd.DataFrame(anecics, columns=["statecd", "countycd", "has_anecic"])

output_3 = pd.merge(output_2, anecic_df, on=["statecd", "countycd"], how="left")

# find if there are ENDOGEIC invasive species in each county
cursor.execute(f"""
    WITH 
    combos AS (
        -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal endogeic)
        SELECT 
            east_us_plot.statecd, 
            east_us_plot.countycd, 
            ecological_groups.ecological_group,
            COALESCE(ecological_groups.ecological_group = 'Endogeic', false) AS is_endogeic_row
        FROM east_us_plot
        LEFT JOIN worms_drake 
        ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
        LEFT JOIN ecological_groups
        ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
        GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
        ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
    )
    SELECT statecd, countycd, BOOL_OR(is_endogeic_row) AS has_endogeic
    FROM combos
    GROUP BY statecd, countycd
    ORDER BY statecd, countycd;
""")

endogeics = cursor.fetchall()

endogeic_df = pd.DataFrame(endogeics, columns=["statecd", "countycd", "has_endogeic"])

output_4 = pd.merge(output_3, endogeic_df, on=["statecd", "countycd"], how="left")

# find if there are EPI-ENDOGEIC invasive species in each county
cursor.execute(f"""
    WITH 
    combos AS (
        -- find all combinations of counties and ecoregions (ecoregions are displayed as booleans for whether they equal epi-endogeic)
        SELECT 
            east_us_plot.statecd, 
            east_us_plot.countycd, 
            ecological_groups.ecological_group,
            COALESCE(ecological_groups.ecological_group = 'Epi-Endogeic', false) AS is_epiendogeic_row
        FROM east_us_plot
        LEFT JOIN worms_drake 
        ON east_us_plot.statecd = worms_drake.statecd AND east_us_plot.countycd = worms_drake.countycd
        LEFT JOIN ecological_groups
        ON ecological_groups.family = worms_drake.family AND ecological_groups.name = worms_drake.name
        GROUP BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
        ORDER BY east_us_plot.statecd, east_us_plot.countycd, ecological_groups.ecological_group
    )
    SELECT statecd, countycd, BOOL_OR(is_epiendogeic_row) AS has_epiendogeic
    FROM combos
    GROUP BY statecd, countycd
    ORDER BY statecd, countycd;
""")

epiendogeics = cursor.fetchall()

epiendogeic_df = pd.DataFrame(epiendogeics, columns=["statecd", "countycd", "has_epiendogeic"])

output_5 = pd.merge(output_4, epiendogeic_df, on=["statecd", "countycd"], how="left")

output_5.to_csv(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/ecological_groups_by_county.csv', index=False)

# clean up
cursor.close()
connection.close()