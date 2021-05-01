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
        conn.close()

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
        c.execute("SELECT * FROM inv WHERE user = ?",(user,))
        result = c.fetchall()
        return result
    else:
        sqlite_insert_with_param = "INSERT INTO inv (user) VALUES (?);"
        data_tuple = (user,)
        c.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()  
        conn.close()
        c.execute("SELECT * FROM inv WHERE user = ?",(user,))
        result = c.fetchall()
        return result



def null_type(user,conn,c):
    itemnum = "0"
    num = 0
    ha = c.fetchone()
    while ha != None:
        item = "item"
        num = num + 1
        num = str(num)
        itemnum = item + num
        num = int(num)
        try:
            c.execute("SELECT ? FROM inv WHERE user = ?",(itemnum,user,))
        except:
            break
    return itemnum

    