# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:40:47 2021

@author: LEOS-7
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
from matplotlib import style

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import time
import serial
import serial.tools.list_ports as ps

from sampyapt import APTMotor

#######################################################################################################
#   for the apt motor interface to work, make sure to include the APT.dll, APT.lib and sampyapt.py in the same directory as of this file


#######################################################################################################




#------------------------------------------------------------------------------------------
# class definition for the graphs:

class MplCanvas(FigureCanvasQTAgg):
        
    def __init__(self, parent=None, width=10, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # self.axes.FigureCanvas
        super(MplCanvas, self).__init__(fig)
        
        
#------------------------------------------------------------------------------------------
# the parallel thread:
    
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
# GUI design class, the MAIN THREAD:
    
class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
      
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1900, 940)
        font = QtGui.QFont()
        font.setPointSize(12)
        font2 = QtGui.QFont()
        font2.setPointSize(24)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.L_heading = QtWidgets.QLabel(self.centralwidget)
        self.L_heading.setText('  TEST CONSOLE - GUI')
        self.L_heading.setStyleSheet("color: blue;")
        self.L_heading.setFont(font2)
        self.G_meterValues = QtWidgets.QGroupBox(self.centralwidget)
        self.G_meterValues.setGeometry(QtCore.QRect(600, 60, 1200, 261))
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
        
        self.checkcom = 0
        self.checkmtr = 0
        self.checkbegin = 0
        
        # motor ------------------------------------------------------
        
        self.G_motorintf = QtWidgets.QGroupBox(self.centralwidget)
        self.G_motorintf.setGeometry(QtCore.QRect(1400, 530 ,400, 350))
        self.G_motorintf.setObjectName("G_motorintf")
        self.G_motorintf.setTitle('motor interface')
    
        self.B_mtstart = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtstart.setGeometry(10, 50, 121, 31)
        self.B_mtstart.setText('start')
        self.B_mtstart.clicked.connect(self.sendmovemotor)
        
        self.B_mtstop = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtstop.setGeometry(250, 50, 121, 31)
        self.B_mtstop.setText('stop')
        self.B_mtstop.clicked.connect(self.stopmotor)
        
        self.B_mtabort = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtabort.setGeometry(10, 100, 121, 31)
        self.B_mtabort.setText('abort')
        self.B_mtabort.clicked.connect(self.endmotorcom)
        
        self.B_mthome = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mthome.setGeometry(250, 100, 121, 31)
        self.B_mthome.setText('home')
        self.B_mthome.clicked.connect(self.sendgoHome)
        
        self.B_mtconnect = QtWidgets.QPushButton(self.G_motorintf)
        self.B_mtconnect.setGeometry(250, 290, 121, 31)
        self.B_mtconnect.setText('connect')
        self.B_mtconnect.clicked.connect(self.motorconnect)
        
        
        self.L_mtfrom = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtfrom.setGeometry(20,195,100,50)
        self.L_mtfrom.setText('From:')
        
        self.L_mtthrough = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtthrough.setGeometry(150,195,100,50)
        self.L_mtthrough.setText('through:')
        
        self.L_mtto = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtto.setGeometry(285,195,100,50)
        self.L_mtto.setText('to:')
        
        self.L_mtcurrentangle = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtcurrentangle.setGeometry(20,150,100,50)
        self.L_mtcurrentangle.setText('Current angle:')
        
        self.E_mtfrom = QtWidgets.QLineEdit(self.G_motorintf)
        self.E_mtfrom.setGeometry(20,240,100,30)
        
        self.E_mtthrough = QtWidgets.QLineEdit(self.G_motorintf)
        self.E_mtthrough.setGeometry(150,240,100,30)
        
        self.E_mtto = QtWidgets.QLineEdit(self.G_motorintf)
        self.E_mtto.setGeometry(280,240,100,30)
        
        self.L_mtstatus = QtWidgets.QLabel(self.G_motorintf)
        self.L_mtstatus.setGeometry(20,280,200,50)
        
       
        
        
