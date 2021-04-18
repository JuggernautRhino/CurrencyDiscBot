import sqlite3

def tableCreation():
    # Connect to database
    conn = sqlite3.connect('Bal.db')

    # create a cursor
    c = conn.cursor()

    #creating the table
    c.execute("""CREATE TABLE users (

        user TEXT,
        balance INTEGER


    )
        """)  #you can define the datatype as one of 5 datatypes == NULL, INTEGER, REAL, TEXT, BLOB