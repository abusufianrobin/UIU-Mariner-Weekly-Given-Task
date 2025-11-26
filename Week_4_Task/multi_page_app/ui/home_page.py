from PyQt5.QtWidgets import *

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Welcome to Dashboard")
        title.setStyleSheet("font-size:28px; font-weight:bold;")

        subtitle = QLabel("This is the home page prototype.")
        subtitle.setStyleSheet("font-size:18px; color:gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        self.setLayout(layout)