#------------------------------------------------------------------------------------------
        # Graph One
        
        self.G_graph = QtWidgets.QGroupBox(self.centralwidget)
        self.G_graph.setGeometry(QtCore.QRect(30, 325, 650, 555))
        self.G_graph.setObjectName("G_graph")
        self.G_graph.setTitle("meter 1")
                
        self.sc = MplCanvas(self.G_graph, width=5, height=5, dpi=100)
        toolbar = NavigationToolbar(self.sc, self.G_graph)
        layout = QtWidgets.QVBoxLayout()          
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        widget = QtWidgets.QWidget(self.G_graph)
        widget.setGeometry(1, 15, 625, 450)
        widget.setLayout(layout)
              
#------------------------------------------------------------------------------------------
        # Graph Two
        
        self.G_graph2 = QtWidgets.QGroupBox(self.centralwidget)
        self.G_graph2.setGeometry(QtCore.QRect(700, 325, 650, 555))
        self.G_graph2.setObjectName("G_graph2")
        self.G_graph2.setTitle("meter2")
    
        self.sc2 = MplCanvas(self.G_graph2, width=10, height=4, dpi=100)  
        # self.sc2.setGeometry(0, 0, 150, 320)
        toolbar2 = NavigationToolbar(self.sc2, self.G_graph2)
        layout2 = QtWidgets.QVBoxLayout() 
        layout2.addWidget(toolbar2)
        layout2.addWidget(self.sc2)
        widget = QtWidgets.QWidget(self.G_graph2)
        widget.setGeometry(1, 15, 625, 450)
        widget.setLayout(layout2)
#------------------------------------------------------------------------------------------
    
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
               
#------------------------------------------------------------------------------------------
        # connecting to the arduino:
            
        self.B_connect.clicked.connect(self.arduinoConnect)
        self.pushButton.clicked.connect(self.ardclose)
        
        self.B_begin.clicked.connect(self.senderfunc)
    
#------------------------------------------------------------------------------------------
        # for combo box:    
            
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
        
#------------------------------------------------------------------------------------------
       # saving the readings:
       
        self.G_savtxt = QtWidgets.QGroupBox(self.centralwidget)
        self.G_savtxt.setGeometry(QtCore.QRect(1400, 325, 400, 200))
        self.G_savtxt.setObjectName("G_savtxt")
        self.G_savtxt.setTitle("save file") 
        self.E_filename = QtWidgets.QLineEdit(self.G_savtxt)
        self.E_filename.setGeometry(10, 40, 250, 31)
        self.B_save = QtWidgets.QPushButton(self.G_savtxt)
        self.B_save.setGeometry(130, 100, 100, 30)
        self.B_save.setText('Save file')
        self.B_createfile = QtWidgets.QPushButton(self.G_savtxt)
        self.B_createfile.setGeometry(10, 100, 100, 30)
        self.B_createfile.setText('Create file')
        self.B_createfile.clicked.connect(self.createthefile)
        self.B_save.clicked.connect(self.savethefile)
        self.a = 0
        self.L_filedisp = QtWidgets.QLabel(self.G_savtxt)
        self.L_filedisp.setGeometry(10, 150, 200, 40)
        self.L_filedisp.setText('')
        self.L_filedisp.setFont(font2)
    
    def savethefile(self):
        if self.a == 1:
            self.f.close()
            self.L_filedisp.setText('file saved')
        else:
            self.L_filedisp.setText('No file created')
            self.L_filedisp.adjustSize()
        
    def createthefile(self):
        self.a = 1
        self.filename = self.E_filename.text()
        # self.f = open('C:/Users/LEOS-7/Desktop/'+self.filename+'.txt', 'a')
        self.f = open(self.filename+'.txt', 'a')
        self.f.write('Fore HH \tFore HU \tAft HU \t\tAft HH\n\n')
        self.L_filedisp.setText('file created')
        
