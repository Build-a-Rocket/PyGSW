import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6 import uic, QtCore
from PyQt6.QtCore import QThread

from serial_thread import SerialThread

class UI(QWidget):
    def __init__(self):
        super().__init__()
        # loading the ui file with uic module
        uic.loadUi('tutorial.ui', self)
        self.button = self.findChild(QPushButton, 'numberButton')
        self.button.clicked.connect(self.buttonClick)
        self.label = self.findChild(QLabel, 'label')

        serial_port = "04-16-2023_16-25-07.csv"
        self.serialStream = SerialThread(serial_port, fake=True)

        self.myThread = QThread()
        self.serialStream.moveToThread(self.myThread)    

        self.myThread.started.connect(self.serialStream.run)
        self.serialStream.dataReceived.connect(self.printSerial)  


    def buttonClick(self):
        self.label.setText(str(random.randint(0, 100)))

    def printSerial(self, data):
        print(data)

app = QApplication([])
window = UI()
window.show()
app.exec()