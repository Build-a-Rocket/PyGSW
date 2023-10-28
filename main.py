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
        self.textBox = self.findChild(QTextEdit, 'outputBox')

        serial_port = "04-16-2023_16-25-07.csv"
        self.serialStream = SerialThread(serial_port, fake=True)
        self.x = 0
        
        self.gyroGraph = TelemetryGraph(self.findChild(PlotWidget, "gyroGraph"))
        self.gyroGraph.setTitle(name="Gyroscope Graph")
        self.gyroGraph.addLine(name="GyroX", color="red")
        self.gyroGraph.addLine(name="GyroY", color="green")
        self.gyroGraph.addLine(name="GyroZ", color="blue")


        self.myThread = QThread()
        self.serialStream.moveToThread(self.myThread)    

        self.myThread.started.connect(self.serialStream.run)
        self.serialStream.dataReceived.connect(self.printSerial)  

        self.myThread.start()






    def buttonClick(self):
        self.label.setText(str(random.randint(0, 100)))

    def printSerial(self, data):
        data = unicode(data, errors='ignore')
        data = data.split(',')
        printdata = "\n"
        printdata += "Altitude: " + data[0] + "\n"
        printdata += "Temperature: " + data[1] + "\n"
        printdata += "GyroX: " + data[2] + "\n"
        printdata += "GyroY: " + data[3] + "\n"
        printdata += "GyroZ: " + data[4] + "\n"
        printdata += "AccelX: " + data[5] + "\n"
        printdata += "AccelY: " + data[6] + "\n"
        printdata += "AccelZ: " + data[7] + "\n"
        printdata += "Accel Mag: " + data[8] + "\n"
        self.x+=1
        self.gyroGraph.plotData(float(data[2]), self.x, "GyroX")
        self.gyroGraph.plotData(float(data[3]), self.x, "GyroY")
        self.gyroGraph.plotData(float(data[4]), self.x, "GyroZ")

        self.textBox.setText(printdata)
        print(data)
        

app = QApplication([])
window = UI()
window.show()
app.exec()