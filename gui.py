import random

from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QApplication, QTextEdit, QPushButton, QProgressBar


class UI(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)

        self.textEdit = self.findChild(QTextEdit, "textEdit")
        self.pushButton = self.findChild(QPushButton, "pushButton")
        self.progressBar = self.findChild(QProgressBar, "progressBar")

        self.pushButton.clicked.connect(self.button_pushed)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)

    def button_pushed(self):
        self.textEdit.insertPlainText('hello world\n')
        self.textEdit.ensureCursorVisible()

    def update_progress(self):
        self.progressBar.setValue(random.randint(0, 100))
        self.timer.start(1000)


app = QApplication([])
window = UI()
window.show()
app.exec()
