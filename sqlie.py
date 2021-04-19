import sqlite3
def connection():
        conn = sqlite3.connect("Bal.db")
        c = conn.cursor()
        return conn,c

def get_value(conn,c,user,amount):
        c.execute("SELECT balance FROM users WHERE user = ?",(user,))
        for row in c.fetchall():
            value = row[0]
        value = value + int(amount)
        c.execute("UPDATE users SET balance = ? WHERE user = ? ",(value,user,))
        conn.commit()

def get_inv(item,quantity):
  