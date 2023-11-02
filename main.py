from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic, QtCore


class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('main.ui', self)


app = QApplication([])
window = UI()
window.show()
app.exec()