#-----------------------------------------------------------------------------------------
    def refresh_coms(self):
        self.the_ports = ps.comports()
        self.newcombo.clear()
        self.newcombo.addItem('select the com')
        for i in self.the_ports:
            self.newcombo.addItem(str(i))
        
    
    def arduinoConnect(self):
        try:
            stat = str(self.newcombo.currentText())[:5]
            self.ard = serial.Serial(stat,9600)
            self.label_2.setText('connection formed')
            self.checkcom = 1
        except:
            self.label_2.setText('not proper')
            self.checkcom = 0
            
    def ardclose(self):
        if self.checkcom == 1:
            self.checkcom = 0
            self.checkbegin = 0
            self.ard.close()
            self.label_2.setText('port closed')
            
        else:
            self.checkcom = 0
            self.label_2.setText('port never formed')
            
        self.L_meter1v.setText("")
        self.L_meter2v.setText("")
        self.L_meter3v.setText("")
        self.L_meter4v.setText("")
        
        
#-----------------------------------------------------------------------------------------
        # MOTOR INTERFACING FUNCTIONS :
            
    def goHomePos(self):
        try:
            self.L_mtstatus.setText('going home')
            self.motor.go_home()
            self.L_mtstatus.setText('reached home')
            self.L_mtcurrentangle.setText('Current angle: '+str(self.motor.getPos()))
            self.L_mtcurrentangle.adjustSize()
        except:
            self.L_mtstatus.setText('stopped due error')
    
    def sendgoHome(self):
        worker2 = Worker(self.goHomePos)
        self.threadpool.start(worker2)        
    
    def endmotorcom(self):
        if self.checkmtr == 1:
            self.motor.cleanUpAPT()   
            self.L_mtstatus.setText('connection ended')
        else:
            self.L_mtstatus.setText('connection was not made')
            
            
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
            self.L_mtcurrentangle.setText('Current angle: '+str(self.motor.getPos()))
            self.L_mtcurrentangle.adjustSize()
        except:
            self.checkmtr = 0
            self.L_mtstatus.setText('did not initialize..')
     
   
    
    
    def movemotor(self):
        
        a = self.E_mtfrom.text()
        b = self.E_mtthrough.text()
        c = self.E_mtto.text()
        if a == '' or b == '' or c == '':
            self.L_mtstatus.setText('please enter the values')
        
        elif b == '0':
            self.L_mtstatus.setText('step cannot be zero')
        
        else: 
            self.L_mtstatus.setText('hold on..')
            self.motor.mAbs(float(a))
            self.L_mtcurrentangle.setText('Current angle: '+str(self.motor.getPos()))
            self.L_mtcurrentangle.adjustSize()
            time.sleep(0.1)
            self.L_mtstatus.setText('moving..')
            self.motor.mcAbs(float(c),float(b))
            self.L_mtcurrentangle.setText('Current angle: '+str(self.motor.getPos()))
            self.L_mtcurrentangle.adjustSize()
            self.L_mtstatus.setText('done..')
            
    
    def sendmovemotor(self):
        worker3 = Worker(self.movemotor)
        self.threadpool.start(worker3)
    
        
    def stopmotor(self):
        self.motor.stop_profiled()
        

      
#-----------------------------------------------------------------------------------------

