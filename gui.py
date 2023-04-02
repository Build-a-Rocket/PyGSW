from PyQt6 import uic
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton, QApplication
from serial import Serial, unicode

from serial_thread import SerialThread


class UI(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)

        self.textEdit = self.findChild(QTextEdit, "textEdit")
        self.pushButton = self.findChild(QPushButton, "pushButton")

        self.pushButton.clicked.connect(self.button_pushed)

        serial = Serial('COM18', 2000000, dsrdtr=True)
        self.serialThread = SerialThread(serial)

        self._thread = QThread()
        self.serialThread.moveToThread(self._thread)
        self._thread.started.connect(self.serialThread.run)

        self.serialThread.dataReceived.connect(self.on_dataReceived)

        self._thread.start()

    def on_dataReceived(self, data):
        self.textEdit.insertPlainText(unicode(data, errors='ignore'))
        self.textEdit.ensureCursorVisible()

    def button_pushed(self):
        self.textEdit.insertPlainText('hello world\n')
        self.textEdit.ensureCursorVisible()


app = QApplication([])
window = UI()
window.show()
app.exec()
