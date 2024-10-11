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
        Signals.resize(1440, 1024)
        self.centralwidget = QtWidgets.QWidget(Signals)
        self.centralwidget.setObjectName("centralwidget")

        
        self.signal1Viewer = QtWidgets.QFrame(self.centralwidget)
        self.signal1Viewer.setGeometry(QtCore.QRect(350, 85, 791, 451))  
        self.signal1Viewer.setStyleSheet("background-color: #2D2D2D;")  
        self.signal1Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signal1Viewer.setObjectName("signal1Viewer")

       
        self.signal1Plot = QFrame(self.signal1Viewer)
        self.signal1Plot.setStyleSheet("background-color: #2D2D2D;")
        self.signal1PlotLayout = QVBoxLayout(self.signal1Plot)
        self.signal1PlotLayout.setContentsMargins(5, 5, 5, 5) 
        self.signal1PlotLayout.setObjectName("signal1PlotLayout")

      
        self.canvas1 = MplCanvas(self.signal1Viewer, width=5, height=4, dpi=100, signal_color="#D55877")

        
        self.titleToolbarLayout1 = QHBoxLayout()
        
        
        self.signal1Title = QLabel("Channel 1", self.signal1Viewer)
        self.signal1Title.setStyleSheet("color: #87EDF1; font-size:15px;")  
        self.titleToolbarLayout1.addWidget(self.signal1Title)

        
        self.signal1TitleEdit = QPushButton(self.signal1Viewer)
        self.signal1TitleEdit.setIcon(QtGui.QIcon("photos/edit.png"))
        self.signal1TitleEdit.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signal1TitleEdit.setFixedSize(25, 25)
        self.titleToolbarLayout1.addWidget(self.signal1TitleEdit)

       
        spacer = QSpacerItem(680, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout1.addSpacerItem(spacer)

       
        
        self.signal1PlotLayout.addLayout(self.titleToolbarLayout1, stretch=1)  

       
        self.signal1PlotLayout.addWidget(self.canvas1, stretch=13)  
        self.Signal1buttonsLayout = QHBoxLayout()

     
        self.Signal1buttonsLayout .addStretch(1)
        self.Signal1buttonsLayout  = QHBoxLayout()
        self.Signal1buttonsLayout .addSpacing(14)

     
        self.timeLabel1 = QtWidgets.QLabel("00:00", self.signal1Viewer)
        self.timeLabel1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel1.setStyleSheet(labelStyle)
        self.Signal1buttonsLayout.addWidget(self.timeLabel1)

        self.Signal1buttonsLayout .addSpacing(123)

       
        self.pauseButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton.setStyleSheet(signalControlButtonStyle) 
        self.pauseButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px;")
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.Signal1buttonsLayout .addWidget(self.pauseButton)

       
        self.Signal1buttonsLayout .addSpacing(5)

        self.playButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton.setStyleSheet(signalControlButtonStyle)  
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.Signal1buttonsLayout .addWidget(self.playButton)

        self.Signal1buttonsLayout .addSpacing(5)

        self.stopButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton.setStyleSheet(signalControlButtonStyle)  
        self.stopButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))
        self.Signal1buttonsLayout .addWidget(self.stopButton)

        self.Signal1buttonsLayout .addSpacing(5)

        self.toStartButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.Signal1buttonsLayout .addWidget(self.toStartButton)

        self.Signal1buttonsLayout .addSpacing(5)

        self.toEndButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton.setStyleSheet(signalControlButtonStyle)  
        self.toEndButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.Signal1buttonsLayout .addWidget(self.toEndButton)

        self.Signal1buttonsLayout .addSpacing(5)

        self.rewindButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton.setStyleSheet(rewindOnButtonStyle)  
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.Signal1buttonsLayout .addWidget(self.rewindButton)

        
        self.Signal1buttonsLayout .addStretch()

       
        self.signal1PlotLayout.addLayout(self.Signal1buttonsLayout , stretch=6)


       
        signal1Layout = QVBoxLayout(self.signal1Viewer)
        signal1Layout.setContentsMargins(10, 5, 10, 5)  
        signal1Layout.addWidget(self.signal1Plot)

        
        self.signal2Viewer = QtWidgets.QFrame(self.centralwidget)
        self.signal2Viewer.setGeometry(QtCore.QRect(350, 540, 791, 451)) 
        self.signal2Viewer.setStyleSheet("background-color: #2D2D2D;")
        self.signal2Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signal2Viewer.setObjectName("signal2Viewer")

        
        self.signal2Container = QFrame(self.signal2Viewer)
        self.signal2Container.setStyleSheet("background-color: #2D2D2D;")
        self.signal2LayoutContainer = QVBoxLayout(self.signal2Container)
        self.signal2LayoutContainer.setContentsMargins(15, 5, 15, 5)
        

       
        self.canvas2 = MplCanvas(self.signal2Viewer, width=5, height=4, dpi=100, signal_color="#76D4D4")

        
        self.titleToolbarLayout2 = QHBoxLayout()
        self.signal2Title = QLabel("Channel 2", self.signal2Viewer)
        self.signal2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.titleToolbarLayout2.addWidget(self.signal2Title)

        self.signal2TitleEdit = QPushButton(self.signal2Viewer)
        self.signal2TitleEdit.setIcon(QtGui.QIcon("photos/edit.png"))
        self.signal2TitleEdit.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signal2TitleEdit.setFixedSize(25, 25)
        self.titleToolbarLayout2.addWidget(self.signal2TitleEdit)

        spacer2 = QSpacerItem(680, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout2.addSpacerItem(spacer2)

        self.signal2LayoutContainer.addLayout(self.titleToolbarLayout2)
        self.signal2LayoutContainer.addWidget(self.canvas2)
        self.signal2Viewer.setLayout(self.signal2LayoutContainer)

        Signals.setCentralWidget(self.centralwidget)
        self.Signal2buttonsLayout  = QHBoxLayout()

        
        self.Signal2buttonsLayout .addSpacing(14)

        
        self.timeLabel2 = QtWidgets.QLabel("00:00", self.signal2Viewer)
        self.timeLabel2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel2.setStyleSheet(labelStyle)
        self.Signal2buttonsLayout .addWidget(self.timeLabel2)

        self.Signal2buttonsLayout .addSpacing(123)

      
        self.pauseButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.pauseButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton2.setStyleSheet(signalControlButtonStyle)  
        self.pauseButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.Signal2buttonsLayout .addWidget(self.pauseButton2)

        
        self.Signal2buttonsLayout .addSpacing(5)

        self.playButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.playButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton2.setStyleSheet(signalControlButtonStyle)  
        self.playButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.Signal2buttonsLayout .addWidget(self.playButton2)

        self.Signal2buttonsLayout .addSpacing(5)

        self.stopButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.stopButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton2.setStyleSheet(signalControlButtonStyle)
        self.stopButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))
        self.Signal2buttonsLayout .addWidget(self.stopButton2)

        self.Signal2buttonsLayout .addSpacing(5)

        self.toStartButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toStartButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton2.setStyleSheet(signalControlButtonStyle)  
        self.toStartButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.Signal2buttonsLayout .addWidget(self.toStartButton2)

        self.Signal2buttonsLayout .addSpacing(5)

        self.toEndButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toEndButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton2.setStyleSheet(signalControlButtonStyle)  
        self.toEndButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.Signal2buttonsLayout .addWidget(self.toEndButton2)

        self.Signal2buttonsLayout .addSpacing(5)

        self.rewindButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.rewindButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton2.setStyleSheet(rewindOnButtonStyle)  
        self.rewindButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.Signal2buttonsLayout .addWidget(self.rewindButton2)

     
        self.Signal2buttonsLayout .addStretch()

       
        self.signal2LayoutContainer.addLayout(self.Signal2buttonsLayout , stretch=6)  


        

# Example of real-time plot 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.signals = Signals()
        self.signals.signalViewerUi(self)
        self.init_plot()

    def init_plot(self):
        t = np.linspace(0, 10, 100)
        signal1 = np.sin(2 * np.pi * t) 
        signal2 = np.cos(2 * np.pi * t)  
        self.update_canvas(self.signals.canvas1, t, signal1)
        self.update_canvas(self.signals.canvas2, t, signal2)

      
        self.anim1 = FuncAnimation(self.signals.canvas1.figure, self.animate1, frames=np.arange(0, 100), interval=100)
        self.anim2 = FuncAnimation(self.signals.canvas2.figure, self.animate2, frames=np.arange(0, 100), interval=100)

    def animate1(self, i):
        t = np.linspace(0, 10, 100)
        signal1 = np.sin(2 * np.pi * (t + i / 10)) 
        self.signals.canvas1.update_plot(t, signal1)

    def animate2(self, i):
        t = np.linspace(0, 10, 100)
        signal2 = np.cos(2 * np.pi * (t + i / 10)) 
        self.signals.canvas2.update_plot(t, signal2)

    def update_canvas(self, canvas, t, signal):
        canvas.update_plot(t, signal)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

