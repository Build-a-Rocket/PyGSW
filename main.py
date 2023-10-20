from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6 import uic, QtCore


class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('UI File Path Here', self)

#app run starts here
app = QApplication([])
window = UI()
window.show()
app.exec()
