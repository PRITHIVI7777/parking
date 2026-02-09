import sqlite3

db = sqlite3.connect("parking.db")
cur = db.cursor()

# Drop table if exists
try:
    cur.execute("DROP TABLE IF EXISTS parking_slots")
except:
    pass

cur.execute("""
CREATE TABLE parking_slots (
    slot_no TEXT PRIMARY KEY,
    zone TEXT,
    vehicle_type TEXT,
    length REAL,
    width REAL,
    status TEXT
)
""")

# Student Car Slots
cur.execute("INSERT INTO parking_slots VALUES ('SC1','student','car',5,2,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('SC2','student','car',4.5,2,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('SC3','student','car',5.5,2.2,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('SC4','student','car',4.8,2.1,'FREE')")

# Student Bike Slots
cur.execute("INSERT INTO parking_slots VALUES ('SB1','student','bike',2.5,1,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('SB2','student','bike',2.3,0.9,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('SB3','student','bike',2.6,1.1,'FREE')")

# Staff Car Slots
cur.execute("INSERT INTO parking_slots VALUES ('TC1','staff','car',5,2.2,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('TC2','staff','car',5.2,2.3,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('TC3','staff','car',4.9,2.1,'FREE')")

# Staff Bike Slots
cur.execute("INSERT INTO parking_slots VALUES ('TB1','staff','bike',2.6,1,'FREE')")
cur.execute("INSERT INTO parking_slots VALUES ('TB2','staff','bike',2.4,0.95,'FREE')")

db.commit()
db.close()
