from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt6 import QtGui, uic, QtCore
from PyQt6.QtCore import Qt, QTimer
from random import randint


class UI(QWidget):

    def __init__(self):
        super().__init__()

        # loading the ui file with uic module
        uic.loadUi('main.ui', self)

        self.resetButton = self.findChild(QPushButton, 'resetButton')
        self.scoreLabel = self.findChild(QLabel, 'scoreLabel')

        self.gameGrid = self.findChild(QGridLayout, 'gameGrid')

        for col in range(0, 16):
            for row in range(0, 16):
                widget = QWidget()
                self.gameGrid.addWidget(widget, col, row)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDisplay)

        self.resetButton.clicked.connect(self.resetGame)
        self.resetGame()

    def resetGame(self):
        for col in range(0, 16):
            for row in range(0, 16):
                self.gameGrid.itemAtPosition(row, col).widget().setStyleSheet("background-color:black;")

        self.gameGrid.itemAtPosition(0, 0).widget().setStyleSheet("background-color:white;")

        self.x_queue = [0]
        self.y_queue = [0]

        self.x = 0
        self.y = 0
        self.score = 5

        self.dir_x = 1
        self.dir_y = 0

        self.addNewApple()

        self.timer.start(100)

    def keyPressEvent(self, a0):

        if a0.key() == Qt.Key.Key_W:
            self.dir_y = -1
            self.dir_x = 0
        elif a0.key() == Qt.Key.Key_S:
            self.dir_y = 1
            self.dir_x = 0
        elif a0.key() == Qt.Key.Key_A:
            self.dir_x = -1
            self.dir_y = 0
        elif a0.key() == Qt.Key.Key_D:
            self.dir_x = 1
            self.dir_y = 0

        return super().keyPressEvent(a0)
    
    def updateDisplay(self):
        # update current square
        if self.score == len(self.x_queue):
            x = self.x_queue.pop(0)
            y = self.y_queue.pop(0)

            if self.gameGrid.itemAtPosition(y, x).widget().styleSheet().find('red') == -1:
                self.gameGrid.itemAtPosition(y, x).widget().setStyleSheet("background-color:black;")

        # update position
        self.x += self.dir_x
        self.x %= 16

        self.y += self.dir_y
        self.y %= 16

        # update new square
        self.x_queue.append(self.x)
        self.y_queue.append(self.y)

        square = self.gameGrid.itemAtPosition(self.y, self.x).widget()
        
        color = square.styleSheet()

        if color.find('red') != -1:
            self.score += 1
            self.scoreLabel.setText('Score: ' + str(self.score))
            self.addNewApple()
        elif color.find('white') != -1:
            self.timer.stop()

        square.setStyleSheet("background-color:white;")

    def addNewApple(self):
        x = randint(0, 15)
        y = randint(0, 15)
        while not self.gameGrid.itemAtPosition(y, x).widget().styleSheet().find('white'):
            x = randint(0, 15)
            y = randint(0, 15)

        self.gameGrid.itemAtPosition(y, x).widget().setStyleSheet("background-color:red;")

app = QApplication([])
window = UI()
window.show()
app.exec()
