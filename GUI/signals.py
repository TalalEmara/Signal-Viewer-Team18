import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from matplotlib.animation import FuncAnimation
from PyQt5.QtCore import Qt

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

        # Toolbar layout with zoom-out button
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(25)
        self.navToolbar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for action in self.navToolbar.actions():
            if action.text() == 'Home':
                action.setIcon(QIcon('photos/home.png'))
            elif action.text() == 'Pan':
                action.setIcon(QIcon('photos/pan.png'))
            elif action.text() == 'Zoom':
                action.setIcon(QIcon('photos/zoomIn.png'))
            elif action.text() == 'Save':
                action.setIcon(QIcon('photos/save.png'))
        
        # Add the navigation toolbar to the toolbar layout
        self.toolbarLayout.addWidget(self.navToolbar)

        # Zoom Out Button
        self.zoomOutButton = QPushButton("", parent)
        self.zoomOutButton.setIcon(QtGui.QIcon("photos/zoomOut.png"))
        self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomOutButton.setFixedSize(25, 25)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        # Add the zoom-out button to the toolbar layout
        self.toolbarLayout.addWidget(self.zoomOutButton)

        # Main layout for the canvas
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.toolbarLayout)  
        self.mainLayout.addWidget(self)  
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def zoom_out(self):
        """Zoom out by adjusting the x and y axis limits."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] - 0.5, xlim[1] + 0.5])
        self.ax.set_ylim([ylim[0] - 0.5, ylim[1] + 0.5])
        self.draw()

    def update_plot(self, t, signal):
        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()


class Signals(QtWidgets.QWidget):  # Inheriting from QWidget instead of object
    def __init__(self):
        super().__init__()
        self.signalViewerUi()

    def signalViewerUi(self):
        self.setObjectName("Signals")
        self.resize(1440, 1024)
        
        # Main layout for the widget
        mainLayout = QVBoxLayout(self)
        
        # Signal 1 Viewer
        self.signal1Viewer = QtWidgets.QFrame(self)
        self.signal1Viewer.setStyleSheet("background-color: #2D2D2D;border:none;")
        self.signal1Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        self.signal1PlotLayout = QVBoxLayout(self.signal1Viewer)
        self.signal1PlotLayout.setContentsMargins(5, 5, 5, 5)

        self.canvas1 = MplCanvas(self.signal1Viewer, width=5, height=4, dpi=100, signal_color="#D55877")
        
        self.titleToolbarLayout1 = QHBoxLayout()
        self.signal1Title = QLabel("Channel 1", self.signal1Viewer)
        self.signal1Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.titleToolbarLayout1.addWidget(self.signal1Title)
        
        self.signal1TitleEdit = QPushButton(self.signal1Viewer)
        self.signal1TitleEdit.setIcon(QtGui.QIcon("photos/edit.png"))
        self.signal1TitleEdit.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signal1TitleEdit.setFixedSize(20, 20)
        self.titleToolbarLayout1.addWidget(self.signal1TitleEdit)

        
        self.signal1PlotLayout.addLayout(self.titleToolbarLayout1, stretch=1)  

       
        self.signal1PlotLayout.addWidget(self.canvas1, stretch=13)  

        spacer = QSpacerItem(1000, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout1.addSpacerItem(spacer)
        
       

        self.signal1PlotLayout.addLayout(self.titleToolbarLayout1)
        self.signal1PlotLayout.addWidget(self.canvas1)

        # Time labels and buttons
        self.Signal1buttonsLayout = QHBoxLayout()
        self.Signal1buttonsLayout .addStretch(1)
        self.Signal1buttonsLayout  = QHBoxLayout()
        self.Signal1buttonsLayout .addSpacing(30)
        
        
        self.timeLabel1 = QtWidgets.QLabel("00:00", self.signal1Viewer)
        self.timeLabel1.setStyleSheet(labelStyle)
        self.Signal1buttonsLayout.addWidget(self.timeLabel1)
        self.Signal1buttonsLayout .addSpacing(70)
        self.pauseButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.Signal1buttonsLayout.addWidget(self.pauseButton)

        self.Signal1buttonsLayout .addSpacing(5)
        
        self.playButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.Signal1buttonsLayout.addWidget(self.playButton)

        self.stopButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.stopButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))
        self.stopButton.setStyleSheet(signalControlButtonStyle)
        self.Signal1buttonsLayout.addWidget(self.stopButton)

        self.toStartButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toStartButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.Signal1buttonsLayout.addWidget(self.toStartButton)

        self.toEndButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toEndButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.Signal1buttonsLayout.addWidget(self.toEndButton)

        self.rewindButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.Signal1buttonsLayout.addWidget(self.rewindButton)

        self.Signal1buttonsLayout.addStretch(6)  # Stretch added here to push buttons to the right
        self.signal1PlotLayout.addLayout(self.Signal1buttonsLayout)
        
        # Add signal1Viewer to the main layout
        mainLayout.addWidget(self.signal1Viewer)
        spacer_between_signals = QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mainLayout.addSpacerItem(spacer_between_signals)
        
        # Signal 2 Viewer (same structure as Signal 1)
        self.signal2Viewer = QtWidgets.QFrame(self)
        self.signal2Viewer.setStyleSheet("background-color: #2D2D2D; border:none;")
        
        self.signal2Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.signal2PlotLayout = QVBoxLayout(self.signal2Viewer)
        self.signal2PlotLayout.setContentsMargins(5, 5, 5, 5)

        self.canvas2 = MplCanvas(self.signal2Viewer, width=5, height=4, dpi=100, signal_color="#76D4D4")

        self.titleToolbarLayout2 = QHBoxLayout()
        self.signal2Title = QLabel("Channel 2", self.signal2Viewer)
        self.signal2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.titleToolbarLayout2.addWidget(self.signal2Title)

        self.signal2TitleEdit = QPushButton(self.signal2Viewer)
        self.signal2TitleEdit.setIcon(QtGui.QIcon("photos/edit.png"))
        self.signal2TitleEdit.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signal2TitleEdit.setFixedSize(20, 20)
        self.titleToolbarLayout2.addWidget(self.signal2TitleEdit)

        spacer2 = QSpacerItem(1000, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout2.addSpacerItem(spacer2)

        self.signal2PlotLayout.addLayout(self.titleToolbarLayout2)
        self.signal2PlotLayout.addWidget(self.canvas2)

        self.Signal2buttonsLayout = QHBoxLayout()
        

        self.Signal2buttonsLayout .addSpacing(30)

        self.timeLabel2 = QtWidgets.QLabel("00:00", self.signal2Viewer)
        self.timeLabel2.setStyleSheet(labelStyle)
        self.Signal2buttonsLayout.addWidget(self.timeLabel2)

        self.Signal2buttonsLayout .addSpacing(70)
        
        self.pauseButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.pauseButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.pauseButton2.setStyleSheet(signalControlButtonStyle)
        self.Signal2buttonsLayout.addWidget(self.pauseButton2)

        self.playButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.playButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.playButton2.setStyleSheet(signalControlButtonStyle)
        self.Signal2buttonsLayout.addWidget(self.playButton2)

        self.stopButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.stopButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))
        self.stopButton2.setStyleSheet(signalControlButtonStyle)
        self.Signal2buttonsLayout.addWidget(self.stopButton2)

        self.toStartButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toStartButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.toStartButton2.setStyleSheet(signalControlButtonStyle)
        self.Signal2buttonsLayout.addWidget(self.toStartButton2)

        self.toEndButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toEndButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.toEndButton2.setStyleSheet(signalControlButtonStyle)
        self.Signal2buttonsLayout.addWidget(self.toEndButton2)

        self.rewindButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.rewindButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton2.setStyleSheet(rewindOffButtonStyle)
        self.Signal2buttonsLayout.addWidget(self.rewindButton2)

        self.Signal2buttonsLayout.addStretch(6)
        self.signal2PlotLayout.addLayout(self.Signal2buttonsLayout)
        
        # Add signal2Viewer to the main layout
        mainLayout.addWidget(self.signal2Viewer)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.signals = Signals()
        self.setCentralWidget(self.signals)
        self.init_plot()

    def init_plot(self):
        t = np.linspace(0, 10, 100)
        signal1 = np.sin(2 * np.pi * t)  # Example signal 1 data
        signal2 = np.cos(2 * np.pi * t)  # Example signal 2 data
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
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
