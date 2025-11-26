import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Test PyQt GUI")
window.setGeometry(100, 100, 400, 200)
label = QLabel("Hello PyQt!", window)
label.move(50, 80)
window.show()
sys.exit(app.exec())
