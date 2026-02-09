import sqlite3

conn = sqlite3.connect("parking.db")
cur = conn.cursor()

cur.execute("SELECT * FROM parking_slots")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
