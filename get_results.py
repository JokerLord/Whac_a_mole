import sqlite3

conn = sqlite3.connect("kipish.db")
curs = conn.cursor()

curs.execute("SELECT * FROM list_of_players")
rows = curs.fetchall()
print(rows)

curs.close()
conn.close()
