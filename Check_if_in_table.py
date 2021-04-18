import sqlite3
def check(user):

    # Create cursor object
    conn = sqlite3.connect('Bal.db')
    c = conn.cursor()
    # run a select query against the table to see if any record exists
    # that has the email or username
    c.execute("SELECT user FROM users WHERE user = ?",(user,))


    result = c.fetchone()

    if result:
        print("")
    else:
        score = 0
        c.execute("INSERT INTO users VALUES (?,?)", (user,score))
        conn.commit()