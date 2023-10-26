import random

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTextEdit
from PyQt6 import uic, QtCore
from PyQt6.QtCore import QThread

from serial_thread import SerialThread
from serial import unicode

from tele_graph import PlotWidget, TelemetryGraph

class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('gsw.ui', self)

        #self.button = self.findChild(QPushButton, 'numberButton')
        #self.button.clicked.connect(self.buttonClick)

        #self.label = self.findChild(QLabel, 'label')

        self.outputBox = self.findChild(QTextEdit, 'outputBox')

        self.altitudeGraph = TelemetryGraph(self.findChild(PlotWidget, 'altitudeGraph'))
        self.altitudeGraph.setTitle('Altitude Graph')
        self.altitudeGraph.addLine()

        self.tempGraph = TelemetryGraph(self.findChild(PlotWidget, 'tempGraph'))
        self.tempGraph.setTitle('Temperature Graph')
        self.tempGraph.addLine()

        self.accelGraph = TelemetryGraph(self.findChild(PlotWidget, 'accelGraph'))
        self.accelGraph.setTitle('Acceleration Graph')
        self.accelGraph.addLine('X', 'red')
        self.accelGraph.addLine('Y', 'green')
        self.accelGraph.addLine('Z', 'blue')

        self.gyroGraph = TelemetryGraph(self.findChild(PlotWidget, 'gyroGraph'))
        self.gyroGraph.setTitle('Gyro Graph')
        self.gyroGraph.addLine('X', 'red')
        self.gyroGraph.addLine('Y', 'green')
        self.gyroGraph.addLine('Z', 'blue')

        serial_port = '04-16-2023_16-25-07.csv'
        self.serial_thread = SerialThread(serial_port, fake=True)

        self._thread = QThread()
        self.serial_thread.moveToThread(self._thread)

        self._thread.started.connect(self.serial_thread.run)

        self.serial_thread.dataReceived.connect(self.data_received)

        self._thread.start()

        self.x = 0

    def buttonClick(self):
        self.label.setText(str(random.randint(0, 100)))

    def data_received(self, data):
        data = unicode(data, errors='ignore')

        self.outputBox.insertPlainText(data + '\n')
        self.outputBox.ensureCursorVisible()

        data = data.split(',')

        self.x += 1

        # graph one a data channel
        self.altitudeGraph.plotData(float(data[0]), self.x)

        self.tempGraph.plotData(float(data[1]), self.x)

        self.accelGraph.plotData(float(data[2]), self.x, 'X')
        self.accelGraph.plotData(float(data[3]), self.x, 'Y')
        self.accelGraph.plotData(float(data[4]), self.x, 'Z')

        self.gyroGraph.plotData(float(data[5]), self.x, 'X')
        self.gyroGraph.plotData(float(data[6]), self.x, 'Y')
        self.gyroGraph.plotData(float(data[7]), self.x, 'Z')

app = QApplication([])
window = UI()
window.show()
app.exec()
