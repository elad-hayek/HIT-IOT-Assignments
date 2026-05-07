import os
import sys
# from PyQt5.QtWidgets import QWidget, QLabel, QApplication

import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        lbl1 = QLabel('Python code', self)
        lbl1.move(15, 10)
 
        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)
         
        lbl3 = QLabel('for IoT programmers', self)
        lbl3.move(55, 70)        
        
        b2 = QPushButton('image',self)
        b2.setIcon(QIcon(QPixmap("icons\\stop.png")))
        b2.clicked.connect(lambda:self.whichbtn(b2))
        b2.setStyleSheet("background-color:#ff0aa0;")
        
        b2.move(106,106)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute coordinates use')    
        self.show()
     
    def whichbtn(self,b):
    
        print('which button routine enabled: '+b.text())    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())