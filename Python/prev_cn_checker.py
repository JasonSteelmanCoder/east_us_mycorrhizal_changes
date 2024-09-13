import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cursor = connection.cursor()

cursor.execute("""

    SELECT prev_tre_cn FROM ri_tree WHERE prev_tre_cn IS NOT NULL

""")

prev_cn_rows = cursor.fetchall()

prev_cns = []

for row in prev_cn_rows:
    prev_cns.append(row[0])

for cn in prev_cns:
    cursor.execute(f"""

    SELECT statecd, unitcd, countycd, plot, subp, tree FROM ri_tree WHERE prev_tre_cn = {cn}

    """)

    referring_tree = cursor.fetchall()

    cursor.execute(f"""

    SELECT statecd, unitcd, countycd, plot, subp, tree FROM ri_tree WHERE cn = {cn}

    """)

    referenced_tree = cursor.fetchall()

    if referenced_tree != referring_tree:
        print("False")
