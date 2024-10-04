# creating database and table using sqlite3

import sqlite3
conn = sqlite3.connect('loan_approval.db') # database created
cur = conn.cursor()

# table creation
query_to_create_table = """
    create table client_details(
        No_of_dependents int,
        Annual_income float,
        Loan_amount float,
        Loan_term int,
        Cibil_Score float,
        Residential_Assets_Value float,
        Commercial_Assets_Value float,
        Luxury_Assets_Value float,
        Bank_Asset_Value float,

        Education varchar (20),
        Self_employed varchar (5),
        Loan_status varchar (10)
    )
"""

cur.execute(query_to_create_table) 
print('YOUR DATABASE AND TABLE HAVE BEEN CREATED')
cur.close()
conn.close()