import os
import sys
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
print(BASE_PATH)
#sys.path.insert(0,BASE_PATH.split('\\test')[0])

import time
import datetime


def check_run():
    
    print('check run started')
    

class MainDock(QDockWidget):
    """Main """
    def __init__(self):
        QDockWidget.__init__(self)
        
        e1 = QLineEdit()
        e1.setValidator(QIntValidator())
        e1.setMaxLength(4)
        e1.setAlignment(Qt.AlignCenter)
        e1.setFont(QFont("Arial",20))
                 
        e2 = QLineEdit()
        e2.setValidator(QDoubleValidator(0.99,99.99,2))        
         
        e3 = QLineEdit()
        e3.setInputMask('99.999.999.999')        
         
        e4 = QLineEdit()
        e4.textChanged.connect(self.textchanged)        
         
        e5 = QLineEdit()
        e5.setEchoMode(QLineEdit.Password)
        e5.editingFinished.connect(self.enterPress)
         
        e6 = QLineEdit("Hello IOT developers")
        e6.setReadOnly(True)        
        
        flo = QFormLayout()
        flo.addRow("integer validator", e1)
        flo.addRow("Double validator",e2)
        flo.addRow("Input Mask",e3)
        flo.addRow("Text changed",e4)
        flo.addRow("Password",e5)
        flo.addRow("Read Only",e6)        
        
        widget = QWidget(self)
        widget.setLayout(flo)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)        
        
        
    def textchanged(self,text):
        print ("contents of text box: "+text)
    
    def enterPress(self):
        print ("edited, enter pressed")    

class SettingsDock(QDockWidget):
    """Settings """

    def __init__(self):
        QDockWidget.__init__(self)

        # size boxes
        size_y_box = QSpinBox(self)
        size_y_box.setMinimum(1)
        size_x_box = QSpinBox(self)
        size_x_box.setMinimum(2)

        # start/goal boxes
        start_y_box = QSpinBox(self)
        start_x_box = QSpinBox(self)
        goal_y_box = QSpinBox(self)
        goal_x_box = QSpinBox(self)

        # main box layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop|Qt.AlignLeft)

        temp_widget = QCheckBox("R")
        temp_widget.setCheckState(Qt.Checked)
        temp_widget.stateChanged.connect(lambda:self.btnstate(temp_widget))
        vbox.addWidget(temp_widget)
        vbox.addWidget(QCheckBox("T"))
        
        vbox.addWidget(QLabel("W"))
        hbox_world_size = QHBoxLayout()
        hbox_world_size.addWidget(QLabel("Y"))
        hbox_world_size.addWidget(size_y_box)
        hbox_world_size.addWidget(QLabel("X"))
        hbox_world_size.addWidget(size_x_box)
        world_size_widget = QWidget()
        world_size_widget.setLayout(hbox_world_size)
        vbox.addWidget(world_size_widget)

        vbox.addWidget(QLabel("S"))
        hbox_start = QHBoxLayout()
        hbox_start.addWidget(QLabel("Y"))
        hbox_start.addWidget(start_y_box)
        hbox_start.addWidget(QLabel("X"))
        hbox_start.addWidget(start_x_box)
        start_widget = QWidget()
        start_widget.setLayout(hbox_start)
        vbox.addWidget(start_widget)

        vbox.addWidget(QLabel("G"))
        hbox_goal = QHBoxLayout()
        hbox_goal.addWidget(QLabel("Y"))
        hbox_goal.addWidget(goal_y_box)
        hbox_goal.addWidget(QLabel("X"))
        hbox_goal.addWidget(goal_x_box)
        goal_widget = QWidget()
        goal_widget.setLayout(hbox_goal)
        vbox.addWidget(goal_widget)

        widget = QWidget(self)
        widget.setLayout(vbox)
        self.setWidget(widget)
        
        
    def btnstate(self,b):
        if b.isChecked() == True:
            print (b.text()+" is selected")
        else:
            print (b.text()+" is deselected")

class MainSettingsDock(QDockWidget):
    """Dock settings."""

    world_list = ["Plu", "Pla"]
    algo_list = ["Plu", "Pla"]
    heuristic_list = ["Plu", "Pla"]

    def __init__(self):
        QDockWidget.__init__(self)

        # 1 chooser
        self.world_combo = QComboBox()
        self.world_combo.addItems(MainSettingsDock.world_list)
        self.world_combo.setItemIcon(0, QIcon('icons/2d_4neigh.png'))
        self.world_combo.setItemIcon(1, QIcon('icons/2d_8neigh.png'))

        # 2 chooser
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(MainSettingsDock.algo_list)
        #self.connect(self.algo_combo, SIGNAL('currentIndexChanged(int)'),
        #        self.update_algo)

        # 3 chooser
        self.heuristic_combo = QComboBox()
        self.heuristic_combo.addItems(MainSettingsDock.heuristic_list)
        self.heuristic_combo.setItemIcon(0, QIcon('icons/heur_manhattan.png'))
        self.heuristic_combo.setItemIcon(1, QIcon('icons/heur_euclidean.png'))

        #  settings
        vbox = QVBoxLayout()
        #vbox.setAlignment(Qt.AlignTop|Qt.AlignHCenter)
        vbox.addWidget(QLabel("Label1"))
        vbox.addWidget(self.world_combo)
        vbox.addWidget(QLabel("Label2"))
        vbox.addWidget(self.algo_combo)
        vbox.addWidget(QLabel("Label3"))
        vbox.addWidget(self.heuristic_combo)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setWidget(widget)
        
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)        

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 100, 600, 600)
        self.setWindowTitle('White Cubes GUI')        

        # Init QDockWidget objects
        #self.main_settings = MainSettingsDock()
        self.settings = SettingsDock()
        self.main = MainDock()
       
        # align to area 
        self.addDockWidget(Qt.RightDockWidgetArea, self.main)
        #self.addDockWidget(Qt.RightDockWidgetArea, self.main_settings)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.settings)        

        """ Build tool bar"""
        # check button
        check_button = QAction(QIcon('icons/play.png'),
                'Check', self)
        check_button.setShortcut('Ctrl+R')
        check_button.setStatusTip('check setups')
        check_button.triggered.connect(self.check)

        # reset button
        reset_button = QAction(QIcon('icons/stop.png'),
                'Reset', self)
        reset_button.setShortcut('Ctrl+T')
        reset_button.setStatusTip('reset setups list')
        reset_button.triggered.connect(self.reset_lists)

        # update button
        update_button = QAction(QIcon('icons/reset.png'),
                'Update', self)
        update_button.setShortcut('Ctrl+Y')
        update_button.setStatusTip('update status')
        update_button.triggered.connect(self.update_status)


        toolbar = self.addToolBar('Control')
        toolbar.addAction(reset_button)
        toolbar.addAction(check_button)
        toolbar_1 = self.addToolBar('Control')
        toolbar_1.addAction(update_button)

        # status bar
        self.statusBar()
    
    # executable methods for Main window's signals
    
    def check(self):
        print('check routine')
        check_run()
    
    def reset_lists(self):
        print('reset routine')
    
    def update_status(self):
        print('update status routine')
   

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
