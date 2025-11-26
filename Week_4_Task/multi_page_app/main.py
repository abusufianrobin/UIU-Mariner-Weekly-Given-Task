import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.home_page import HomePage
from ui.students_page import StudentsPage
from ui.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Multi-Page Prototype")
        self.setGeometry(200, 100, 1000, 600)

        # Main layout
        container = QWidget()
        main_layout = QHBoxLayout(container)

        # =============== Sidebar ==================
        sidebar = QVBoxLayout()
        sidebar.setSpacing(20)
        sidebar.setContentsMargins(15, 15, 15, 15)

        btn_home = QPushButton("🏠 Home")
        btn_students = QPushButton("👨‍🎓 Students")
        btn_settings = QPushButton("⚙ Settings")

        for btn in (btn_home, btn_students, btn_settings):
            btn.setFixedHeight(45)
            btn.setStyleSheet("font-size:16px; text-align:left; padding-left:10px;")
            sidebar.addWidget(btn)

        sidebar.addStretch()

        # =============== Stacked Pages ==================
        self.pages = QStackedWidget()
        self.pages.addWidget(HomePage())
        self.pages.addWidget(StudentsPage())
        self.pages.addWidget(SettingsPage())

        # Add to main layout
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.pages, 4)

        self.setCentralWidget(container)

        # Button events
        btn_home.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        btn_students.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        btn_settings.clicked.connect(lambda: self.pages.setCurrentIndex(2))


# Run App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
