from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt6 import QtGui, uic, QtCore
from PyQt6.QtCore import Qt, QTimer
from random import randint


class UI(QWidget):

    def __init__(self):
        super().__init__()


        self.xq = [0]
        self.yq = [0]
        self.x = 0
        self.y = 0
        self.xdir = 1
        self.ydir = 0
        self.score = 5
        # loading the ui file with uic module
        uic.loadUi('main.ui', self)
        self.gameBoard = self.findChild(QGridLayout, "gridLayout")
        self.scoreLabel = self.findChild(QLabel, "label")
        self.resetButton = self.findChild(QPushButton, "pushButton")
        
        for col in range(16):
            for row in range(16):
                widget = QWidget()
                self.gameBoard.addWidget(widget, col, row)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGame)

        self.resetButton.clicked.connect(self.reset)
        self.reset()
        
        
    def reset(self):
        for col in range(16):
            for row in range(16):
                self.gameBoard.itemAtPosition(col, row).widget().setStyleSheet("background-color:black;")
        
        self.gameBoard.itemAtPosition(0, 0).widget().setStyleSheet("background-color:white;")
        self.xq = [0]
        self.yq = [0]
        self.x = 0
        self.y = 0
        self.xdir = 1
        self.ydir = 0
        self.score = 5
        self.scoreLabel.setText("Score: " + str(self.score))
        
        self.createApple()
        self.timer.start(100)
        print("hello")
      
      
    def keyPressEvent(self, a0):
        
        if a0.key() == Qt.Key.Key_W:
            print("w")

            self.xdir = 0
            self.ydir = -1
        if a0.key() == Qt.Key.Key_A:
            print("a")
            self.xdir = -1
            self.ydir = 0

        if a0.key() == Qt.Key.Key_S:
            print("s")
            

            self.xdir = 0
            self.ydir = 1
        if a0.key() == Qt.Key.Key_D:
            print("d")
            self.xdir = 1
            self.ydir = 0

            
        return super().keyPressEvent(a0)
          
    def updateGame(self):
        if self.score == len(self.xq):
            x = self.xq.pop(0)
            y = self.yq.pop(0)
            
            if self.gameBoard.itemAtPosition(y, x).widget().styleSheet().find("red"):
                self.gameBoard.itemAtPosition(y, x).widget().setStyleSheet("background-color:black;")
            
        self.x += self.xdir
        self.y += self.ydir
        
        self.x %= 16
        self.y %= 16
        
        self.xq.append(self.x)
        self.yq.append(self.y)
        wid = self.gameBoard.itemAtPosition(self.y, self.x).widget()
        
        if wid.styleSheet().find("white") != -1:
            self.timer.stop()
            
        if wid.styleSheet().find("red") != -1:
            
            self.createApple()
            self.score += 1
            self.scoreLabel.setText("Score: " + str(self.score))
        
        wid.setStyleSheet("background-color:white;")
        

    def createApple(self):
        x = randint(0, 15)
        y = randint(0, 15)
        self.gameBoard.itemAtPosition(y, x).widget().setStyleSheet("background-color:red;")
        

app = QApplication([])
window = UI()
window.show()
app.exec()
