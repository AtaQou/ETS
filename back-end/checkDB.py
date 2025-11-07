import sqlite3

conn = sqlite3.connect('ETSsqLiteDB')
c = conn.cursor()
c.execute("SELECT * FROM users")
users = c.fetchall()
print(users)
conn.close()
