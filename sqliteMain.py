import sqlite3

conn = sqlite3.connect(r"data\bills.db")
cursor = conn.cursor()

with open("data/test.jpg", 'rb') as f:
    img = f.read()
name = 'test'
cursor.execute("""CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT, img BLOB) """)
cursor.execute("""INSERT INTO my_table (name,img) VALUES (?,?)""", (name,img))

conn.commit()
cursor.close()
conn.close()


"""CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, img BLOB) """