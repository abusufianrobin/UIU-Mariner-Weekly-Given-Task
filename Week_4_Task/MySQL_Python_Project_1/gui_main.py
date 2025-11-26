import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from db_connect import create_connection
from pandas_sql import export_to_csv

class StudentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UIU Mariner Student Management")
        self.setGeometry(100, 100, 700, 400)
        try:
            self.conn = create_connection()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            sys.exit(1)
        self.initUI()
        self.load_data()

    def initUI(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        # Input fields
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Name")
        self.email_input = QLineEdit(); self.email_input.setPlaceholderText("Email")
        self.age_input = QLineEdit(); self.age_input.setPlaceholderText("Age")
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.email_input)
        input_layout.addWidget(self.age_input)
        self.layout.addLayout(input_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Student")
        self.update_btn = QPushButton("Update Email")
        self.delete_btn = QPushButton("Delete Student")
        self.export_btn = QPushButton("Export to CSV")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.export_btn)
        self.layout.addLayout(btn_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Age"])
        self.layout.addWidget(self.table)

        # Connect buttons
        self.add_btn.clicked.connect(self.add_student)
        self.update_btn.clicked.connect(self.update_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.export_btn.clicked.connect(self.export_csv)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def load_data(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            self.table.setRowCount(0)
            for row_idx, row_data in enumerate(rows):
                self.table.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Data", str(e))

    def add_student(self):
        name, email, age = self.name_input.text(), self.email_input.text(), self.age_input.text()
        if name and email and age:
            try:
                cur = self.conn.cursor()
                cur.execute(
                    "INSERT INTO students (name,email,age) VALUES (%s,%s,%s)",
                    (name,email,int(age))
                )
                self.conn.commit()
                QMessageBox.information(self,"Success","Student added successfully!")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self,"Error", str(e))
        else:
            QMessageBox.warning(self,"Input Error","Please fill all fields.")

    def update_student(self):
        selected = self.table.currentRow()
        if selected >= 0:
            student_id = int(self.table.item(selected,0).text())
            new_email = self.email_input.text()
            if new_email:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE students SET email=%s WHERE id=%s",(new_email, student_id))
                    self.conn.commit()
                    QMessageBox.information(self,"Success","Email updated successfully!")
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self,"Error", str(e))
            else:
                QMessageBox.warning(self,"Input Error","Enter new email to update.")
        else:
            QMessageBox.warning(self,"Selection Error","Select a student first.")

    def delete_student(self):
        selected = self.table.currentRow()
        if selected >= 0:
            student_id = int(self.table.item(selected,0).text())
            try:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM students WHERE id=%s",(student_id,))
                self.conn.commit()
                QMessageBox.information(self,"Success","Student deleted successfully!")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self,"Error", str(e))
        else:
            QMessageBox.warning(self,"Selection Error","Select a student first.")

    def export_csv(self):
        try:
            export_to_csv()
            QMessageBox.information(self,"Export","Data exported to students.csv successfully!")
        except Exception as e:
            QMessageBox.critical(self,"Error", str(e))


if __name__ == "__main__":
    import sys
    try:
        app = QApplication(sys.argv)
        window = StudentApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        print("Error launching GUI:")
        traceback.print_exc()

