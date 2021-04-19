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




def inv_tableCreation():
    # Connect to database
    conn = sqlite3.connect('Bal.db')

    # create a cursor
    c = conn.cursor()

    #creating the table
    c.execute("""CREATE TABLE inv (

        user TEXT,
        item1 TEXT,
        item2 TEXT,
        item3 TEXT,
        item4 TEXT,
        item5 TEXT,
        item6 TEXT,
        item7 TEXT,
        item8 TEXT,
        item9 TEXT,
        item10 TEXT,
        item11 TEXT,
        item12 TEXT,
        item13 TEXT,
        item14 TEXT,
        item15 TEXT,
        item16 TEXT,
        item17 TEXT,
        item18 TEXT,
        item19 TEXT,
        item20 TEXT,
        item21 TEXT,
        item22 TEXT,
        item23 TEXT,
        item24 TEXT,
        item25 TEXT

    )
        """)  #you can define the datatype as one of 5 datatypes == NULL, INTEGER, REAL, TEXT, BLOB