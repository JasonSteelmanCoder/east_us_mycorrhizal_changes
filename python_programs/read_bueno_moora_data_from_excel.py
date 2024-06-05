import pandas as pd
import csv
from dotenv import load_dotenv
import os

load_dotenv()

file_path = f"C:/Users/{os.getenv("MS_USER_NAME")}/Downloads/geb12582-sup-0007-suppinfo7.xlsx"
sheet_name = 'Main'
column_name = 'Species (taken from The Plant List)'

df = pd.read_excel(file_path, sheet_name=sheet_name)

column_data = df[column_name]

genera = {}

for genus in column_data:
    genera[genus.split()[0]] = True

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/genera_without_association.csv', 'r') as search_terms:
    reader = csv.reader(search_terms)

    for search_term in reader:
        for genus in genera.keys():
            if search_term[0].strip() in genus.strip():
                print(genus)

# CONCLUSION: Bueno Moora paper only provides 6 more unknown genera