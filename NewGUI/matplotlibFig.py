import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtCore import Qt
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#242424')
        self.ax.set_facecolor('#242424')

        self.line, = self.ax.plot([], [], lw=2)

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

        self.ax.set_xlim(0, 10)  
        self.ax.set_ylim(0, 5)

        self.min_y_value = 0

        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.zoomInButton = QPushButton("", parent)
        self.zoomInButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/zoomIn.png"))
        self.zoomInButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomInButton.setFixedSize(25, 25)
        self.zoomInButton.clicked.connect(self.zoom_in)
        self.toolbarLayout.addWidget(self.zoomInButton)

        self.zoomOutButton = QPushButton("", parent)
        self.zoomOutButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/zoomOut.png"))
        self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomOutButton.setFixedSize(25, 25)
        self.zoomOutButton.clicked.connect(self.zoom_out)
        self.toolbarLayout.addWidget(self.zoomOutButton)

        self.panButton = QPushButton("", parent)
        self.panButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/pan.png"))
        self.panButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.panButton.setFixedSize(25, 25)
        self.panButton.setCheckable(True)
        self.panButton.clicked.connect(self.toggle_pan_mode)
        self.toolbarLayout.addWidget(self.panButton)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.toolbarLayout)
        self.mainLayout.addWidget(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.panning = False
        self.lastMouseX = None

    def zoom_in(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Zoom in with minimum x-limit
        new_xlim = [max(0, xlim[0]), max(0.5,xlim[1] - 0.5)]
        new_ylim = [max(self.min_y_value, ylim[0] + 0.5), ylim[1] - 0.5]
        
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.draw()

    def zoom_out(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Zoom out with minimum x-limit
        new_xlim = [max(0, xlim[0]), xlim[1] + 0.5]
        new_ylim = [max(self.min_y_value, ylim[0] - 0.5), ylim[1] + 0.5]
        
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.draw()

    def toggle_pan_mode(self):
        self.panning = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.panning:
            self.lastMouseX = event.x()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.panning and self.lastMouseX is not None:
            xlim = self.ax.get_xlim()
            delta = (event.x() - self.lastMouseX) * 0.01 

            # Allow panning without upper limit, but do not allow going below 0
            new_xlim = [max(0, xlim[0] - delta), xlim[1] - delta]

            # Maintain some width even when dragging
            if new_xlim[1] < new_xlim[0]:
                new_xlim[1] = new_xlim[0] + 1  

            self.ax.set_xlim(new_xlim)
            self.draw()
            self.lastMouseX = event.x()
        super().mouseMoveEvent(event)

    def update_plot(self, t, signal):
        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view()
        self.min_y_value = min(signal)  
        self.draw()
