import psycopg2
from itertools import combinations
import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

load_dotenv()

# Get the data from the database

connection = psycopg2.connect(
    dbname = 'fire_characteristics',
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

cursor.execute("""
               
    WITH
    viable_trees AS (
        SELECT scientific_name, flame_duration_s, common_name, percent_consumed, mean_litter_k, mean_litter_cn, bark_vol_pct, bark_diameter_ratio, smoulder_duration_s
        FROM fire_characteristics
    )
    SELECT 
        flame_duration_s::double precision, percent_consumed::double precision, mean_litter_k::double precision, mean_litter_cn::double precision, bark_vol_pct, bark_diameter_ratio, smoulder_duration_s::double precision
    FROM viable_trees
    LEFT JOIN  common_trees
    ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
    ORDER BY (
        CASE WHEN mean_litter_k IS NULL THEN 1 ELSE 0 END + CASE WHEN flame_duration_s IS NULL THEN 1 ELSE 0 END + CASE WHEN percent_consumed IS NULL THEN 1 ELSE 0 END + CASE WHEN mean_litter_cn IS NULL THEN 1 ELSE 0 END + CASE WHEN bark_vol_pct IS NULL THEN 1 ELSE 0 END + CASE WHEN bark_diameter_ratio IS NULL THEN 1 ELSE 0 END + CASE WHEN smoulder_duration_s IS NULL THEN 1 ELSE 0 END
    ), rank_by_basal_area
               
""")

rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=["flame_duration_s", "percent_consumed", "mean_litter_k", "mean_litter_cn", "bark_vol_pct", "bark_diameter_ratio", "smoulder_duration_s"])

cursor.close()
connection.close()


# find all of the possible combinations of columns 

column_nums = [0, 1, 2, 3, 4, 5, 6]

combos = []

for i in range(5, len(column_nums) + 1):
    combos.extend(combinations(column_nums, i))


# make PCA's of each combination

winning_combo = tuple()
winning_variance = 0

for combo in combos:
    subframe = pd.DataFrame(df.iloc[:, list(combo)]).dropna()
    
    X = subframe.values
    X_standardized = StandardScaler().fit_transform(X)
    pca = PCA()
    principal_components = pca.fit_transform(X_standardized)
    variance = pca.explained_variance_ratio_
    
    current_variance = variance[0] + variance[1]
    if current_variance > winning_variance:
        winning_combo = combo
        winning_variance = current_variance
        print(f'columns: {winning_combo}')
        print(f'number of species: {len(subframe)}')
        print(f'explained variance in two PC\'s: {winning_variance}')
        print('\n')
    
