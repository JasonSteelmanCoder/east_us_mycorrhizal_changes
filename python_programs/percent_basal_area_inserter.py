import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

common_trees_df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/common_trees/common_trees_for_duration_of_study.csv')

input_df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_24_2024.csv')

input_df["pct_of_basal"] = common_trees_df["pct_of_basal"]

input_df.to_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/pca_input_7_29_2024.csv')