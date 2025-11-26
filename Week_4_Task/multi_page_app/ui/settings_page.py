from PyQt5.QtWidgets import *

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setStyleSheet("font-size:26px; font-weight:bold;")

        layout.addWidget(title)
        layout.addWidget(QLabel("Settings page prototype"))
        layout.addStretch()

        self.setLayout(layout)
