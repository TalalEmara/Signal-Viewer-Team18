import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QLineEdit
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtCore import Qt
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader
from matplotlibFig import MplCanvas

class Viewer2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_paused = False

    def initUI(self):
        self.setStyleSheet("background-color: #2D2D2D;")
        self.setObjectName("Viewer 2")
        self.resize(792, 434)

        mainLayout = QVBoxLayout(self)
        self.signalViewer = QFrame(self)
        self.signalViewer.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signalViewer.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.signalPlotLayout = QVBoxLayout(self.signalViewer)
        self.signalPlotLayout.setContentsMargins(5, 5, 5, 5)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.draw()

        self.titleToolbarLayout = QHBoxLayout()
        self.signalTitle = QLabel("Channel 2", self.signalViewer)
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
        self.pauseButton.clicked.connect(self.pauseAction)
        self.SignalbuttonsLayout.addWidget(self.pauseButton)

        self.playButton = QtWidgets.QPushButton(self.signalViewer)
        self.playButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/play.png"))
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.clicked.connect(self.playAction)
        self.SignalbuttonsLayout.addWidget(self.playButton)

        self.toStartButton = QtWidgets.QPushButton(self.signalViewer)
        self.toStartButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/start.png"))
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.clicked.connect(self.toStartAction)
        self.SignalbuttonsLayout.addWidget(self.toStartButton)

        self.toEndButton = QtWidgets.QPushButton(self.signalViewer)
        self.toEndButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/end.png"))
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.clicked.connect(self.toEndAction)
        self.SignalbuttonsLayout.addWidget(self.toEndButton)

        self.rewindButton = QtWidgets.QPushButton(self.signalViewer)
        self.rewindButton.setIcon(QtGui.QIcon("NewGUI/Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setCheckable(True)
        self.rewindButton.toggled.connect(self.toggleRewind)
        self.SignalbuttonsLayout.addWidget(self.rewindButton)

        self.SignalbuttonsLayout.addStretch(6)

        self.signalPlotLayout.addLayout(self.titleToolbarLayout)
        self.signalPlotLayout.addWidget(self.canvas)
        self.signalPlotLayout.addLayout(self.SignalbuttonsLayout)

        self.signalViewer.setLayout(self.signalPlotLayout)
        mainLayout.addWidget(self.signalViewer)
        self.setLayout(mainLayout)

    def pauseAction(self):
        self.parent().anim.event_source.stop()
        self.parent().is_paused = True

    def playAction(self):
        if self.parent().is_paused:
            self.parent().anim.event_source.start()
            self.parent().is_paused = False

    def toStartAction(self):
        current_ylim = self.canvas.ax.get_ylim()
        self.canvas.ax.set_xlim([0, 0])
        self.canvas.ax.set_ylim(current_ylim)
        self.canvas.draw()

    def toEndAction(self):
        current_ylim = self.canvas.ax.get_ylim()
        self.canvas.ax.set_xlim([10, 10])
        self.canvas.ax.set_ylim(current_ylim)
        self.canvas.draw()

    def toggleRewind(self, checked):
        self.parent().rewind_enabled = checked
        if checked:
            self.parent().reset_signal_animation(1)
            self.rewindButton.setStyleSheet(rewindOnButtonStyle)
        else:
            self.rewindButton.setStyleSheet(rewindOffButtonStyle)

    def editTitle(self, label, layout):
        edit_line = QLineEdit(label.text(), self.signalViewer)
        edit_line.setMaxLength(12)
        edit_line.setStyleSheet("color: #EFEFEF; font-size:15px; background-color:#2D2D2D;")

def main():
    app = QtWidgets.QApplication(sys.argv)
    viewer = Viewer2()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
