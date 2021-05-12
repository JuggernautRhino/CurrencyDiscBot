import sqlite3

def connection():
    conn = sqlite3.connect("Bal.db")
    c = conn.cursor()
    return conn, c


def get_value(conn, c, user, amount):
    c.execute("SELECT balance FROM users WHERE user = ?", (user, ))
    for row in c.fetchall():
        value = row[0]
    value = value + int(amount)
    c.execute("UPDATE users SET balance = ? WHERE user = ? ", (
        value,
        user,
    ))
    conn.commit()



#can be negative
def get_inv(conn,c,user,iitem):
    num = 0
    ha = "aaaaaaa"
    while ha != (None,):
        item = "item"
        num = num + 1
        num = str(num)
        global itemnum
        itemnum = str(item + num)
        num = int(num)
        try:
            buying = "SELECT "+itemnum+" FROM inv WHERE user = ?"
            c.execute(buying, (user,))

            ha = c.fetchone()#omg did i just find an actual use for a do-while loop   -- guess not
            print(ha)#possibly      
#this is mad
        except:
            break
    print(itemnum)                        
    buying = "UPDATE inv SET "+itemnum+" = ? WHERE user = ? "
    c.execute(buying, (iitem,user,))
    conn.commit()
