import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="AJecDSgxvS8eai4#", database="UIU_Mariner",port=3306)


if conn.is_connected():
    print("Successfully connected to the database")