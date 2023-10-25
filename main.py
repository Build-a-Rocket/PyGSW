from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit
from PyQt6 import uic, QtCore
from pyqtgraph import PlotWidget
from serial import Serial, unicode

from serial_thread import SerialThread
from tele_graph import TelemetryGraph


class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('gsw.ui', self)

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

        self.outputBox = self.findChild(QTextEdit, 'outputBox')
        self.messageBox = self.findChild(QTextEdit, 'messageBox')
        self.serialThread.dataReceived.connect(self.updateOutputBox)

        # setup graphs
        self.altitudeGraph = TelemetryGraph(self.findChild(PlotWidget, 'altitudeGraph'))
        self.altitudeGraph.setTitle('Altitude')
        self.altitudeGraph.addLine()

        self.tempGraph = TelemetryGraph(self.findChild(PlotWidget, 'tempGraph'))
        self.tempGraph.setTitle('Temperature')
        self.tempGraph.addLine()

        self.accelGraph = TelemetryGraph(self.findChild(PlotWidget, 'accelGraph'), legend=True)
        self.accelGraph.setTitle('Acceleration')
        self.accelGraph.addLine('x', 'red')
        self.accelGraph.addLine('y', 'green')
        self.accelGraph.addLine('z', 'blue')

        self.gyroGraph = TelemetryGraph(self.findChild(PlotWidget, 'gyroGraph'), legend=True)
        self.gyroGraph.setTitle('Gyro')
        self.gyroGraph.addLine('x', 'red')
        self.gyroGraph.addLine('y', 'green')
        self.gyroGraph.addLine('z', 'blue')

        self.x = 0

        self._thread.start()  # do this last!!!! this will make the serial port start reading

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
        try:
            data = unicode(data, errors='ignore').split(',')

            telemetry = 'Altitude: %s\nTemperature: %s\n'\
                        'Accel X: %s\nAccel Y: %s\nAccel Z: %s\n'\
                        'Gyro X: %s\nGyro Y: %s\nGyro Z: %s\n\n'\
                        % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

            self.outputBox.insertPlainText(telemetry)
            self.outputBox.ensureCursorVisible()

            self.x += 1

            self.altitudeGraph.plotData(float(data[1]), self.x)
            self.tempGraph.plotData(float(data[2]), self.x)

            self.accelGraph.plotData(float(data[3]), self.x, name='x')
            self.accelGraph.plotData(float(data[4]), self.x, name='y')
            self.accelGraph.plotData(float(data[5]), self.x, name='z')

            self.gyroGraph.plotData(float(data[6]), self.x, name='x')
            self.gyroGraph.plotData(float(data[7]), self.x, name='y')
            self.gyroGraph.plotData(float(data[8]), self.x, name='z')

        except Exception as e:
            print(str(e))

    def closeEvent(self, event):
        self.serialThread.stop()
        self._thread.quit()
        self._thread.wait()


app = QApplication([])
window = UI()
window.show()
app.exec()