import os
from dotenv import load_dotenv
import csv

load_dotenv()

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_percents_and_ratios_by_plot.csv', 'r') as file:
    reader = csv.reader(file)

    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/cleaned_east_us_percents_and_ratios.csv', 'w') as output:

        for row in reader:
            for word in row:
                if word == 'None':
                    output.write(',')
                else:
                    output.write(f'{word},')
            output.write('\n')