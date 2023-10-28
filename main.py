import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6 import uic, QtCore

class UI(QWidget):
    def __init__(self):
        super().__init__()
        # loading the ui file with uic module
        uic.loadUi('tutorial.ui', self)
        self.button = self.findChild(QPushButton, 'numberButton')
        self.button.clicked.connect(self.buttonClick)
        self.label = self.findChild(QLabel, 'label')
    def buttonClick(self):
        self.label.setText(str(random.randint(0, 100)))

app = QApplication([])
window = UI()
window.show()
app.exec()