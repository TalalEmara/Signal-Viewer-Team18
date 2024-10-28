import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QLineEdit
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from Core.Data_load import DataLoader
from matplotlibFig import MplCanvas
from plotting import Plotting
import numpy as np
from PyQt5.QtCore import pyqtSignal 
from PyQt5.QtWidgets import QSlider
from pyqtgraph import PlotWidget, mkPen, plot
from PyQt5.QtCore import QTimer

class NViewer(QWidget):
    play_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    to_start_signal = pyqtSignal()
    to_end_signal = pyqtSignal()
    rewind_signal = pyqtSignal()
    frame_signal = pyqtSignal()

    def __init__(self, data_list, channel_name="Channel 1", show_rewind_button=True):
        super().__init__()
        
        self.channel_name = channel_name  # Ensure the channel_name is defined
        self.data_list = data_list
        self.x_data = data_list[0]['x_data']
        self.y_data = data_list[0]['y_data']
        self.show_rewind_button = show_rewind_button
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

     
        self.canvas = PlotWidget()

        self.canvas.setLabel('bottom', 'Time', units='s')
        if self.data_list:
            # Prepare to plot the initial data
            self.x_data = self.data_list[0]['x_data']
            self.y_data = self.data_list[0]['y_data']
            self.canvas.plot(self.x_data, self.y_data, pen=mkPen(color="b", width=2))

            # Initialize the timer for updating the plot
            self.time_index = 0
            self.timer = QTimer()
            self.timer.setInterval(50)  # Update every 50 ms
            self.timer.timeout.connect(self.update_plot_data)
            self.timer.start()




        self.titleToolbarLayout = QHBoxLayout()
        self.signalTitle = QLabel(self.channel_name, self.signalViewer)  
        self.signalTitle.setStyleSheet("color: #87EDF1; font-size: 15px;")
        self.titleToolbarLayout.addWidget(self.signalTitle)

       
        self.signalTitleEditButton = QPushButton(self.signalViewer)
        self.signalTitleEditButton.setIcon(QtGui.QIcon("Assets/MatPlotToolBar/edit.png"))
        self.signalTitleEditButton.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signalTitleEditButton.setFixedSize(20, 20)
        self.signalTitleEditButton.clicked.connect(lambda: self.editTitle(self.signalTitle, self.titleToolbarLayout))
        self.titleToolbarLayout.addWidget(self.signalTitleEditButton)

        spacer = QSpacerItem(792, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout.addSpacerItem(spacer)
      
        self.SignalbuttonsLayout = QHBoxLayout()
        self.SignalbuttonsLayout.addStretch(1)

        self.pauseButton = QtWidgets.QPushButton(self.signalViewer)
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.SignalbuttonsLayout.addWidget(self.pauseButton)

        self.playButton = QtWidgets.QPushButton(self.signalViewer)
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.SignalbuttonsLayout.addWidget(self.playButton)

        self.rewindButton = None  # Initialize the rewind button to None

        # Add the rewind button only if show_rewind_button is True
        if self.show_rewind_button:
            self.rewindButton = QtWidgets.QPushButton(self.signalViewer)
            self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
            self.rewindButton.setStyleSheet(rewindOffButtonStyle)
            self.rewindButton.setCheckable(True)
            self.SignalbuttonsLayout.addWidget(self.rewindButton)

     
        self.slider = QSlider(QtCore.Qt.Horizontal, self.signalViewer)
        self.slider.setRange(0, 100)  # Set the range based on your data
        self.slider.setValue(0)  # Initial position
        self.SignalbuttonsLayout.addWidget(self.slider)

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

        def save_changes():
            new_text = edit_line.text()

            label.setText(new_text)

            layout.replaceWidget(edit_line, label)

            edit_line.deleteLater()

        edit_line.returnPressed.connect(save_changes)

        edit_line.setFocus()

        layout.replaceWidget(label, edit_line)


        def on_focus_out(event):
            if event.reason() == QtCore.Qt.FocusReason.LostFocus:
                layout.replaceWidget(edit_line, label)

                edit_line.deleteLater()

        edit_line.focusOutEvent = on_focus_out


    def update_rewind_button(self, enabled):
       
        if enabled:
            self.rewindButton.setStyleSheet(rewindOnButtonStyle)
            self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOn.png"))
        else:
            self.rewindButton.setStyleSheet(rewindOffButtonStyle)
            self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))

    def get_current_frame_data(self):
        """Retrieve the current frame's x and y data from the plotting instance."""
        return self.plotting_instance.get_current_data()

    def update_plot_data(self):
        """Update the plot with new data."""
        # Check if time index exceeds the length of the data
        if self.time_index < len(self.x_data):
            # Update the plot data
            self.canvas.clear()  # Clear the previous plot
            self.canvas.plot(self.x_data[:self.time_index + 1], self.y_data[:self.time_index + 1],
                             pen=mkPen(color="b", width=2))

            # Update min/max values based on current data
            self.y_min = np.min(self.y_data[:self.time_index + 1])
            self.y_max = np.max(self.y_data[:self.time_index + 1])
            self.x_max = np.max(self.x_data[:self.time_index + 1])

            # Reset X-axis limits to prevent zooming in or out
            self.canvas.setXRange(0, self.x_max, padding=0)

            # Get current view range after any potential zoom
            current_y_limits = self.canvas.viewRange()[1]
            print(current_y_limits)

            # Check if the current Y limits are outside the defined range
            if (current_y_limits[0] < self.y_min or current_y_limits[1] > self.y_max):
                # If out of bounds, reset to the defined limits
                print("out")
                print(self.y_min)
                print(self.y_max)
                self.canvas.setYRange(self.y_min, self.y_max, padding=0.5)
            else:
                # Set the Y range based on the current limits if within bounds
                self.canvas.setYRange(current_y_limits[0], current_y_limits[1], padding=0.5)
                print("zoomed")

            # Move to the next time index
            self.time_index += 1
        else:
            self.timer.stop()  # Stop the timer if all data is plotted


def main():
    app = QtWidgets.QApplication(sys.argv)

    x_data = np.linspace(0, 10, 1000)
    y_data = np.sin(x_data)
    plot_data_list = [{'x_data': x_data, 'y_data':y_data}]
    # plot_data_list = ImportWindow.importFile(ImportWindow)

    viewer = NViewer(plot_data_list)
    viewer.setWindowTitle("Signal Viewer")
    viewer.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()