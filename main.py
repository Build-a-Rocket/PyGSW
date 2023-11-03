from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt6 import QtGui, uic, QtCore
from PyQt6.QtCore import Qt, QTimer
from random import randint


class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('main.ui', self)



app = QApplication([])
window = UI()
window.show()
app.exec()
