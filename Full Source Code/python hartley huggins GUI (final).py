# parts :
    # THE ALL GRAPH WINDOW
    # GUI design class (MAIN THREAD)
    # MOTOR FRONT END SECTION
    # GRAPH SECTION 
    # COMBO BOXES
    # SAVING THE FILES
    # RESUME AND PAUSE
    # MOTOR  MOVEMENT 
    # ARDUINO  STATIONARY  SECTION 
    # NEW WINDOW FOR GRAPH FUNCTION
# ------------------------------------------------


# Library imports -------------------------------------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib import style

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import time
import serial
import serial.tools.list_ports as ps
from math import sqrt
import numpy as np

# from sampyapt import APTMotor

#######################################################################################################
#   for the apt motor interface to work, make sure to include the APT.dll, APT.lib and sampyapt.py in the same directory as of this file


#######################################################################################################

#------------------------------------------------------------------------------------------
    # class definition for the graphs -------------------------------------------------------------

class MplCanvas(FigureCanvasQTAgg):
        
    def __init__(self, parent=None, width=10, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # self.axes.FigureCanvas
        super(MplCanvas, self).__init__(fig)
        
        
#------------------------------------------------------------------------------------------
    # the parallel thread -------------------------------------------------------------
    
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker,self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        
    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        self.fn(*self.args, **self.kwargs)


#------------------------------------------------------------------------------------------
#                                     THE ALL GRAPH WINDOW
#------------------------------------------------------------------------------------------
       
class graphwindow(QWidget):
    def __init__(self,g1,g2,g3,g4,g5,fromVal,toVal,motor):
        super().__init__()
        self.setGeometry(50, 50, 1850, 900)
        self.setWindowTitle('GUI graphs')
        layout2 = QVBoxLayout()
        self.setObjectName('graphwindow')
        
        self.setLayout(layout2)
        # initializing the lists containing the graph vals ---------------------
        self.g1 = g1        
        self.g2 = g2
        self.g3 = g3
        self.g4 = g4
        self.g5 = g5
        self.fromVal = fromVal
        self.toVal = toVal
        self.fna1 = []
        self.fna2 = []
        self.motor = motor

        # addition for getting fore+aft -----------------
        for i in range(len(g1)):
            self.fna1.append(g1[i]+g4[i])
            self.fna2.append(g2[i]+g3[i])
       
        self.theplotted(self.g1,'Fore HH',10,10,440,400)
        self.theplotted(self.g2,'Fore HU',475,10,440,400)                                                          
        self.theplotted(self.g3,'Aft HU',10,430,440,400)                                                           
        self.theplotted(self.g4,'Aft HH',475,430,440,400)                                                          
        self.theplotted(self.fna1,'HH combined',935,10,440,400)                                                    
        self.theplotted(self.fna2,'HU combined',1400,10,440,400)                                                   
        self.theplottedtwice(self.g1,self.g4,'Fore+Aft HH',935,430,440,400)                                        
        self.theplottedtwice(self.g2,self.g3,'Fore+Aft HU',1400,430,440,400)                                                
        
    # Common Function for plotting the graph: ---------------- 
              # x = the first plot
              # y = the second plot
              # a,b,c,d = geometry of grBox, cor(a,b),size(c,d)
              # name    = name of the grBox
              # fromVal,toVal = the range of motion in degrees
              # motor   = True if mode is FOV
              
    
    # Graph with one plot:
    def theplotted(self,x,name,a,b,c,d):
        self.G_grph = QtWidgets.QGroupBox(self)
        self.G_grph.setGeometry(QtCore.QRect(a, b, c, d))
        self.G_grph.setObjectName(name)
        self.G_grph.setTitle(name)
            
        self.sy = MplCanvas(self.G_grph, width=20, height=4, dpi=100)
        toolbar = NavigationToolbar(self.sy, self.G_grph)
        layout = QVBoxLayout()          
        layout.addWidget(toolbar)
        layout.addWidget(self.sy)
        widget = QtWidgets.QWidget(self.G_grph)
        widget.setGeometry(1, 15, 435, 380)
        widget.setLayout(layout) 
            
        if not self.motor: 
            self.sy.axes.plot(x, color='red', linewidth=1.0)
            self.sy.axes.scatter(len(x)-1, x[-1],linewidth=0.1,color='red')
            self.sy.axes.text(len(x)-1, x[-1]+2, "{}".format(x[-1]))
            self.sy.axes.text(.985,1.15,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sy.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
            
            self.sy.axes.set_xlabel("time(s)")
            self.sy.axes.set_title(name, horizontalalignment='right', verticalalignment='top', transform=self.sy.axes.transAxes)
            self.sy.axes.set_ylabel("HH (Counts)")
                        
        else:
            self.sy.axes.plot(self.g5,x, color='blue', linewidth=1.0)
            self.sy.axes.scatter(self.g5[-1], x[-1],linewidth=0.1,color='blue')
            self.sy.axes.text(self.g5[-1], x[-1]+2, "{}".format(x[-1]))
            self.sy.axes.text(.985,1.15,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sy.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
            
            self.sy.axes.set_xlabel("angles(degrees)")
            self.sy.axes.set_title(name)
            self.sy.axes.set_ylabel("HH (Counts)")
                        
            self.sy.axes.set_xlim(self.fromVal,self.toVal)
        
        self.sy.axes.grid()
        # self.sy.fig.tight_layout()
        # self.sy.axes.adjustSize()
        
    # Graph with two plots: 
    def theplottedtwice(self,x,y,name,a,b,c,d):
        self.G_grph = QtWidgets.QGroupBox(self)
        self.G_grph.setGeometry(QtCore.QRect(a, b, c, d))
        self.G_grph.setObjectName(name)
        self.G_grph.setTitle(name)
          
        self.sc = MplCanvas(self.G_grph, width=10, height=5, dpi=100)
        toolbar = NavigationToolbar(self.sc, self.G_grph)
        layout = QVBoxLayout()          
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        widget = QtWidgets.QWidget(self.G_grph)
        widget.setGeometry(1, 15, 425, 380)
        widget.setLayout(layout) 
        
        if not self.motor:
            self.sc.axes.plot(y, color='r', linewidth=1.0)
            self.sc.axes.plot(x, color='b', linewidth=1.0)
           
            self.sc.axes.scatter(len(y)-1, y[-1],linewidth=0.1,color='r')
            self.sc.axes.text(len(y)-1, y[-1]+2, "{}".format(y[-1]))
            self.sc.axes.scatter(len(x)-1, x[-1],linewidth=0.1,color='b')
            self.sc.axes.text(len(x)-1, x[-1]+2, "{}".format(x[-1]))
         
            # self.sc.axes.set_xlim(0,max(len(y),len(x))+5)   # max btw lenght of x and y will decide the x limit
            # self.sc.axes.set_ylim(0,max(y[-1],x[-1])+5)     # max btw the final value of x and y will decide the y limit
                       
            self.sc.axes.text(.985,1.15,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
            
            self.sc.axes.set_xlabel("time(s)")
            self.sc.axes.set_title(name)
            self.sc.axes.set_ylabel("(Counts)")
        else:
            self.sc.axes.plot(self.g5,y, color='r', linewidth=1.0)
            self.sc.axes.plot(self.g5,x, color='b', linewidth=1.0)
           
            self.sc.axes.scatter(self.g5[-1], y[-1],linewidth=0.1,color='r')
            self.sc.axes.text(self.g5[-1], y[-1]+2, "{}".format(y[-1]))
            self.sc.axes.scatter(self.g5[-1], x[-1],linewidth=0.1,color='b')
            self.sc.axes.text(self.g5[-1], x[-1]+2, "{}".format(x[-1]))
         
            # self.sc.axes.set_xlim(self.fromVal,self.toVal)
            # self.sc.axes.set_ylim(0,max(y[-1],x[-1])+5)     # max btw the final value of x and y will decide the y limit
                       
            self.sc.axes.text(.985,1.15,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
            
            self.sc.axes.set_xlabel("angles(degrees)")
            self.sc.axes.set_title(name)
            self.sc.axes.set_ylabel("(Counts)")
        
        self.sc.axes.grid()
            
            
        
#------------------------------------------------------------------------------------------
#                                GUI design class (MAIN THREAD) 
#------------------------------------------------------------------------------------------

class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.threadpool = QThreadPool()
      
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1900, 1000)
        
        # fonts:
        font = QtGui.QFont()
        font.setPointSize(11)
        
        font2 = QtGui.QFont()
        font2.setPointSize(20)
        
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.L_heading = QtWidgets.QLabel(self.centralwidget)
        self.L_heading.setText('  TEST CONSOLE - GUI')
        self.L_heading.setStyleSheet("color: blue;")
        self.L_heading.setFont(font2)
        self.G_meterValues = QtWidgets.QGroupBox(self.centralwidget)
        self.G_meterValues.setGeometry(QtCore.QRect(600, 60, 1250, 261))
        self.G_meterValues.setObjectName("G_meterValues")
        self.L_dspgrph = QtWidgets.QLabel(self.G_meterValues)
        self.L_dspgrph.setGeometry(QtCore.QRect(10, 40, 400, 31))
        self.L_dspgrph.setText('Display graph:')
        self.L_meter1v = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter1v.setGeometry(QtCore.QRect(150, 120, 131, 51))
        self.L_meter1v.setStyleSheet("background-color:white;color: red;")
        self.L_meter1v.setText("")
        self.L_meter1v.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter1v.setObjectName("L_meter1v")
        self.L_meter2v = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter2v.setGeometry(QtCore.QRect(420, 120, 131, 51))
        self.L_meter2v.setStyleSheet("background-color:white;color: blue;")
        self.L_meter2v.setText("")
        self.L_meter2v.setObjectName("L_meter2v")
        self.L_meter2v.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter3v = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter3v.setGeometry(QtCore.QRect(660, 120, 131, 51))
        self.L_meter3v.setStyleSheet("background-color:white;color: red;")
        self.L_meter3v.setText("")
        self.L_meter3v.setObjectName("L_meter3v")
        self.L_meter3v.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter4v = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter4v.setGeometry(QtCore.QRect(890, 120, 131, 51))
        self.L_meter4v.setStyleSheet("background-color:white;color: blue;")
        self.L_meter4v.setText("")
        self.L_meter4v.setObjectName("L_meter4v")
        self.L_meter4v.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter1head = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter1head.setGeometry(QtCore.QRect(150, 80, 131, 41))
        self.L_meter1head.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter1head.setObjectName("L_meter1head")
        self.L_meter2head = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter2head.setGeometry(QtCore.QRect(420, 80, 131, 41))
        self.L_meter2head.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter2head.setObjectName("L_meter2head")
        self.L_meter3head = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter3head.setGeometry(QtCore.QRect(660, 80, 131, 41))
        self.L_meter3head.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter3head.setObjectName("L_meter3head")
        self.L_meter4head = QtWidgets.QLabel(self.G_meterValues)
        self.L_meter4head.setGeometry(QtCore.QRect(890, 80, 131, 41))
        self.L_meter4head.setAlignment(QtCore.Qt.AlignCenter)
        self.L_meter4head.setObjectName("L_meter4head")
        self.B_begin = QtWidgets.QPushButton(self.G_meterValues)
        self.B_begin.setGeometry(QtCore.QRect(30, 190, 131, 41))
        self.B_begin.setObjectName("B_begin")
        self.G_connectionstat = QtWidgets.QGroupBox(self.centralwidget)
        self.G_connectionstat.setGeometry(QtCore.QRect(30, 60, 550, 261))
        self.G_connectionstat.setObjectName("G_connectionstat")
        self.L_comport = QtWidgets.QLabel(self.G_connectionstat)
        self.L_comport.setGeometry(QtCore.QRect(30, 70, 111, 31))
        self.L_comport.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.L_comport.setObjectName("L_comport")
        self.B_connect = QtWidgets.QPushButton(self.G_connectionstat)
        self.B_connect.setGeometry(QtCore.QRect(20, 190, 131, 41))
        self.B_connect.setObjectName("B_connect")
        self.label = QtWidgets.QLabel(self.G_connectionstat)
        self.label.setGeometry(QtCore.QRect(40, 140, 111, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.G_connectionstat)
        self.label_2.setGeometry(QtCore.QRect(140, 135, 171, 31))
        self.label_2.setStyleSheet("background-color:white;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.G_connectionstat)
        self.pushButton.setGeometry(QtCore.QRect(160, 190, 131, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 34))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.L_beginlabel = QtWidgets.QLabel(self.G_meterValues)
        self.L_beginlabel.setText('')
        self.L_beginlabel.setGeometry(170, 195, 131, 41)
        self.B_refreshcom = QtWidgets.QPushButton(self.G_connectionstat)
        self.B_refreshcom.setGeometry(390, 190, 131, 41)
        self.B_refreshcom.setText('Refresh COMs')
        self.B_refreshcom.clicked.connect(self.refresh_coms)
                
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        
        self.B_save = QtWidgets.QPushButton(self.G_meterValues)
        self.B_save.setGeometry(200, 190, 125, 40)
        self.B_save.setText('End')
        self.B_save.clicked.connect(self.ardend)
        
        self.E_totaltime = QtWidgets.QLineEdit(self.centralwidget)
        self.E_totaltime.setGeometry(1050,260,110,30)
        self.E_totaltime.setText('60')
        
        self.C_totaltime = QtWidgets.QCheckBox(self.centralwidget)
        self.C_totaltime.setText('Run time (s): ')
        self.C_totaltime.setGeometry(940, 255, 131, 41)
        # self.C_totaltime.stateChanged.connect(self.sendcounter)
        
        # Button connection for arduino -----------------------------------
            
        self.B_connect.clicked.connect(self.arduinoConnect)
        self.pushButton.clicked.connect(self.ardclose)
        self.B_begin.clicked.connect(self.senderfunc)
        
        # check bits --------------------------------------------------
        
        self.file= 0
        self.checkcom = 0
        self.checkmtr = 0
        self.checkbegin = 0
        self.checkrespos = bool()
        self.checkpause = False
        self.checknull = bool()
        self.csteps = []
        self.cx,self.cy,self.cz,self.cw = [],[],[],[]
        self.cfa1,self.cfa2 = [],[]
        
        self.timernow = []
        self.atimernow = []
        
        self.gridder = 0
        self.checkstat = bool()
        self.checkrunning = False
        
        self.calthemean = False
        
        self.customtimdelay = 1
        self.currentgraph = ''
#------------------------------------------------------------------------------
#                               MOTOR FRONT END SECTION
#------------------------------------------------------------------------------

        self.G_motorintf = QtWidgets.QGroupBox(self.centralwidget)
        self.G_motorintf.setGeometry(QtCore.QRect(1375, 325 ,475, 620))
        self.G_motorintf.setObjectName("G_motorintf")
        self.G_motorintf.setTitle('Motor Interface')
                
        self.G_angles = QtWidgets.QGroupBox(self.G_motorintf)
        self.G_angles.setGeometry(QtCore.QRect(10, 120 ,450, 220))
        self.G_angles.setObjectName("G_angles")
               
        self.G_jogging = QtWidgets.QGroupBox(self.G_motorintf)
        self.G_jogging.setGeometry(QtCore.QRect(12, 425 ,450, 100))
        self.G_jogging.setObjectName("G_jogging")
                             
        self.B_mtstart = QtWidgets.QPushButton(self.G_angles)
        self.B_mtstart.setGeometry(20, 100, 140, 40)
        self.B_mtstart.setText('Start')
        self.B_mtstart.clicked.connect(self.sendmovemotor)
        
        self.B_mtrsp = QtWidgets.QPushButton(self.G_angles)
        self.B_mtrsp.setGeometry(285, 100, 140, 40)
        self.B_mtrsp.setText('Pause')
        self.B_mtrsp.clicked.connect(self.sendresumepause)
                
        self.B_mthome = QtWidgets.QPushButton(self.G_angles)
        self.B_mthome.setGeometry(285, 160, 140, 40)
        self.B_mthome.setText('Home')
        self.B_mthome.clicked.connect(self.sendgoHome)
        
        self.B_mtsp = QtWidgets.QPushButton(self.G_angles)
        self.B_mtsp.setGeometry(20, 160, 140, 40)
        self.B_mtsp.setText('Stop')
        self.B_mtsp.clicked.connect(self.motorstop)
        
        self.B_mtabort = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtabort.setGeometry(275, 550, 150, 45)
        self.B_mtabort.setText('Abort')
        self.B_mtabort.clicked.connect(self.endmotorcom)
                
        self.B_mtconnect = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtconnect.setGeometry(50, 550, 150, 45)
        self.B_mtconnect.setText('Connect')
        self.B_mtconnect.clicked.connect(self.motorconnect)
        
        self.L_mtfrom = QtWidgets.QLabel(self.G_angles)
        self.L_mtfrom.setGeometry(20,10,100,50)
        self.L_mtfrom.setText('From:')
        
        self.L_mtthrough = QtWidgets.QLabel(self.G_angles)
        self.L_mtthrough.setGeometry(175,10,100,50)
        self.L_mtthrough.setText('through:')
        
        self.L_mtto = QtWidgets.QLabel(self.G_angles)
        self.L_mtto.setGeometry(330,10,100,50)
        self.L_mtto.setText('to:')
        
        self.L_mtcurrentangle = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtcurrentangle.setGeometry(10,30,200,50)
        self.L_mtcurrentangle.setText('Current angle:')
        
        self.E_mtfrom = QtWidgets.QLineEdit(self.G_angles)
        self.E_mtfrom.setGeometry(20,50,110,30)
        self.E_mtfrom.setText('-90')
        
        self.E_mtthrough = QtWidgets.QLineEdit(self.G_angles)
        self.E_mtthrough.setGeometry(175,50,110,30)
        self.E_mtthrough.setText('5')
        
        self.E_mtto = QtWidgets.QLineEdit(self.G_angles)
        self.E_mtto.setGeometry(330,50,110,30)
        self.E_mtto.setText('90')
        
        self.L_mtstatus = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtstatus.setGeometry(10,60,300,50)
        self.L_mtstatus.setText('status')
              
        self.B_jogup = QtWidgets.QPushButton(self.G_jogging)
        self.B_jogup.setGeometry(10, 40, 121, 40)
        self.B_jogup.setText('Jog Up')
        self.B_jogup.clicked.connect(lambda: self.jogger(float(self.E_mtjogsize.text()))) 
        
        self.L_mtjog = QtWidgets.QLabel(self.G_jogging)
        self.L_mtjog.setGeometry(190,5,100,30)
        self.L_mtjog.setText('jog size')
        
        self.E_mtjogsize = QtWidgets.QLineEdit(self.G_jogging)
        self.E_mtjogsize.setGeometry(160,40,125,40)
        self.E_mtjogsize.setText('5')
        
        self.B_jogdown = QtWidgets.QPushButton(self.G_jogging)
        self.B_jogdown.setGeometry(310, 40, 121, 40)
        self.B_jogdown.setText('Jog Down')
        self.B_jogdown.clicked.connect(lambda: self.jogger(-1*float(self.E_mtjogsize.text()))) 
        
        self.C_nullcheck = QtWidgets.QCheckBox(self.G_motorintf)
        self.C_nullcheck.setGeometry(30, 360, 100, 31)
        self.C_nullcheck.setText('Null Point')
        self.C_nullcheck.stateChanged.connect(self.nullpoint)
        
        self.E_mtrNullpoint = QtWidgets.QLineEdit(self.G_motorintf)
        self.E_mtrNullpoint.setGeometry(180, 360, 100, 35)
        self.E_mtrNullpoint.setText('0')
        
        self.B_mtgonull = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtgonull.setGeometry(310, 360, 125, 35)
        self.B_mtgonull.setText('Null')
        self.B_mtgonull.clicked.connect(self.makenull)
        
        self.B_getgwindow = QtWidgets.QPushButton(self.centralwidget)
        self.B_getgwindow.setGeometry(1200, 250, 150, 41)
        self.B_getgwindow.setText('graphs')
        self.B_getgwindow.clicked.connect(self.callgraphs)
                
#------------------------------------------------------------------------------------------
#                                   GRAPH SECTION 
#------------------------------------------------------------------------------------------

        # Graph One -------------------------------------------------------------
        
        self.G_graph = QtWidgets.QGroupBox(self.centralwidget)
        self.G_graph.setGeometry(QtCore.QRect(30, 325, 650, 515))
        self.G_graph.setObjectName("G_graph")
        self.G_graph.setTitle("meter 1")
                        
        self.sc = MplCanvas(self.G_graph, width=5, height=5, dpi=100)
        toolbar = NavigationToolbar(self.sc, self.G_graph)
        layout = QtWidgets.QVBoxLayout()          
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        self.widget = QtWidgets.QWidget(self.G_graph)
        self.widget.setGeometry(1, 15, 645, 450)
        self.widget.setLayout(layout)
        
                                     
        # self.sc2.axes.set_xlim(self.fromval, self.toval)
        
        # Graph Two -------------------------------------------------------------
        
        self.G_graph2 = QtWidgets.QGroupBox(self.centralwidget)
        self.G_graph2.setGeometry(QtCore.QRect(700, 325, 650, 515))
        self.G_graph2.setObjectName("G_graph2")
        self.G_graph2.setTitle("meter2")
    
        self.sc2 = MplCanvas(self.G_graph2, width=10, height=4, dpi=100)  
        toolbar2 = NavigationToolbar(self.sc2, self.G_graph2)
        layout2 = QtWidgets.QVBoxLayout() 
        layout2.addWidget(toolbar2)
        layout2.addWidget(self.sc2)
        widget = QtWidgets.QWidget(self.G_graph2)
        widget.setGeometry(1, 15, 645, 450)
        widget.setLayout(layout2)   
        
        self.L_latestread = QtWidgets.QLabel(self.G_graph)
        self.L_latestread.setGeometry(20,60,250,50)
        self.L_latestread.setText('current value')
        
        self.L_latestread2 = QtWidgets.QLabel(self.G_graph2)
        self.L_latestread2.setGeometry(20,60,250,50)
        self.L_latestread2.setText('current value')
        #-------------------------------------------
        self.C_cal = QtWidgets.QCheckBox(self.G_graph)
        self.C_cal.setGeometry(475, 470, 150, 31)
        self.C_cal.setText('find mean and SD')
        self.C_cal.stateChanged.connect(self.calmean)
        
        self.E_strsigma1=QtWidgets.QLineEdit(self.G_graph)
        self.E_strsigma1.setGeometry(20,470,50,30)
        self.E_strsigma1.setText('0')
        
        self.E_stpsigma1=QtWidgets.QLineEdit(self.G_graph)
        self.E_stpsigma1.setGeometry(80,470,50,30)
        self.E_stpsigma1.setText('0')
        
        self.L_mean = QtWidgets.QLabel(self.G_graph)
        self.L_mean.setGeometry(150,460,50,50)
        self.L_mean.setText('mean:    ')
        
        self.L_std = QtWidgets.QLabel(self.G_graph)
        self.L_std.setGeometry(310,460,50,50)
        self.L_std.setText('Sigma:    ')
        
        self.E_strsigma2=QtWidgets.QLineEdit(self.G_graph2)
        self.E_strsigma2.setGeometry(20,470,50,30)
        self.E_strsigma2.setText('0')
        
        self.E_stpsigma2=QtWidgets.QLineEdit(self.G_graph2)
        self.E_stpsigma2.setGeometry(80,470,50,30)
        self.E_stpsigma2.setText('0')
        
        self.L_mean2 = QtWidgets.QLabel(self.G_graph2)
        self.L_mean2.setGeometry(150,460,50,50)
        self.L_mean2.setText('mean:    ')
        
        self.L_std2 = QtWidgets.QLabel(self.G_graph2)
        self.L_std2.setGeometry(310,460,50,50)
        self.L_std2.setText('Sigma:    ')
        
#------------------------------------------------------------------------------------------
#                                        COMBO BOXES
#------------------------------------------------------------------------------------------

        # CONNECTION TO COM PORTS:
        
        self.the_ports = ps.comports()
        self.newcombo = QtWidgets.QComboBox(self.G_connectionstat)
        self.newcombo.setGeometry(QtCore.QRect(140, 70, 400, 31))
        self.newcombo.setObjectName('newcombo')
        self.newcombo.addItem('select the com')
        # button for com ports
        for i in self.the_ports:
            self.newcombo.addItem(str(i))
            
            
        # CHANGING THE GRAPH:
        self.combo1 = QtWidgets.QComboBox(self.G_meterValues)
        self.combo1.setGeometry(QtCore.QRect(147, 40, 400, 31))
        self.combo1.setObjectName('newcombo')  
        self.combo1.addItem('Fore readings')
        self.combo1.addItem('Aft readings')
        self.combo1.addItem('All four readings')
        self.combo1.addItem('Fore + Aft readings')
        
        # drop down menu for selecting the mode:
        self.comboMod = QtWidgets.QComboBox(self.G_meterValues)
        self.comboMod.setGeometry(QtCore.QRect(950, 200, 200, 31))
        self.comboMod.setObjectName('modes')  
        self.comboMod.addItem('Stationary')
        self.comboMod.addItem('FOV')
        # label to the right of combobox
        self.L_mode = QtWidgets.QLabel(self.G_meterValues)
        self.L_mode.setGeometry(800,205,10,31)
        self.L_mode.setText('Current Mode:')
        self.L_mode.adjustSize()
        
        
#------------------------------------------------------------------------------------------
       #                           SAVING THE FILES
#------------------------------------------------------------------------------------------
        self.G_savtxt = QtWidgets.QGroupBox(self.centralwidget)
        self.G_savtxt.setGeometry(QtCore.QRect(30, 850, 1320, 135))
        self.G_savtxt.setObjectName("G_savtxt")
        self.G_savtxt.setTitle("Save file") 
        self.E_filename = QtWidgets.QLineEdit(self.G_savtxt)
        self.E_filename.setGeometry(50, 50, 250, 40)
        
        self.B_createfile = QtWidgets.QPushButton(self.G_savtxt)
        self.B_createfile.setGeometry(350, 50, 125, 40)
        self.B_createfile.setText('Create file')
        self.B_createfile.clicked.connect(self.saveprev)
        # self.B_save.clicked.connect(self.savethefile)
        self.L_filedisp = QtWidgets.QLabel(self.G_savtxt)
        self.L_filedisp.setGeometry(500, 50, 350, 40)
        self.L_filedisp.setText('Type file name')
        self.L_filedisp.setFont(font2)
        
        self.E_mttimdelentr = QtWidgets.QLineEdit(self.centralwidget)      
        self.E_mttimdelentr.setGeometry(1150,880,90,30)
        self.E_mttimdelentr.setText('1')
        
        self.C_timdelcheck = QtWidgets.QCheckBox(self.centralwidget)
        self.C_timdelcheck.setGeometry(1150, 840, 150, 31)
        self.C_timdelcheck.setText('Time Delay (s)')
        self.C_timdelcheck.stateChanged.connect(self.custimdel)
        
    def saveprev(self):
        
        self.filename = self.E_filename.text()
        self.fl = open(self.filename+'.txt', 'a')
        if self.comboMod.currentText() == 'FOV':
            self.fl.write('Fore HH \tFore HU \tAft HU \t\tAft HH\t\tangle\t\ttime\t\t\tFOV test\n\n')
            self.L_filedisp.setText('File:'+self.E_filename.text()+' (FOV)')
            for i in range(len(self.cx)):                
                self.fl.write(str(self.cx[i])+'\t\t'+str(self.cy[i])+'\t\t'+str(self.cz[i])+'\t\t'+str(self.cw[i])+'\t\t'+str(self.csteps[i])+'\t\t'+self.timernow[i]+'\n')
                # self.f.write(str(self.var[0])[:-2]+'\t\t'+str(self.var[1])[:-2]+'\t\t'+str(self.var[2])[:-2]+'\t\t'+str(self.var[3])[:-2]+'\t\t'+str(steps[-1])+'\t\t'+time.ctime())
        else:
            self.fl.write('Fore HH \tFore HU \tAft HU \t\tAft HH\t\ttime\t\t\t\tStationary test\n\n')
            self.L_filedisp.setText('File:'+self.E_filename.text()+'(stat)')
            for i in range(len(self.cx)):                
                self.fl.write(str(self.cx[i])+'\t\t'+str(self.cy[i])+'\t\t'+str(self.cz[i])+'\t\t'+str(self.cw[i])+'\t\t'+self.atimernow[i]+'\n')
        self.fl.write('\n')
        self.fl.close()
        
    
   
        
#-----------------------------------------------------------------------------------------
    # Refreshing comports ------------------------------------------------------------------------

    def refresh_coms(self):
        self.the_ports = ps.comports()
        self.newcombo.clear()
        self.newcombo.addItem('select the com')
        for i in self.the_ports:
            self.newcombo.addItem(str(i))
        
    # arduino connect and disconnect -------------------------------------------------------------
    
    def arduinoConnect(self):
        if self.checkcom == 0:
            try:
                stat = str(self.newcombo.currentText())[:5] # the port number to connect, after cutting out the rest
                self.ard = serial.Serial(stat,9600)
                self.label_2.setText('connection formed')
                self.checkrunning = False
                self.sendinfinitechecker()
                self.checkcom = 1
            except:
                self.label_2.setText('not proper')
                self.checkcom = 0
            
    def ardclose(self):
        if self.checkcom == 1:
            self.checkcom = 0
            self.checkbegin = 0
            self.checkrunning = True
            self.ard.close()
            self.label_2.setText('port closed')
            
        else:
            self.checkcom = 0
            self.label_2.setText('port never formed')
    
    def ardend(self):
        self.checkstat = False
        # self.checkrunning = False
        # self.sendinfinitechecker()
        self.checkbegin = 0
        
    def timecounter(self):
        if self.C_totaltime.checkState():
            self.totaltime = int(self.E_totaltime.text())
        
    def infinitechecker(self):
        self.sc.draw()
        while True:
            if self.checkrunning == False:
                
                if self.comboMod.currentText() == 'FOV':
                    
                    self.sc.axes.set_xlim(int(self.E_mtfrom.text()), int(self.E_mtto.text()))
                    self.sc2.axes.set_xlim(int(self.E_mtfrom.text()), int(self.E_mtto.text()))
                    
                    self.sc.axes.set_title('FOV')
                    self.sc2.axes.set_title('FOV')
                    self.sc.axes.set_ylabel('Counts')
                    self.sc2.axes.set_ylabel('Counts')
                    self.sc.axes.set_xlabel('angles(degrees)')
                    self.sc2.axes.set_xlabel('angles(degrees)')
                    
                    # if self.gridder == 0:
                    #     self.sc.axes.grid()
                    #     self.sc2.axes.grid()
                    #     self.gridder = 1
                    self.sc.draw()
                    self.sc2.draw()
                    
                else:
                    
                    self.sc.axes.set_title('Stat')
                    self.sc2.axes.set_title('Stat')
                    self.sc.axes.set_ylabel('Counts')
                    self.sc2.axes.set_ylabel('Counts')
                    self.sc.axes.set_xlabel('time(s)')
                    self.sc2.axes.set_xlabel('time(s)')
                    self.sc.axes.set_xlim(0,int(self.E_totaltime.text()))
                    self.sc2.axes.set_xlim(0,int(self.E_totaltime.text()))
                    
                    # if self.gridder == 0:
                    #     self.sc.axes.grid()
                    #     self.sc2.axes.grid()
                    #     self.gridder = 1
                    
                    self.sc.draw()
                    self.sc2.draw()
                    
            else:
                break
            time.sleep(1)
        
        
    def sendinfinitechecker(self):
        
        worker6 = Worker(self.infinitechecker)
        self.threadpool.start(worker6)   
        
    def calmean(self):
         if self.C_cal.checkState():   
            self.calthemean = True
         else:
            self.calthemean = False
    
#-----------------------------------------------------------------------------------------
    # motor interface functions -------------------------------------------------------------
        
    # homing function -------------------------------------------------------------    
    def goHomePos(self):
        try:
            self.L_mtstatus.setText('going home')
            self.motor.go_home()
            self.L_mtstatus.setText('reached home')
            self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
            # self.L_mtcurrentangle.adjustSize()
        except:
            self.L_mtstatus.setText('stopped due error')
    
    # thread for goHomePos -------------------------------------------------------------
    def sendgoHome(self):
        worker2 = Worker(self.goHomePos)
        self.threadpool.start(worker2)        
    
    
    # to make the current angle as the null point --------------------------------------
    
    def makenull(self):
        if self.checkmtr :
            self.E_mtrNullpoint.setText(str(round(self.motor.getPos(),3)))
        else:
            self.L_mtstatus.setText('motor not connected..')
    
    
    # to set the null position -------------------------------------------------------------
    def gotonull(self):
        if self.checkmtr == 1:
            if self.checknull:
                self.L_mtstatus.setText('going to Null point..')
                self.motor.mAbs(int(self.E_mtrNullpoint.text()))
                self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
                self.L_mtstatus.setText('reached Null Point...')
            else:
                self.L_mtstatus.setText('Check the Null Box..')
        else:
            self.L_mtstatus.setText('motor not connected..')
    
    # thread for gotonull -------------------------------------------------------------
    def sendgotonull(self):
        worker5 = Worker(self.gotonull)
        self.threadpool.start(worker5)   
    
    # to disconnect the motor -------------------------------------------------------------        
    def endmotorcom(self):
        if self.checkmtr == 1:
            self.motor.cleanUpAPT()   
            self.L_mtstatus.setText('motor disconnected')
        else:
            self.L_mtstatus.setText('motor connection was not made')
            
    # to connect the motor -------------------------------------------------------------        
    def motorconnect(self):
        try:
            self.checkmtr = 1
            self.L_mtstatus.setText('initializing motor..')
            self.motor = APTMotor()
            self.motornum = self.motor.getSerialNumberByIdx(0)
            self.motornum = int(str(self.motornum)[7:-1])
            self.motor.setSerialNumber(self.motornum)
            self.motor.initializeHardwareDevice()
            self.L_mtstatus.setText('motor initialized !')
            self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
        except:
            self.checkmtr = 0
            self.L_mtstatus.setText('did not initialize..')
     
     # stops the motor ----------------------------------------------------------
     
    def motorstop(self):
        if self.checkmtr == 1:
            self.checkrespos = True  
            # self.sendinfinitechecker()
        else:
            self.L_mtstatus.setText('motor is not ready')
    
    # Null Point --------------------------------------------------------------------
    def nullpoint(self):
        self.takenull = round(float(self.E_mtrNullpoint.text()),3)
        if self.C_nullcheck.checkState():   
            self.checknull = True
        else:
            self.checknull = False
    
    # Gives custom time delay between each cycle ----------------------------------
    def custimdel(self):
        if self.C_timdelcheck.checkState():
            self.customtimdelay = float(self.E_mttimdelentr.text())
        else:
            self.customtimdelay = 1
        
                
#-------------------------------------------------------------------------------------   
    #                                   RESUME AND PAUSE
#-------------------------------------------------------------------------------------   

    
    def resumepause(self):
        self.checkrunning = True
        if self.checkmtr == 1:
            self.checkpause = not(self.checkpause)
            if self.checkpause:
                self.B_mtrsp.setText('resume')
                self.gridder = 0 # to put grid again 
                # self.currentgraph = ''
                self.motorstop()
            else:
                 self.currentpos = round(self.motor.getPos())
                 print(self.currentpos)
                 if self.currentpos > 180:
                     self.currentpos = self.currentpos-360
                 print(self.currentpos)
                
                 self.checkrespos = False
                
                 b = self.E_mtthrough.text()
                 c = self.E_mtto.text()
                 if  b == '' or c == '':
                     self.L_mtstatus.setText('please enter the values')
        
                 elif b == '0':
                     self.L_mtstatus.setText('step cannot be zero')
        
                 else: 
                    
                    self.B_mtrsp.setText('pause')
                    self.L_mtstatus.setText('moving...')
                    
                    if self.checknull:
                        c = int(c) + self.takenull
                        
                    # x,y,z,w,fa1,fa2=[],[],[],[],[],[]
                    x,y,z,w,fa1,fa2,steps=self.cx,self.cy,self.cz,self.cw,self.cfa1,self.cfa2,self.csteps
                    timenow = self.timernow
                    
                    self.L_beginlabel.setText('3..')
                    time.sleep(1)
                    self.L_beginlabel.setText('2..')
                    time.sleep(1)
                    self.L_beginlabel.setText('1..')
                    time.sleep(1)
                    self.L_beginlabel.setText('')
                    count=0
                    
                    # the range for the motor movement:
                    self.fromval = int(self.E_mtfrom.text())
                    self.toval = int(self.E_mtto.text())
                    
                    self.sc.axes.clear()
                    self.sc2.axes.clear()
                    
                    if self.gridder == 0:
                        self.sc.axes.grid()
                        self.sc2.axes.grid()
                        self.gridder = 1
                    
                    self.currentgraph = ''
                
                    for i in range(self.currentpos+int(b),int(c)+1,int(b)):  
                        self.L_mtcurrentangle.setText('Current angle: moving..')
                        self.motor.mAbs((int(i)))
                        
                        time.sleep(self.customtimdelay) 
                        
                        self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3))) 
                        
                        if self.comboMod.currentText() == 'FOV':
                            self.var = [0,0,0,0]
                            self.ard.write(b'1')
                            self.var[0] = self.ard.readline().decode('utf-8')
                            self.ard.write(b'2')
                            self.var[1] = self.ard.readline().decode('utf-8')
                            self.ard.write(b'3')
                            self.var[2] = self.ard.readline().decode('utf-8')
                            self.ard.write(b'4')
                            self.var[3] = self.ard.readline().decode('utf-8')
                            
                            #for values greater than 32000 (16 bit)  ---------------------
                            
                            if int(self.var[0])< 0 or int(self.var[0]) >32000:
                                self.var[0] = 0
                            if int(self.var[1])< 0 or int(self.var[1]) >32000:
                                self.var[1] = 0
                            if int(self.var[2])< 0 or int(self.var[2]) >32000:
                                self.var[2] = 0
                            if int(self.var[3])< 0 or int(self.var[3]) >32000:
                                self.var[3] = 0
                            
                            # meter display section ----------------------------------------------
                            self.L_meter1v.setText(str(self.var[0]))
                            self.L_meter2v.setText(str(self.var[1]))
                            self.L_meter3v.setText(str(self.var[2]))
                            self.L_meter4v.setText(str(self.var[3]))
                            
                            
                            # ploting graph section ----------------------------------------------
                            x.append(int(self.var[0]))
                            y.append(int(self.var[1]))
                            z.append(int(self.var[2]))
                            w.append(int(self.var[3]))
                            fa1.append(int(self.var[0]) + int(self.var[3]))
                            fa2.append(int(self.var[1]) + int(self.var[2]))
                            
                
                            
                            if self.checknull:
                                steps.append(round(i-self.takenull,3))
                            else:
                                steps.append(round(i,3))
                            print('current step val:',steps[-1])
                            
                            timenow.append(time.ctime())
                            
                            self.cx,self.cy,self.cz,self.cw,self.csteps= x.copy(),y.copy(),z.copy(),w.copy(),steps.copy()
                            self.timernow = timenow.copy()
                            
                            
                            # Fore reading -------------------------------------------------------
                            if self.combo1.currentText() == 'Fore readings':
                                                                
                                if self.currentgraph != 'Fore readings':
                                    self.sc.axes.clear()
                                    self.sc2.axes.clear()
                                    self.sc.axes.grid()
                                    self.sc2.axes.grid()
                                    self.sc.axes.plot(steps[:-1],x[:-1], color='violet', linewidth=1.0)
                                    self.sc2.axes.plot(steps[:-1],y[:-1], color='orange', linewidth=1.0)
                                    self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                    self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            
                                self.G_graph.setTitle('Fore readings')
                                self.G_graph2.setTitle('Fore readings')
                                # self.sc.axes.plot(x, color='violet', linewidth=1.0)
                                self.sc.axes.plot(steps[-2:], x[-2:],color='violet', linewidth=1.0)
                                self.sc2.axes.plot(steps[-2:],y[-2:], color='orange', linewidth=1.0)
                                
                                self.L_latestread.setText('current value: '+str(x[-1])+'Count')
                                self.L_latestread2.setText('current value: '+str(y[-1])+'Count')
                               
                                self.sc.axes.set_xlim(self.fromval, self.toval)
                                
                                self.sc2.axes.set_xlim(self.fromval, self.toval)
                                
                                
                                self.sc.axes.set_xlabel("angles(degree)")
                                self.sc.axes.set_title("Fore HH ")
                                self.sc.axes.set_ylabel("HH (Counts)")
                                
                        
                                self.sc2.axes.set_xlabel("angles(degree)")
                                self.sc2.axes.set_title("Fore HU")
                                self.sc2.axes.set_ylabel("HU (Counts)")
                                
                                self.currentgraph = 'Fore readings'
                                
                            # Aft reading -----------------------------------------------------    
                            elif self.combo1.currentText() == 'Aft readings':
                                
                                if self.currentgraph != 'Aft readings':
                                    self.sc.axes.clear()
                                    self.sc2.axes.clear()
                                    self.sc.axes.grid()
                                    self.sc2.axes.grid()
                                    self.sc.axes.plot(steps[:-1],w[:-1], color='g', linewidth=1.0)
                                    self.sc2.axes.plot(steps[:-1],z[:-1], color='blue', linewidth=1.0)
                                    self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                    self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            
                            # meters 3 and 4
                                self.G_graph.setTitle(' Aft readings')
                                self.G_graph2.setTitle('Aft readings')
                                self.sc2.axes.plot(steps[-2:],z[-2:],color='blue',linewidth=1.0)
                                self.sc.axes.plot(steps[-2:],w[-2:], color='g', linewidth=1.0)
                                
                                self.L_latestread.setText('current value: '+str(w[-1])+'Count')
                                self.L_latestread2.setText('current value: '+str(z[-1])+'Count')
                                
                                self.sc2.axes.set_xlim(self.fromval, self.toval)
                                
                                self.sc.axes.set_xlim(self.fromval, self.toval)
                                
                                self.sc2.axes.set_xlabel("angles(degree)")
                                self.sc2.axes.set_title("Aft HU")
                                self.sc2.axes.set_ylabel("HU (Counts)")
                                
                                self.sc.axes.set_xlabel("angles(degree)")
                                self.sc.axes.set_title("Aft HH")
                                self.sc.axes.set_ylabel("HH (Counts)")
                                
                                self.currentgraph = 'Aft readings'
                            # fore and aft separate in one plot --------------------------------------
                            elif self.combo1.currentText() == 'All four readings':
                                if self.currentgraph != 'All four readings':                        
                                       self.sc.axes.clear()
                                       self.sc2.axes.clear()
                                       self.sc.axes.grid()
                                       self.sc2.axes.grid()
                                       self.sc2.axes.plot(steps[:-1],z[:-1],linewidth=1.0, color='r')
                                       self.sc2.axes.plot(steps[:-1],y[:-1],linewidth=1.0, color='b')
                                       self.sc.axes.plot(steps[:-1],w[:-1], color='r', linewidth=1.0)
                                       self.sc.axes.plot(steps[:-1],x[:-1], color='b', linewidth=1.0)
                                       self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                       self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            
                                self.G_graph.setTitle('HU (Fore and Aft)')
                                self.G_graph2.setTitle('HH (Fore and Aft)')
                                self.sc2.axes.plot(steps[-2:],z[-2:],linewidth=1.0, color='r')
                                self.sc2.axes.plot(steps[-2:],y[-2:],linewidth=1.0, color='b')
                                self.sc.axes.plot(steps[-2:],w[-2:], color='r', linewidth=1.0)
                                self.sc.axes.plot(steps[-2:],x[-2:], color='b', linewidth=1.0)
                                
                                self.L_latestread.setText('current value: '+str(x[-1])+', '+str(w[-1])+'Count')
                                self.L_latestread2.setText('current value: '+str(y[-1])+', '+str(z[-1])+'Count')
                               
                                self.sc2.axes.set_xlim(self.fromval, self.toval)
                                self.sc.axes.set_xlim(self.fromval, self.toval)
                               
                                self.sc2.axes.set_xlabel("angles(degree)")
                                self.sc2.axes.set_title("HH Fore and Aft values")
                                self.sc2.axes.set_ylabel("HH (Counts)")
                                
                                self.sc.axes.set_xlabel("angles(degree)")
                                self.sc.axes.set_title("HU Fore and Aft values")
                                self.sc.axes.set_ylabel("HU (Counts)")
                            
                                self.currentgraph = 'All four readings'
                                
                            # fore and aft combined as one plot ----------------------------
                            elif self.combo1.currentText() == 'Fore + Aft readings':
                                if self.currentgraph != 'Fore + Aft readings':
                                   self.sc.axes.clear()
                                   self.sc2.axes.clear()
                                   self.sc.axes.grid()
                                   self.sc2.axes.grid()
                                   self.sc.axes.plot(steps[:-1],fa1[:-1], color='blue', linewidth=1.0)
                                   self.sc2.axes.plot(steps[:-1],fa2[:-1], color='g', linewidth=1.0)
                                   self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                   self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                                self.G_graph.setTitle('HH Fore + Aft')
                                self.G_graph2.setTitle('HU Fore + Aft')
                                self.sc.axes.plot(steps[-2:],fa1[-2:],color='blue',linewidth=1.0)
                                self.sc2.axes.plot(steps[-2:],fa2[-2:], color='g', linewidth=1.0)
                                
                                self.L_latestread.setText('current value: '+str(fa1[-1])+'Count')
                                self.L_latestread2.setText('current value: '+str(fa2[-1])+'Count')
                        
                                
                                self.sc.axes.set_xlim(self.fromval, self.toval)
                                self.sc2.axes.set_xlim(self.fromval, self.toval)
                                
                                self.sc.axes.set_xlabel("angles(degree)")
                                self.sc.axes.set_title("HH combined")
                                self.sc.axes.set_ylabel("HH (Counts)")
                                
                                self.sc2.axes.set_xlabel("angles(degree)")
                                self.sc2.axes.set_title("HU combined")
                                self.sc2.axes.set_ylabel("HU (Counts)")
                                
                                self.currentgraph = 'Fore + Aft readings'    
        
                                
                            count+=1   
                            
                            self.sc.draw()
                            self.sc2.draw()
                            
                        
                        #writing the file----------
                        # if self.file== 1 and self.checkmtr == 1 :  
                            # print('inside the text file ') 
                            # self.f.write(str(self.var[0])[:-2]+'\t\t'+str(self.var[1])[:-2]+'\t\t'+str(self.var[2])[:-2]+'\t\t'+str(self.var[3])[:-2]+'\t\t'+str(steps[-1])+'\t\t'+time.ctime())
                            
                            # self.f.write('\n') 
                          
                        # if stop is required, it will stop 
                        if self.checkrespos:
                            break
                                                
                        
                        
                        
                # to reach the final required angle
                 if self.L_mtcurrentangle != str(int(c)) and self.checkrespos == False:
                            print('in the extra step')
                            self.motor.mAbs(int(c))
                            self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
                            # write the readings in this final step
                            # if self.file== 1 and self.checkmtr == 1 :     
                            #     self.f.write(str(self.var[0])[:-2]+'\t\t'+str(self.var[1])[:-2]+'\t\t'+str(self.var[2])[:-2]+'\t\t'+str(self.var[3])[:-2]+'\t\t'+str(steps[-1])+'\t\t'+time.ctime())   
                            #     self.f.write('\n') 
                  # movement is done   
                 self.L_mtstatus.setText('moving done...') 
                 self.checkrunning = False
                 self.sendinfinitechecker()
                 if int(i) == int(c):
                      print('here')
                      if self.checknull: 
                          self.motor.mAbs(self.takenull)
                          self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
                      else:
                          self.motor.mRel(-int(c))
                          self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
                      self.L_mtstatus.setText('back to 0...')
                  
        else:
            # checkng condition
            self.L_mtstatus.setText('motor is not initialised')
            
    
    
#-----------------------------------------------------------------------------------------    
  #                                        MOTOR  MOVEMENT 
#-----------------------------------------------------------------------------------------
    def movemotor(self):
        self.checkrunning = True
        self.checkrespos = False
        a = self.E_mtfrom.text()
        b = self.E_mtthrough.text()
        c = self.E_mtto.text()
        if a == '' or b == '' or c == '':
            self.L_mtstatus.setText('please enter the values')
        
        elif b == '0':
            self.L_mtstatus.setText('step cannot be zero')
        
        else: 
            self.L_mtstatus.setText('moving...')
            if self.checknull:
                a = int(a) + self.takenull
                c = int(c) + self.takenull
            else:
                pass
            # print('going to for ') 
            
             # stores the values from begining:
            x,y,z,w,fa1,fa2=[],[],[],[],[],[]
            steps = []
            timenow = []
            self.L_beginlabel.setText('3..')
            time.sleep(1)
            self.L_beginlabel.setText('2..')
            time.sleep(1)
            self.L_beginlabel.setText('1..')
            time.sleep(1)
            self.L_beginlabel.setText('')
            
            self.sc.axes.clear()
            self.sc2.axes.clear()
            
            self.sc.axes.grid()
            self.sc2.axes.grid()
            
            self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
            self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                            
            
            count=0
            
            # the range for the motor movement:
            self.fromval = int(self.E_mtfrom.text())
            self.toval = int(self.E_mtto.text())
            self.stepval = int(self.E_mtthrough.text())
            
            for i in range(int(a),int(c)+1,int(b)): 
                    self.L_mtcurrentangle.setText('Current angle: moving..')
                    self.motor.mAbs(i)
                    
                    time.sleep(self.customtimdelay) 
                    
                    self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3))) 
                       
                    if self.comboMod.currentText() == 'FOV':
                        self.var = [0,0,0,0]
                        self.ard.write(b'1')
                        self.var[0] = self.ard.readline().decode('utf-8')
                        self.ard.write(b'2')
                        self.var[1] = self.ard.readline().decode('utf-8')
                        self.ard.write(b'3')
                        self.var[2] = self.ard.readline().decode('utf-8')
                        self.ard.write(b'4')
                        self.var[3] = self.ard.readline().decode('utf-8')
                        
                        #for values greater than 32000 (16 bit)  ---------------------
                        
                        if int(self.var[0])< 0 or int(self.var[0]) >32000:
                            self.var[0] = 0
                        if int(self.var[1])< 0 or int(self.var[1]) >32000:
                            self.var[1] = 0
                        if int(self.var[2])< 0 or int(self.var[2]) >32000:
                            self.var[2] = 0
                        if int(self.var[3])< 0 or int(self.var[3]) >32000:
                            self.var[3] = 0
                        
                        # meter display section ----------------------------------------------
                        self.L_meter1v.setText(str(self.var[0]))
                        self.L_meter2v.setText(str(self.var[1]))
                        self.L_meter3v.setText(str(self.var[2]))
                        self.L_meter4v.setText(str(self.var[3]))
                        
                        
                        # ploting graph section ----------------------------------------------
                        x.append(int(self.var[0]))
                        y.append(int(self.var[1]))
                        z.append(int(self.var[2]))
                        w.append(int(self.var[3]))
                        fa1.append(int(self.var[0]) + int(self.var[3]))
                        fa2.append(int(self.var[1]) + int(self.var[2]))
                        
                        
                        # making the current iternation value of i as the angle reading
                        if self.checknull:
                            steps.append(round(i-self.takenull,3))
                        else:
                            steps.append(round(i,3))
                        print('current step val:',steps[-1])
                        
                        timenow.append(time.ctime())
                        
                        self.cx,self.cy,self.cz,self.cw,self.csteps= x.copy(),y.copy(),z.copy(),w.copy(),steps.copy()
                        self.cfa1,self.cfa2 = fa1.copy(),fa2.copy()
                        self.timernow = timenow.copy()
                        # Fore reading -------------------------------------------------------
                        if self.combo1.currentText() == 'Fore readings':
                            if self.currentgraph != 'Fore readings':
                                self.sc.axes.clear()
                                self.sc2.axes.clear()
                                self.sc.axes.grid()
                                self.sc2.axes.grid()
                                self.sc.axes.plot(steps[:-1],x[:-1], color='violet', linewidth=1.0)
                                self.sc2.axes.plot(steps[:-1],y[:-1], color='orange', linewidth=1.0)
                                self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            
                            self.G_graph.setTitle('Fore readings')
                            self.G_graph2.setTitle('Fore readings')
                            # self.sc.axes.plot(x, color='violet', linewidth=1.0)
                            self.sc.axes.plot(steps[-2:], x[-2:],color='violet', linewidth=1.0)
                            self.sc2.axes.plot(steps[-2:],y[-2:], color='orange', linewidth=1.0)
                            
                            self.L_latestread.setText('current value: '+str(x[-1])+'Count')
                            self.L_latestread2.setText('current value: '+str(y[-1])+'Count')
                           
                            
                            self.sc.axes.set_xlim(self.fromval, self.toval)
                            
                            self.sc2.axes.set_xlim(self.fromval, self.toval)
                            
                            
                            self.sc.axes.set_xlabel("angles(degree)")
                            self.sc.axes.set_title("Fore HH ")
                            self.sc.axes.set_ylabel("HH (Counts)")
                            
                    
                            self.sc2.axes.set_xlabel("angles(degree)")
                            self.sc2.axes.set_title("Fore HU")
                            self.sc2.axes.set_ylabel("HU (Counts)")
                            
                            self.currentgraph = 'Fore readings'
                            
                        # Aft reading -----------------------------------------------------    
                        elif self.combo1.currentText() == 'Aft readings':
                            if self.currentgraph != 'Aft readings':
                                self.sc.axes.clear()
                                self.sc2.axes.clear()
                                self.sc.axes.grid()
                                self.sc2.axes.grid()
                                self.sc.axes.plot(steps[:-1],w[:-1], color='g', linewidth=1.0)
                                self.sc2.axes.plot(steps[:-1],z[:-1], color='blue', linewidth=1.0)
                                self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            
                            # meters 3 and 4
                            self.G_graph.setTitle(' Aft readings')
                            self.G_graph2.setTitle('Aft readings')
                            self.sc2.axes.plot(steps[-2:],z[-2:],color='blue',linewidth=1.0)
                            self.sc.axes.plot(steps[-2:],w[-2:], color='g', linewidth=1.0)
                            
                            self.L_latestread.setText('current value: '+str(w[-1])+'Count')
                            self.L_latestread2.setText('current value: '+str(z[-1])+'Count')
                           
                            self.sc2.axes.set_xlim(self.fromval, self.toval)
                            
                            self.sc.axes.set_xlim(self.fromval, self.toval)
                            
                            self.sc2.axes.set_xlabel("angles(degree)")
                            self.sc2.axes.set_title("Aft HU")
                            self.sc2.axes.set_ylabel("HU (Counts)")
                            
                            self.sc.axes.set_xlabel("angles(degree)")
                            self.sc.axes.set_title("Aft HH")
                            self.sc.axes.set_ylabel("HH (Counts)")
                            
                            self.currentgraph = 'Aft readings'
                        
                        # fore and aft separate in one plot --------------------------------------
                        elif self.combo1.currentText() == 'All four readings':
                            if self.currentgraph != 'All four readings':                        
                                   self.sc.axes.clear()
                                   self.sc2.axes.clear()
                                   self.sc.axes.grid()
                                   self.sc2.axes.grid()
                                   self.sc2.axes.plot(steps[:-1],z[:-1],linewidth=1.0, color='r')
                                   self.sc2.axes.plot(steps[:-1],y[:-1],linewidth=1.0, color='b')
                                   self.sc.axes.plot(steps[:-1],w[:-1], color='r', linewidth=1.0)
                                   self.sc.axes.plot(steps[:-1],x[:-1], color='b', linewidth=1.0)
                                   self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                                   self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            
                            self.G_graph.setTitle('HU (Fore and Aft)')
                            self.G_graph2.setTitle('HH (Fore and Aft)')
                            self.sc2.axes.plot(steps[-2:],z[-2:],linewidth=1.0, color='r')
                            self.sc2.axes.plot(steps[-2:],y[-2:],linewidth=1.0, color='b')
                            self.sc.axes.plot(steps[-2:],w[-2:], color='r', linewidth=1.0)
                            self.sc.axes.plot(steps[-2:],x[-2:], color='b', linewidth=1.0)
                            
                            self.L_latestread.setText('current value: '+str(x[-1])+', '+str(w[-1])+'Count')
                            self.L_latestread2.setText('current value: '+str(y[-1])+', '+str(z[-1])+'Count')
                            
                            
                            self.sc2.axes.set_xlim(self.fromval, self.toval)
                            self.sc.axes.set_xlim(self.fromval, self.toval)
                           
                            self.sc2.axes.set_xlabel("angles(degree)")
                            self.sc2.axes.set_title("HH Fore and Aft values")
                            self.sc2.axes.set_ylabel("HH (Counts)")
                            
                            self.sc.axes.set_xlabel("angles(degree)")
                            self.sc.axes.set_title("HU Fore and Aft values")
                            self.sc.axes.set_ylabel("HU (Counts)")
                        
                            self.currentgraph = 'All four readings'
                            
                        # fore and aft combined as one plot ----------------------------
                        elif self.combo1.currentText() == 'Fore + Aft readings':
                            if self.currentgraph != 'Fore + Aft readings':
                               self.sc.axes.clear()
                               self.sc2.axes.clear()
                               self.sc.axes.grid()
                               self.sc2.axes.grid()
                               self.sc.axes.plot(steps[:-1],fa1[:-1], color='blue', linewidth=1.0)
                               self.sc2.axes.plot(steps[:-1],fa2[:-1], color='g', linewidth=1.0)
                               self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                               self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                            self.G_graph.setTitle('HH Fore + Aft')
                            self.G_graph2.setTitle('HU Fore + Aft')
                            self.sc.axes.plot(steps[-2:],fa1[-2:],color='blue',linewidth=1.0)
                            self.sc2.axes.plot(steps[-2:],fa2[-2:], color='g', linewidth=1.0)
                            
                            self.L_latestread.setText('current value: '+str(fa1[-1])+'Count')
                            self.L_latestread2.setText('current value: '+str(fa2[-1])+'Count')
                            
                            
                            self.sc.axes.set_xlim(self.fromval, self.toval)
                            self.sc2.axes.set_xlim(self.fromval, self.toval)
                            
                            self.sc.axes.set_xlabel("angles(degree)")
                            self.sc.axes.set_title("HH combined")
                            self.sc.axes.set_ylabel("HH (Counts)")
                            
                            self.sc2.axes.set_xlabel("angles(degree)")
                            self.sc2.axes.set_title("HU combined")
                            self.sc2.axes.set_ylabel("HU (Counts)")
                            
                            self.currentgraph = 'Fore + Aft readings'
                            
                        count+=1   
                        
                        self.sc.draw()
                        self.sc2.draw()
                        
                   
                    # if stop is required, it will break
                    if self.checkrespos:
                        break
                    
                    
                    
                   
                   
            # to make sure the final required angle is reached        
            if self.L_mtcurrentangle != str(int(c)) and self.checkrespos == False:
                        self.motor.mAbs(int(c))
                        self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
                        
            # movement is finished                
            self.L_mtstatus.setText('moving done...') 
            self.checkrunning = False
            # print(i,c)
            if int(i) == (int(c)):
               print('here')
               if self.checknull: 
                   self.motor.mAbs(self.takenull)
                   self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
               else:
                   self.motor.mRel(-int(c))
                   self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
                   self.L_mtstatus.setText('back to 0...')
    
    # thread for resumepause --------------------------------------------------------------
    def sendresumepause(self):
         worker4 = Worker(self.resumepause)
         self.threadpool.start(worker4)
    
    # thread for movemotor ----------------------------------------------------------------
    def sendmovemotor(self):
        worker3 = Worker(self.movemotor)
        self.threadpool.start(worker3)
    
    # to stop the motor movement midway --------------------------------------------------- 
    def stopmotor(self):
        self.motor.stop_profiled()
     
        
    # motor jog function ------------------------------------------------------------------
    def jogger(self,val):
        if self.checkmtr:
            self.L_mtstatus.setText('moving..')
            self.motor.mRel(float(val))
            self.L_mtcurrentangle.setText('Current angle: '+str(round(self.motor.getPos(),3)))
            self.L_mtstatus.setText('moved !')
        else:
            self.L_mtstatus.setText('Motor not initialized !')

      