#################################################
    def bringVals(self):
         self.checkbegin = 1
         x,y,z,w,fa1,fa2=[],[],[],[],[],[]
         self.L_beginlabel.setText('3..')
         time.sleep(1)
         self.L_beginlabel.setText('2..')
         time.sleep(1)
         self.L_beginlabel.setText('1..')
         time.sleep(1)
         self.L_beginlabel.setText('')
         count=0
         while True: 
            if self.checkcom == 1:
                self.var = [0,0,0,0]
                self.ard.write(b'1')
                self.var[0] = self.ard.readline().decode('utf-8')
                self.ard.write(b'2')
                self.var[1] = self.ard.readline().decode('utf-8')
                self.ard.write(b'3')
                self.var[2] = self.ard.readline().decode('utf-8')
                self.ard.write(b'4')
                self.var[3] = self.ard.readline().decode('utf-8')
                
                #for values greater than 32000
                
                if int(self.var[0])< 0 or int(self.var[0]) >32000:
                    self.var[0] = 0
                if int(self.var[1])< 0 or int(self.var[1]) >32000:
                    self.var[1] = 0
                if int(self.var[2])< 0 or int(self.var[2]) >32000:
                    self.var[2] = 0
                if int(self.var[3])< 0 or int(self.var[3]) >32000:
                    self.var[3] = 0
                    
                self.L_meter1v.setText(str(self.var[0]))
                self.L_meter2v.setText(str(self.var[1]))
                self.L_meter3v.setText(str(self.var[2]))
                self.L_meter4v.setText(str(self.var[3]))
                self.sc.axes.clear()
                self.sc2.axes.clear()
                
                x.append(int(self.var[0]))
                y.append(int(self.var[1]))
                z.append(int(self.var[2]))
                w.append(int(self.var[3]))
                fa1.append(int(self.var[0]) + int(self.var[3]))
                fa2.append(int(self.var[1]) + int(self.var[2]))
               
                if self.combo1.currentText() == 'Fore readings':
                    # meters 1 and 2
                    self.G_graph.setTitle('Fore readings')
                    self.G_graph2.setTitle('Fore readings')
                    self.sc.axes.plot(x, color='violet', linewidth=1.0)
                    self.sc2.axes.plot(y, color='orange', linewidth=1.0)
                    
                    self.sc.axes.scatter(len(x)-1, x[-1],linewidth=0.1,color='violet')
                    self.sc.axes.text(len(x)-1, x[-1]+2, "{}".format(x[-1]))
                    self.sc2.axes.scatter(len(y)-1, y[-1],linewidth=0.1,color='orange')
                    self.sc2.axes.text(len(y)-1, y[-1]+2, "{} ".format(y[-1]))
                    
                    self.sc.axes.set_xlim(0, count+(.5*count))
                    
                    self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V', horizontalalignment='right', verticalalignment='top', transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    
                    self.sc2.axes.set_xlim(0,count+(.5*count))
                    
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("Fore HH ")
                    self.sc.axes.set_ylabel("HH (V)")
                    
            
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("Fore HU")
                    self.sc2.axes.set_ylabel("HU (V)")
                    
                    
                elif self.combo1.currentText() == 'Aft readings':
                    # meters 3 and 4
                    self.G_graph.setTitle(' Aft readings')
                    self.G_graph2.setTitle('Aft readings')
                    self.sc2.axes.plot(z,color='blue',linewidth=1.0)
                    self.sc.axes.plot(w, color='g', linewidth=1.0)
                    
                    self.sc2.axes.scatter(len(z)-1, z[-1],linewidth=0.1,color='blue')
                    self.sc2.axes.text(len(z)-1, z[-1]+2, "{}".format(z[-1]))
                    self.sc.axes.scatter(len(w)-1, w[-1],linewidth=0.1,color='g')
                    self.sc.axes.text(len(w)-1, w[-1]+2, "{}".format(w[-1]))
                    
                    self.sc2.axes.set_xlim(0,count+(.5*count))
                    
                    self.sc.axes.set_xlim(0,count+(.5*count))
                    
                    
                    self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("Aft HU")
                    self.sc2.axes.set_ylabel("HH (V)")
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("Aft HH")
                    self.sc.axes.set_ylabel("HU (V)")
                    
                elif self.combo1.currentText() == 'All four readings':
                    # meters 3, 2 and 4,1   sc = hh and sc2 = hu
                    self.G_graph.setTitle('HU (Fore and Aft)')
                    self.G_graph2.setTitle('HH (Fore and Aft)')
                    self.sc2.axes.plot(z,linewidth=1.0, color='r')
                    self.sc2.axes.plot(y,linewidth=1.0, color='b')
                    self.sc.axes.plot(w, color='r', linewidth=1.0)
                    self.sc.axes.plot(x, color='b', linewidth=1.0)
                    
                    self.sc2.axes.scatter(len(z)-1, z[-1],linewidth=0.1,color='r')
                    
                    self.sc2.axes.text(len(z)-1, z[-1]+2, "{}".format(z[-1]))
                    self.sc2.axes.scatter(len(y)-1, y[-1],linewidth=0.1,color='b')
                    self.sc2.axes.text(len(y)-1, y[-1]+2, "{}".format(y[-1]))
                    
                    self.sc.axes.scatter(len(w)-1, w[-1],linewidth=0.1,color='r')
                    self.sc.axes.text(len(w)-1, w[-1]+2, "{}".format(w[-1]))
                    self.sc.axes.scatter(len(x)-1, x[-1],linewidth=0.1,color='b')
                    self.sc.axes.text(len(x)-1, x[-1]+2, "{}".format(x[-1]))
                    
                    self.sc2.axes.set_xlim(0,count+(.5*count))
                    self.sc.axes.set_xlim(0,count+(.5*count))
                   
                    
                    self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("HH Fore and Aft values")
                    self.sc2.axes.set_ylabel("HH (V)")
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("HU Fore and Aft values")
                    self.sc.axes.set_ylabel("HU (V)")
                    # self.sc.axes.tight_layout()
                 
                elif self.combo1.currentText() == 'Fore + Aft readings':
                    # meters added fa1 = 1 and 4, fa2 = 2 and 3
                    self.G_graph.setTitle('HH Fore + Aft')
                    self.G_graph2.setTitle('HU Fore + Aft')
                    self.sc.axes.plot(fa1,color='blue',linewidth=1.0)
                    self.sc2.axes.plot(fa2, color='g', linewidth=1.0)
                    
                    self.sc.axes.scatter(len(fa1)-1, fa1[-1],linewidth=0.1,color='blue')
                    self.sc.axes.text(len(fa1)-1, fa1[-1]+2, "{}".format(fa1[-1]))
                    self.sc2.axes.scatter(len(fa2)-1, fa2[-1],linewidth=0.1,color='g')
                    self.sc2.axes.text(len(fa2)-1, fa2[-1]+2, "{}".format(fa2[-1]))
                    
                    self.sc.axes.set_xlim(0,count+(.5*count))
                    # self.sc.axes.set_ylim(0, max((fa1))*2)
                    self.sc2.axes.set_xlim(0,count+(.5*count))
                    # self.sc2.axes.set_ylim(0, max((fa2))*2)
                    
                    self.sc.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    self.sc2.axes.text(.985,1.12,'x axis=1 sec\ny axis =1 V',horizontalalignment='right',verticalalignment='top',transform=self.sc.axes.transAxes,bbox= dict(facecolor='w',alpha=0.5))
                    
                    self.sc.axes.set_xlabel("time(s)")
                    self.sc.axes.set_title("HH combined")
                    self.sc.axes.set_ylabel("HH (V)")
                    
                    self.sc2.axes.set_xlabel("time(s)")
                    self.sc2.axes.set_title("HU combined")
                    self.sc2.axes.set_ylabel("HU (V)")
                
                count+=1   
                
                self.sc.axes.grid()
                self.sc2.axes.grid()
                
                self.sc.draw()
                self.sc2.draw()
                if self.a == 1:
                    # self.f.writelines('v1: '+str(self.var[0])+'\tv2: '+str(self.var[1])+'\tv3: '+str(self.var[2])+'\tv4: '+str(self.var[3]))
                    
                    self.f.write(str(self.var[0][:-2])+'\t\t'+str(self.var[1][:-2])+'\t\t'+str(self.var[2][:-2])+'\t\t'+str(self.var[3][:-2]))    
                    self.f.write('\n') 
                
                time.sleep(1)
            else:
                break
#################################################

#-----------------------------------------------------------------------------------------
    # GATEWAY TO PARALLEL THREAD ( Worker class)
         
    def senderfunc(self):
         if self.checkbegin == 0:
             
             worker = Worker(self.bringVals)
             self.threadpool.start(worker)
         else:
             pass
    
    
#-----------------------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Gui interface for hartley huggins sensor"))
        self.G_meterValues.setTitle(_translate("MainWindow", "Meter Values"))
        self.L_meter1head.setText(_translate("MainWindow", "Fore HH"))
        self.L_meter2head.setText(_translate("MainWindow", "Fore HU"))
        self.L_meter3head.setText(_translate("MainWindow", "Aft HU"))
        self.L_meter4head.setText(_translate("MainWindow", "Aft HH"))
        self.B_begin.setText(_translate("MainWindow", "Begin"))
        self.G_connectionstat.setTitle(_translate("MainWindow", "connection status"))
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
    