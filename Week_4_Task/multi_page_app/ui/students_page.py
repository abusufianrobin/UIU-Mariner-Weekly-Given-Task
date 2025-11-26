from PyQt5.QtWidgets import *

class StudentsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Students Page")
        title.setStyleSheet("font-size:26px; font-weight:bold;")

        table = QTableWidget(3, 3)
        table.setHorizontalHeaderLabels(["Name", "Email", "Age"])

        table.setItem(0, 0, QTableWidgetItem("Rajib"))
        table.setItem(0, 1, QTableWidgetItem("rajib@uiu.ac.bd"))
        table.setItem(0, 2, QTableWidgetItem("23"))

        table.setItem(1, 0, QTableWidgetItem("Tanvir"))
        table.setItem(1, 1, QTableWidgetItem("tanvir@uiu.ac.bd"))
        table.setItem(1, 2, QTableWidgetItem("24"))

        layout.addWidget(title)
        layout.addWidget(table)
        layout.addStretch()

        self.setLayout(layout)
