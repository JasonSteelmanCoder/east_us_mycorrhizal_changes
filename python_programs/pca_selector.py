import psycopg2
from itertools import combinations
import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt 
from adjustText import adjust_text
import numpy as np

load_dotenv()

# SET THE SAVE FOLDER HERE:
save_to = f'C:/Users/{os.getenv('MS_USER_NAME')}/Pictures/optimized_pcas/automatic_saves'

for i in range(3, 8):
# for i in range(5, 6):
    num_variables = i

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
            SELECT scientific_name, flame_duration_s, common_name, percent_consumed, mean_litter_k, mean_litter_cn, bark_vol_percent, bark_diameter_ratio, smoulder_duration_s
            FROM fire_characteristics
        )
        SELECT 
            flame_duration_s::double precision, percent_consumed::double precision, mean_litter_k::double precision, mean_litter_cn::double precision, bark_vol_percent, bark_diameter_ratio, smoulder_duration_s::double precision
        FROM viable_trees
        LEFT JOIN  common_trees
        ON LOWER(TRIM(' ' FROM viable_trees.scientific_name)) = LOWER(TRIM(' ' FROM common_trees.genus || ' ' || common_trees.species))
        ORDER BY (
            CASE WHEN mean_litter_k IS NULL THEN 1 ELSE 0 END + CASE WHEN flame_duration_s IS NULL THEN 1 ELSE 0 END + CASE WHEN percent_consumed IS NULL THEN 1 ELSE 0 END + CASE WHEN mean_litter_cn IS NULL THEN 1 ELSE 0 END + CASE WHEN bark_vol_percent IS NULL THEN 1 ELSE 0 END + CASE WHEN bark_diameter_ratio IS NULL THEN 1 ELSE 0 END + CASE WHEN smoulder_duration_s IS NULL THEN 1 ELSE 0 END
        ), rank_by_basal_area
                
    """)

    rows = cursor.fetchall()

    column_names = ["flame_duration_s", "percent_consumed", "mean_litter_k", "mean_litter_cn", "bark_vol_percent", "bark_diameter_ratio", "smoulder_duration_s"]

    df = pd.DataFrame(rows, columns=column_names)



    # find all of the possible combinations of columns 

    column_nums = [0, 1, 2, 3, 4, 5, 6]

    combos = []

    for j in range(num_variables, len(column_nums) + 1):
        combos.extend(combinations(column_nums, j))


    # make PCA's of each combination

    winning_combo = tuple()
    winning_variance = 0

    for combo in combos:
        subframe = pd.DataFrame(df.iloc[:, list(combo)]).dropna().reset_index(drop=True)
        
        X = subframe.values
        X_standardized = StandardScaler().fit_transform(X)
        pca = PCA()
        points = pca.fit_transform(X_standardized)
        variance = pca.explained_variance_ratio_
        
        current_variance = variance[0] + variance[1]
        if current_variance > winning_variance:
            winning_combo = combo
            winning_variance = current_variance
            print(f'columns: {winning_combo}')
            print(f'number of species: {len(subframe) - 1}')
            print(f'explained variance in two PC\'s: {winning_variance}')
            print('\n')

    # plot the PCA for the winning combination of variables
        
    winning_columns = []

    for num in winning_combo:
        winning_columns.append(column_names[num])

    cursor.execute(f"""
        SELECT 
            fire_characteristics.scientific_name, 
            CASE WHEN ref_species.association = 'AM' THEN '#5AB4AC' ELSE '#D8B365' END AS color_by_association,
            pct_of_basal,
            {'::double precision, '.join(winning_columns)} 
        FROM fire_characteristics 
        INNER JOIN ref_species
        ON LOWER(TRIM(BOTH ' ' FROM ref_species.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name))
        INNER JOIN basal_areas
        ON LOWER(TRIM(BOTH ' ' FROM basal_areas.scientific_name)) = LOWER(TRIM(BOTH ' ' FROM fire_characteristics.scientific_name))
        ORDER BY pct_of_basal DESC
    """)

    winning_rows = cursor.fetchall()

    output_columns = ["scientific_name", "color_by_association", "pct_basal_area"]
    output_columns.extend(winning_columns)

    winning_df = pd.DataFrame(winning_rows, columns=output_columns)
    winning_df = winning_df.dropna().reset_index(drop=True)

    X_win = winning_df.iloc[:, 3:]
    colors = winning_df.iloc[:, 1]
    sizes = winning_df.iloc[:, 2]
    labels = winning_df.iloc[:, 0]

    X_win_standardized = StandardScaler().fit_transform(X_win)

    pca_win = PCA()
    points_win = pca_win.fit_transform(X_win_standardized)
    loadings = pca_win.components_.T * np.sqrt(pca_win.explained_variance_)

    plt.figure(figsize=(10, 8))
    plt.scatter(points_win[:, 0], points_win[:, 1], c=colors, edgecolor='k', s = sizes * 150, linewidths=0.5)
    texts = []
    for k in range(loadings.shape[0]):
        plt.quiver(0, 0, loadings[k, 0], loadings[k, 1], angles='xy', scale_units='xy', scale=0.5, alpha=0.25)
        texts.append(plt.annotate(winning_columns[k], (loadings[k, 0] * 1.5, loadings[k, 1] * 1.5), weight='bold', alpha=0.5))
    for m, label in enumerate(labels):
        texts.append(plt.annotate(label, (points_win[m, 0], points_win[m, 1]), fontsize=7))
    adjust_text(texts, only_move={'texts':'xy'})
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(f'PCA of {num_variables} Variables:\n{', '.join(winning_columns)}')
    plt.savefig(f'{save_to}/{num_variables}d.png')

    cursor.close()
    connection.close()