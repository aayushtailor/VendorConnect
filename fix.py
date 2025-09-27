import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("ALTER TABLE vendors ADD COLUMN description TEXT")
conn.commit()
conn.close()
print("Column 'description' added successfully.")
