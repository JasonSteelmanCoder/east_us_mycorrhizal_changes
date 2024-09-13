import csv
from dotenv import load_dotenv
import os

load_dotenv()

rows = []

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/mycorrhizal_associations.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        rows.append(row[:3])
    print(rows)

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/mycorrhizal_associations_1.csv', 'w') as stripped_file:
    for row in rows:
        for entry in row:
            cleaned_entry = entry.replace("[", "").replace("]", "")
            stripped_file.write(f'{cleaned_entry},')
        stripped_file.write('\n')