import mysql.connector

def connetc_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="AJecDSgxvS8eai4#",
            database="Team_AURA",
            port=3306
        )
        if connection.is_connected():
            query = """CREATE DATABASE IF NOT EXISTS Team_AURA"""
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.execute("USE Team_AURA;")
            print("Successfully connected to the database.")
            return connection

    except Exception as err:
        print(f"Error: {err}")
        return None
    
def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully.")
    except Exception as err:
        print(f"Error: {err} with data {data} and query {query}")


def create_Table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(50),
        age INT
    );
    """
    execute_query(conn, query)

def insert_student(conn, name, email, age):
    query = """
    INSERT INTO students (name, email, age)
    VALUES (%s, %s, %s);
    """
    data = (name, email, age)
    execute_query(conn, query, data)

def fetch_all(connection):
    query = "SELECT * FROM students;"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as err:
        print(f"Error: {err} while fetching data.")
        return None
        
def update_student(conn, name, email, age, student_id):
    query = """
    UPDATE students set name = %s, email = %s, age = %s
    WHERE id = %s;
    """
    data = (name, email, age, student_id)
    execute_query(conn, query, data)

def delete_student(conn, student_id):
    query = "DELETE FROM students WHERE id = %s;"
    data = (student_id,)
    execute_query(conn, query, data)

def main():
    connection = connetc_db()
    #create_Table(connection)
    #insert_student(connection, "John Doe", "john.doe@example.com", 25)
    #update_student(connection, "Jane Smith", "jane.smith@example.com", 30, 14)
    print(fetch_all(connection))
    delete_student(connection, 1)
    

main()