#-----------------------------------------------------------------------------------------
#                             ARDUINO  STATIONARY  SECTION 
#-----------------------------------------------------------------------------------------

    # to take the value from arduino and do the graph and save ---------------------------
    def bringVals(self):
         self.checkrunning = True
         self.checkbegin = 1
         self.checkstat = True
         
         
         x,y,z,w,fa1,fa2=[],[],[],[],[],[]
         steps = []
         
         self.currentgraph = 'Fore readings'
         
         self.L_beginlabel.setText('3..')
         time.sleep(1)
         self.L_beginlabel.setText('2..')
         time.sleep(1)
         self.L_beginlabel.setText('1..')
         time.sleep(1)
         self.L_beginlabel.setText('')
         
         atime = []
         
         count=0
         
         self.sc.axes.clear()
         self.sc2.axes.clear()
         
         self.sc.axes.grid()
         self.sc2.axes.grid()
         
         self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
         self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
         
        
         while True: 
            
            if self.C_totaltime.checkState() and count >= int(self.E_totaltime.text())+1:
                break
           
            if self.checkcom == 1 and self.comboMod.currentText() == 'Stationary' and self.checkstat:
                self.var = [0,0,0,0]
                self.ard.write(b'1')
                self.var[0] = self.ard.readline().decode('utf-8')
                self.ard.write(b'2')
                self.var[1] = self.ard.readline().decode('utf-8')
                self.ard.write(b'3')
                self.var[2] = self.ard.readline().decode('utf-8')
                self.ard.write(b'4')
                self.var[3] = self.ard.readline().decode('utf-8')
                
                #for values greater than 32000 (16 bit)  ---------------------
                
                if int(self.var[0])< 0 or int(self.var[0]) >32000:
                    self.var[0] = 0
                if int(self.var[1])< 0 or int(self.var[1]) >32000:
                    self.var[1] = 0
                if int(self.var[2])< 0 or int(self.var[2]) >32000:
                    self.var[2] = 0
                if int(self.var[3])< 0 or int(self.var[3]) >32000:
                    self.var[3] = 0
                
                # meter display section ----------------------------------------------
                self.L_meter1v.setText(str(self.var[0]))
                self.L_meter2v.setText(str(self.var[1]))
                self.L_meter3v.setText(str(self.var[2]))
                self.L_meter4v.setText(str(self.var[3]))
               
                # ploting graph section ----------------------------------------------
                x.append(int(self.var[0]))
                y.append(int(self.var[1]))
                z.append(int(self.var[2]))
                w.append(int(self.var[3]))
                fa1.append(int(self.var[0]) + int(self.var[3]))
                fa2.append(int(self.var[1]) + int(self.var[2]))
                steps.append(count)
                r,q,r1,q1 = 0,1,0,1
                
                if self.calthemean:
                    for k in range(len(steps)):
                        if int(self.E_strsigma1.text()) == steps[k]:
                            q = k
                        if int(self.E_stpsigma1.text()) == steps[k]:
                            r = k
                        if int(self.E_strsigma2.text()) == steps[k]:
                            q1 = k
                        if int(self.E_stpsigma2.text()) == steps[k]:
                            r1 = k
                   
                s,s1,s2,s3 = [],[],[],[]
                mean,mean1,mean2,mean3 = 0,0,0,0
                l,l1 = 0,0
                
                atime.append(time.ctime())
                
                self.cx,self.cy,self.cz,self.cw = x.copy(),y.copy(),z.copy(),w.copy()
                self.atimernow = atime.copy()
                # Fore reading -------------------------------------------------------
               
                
                if self.combo1.currentText() == 'Fore readings':
                    if self.calthemean:
                        for t in range(q,r+1):
                            # s += x[t]**2
                            s.append(x[t])
                            mean += x[t]
                            l += 1
                        for t in range(q1,r1+1):
                            # s1 += y[t]**2
                            s1.append(y[t])
                            mean1 += y[t]
                            l1 += 1
                       
                        # sd1 = sqrt(s1) 
                        sd = np.std(s)
                        # sd = sqrt(s)
                        sd1=np.std(s1) 
                        mean = mean/l
                        mean1 = mean1/l1
                        
                        self.L_mean2.setText('mean:'+str(round(mean1,2)))
                        self.L_mean2.adjustSize()
                        self.L_std2.setText('SD:'+str(round(sd1,3)))
                        self.L_std2.adjustSize()
                       
                        self.L_mean.setText('mean:'+str(round(mean,2)))
                        self.L_mean.adjustSize()
                        self.L_std.setText('SD:'+str(round(sd,3)))
                        self.L_std.adjustSize()
                    
                    
                    if self.currentgraph != 'Fore readings':
                         self.sc.axes.clear()
                         self.sc2.axes.clear()
                         self.sc.axes.grid()
                         self.sc2.axes.grid()
                         self.sc.axes.plot(steps[:-1],x[:-1], color='violet', linewidth=1.0)
                         self.sc2.axes.plot(steps[:-1],y[:-1], color='orange', linewidth=1.0)
                         self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                         self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                                       
                    self.G_graph.setTitle('Fore readings')
                    self.G_graph2.setTitle('Fore readings')
                    self.sc.axes.plot(steps[-2:],x[-2:], color='violet', linewidth=1.0)
                    self.sc2.axes.plot(steps[-2:],y[-2:], color='orange', linewidth=1.0)
                    
                    self.L_latestread.setText('current value: '+str(x[-1])+'Count')
                    self.L_latestread2.setText('current value: '+str(y[-1])+'Count')
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("Fore HH ")
                    self.sc.axes.set_ylabel("HH (Counts)")
                    
            
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("Fore HU")
                    self.sc2.axes.set_ylabel("HU (Counts)")
                    
                    self.currentgraph = 'Fore readings'
                
                # Aft reading -----------------------------------------------------    
                elif self.combo1.currentText() == 'Aft readings':
                    
                    if self.calthemean:
                        for t in range(q,r+1):
                            s.append(z[t])
                            mean += z[t]
                            l += 1
                        for t in range(q1,r1+1):
                            s1.append(w[t])
                            mean1 += w[t]
                            l1 += 1
                       
                        # sd1 = sqrt(s1) 
                        # sd = sqrt(s)
                        sd = np.std(s)
                        sd1 = np.std(s1)
                        
                        mean = mean/l
                        mean1 = mean1/l1
                        
                        self.L_mean2.setText('mean:'+str(round(mean1,2)))
                        self.L_mean2.adjustSize()
                        self.L_std2.setText('SD:'+str(round(sd1,3)))
                        self.L_std2.adjustSize()
                       
                        self.L_mean.setText('mean:'+str(round(mean,2)))
                        self.L_mean.adjustSize()
                        self.L_std.setText('SD:'+str(round(sd,3)))
                        self.L_std.adjustSize()
                    
                    if self.currentgraph != 'Aft readings':
                        self.sc.axes.clear()
                        self.sc2.axes.clear()
                        self.sc.axes.grid()
                        self.sc2.axes.grid()
                        self.sc2.axes.plot(steps[:-1],z[:-1], color='blue', linewidth=1.0)
                        self.sc.axes.plot(steps[:-1],w[:-1], color='g', linewidth=1.0)
                        self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                        self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                     # meters 3 and 4
                    self.G_graph.setTitle(' Aft readings')
                    self.G_graph2.setTitle('Aft readings')
                    self.sc2.axes.plot(steps[-2:],z[-2:],color='blue',linewidth=1.0)
                    self.sc.axes.plot(steps[-2:],w[-2:], color='g', linewidth=1.0)
                    
                    self.L_latestread.setText('current value: '+str(w[-1])+'Count')
                    self.L_latestread2.setText('current value: '+str(z[-1])+'Count')
                    
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("Aft HU")
                    self.sc2.axes.set_ylabel("HH (Counts)")
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("Aft HH")
                    self.sc.axes.set_ylabel("HU (Counts)")
                    
                    self.currentgraph = 'Aft readings'
                
                # fore and aft separate in one plot --------------------------------------
                elif self.combo1.currentText() == 'All four readings':
                    if self.calthemean:
                        for t in range(q,r+1):
                            s.append(z[t])
                            s2.append(y[t])
                            mean += z[t]
                            mean2 += y[t]
                            l += 1
                        for t in range(q1,r1+1):
                            s1.append(w[t])
                            s3.append(x[t])
                            mean1 += w[t]
                            mean3 += x[t]
                            l1 += 1
                       
                        # sd1 = sqrt(s1) 
                        # sd2 = sqrt(s2)
                        # sd3 = sqrt(s3)
                        # sd = sqrt(s)
                        sd1 = np.std(s1)
                        sd2 = np.std(s2)
                        sd3 = np.std(s3)
                        sd = np.std(s)
                        
                        mean = mean/l
                        mean2 = mean2/l
                        
                        mean1 = mean1/l1
                        mean3 = mean3/l1
                                                
                        self.L_mean2.setText('mean:'+str(round(mean1,2))+', '+str(round(mean3,2)))
                        self.L_mean2.adjustSize()
                        self.L_std2.setText('SD:'+str(round(sd1,3))+', '+str(round(sd3,3)))
                        self.L_std2.adjustSize()
                       
                        self.L_mean.setText('mean:'+str(round(mean,2))+', '+str(round(mean2,2)))
                        self.L_mean.adjustSize()
                        self.L_std.setText('SD:'+str(round(sd,3))+', '+str(round(sd2,3)))
                        self.L_std.adjustSize()
                    
                    if self.currentgraph != 'All four readings':                        
                       self.sc.axes.clear()
                       self.sc2.axes.clear()
                       self.sc.axes.grid()
                       self.sc2.axes.grid()
                       self.sc2.axes.plot(steps[:-1],z[:-1],linewidth=1.0, color='r')
                       self.sc2.axes.plot(steps[:-1],y[:-1],linewidth=1.0, color='b')
                       self.sc.axes.plot(steps[:-1],w[:-1], color='r', linewidth=1.0)
                       self.sc.axes.plot(steps[:-1],x[:-1], color='b', linewidth=1.0)
                       self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                       self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                    
                    self.G_graph.setTitle('HU (Fore and Aft)')
                    self.G_graph2.setTitle('HH (Fore and Aft)')
                   
                    self.sc2.axes.plot(steps[-2:],z[-2:],linewidth=1.0, color='r')
                    self.sc2.axes.plot(steps[-2:],y[-2:],linewidth=1.0, color='b')
                    self.sc.axes.plot(steps[-2:],w[-2:], color='r', linewidth=1.0)
                    self.sc.axes.plot(steps[-2:],x[-2:], color='b', linewidth=1.0)
                    
                    self.L_latestread.setText('current value: '+str(x[-1])+', '+str(w[-1])+'Count')
                    self.L_latestread2.setText('current value: '+str(y[-1])+', '+str(z[-1])+'Count')
                    
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("HH Fore and Aft values")
                    self.sc2.axes.set_ylabel("HH (Counts)")
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("HU Fore and Aft values")
                    self.sc.axes.set_ylabel("HU (Counts)")
                    
                    self.currentgraph = 'All four readings'
                
                # fore and aft combined as one plot ----------------------------
                elif self.combo1.currentText() == 'Fore + Aft readings':
                    
                    
                    if self.calthemean:
                        for t in range(q,r+1):
                            s.append(fa1[t])
                            mean += fa1[t]
                            l += 1
                        for t in range(q1,r1+1):
                            s1.append(fa2[t])
                            mean1 += fa2[t]
                            l1 += 1
                       
                        # sd1 = sqrt(s1) 
                        # sd = sqrt(s)
                        sd = np.std(s)
                        sd1 = np.std(s1) 
                        mean = mean/l
                        mean1 = mean1/l1
                        
                        self.L_mean2.setText('mean:'+str(mean1))
                        self.L_mean2.adjustSize()
                        self.L_std2.setText('SD:'+str(round(sd1,3)))
                        self.L_std2.adjustSize()
                       
                        self.L_mean.setText('mean:'+str(round(mean,2)))
                        self.L_mean.adjustSize()
                        self.L_std.setText('SD:'+str(round(sd,3)))
                        self.L_std.adjustSize()
                    
                    if self.currentgraph != 'Fore + Aft readings':                        
                        self.sc.axes.clear()
                        self.sc2.axes.clear()
                        self.sc.axes.grid()
                        self.sc2.axes.grid()
                        self.sc.axes.plot(steps[:-1],fa1[:-1], color='blue', linewidth=1.0)
                        self.sc2.axes.plot(steps[:-1],fa2[:-1], color='g', linewidth=1.0)
                        self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                        self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 Count',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))

                    
                    self.G_graph.setTitle('HH Fore + Aft')
                    self.G_graph2.setTitle('HU Fore + Aft')
                    self.sc.axes.plot(steps[-2:],fa1[-2:],color='blue',linewidth=1.0)
                    self.sc2.axes.plot(steps[-2:],fa2[-2:], color='g', linewidth=1.0)
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("HH combined")
                    self.sc.axes.set_ylabel("HH (Counts)")
                    
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("HU combined")
                    self.sc2.axes.set_ylabel("HU (Counts)")
                
                    self.currentgraph = 'Fore + Aft readings'
                
                count+=self.customtimdelay
                
                self.sc.draw()
                self.sc2.draw()
               
                if self.file== 1:     
                    self.f.write(str(self.var[0][:-2])+'\t\t'+str(self.var[1][:-2])+'\t\t'+str(self.var[2][:-2])+'\t\t'+str(self.var[3][:-2])+'\t\t'+time.ctime())    
                    self.f.write('\n') 
                
                time.sleep(self.customtimdelay) # delay for each call
            else:
                break
                # self.checkrunning = False
  
