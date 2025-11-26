import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Team_AURA",
    port=3308
)
print("Connection OK")
if conn.is_connected():
    print("Successfully connected to the database")