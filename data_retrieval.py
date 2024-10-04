
import sqlite3
conn = sqlite3.connect('loan_approval.db')
cur = conn.cursor()

query = "select * from client_details;"
cur.execute(query)

for record in cur.fetchall():
    print(record)

cur.close()
conn.close()
