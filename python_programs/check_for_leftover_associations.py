import csv
from dotenv import load_dotenv
import os

load_dotenv()

identified_genera = {}

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/genera_without_association.csv', 'r') as genera:
    genera_reader = csv.reader(genera)

    for genus in genera:
        print(genus)

        with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/myco_db.csv', 'r') as myco_db:
            myco_reader = csv.reader(myco_db)

            for m_row in myco_reader:
                if genus.strip() in m_row[2]:
                    print(f'genus: {genus}', end=', ')
                    print(f'association: {m_row[2]}')
                    identified_genera[m_row[2]] = m_row[6]

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/associations_for_unknown_genera.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['genus', 'association'])
    for key, value in identified_genera.items():
        writer.writerow([key, value])