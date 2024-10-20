import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QLineEdit
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader
from matplotlibFig import MplCanvas
from plotting import Plotting
import numpy as np

class Viewer(QtWidgets.QWidget):
    def __init__(self,data_list):
        super().__init__()
        
        self.data_list = data_list
        self.ViewerUi()
        

    def ViewerUi(self):
        self.setStyleSheet("background-color: #2D2D2D;")
        self.setObjectName("Viewer 1")
        self.resize(792, 434)

        mainLayout = QVBoxLayout(self)
        self.signalViewer = QFrame(self)
        self.signalViewer.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signalViewer.setFrameShape(QtWidgets.QFrame.StyledPanel)

      
        self.signalPlotLayout = QVBoxLayout(self.signalViewer)
        self.signalPlotLayout.setContentsMargins(5, 5, 5, 5)

     
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.plotting_instance = Plotting(self.canvas, self.data_list)
        self.canvas.draw()

        self.titleToolbarLayout = QHBoxLayout()
        self.signalTitle = QLabel("Channel 1", self.signalViewer)
        self.signalTitle.setStyleSheet("color: #87EDF1; font-size: 15px;")
        self.titleToolbarLayout.addWidget(self.signalTitle)

       
        self.signalTitleEditButton = QPushButton(self.signalViewer)
        self.signalTitleEditButton.setIcon(QtGui.QIcon("NewGUI/Assets/MatPlotToolBar/edit.png"))
        self.signalTitleEditButton.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signalTitleEditButton.setFixedSize(20, 20)
        self.signalTitleEditButton.clicked.connect(lambda: self.editTitle(self.signalTitle, self.titleToolbarLayout))
        self.titleToolbarLayout.addWidget(self.signalTitleEditButton)

        spacer = QSpacerItem(792, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout.addSpacerItem(spacer)
      
        self.SignalbuttonsLayout = QHBoxLayout()
        self.SignalbuttonsLayout.addStretch(1)

        self.timeLabel = QtWidgets.QLabel("00:00", self.signalViewer)
        self.timeLabel.setStyleSheet(labelStyle)
        self.SignalbuttonsLayout.addWidget(self.timeLabel)
        self.SignalbuttonsLayout.addSpacing(70)

        self.pauseButton = QtWidgets.QPushButton(self.signalViewer)
        self.pauseButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/pause.png"))
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.clicked.connect(self.plotting_instance.pause)
        self.SignalbuttonsLayout.addWidget(self.pauseButton)

        self.playButton = QtWidgets.QPushButton(self.signalViewer)
        self.playButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/play.png"))
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.clicked.connect(self.plotting_instance.play)
        self.SignalbuttonsLayout.addWidget(self.playButton)

        self.toStartButton = QtWidgets.QPushButton(self.signalViewer)
        self.toStartButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/start.png"))
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.clicked.connect(self.plotting_instance.to_start)
        self.SignalbuttonsLayout.addWidget(self.toStartButton)

        self.toEndButton = QtWidgets.QPushButton(self.signalViewer)
        self.toEndButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/end.png"))
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.clicked.connect(self.plotting_instance.to_end)
        self.SignalbuttonsLayout.addWidget(self.toEndButton)

        self.rewindButton = QtWidgets.QPushButton(self.signalViewer)
        self.rewindButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setCheckable(True)
        self.rewindButton.toggled.connect(self.plotting_instance.toggle_rewind)
        self.SignalbuttonsLayout.addWidget(self.rewindButton)

        self.SignalbuttonsLayout.addStretch(6)

        self.signalPlotLayout.addLayout(self.titleToolbarLayout)  
        self.signalPlotLayout.addWidget(self.canvas)  
        self.signalPlotLayout.addLayout(self.SignalbuttonsLayout)

        self.signalViewer.setLayout(self.signalPlotLayout)

        mainLayout.addWidget(self.signalViewer)

        self.setLayout(mainLayout)


    def set_properties(self, properties):
        self.plotting_instance.plot_selected.connect(properties.update_properties)
    
    def on_plot_selected(self, index, color, thickness, speed):

        if self.RightPanelInstance:
            self.RightPanelInstance.update_properties(index, color, thickness, speed)

        
    def editTitle(self, label, layout):
        edit_line = QLineEdit(label.text(), self.signalViewer)
        edit_line.setMaxLength(12)
        edit_line.setStyleSheet("color: #EFEFEF; font-size:15px; background-color:#2D2D2D;")
        
def main():
    app = QtWidgets.QApplication(sys.argv)

   
    x_data = np.linspace(0, 10, 1000)
    plot_data_list = [
        {'x_data': x_data, 'y_data': np.sin(x_data), 'color': '#FF5733', 'thickness': 2, 'speed': 50},
        {'x_data': x_data, 'y_data': np.cos(x_data), 'color': '#33FF57', 'thickness': 3, 'speed': 100},
        {'x_data': x_data, 'y_data': np.sin(2 * x_data), 'color': '#3357FF', 'thickness': 4, 'speed': 150}
    ]


    viewer = Viewer(plot_data_list)
    viewer.setWindowTitle("Signal Viewer")
    viewer.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()