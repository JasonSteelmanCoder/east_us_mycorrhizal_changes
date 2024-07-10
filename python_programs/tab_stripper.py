import os
from dotenv import load_dotenv
import csv

load_dotenv()

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/try_fire_characteristics.csv', 'r') as source_file:
    reader = csv.reader(source_file)
    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/try_data.csv', 'w') as output_file:
        for row in reader:
            print(row[0].rstrip('\t'))
            output_file.write(f'{row[0].rstrip('\t')}\n')