#-----------------------------------------------------------------------------------------      
#                                   NEW WINDOW FOR GRAPH FUNCTION
#-----------------------------------------------------------------------------------------      
    def callgraphs(self):
     
       if self.comboMod.currentText() == 'Stationary':
           self.gw = graphwindow(self.cx,self.cy,self.cz,self.cw ,self.csteps,int(self.E_mtfrom.text()),int(self.E_mtto.text()),False)
           self.gw.show()
       else:
           self.gw = graphwindow(self.cx,self.cy,self.cz,self.cw ,self.csteps,int(self.E_mtfrom.text()),int(self.E_mtto.text()),True)
           self.gw.show()
       
#-----------------------------------------------------------------------------------------

    # GATEWAY TO PARALLEL THREAD ( Worker class)
         
    def senderfunc(self):
         if self.checkbegin == 0:            
             worker = Worker(self.bringVals)
             self.threadpool.start(worker)
               
#-----------------------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PYTHON GUI FOR TEST CONSOLE OF HARTLEY HUGGINS SENSOR"))
        self.G_meterValues.setTitle(_translate("MainWindow", "Meter Values"))
        self.L_meter1head.setText(_translate("MainWindow", "Fore HH"))
        self.L_meter2head.setText(_translate("MainWindow", "Fore HU"))
        self.L_meter3head.setText(_translate("MainWindow", "Aft HU"))
        self.L_meter4head.setText(_translate("MainWindow", "Aft HH"))
        self.B_begin.setText(_translate("MainWindow", "Begin"))
        self.G_connectionstat.setTitle(_translate("MainWindow", "Connection status"))
        self.L_comport.setText(_translate("MainWindow", "COM port : "))
        self.B_connect.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "status      :"))
        self.pushButton.setText(_translate("MainWindow", "Close Port"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
#--------------------------------------------------------------------------------------------#   THE END   #--------------------------------------------------------------------------------------------#