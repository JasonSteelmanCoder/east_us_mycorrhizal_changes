""" This program provides a function for writing a SQL query. The query will create a 
table in the database with all of the columns from your state level csv table. It takes its 
best guess at what datatype each column should be. Incorrect datatypes can be corrected with 
ALTER TABLE queries. (See alter_looper.py.) """

import csv
import re
from dotenv import load_dotenv
import os

load_dotenv()

# SAMPLE ARGUMENTS:
# table_name = "al_plot"
# path = f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/eastern_us_data/AL_PLOT.csv'

def write_sql_query_to_make_csv_columns(table_name, path):

    with open(path, 'r') as file:
        csv_reader = csv.reader(file)

        # make the reader into a list of two rows
        csv_rows = []
        i = 0
        for row in csv_reader:
            if i > 1:
                break
            else:
                csv_rows.append(row)
                i += 1

        # make lists of the columns and values
        columns = [column for column in csv_rows[0]]
        values = [value for value in csv_rows[1]]
        
        # build query
        query = f'CREATE TABLE {table_name} (\n'
        for i in range(len(columns)):
            # add the column name to the query
            query += '\t'
            query += columns[i]
            query += " "

            # find datatype and add it to the query
            datatype = ""
            if len(values[i]) == 0:
                datatype = "double precision"
            elif values[i].isnumeric() and not values[i].isalpha():
                if int(values[i]) < 9999:
                    datatype = "smallint"
                else:
                    datatype = "bigint"
            elif re.match(r'^\d*\.\d+$', values[i]):
                datatype = "double precision"
            else:
                datatype = "text"
            query += datatype
            query += ",\n"

        query = query[:-2]      # strip the trailing comma
        query += "\n);"
        print(query)
        return query

if __name__ == "__main__":
    # replace the arguments below to use the function without exporting it.
    write_sql_query_to_make_csv_columns('sites', f'C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/phillips_worm_data/1880_Phillips/SiteData_sWorm_2021-02-18.csv')