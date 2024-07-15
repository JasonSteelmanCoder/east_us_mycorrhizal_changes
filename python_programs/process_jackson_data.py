import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/jackson_calculations_orig.csv')

df = df.drop(columns=['adult_perc'])

df['total_bark_thickness'] = df['outer_bark_thickness'] * 1.125

df['bark_dbh_ratio'] = df['total_bark_thickness'] / df['adult_diameter']

df.to_csv(f'C:/Users/{os.getenv('MS_USER_NAME')}/Desktop/jackson_calculations.csv', index=False)