""" This program writes SQL queries to help you copy data from state CSV files into existing tables in your database.
You need to have already created the tables in the database before trying to copy to them. (See converter_looper.py.)

The program assumes that you have a folder with all of the relevant state tables in CSV format.

Some columns may be of an incorrect datatype. Those columns can be altered using alterer_looper.py. """

import os
import glob
from dotenv import load_dotenv
import os

load_dotenv()

# This is the folder that contains all of your state TREE tables in CSV format
folder = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/eastern_us_data/COND_BY_STATE'

# get the paths to all your state TREE tables
file_paths = glob.glob(os.path.join(folder, '*'))


for file_path in file_paths:
    # get the filename for each csv table
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # for each csv table, make a COPY FROM query and write them all to output_file
    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/queries_to_copy_cond_tables.txt', 'a') as output_file:
        output_file.write(f"""COPY {table_name}
FROM \'{file_path}\'
CSV HEADER DELIMITER ',';\n\n""")