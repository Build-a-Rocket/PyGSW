import random

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6 import uic, QtCore
from PyQt6.QtCore import QThread

from serial import Serial, unicode
from serial_thread import SerialThread



class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('tutorial.ui', self)

        self.button = self.findChild(QPushButton, 'numberButton')
        self.button.clicked.connect(self.buttonClick)

        self.label = self.findChild(QLabel, 'label')

        # Initiate serial port
        #self.serial_port = Serial('COM18', 2000000, dsrdtr=True)
        self.serial_port = '04-16-2023_16-25-07.csv'

        # Initiate Serial Thread
        self.serialThread = SerialThread(self.serial_port, fake=True)
        self._thread = QThread()
        self.serialThread.moveToThread(self._thread)

        self.serialThread.connectionSuccess.connect(self.connection_success)
        self.serialThread.connectionFailed.connect(self.connection_failed)
        self.serialThread.readFailed.connect(self.error_on_read)

        self._thread.started.connect(self.serialThread.run)

        self.serialThread.dataReceived.connect(self.updateOutputBox)

        self._thread.start()

    def buttonClick(self):
        self.label.setText(str(random.randint(0, 100)))

    @QtCore.pyqtSlot()
    def connection_success(self):
        print('Connected!')

    @QtCore.pyqtSlot(str)
    def connection_failed(self, error):
        print(error)

    @QtCore.pyqtSlot(str)
    def error_on_read(self, error):
        print(error)

    @QtCore.pyqtSlot(bytes)
    def updateOutputBox(self, data):
        print(unicode(data, errors='ignore'))

    def closeEvent(self, event):
        self.serialThread.stop()
        self._thread.quit()
        self._thread.wait()


app = QApplication([])
window = UI()
window.show()
app.exec()
