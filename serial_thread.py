from time import sleep
import serial
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QObject


class SerialThread(QObject):

    connectionFailed = pyqtSignal(str)
    connectionSuccess = pyqtSignal()
    readFailed = pyqtSignal(str)
    dataReceived = pyqtSignal(bytes)

    def __init__(self, serial_instance, fake=False, frequency=0.5):
        """\
        Initialize thread.
        Note that the serial_instance' timeout is set to one second!
        Other settings are not changed.
        """
        QObject.__init__(self)
        
        if not fake:
            self.serial = serial_instance
            self.serial.close()
            self.faking = False
        else:
            self.serial = open(serial_instance).readlines()
            self.faking = True
            self.frequency = frequency

        self.alive = True

    def stop(self):
        """Stop the reader thread"""
        self.alive = False

        if not self.faking:
            if hasattr(self.serial, 'cancel_read'):
                self.serial.cancel_read()

            self.serial.close()

    def run(self):
        if not self.faking:
            if not hasattr(self.serial, 'cancel_read'):
                self.serial.timeout = 1

            try:
                self.serial.open()
            except Exception as e:
                self.alive = False
                self.connectionFailed.emit(str(e))
                return
            error = None
            self.connectionSuccess.emit()

            while self.alive and self.serial.is_open:
                try:
                    # read all that is there or wait for one byte (blocking)
                    data = self.serial.read(self.serial.in_waiting or 1)
                except serial.SerialException as e:
                    # probably some I/O problem such as disconnected USB serial
                    # adapters -> exit
                    error = e
                    self.readFailed.emit(str(e))
                    break
                else:
                    if data:
                        # make a separated try-except for called user code
                        try:
                            self.dataReceived.emit(data)
                        except Exception as e:
                            error = e
                            self.readFailed.emit(str(e))
                            break
            self.alive = False
            self.connectionFailed.emit('Serial disconnected.')
        else:
            self.connectionSuccess.emit()
            i = 0

            while self.alive:
                try:
                    # wait and send a line of the csv
                    sleep(self.frequency)
                    self.dataReceived.emit(self.serial[i].encode('utf-8'))
                except serial.SerialException as e:
                    # probably something with the file we're reading
                    error = e
                    self.readFailed.emit(str(e))
                    break

                i += 1
                if i >= len(self.serial):
                    i = 0

            self.alive = False
            self.connectionFailed.emit('Serial disconnected.')

    @QtCore.pyqtSlot(bytes)
    def write(self, data):
        if not self.faking:
            self.serial.write(data)
