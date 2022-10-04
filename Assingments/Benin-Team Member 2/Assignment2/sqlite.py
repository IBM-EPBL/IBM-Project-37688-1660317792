import sqlite3

conn=sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE registerDetails(firstname TEXT,lastname TEXT,email TEXT,password TEXT)')
print("Table created sucessfully")
conn.close()