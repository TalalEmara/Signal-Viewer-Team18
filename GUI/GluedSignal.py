import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle, linkedButtonOffStyle, linkedButtonOnStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from matplotlib.animation import FuncAnimation


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, signal_color="#D55877"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#242424')  
        self.ax.set_facecolor('#242424')    

        self.line, = self.ax.plot([], [], color=signal_color, lw=2)  

        self.ax.tick_params(axis='x', colors='#EFEFEF')
        self.ax.tick_params(axis='y', colors='#EFEFEF')
        self.ax.xaxis.label.set_color('#EFEFEF')
        self.ax.yaxis.label.set_color('#EFEFEF')
        self.ax.spines['bottom'].set_color('#EFEFEF')
        self.ax.spines['left'].set_color('#EFEFEF')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.grid(True, color='#EFEFEF', linestyle='--', alpha=0.1)  

        super(MplCanvas, self).__init__(fig)

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(30)  
        self.navToolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.toolbarLayout = QVBoxLayout(self)
        self.toolbarLayout.addWidget(self.navToolbar)
        self.toolbarLayout.addWidget(self)

        self.toolbarLayout.setAlignment(self.navToolbar, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

    def update_plot(self, t, signal):
        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()

class Signals(object):
    def __init__(self):
        super().__init__()

    def signalViewerUi(self, Signals):
        Signals.setObjectName("Signals")
        Signals.resize(1000, 700)

        
        Signals.setWindowTitle("Glued Signal") 

        self.centralwidget = QtWidgets.QWidget(Signals)
        self.centralwidget.setObjectName("centralwidget")
        Signals.setCentralWidget(self.centralwidget)

        mainLayout = QVBoxLayout(self.centralwidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.GluedSignal = QFrame(self.centralwidget)
        self.GluedSignal.setStyleSheet("background-color: #2D2D2D;")  
        self.GluedSignal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        mainLayout.addWidget(self.GluedSignal)

        self.GluedSignalPlot = QFrame(self.GluedSignal)
        self.GluedSignalPlot.setStyleSheet("background-color: #2D2D2D;")
        self.GluedSignalPlotLayout = QVBoxLayout(self.GluedSignalPlot)
        self.GluedSignalPlotLayout.setContentsMargins(5, 5, 5, 5)
        self.GluedSignalPlotLayout.setObjectName("GluedSignalPlotLayout")

        self.canvas1 = MplCanvas(self.GluedSignal, width=5, height=4, dpi=100, signal_color="#D55877")

        self.titleToolbarLayout = QHBoxLayout()
        self.GluedsignalTitle = QLabel("Glued Signal", self.GluedSignal)
        self.GluedsignalTitle.setStyleSheet("color: #87EDF1; font-size:15px;")  
        self.titleToolbarLayout.addWidget(self.GluedsignalTitle)
        
        self.GluedsignalTitleEdit = QPushButton(self.GluedSignal)
        self.GluedsignalTitleEdit.setIcon(QtGui.QIcon("photos/edit.png"))
        self.GluedsignalTitleEdit.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.GluedsignalTitleEdit.setFixedSize(25, 25)
        self.titleToolbarLayout.addWidget(self.GluedsignalTitleEdit)

        self.titleToolbarLayout.addSpacing(680)  

        self.snapShotButton = QPushButton("SnapShot", self.GluedSignal)
        self.snapShotButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.snapShotButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 5px; background-color: #2D2D2D; color: #76D4D4; width:100px; font-size:17px;")
        self.titleToolbarLayout.addWidget(self.snapShotButton)

        self.exportPdfButton = QPushButton("Export to PDF", self.GluedSignal)
        self.exportPdfButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exportPdfButton.setStyleSheet("border: 2px solid #EFEFEF; border-radius: 5px; background-color: #2D2D2D; color: #EFEFEF; width:120px;font-size:17px;")
        self.titleToolbarLayout.addWidget(self.exportPdfButton)

        self.GluedSignalPlotLayout.addLayout(self.titleToolbarLayout, stretch=1)  
        self.GluedSignalPlotLayout.addWidget(self.canvas1, stretch=13)  

        self.GluedSignalbuttonsLayout = QHBoxLayout()
        self.GluedSignalbuttonsLayout.addSpacing(10)  

        self.timeLabel = QtWidgets.QLabel("00:00", self.GluedSignal)
        self.timeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel.setStyleSheet(labelStyle)
        self.GluedSignalbuttonsLayout.addWidget(self.timeLabel)

        self.GluedSignalbuttonsLayout.addSpacing(123)

        self.pauseButton = QtWidgets.QPushButton(self.GluedSignal)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.pauseButton)

        self.GluedSignalbuttonsLayout.addSpacing(5)

        self.playButton = QtWidgets.QPushButton(self.GluedSignal)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.playButton)

        self.GluedSignalbuttonsLayout.addSpacing(5)

        self.stopButton = QtWidgets.QPushButton(self.GluedSignal)
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.stopButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.stopButton)

        self.GluedSignalbuttonsLayout.addSpacing(5)

        self.toStartButton = QtWidgets.QPushButton(self.GluedSignal)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.toStartButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.toStartButton)

        self.GluedSignalbuttonsLayout.addSpacing(5)

        self.toEndButton = QtWidgets.QPushButton(self.GluedSignal)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.toEndButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.toEndButton)

        self.GluedSignalbuttonsLayout.addSpacing(5)

        self.rewindButton = QtWidgets.QPushButton(self.GluedSignal)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton.setStyleSheet(rewindOnButtonStyle)  
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.rewindButton)

        self.GluedSignalbuttonsLayout.addStretch()
        self.GluedSignalPlotLayout.addLayout(self.GluedSignalbuttonsLayout, stretch=6)

        GluedSignalLayout = QVBoxLayout(self.GluedSignal)
        GluedSignalLayout.setContentsMargins(0, 0, 0, 0) 
        GluedSignalLayout.addWidget(self.GluedSignalPlot)
        self.GluedSignal.setLayout(GluedSignalLayout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SignalsApp = QtWidgets.QMainWindow()
    ui = Signals()
    
    ui.signalViewerUi(SignalsApp)
    SignalsApp.show()
    sys.exit(app.exec_())
