import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

common_trees_df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/common_trees/common_trees_for_duration_of_study.csv')

input_df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_24_2024.csv')

input_df = input_df.merge(common_trees_df, how='inner', on='scientific_name')

input_df.to_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_29_2024.csv', index=False)