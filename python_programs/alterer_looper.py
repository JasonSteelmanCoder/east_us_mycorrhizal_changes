""" This program writes a series of SQL queries to help you alter columns with incorrectly assigned datatypes. It uses the names of files in your 
folder of state csv files to name all of the columns to be altered. """

import os
import glob
from dotenv import load_dotenv
import os

load_dotenv()

column = 'NBR_LIVE_STEMS'            # the column to alter
data_type = 'text'                  # the datatype to change the column to
folder = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/eastern_us_data/COND_BY_STATE'       # the folder that has all of your state TREE tables, or state PLOT tables

# get the filepaths for all of the state_tree tables (We need them to know what tables in the database to query.)
file_paths = glob.glob(os.path.join(folder, '*'))


for file_path in file_paths:
    # get the filenames from their paths
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # write an ALTER TABLE query for each table, then write them to output_file
    with open(f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/queries_to_alter_cond_tables.txt', 'a') as output_file:
        output_file.write(f"""ALTER TABLE {table_name} 
ALTER COLUMN {column}
TYPE {data_type};\n\n""")