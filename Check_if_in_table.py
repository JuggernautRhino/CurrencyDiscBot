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

def check_inv(user,conn,c):
    user = str(user)
    # Create cursor object
    conn = sqlite3.connect('Bal.db')
    c = conn.cursor()
    # run a select query against the table to see if any record exists
    # that has the email or username
    c.execute("SELECT user FROM inv WHERE user = ?",(user,))


    result = c.fetchone()

    if result:
        conn.close()
    else:
        sqlite_insert_with_param = "INSERT INTO inv (user) VALUES (?);"
        data_tuple = (user,)
        c.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()  
        conn.close()
    return result



def nulltype(user,conn,c):
    num = 0
    while 0 != True:
        item = "item"
        num = num + 1
        num = str(num)
        itemnum = item + num
        try:
            print("")
        except:
            break

    