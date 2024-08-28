import os
from dotenv import load_dotenv
import csv

load_dotenv()

with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/east_us_am_dominance.csv', 'r') as file:
    reader = csv.reader(file)

    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/cleaned_east_us_am_dominance.csv', 'w') as output:

        for row in reader:
            write_line = ''
            for word in row:
                if word == 'None':
                    write_line += ','
                else:
                    write_line += f'{word},'
            output.write(write_line[:-1])       # clip the trailing comma
            output.write('\n')