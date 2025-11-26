from db_connect import create_connection

def insert_student(name, email, age):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, email, age) VALUES (%s,%s,%s)",
                (name, email, age))
    conn.commit()
    conn.close()

def read_students():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(student_id, new_email):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET email=%s WHERE id=%s",
                (new_email, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()
