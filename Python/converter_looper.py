""" This program writes SQL queries that will create new tables to transfer your data into a database from csv format.

The program assumes that it is in the same folder as csv_to_sql_converter.py. It also assumes that you have a folder 
with all of the state-level CSV files in it. """

import os
import glob
from csv_to_sql_converter import write_sql_query_to_make_csv_columns
from dotenv import load_dotenv
import os

load_dotenv()

# this is the path to the folder that holds all of your state tables in CSV format
folder = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/updated_east_us_data/east_us_plot'

# get the paths to all the state PLOT tables
file_paths = glob.glob(os.path.join(folder, '*'))

for file_path in file_paths:
    # get the name of the file itself
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # make a CREATE TABLE query for every plot table, then write it to output_file 
    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/queries_to_create_new_plot.txt', 'a') as output_file:
        output_file.write(write_sql_query_to_make_csv_columns(table_name, file_path) + '\n\n')