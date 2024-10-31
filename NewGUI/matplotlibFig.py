# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QLineEdit
# from PyQt5.QtGui import QIcon
# from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from PyQt5.QtCore import Qt
# import numpy as np
#
# class MplCanvas(FigureCanvas):
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.ax = fig.add_subplot(111)
#
#         fig.patch.set_facecolor('#242424')
#         self.ax.set_facecolor('#242424')
#
#         self.lines = []
#
#         super(MplCanvas, self).__init__(fig)
#
#         # Customize the plot appearance
#         self.ax.tick_params(axis='x', colors='#EFEFEF')
#         self.ax.tick_params(axis='y', colors='#EFEFEF')
#         self.ax.xaxis.label.set_color('#EFEFEF')
#         self.ax.yaxis.label.set_color('#EFEFEF')
#         self.ax.spines['bottom'].set_color('#EFEFEF')
#         self.ax.spines['left'].set_color('#EFEFEF')
#         self.ax.spines['top'].set_visible(False)
#         self.ax.spines['right'].set_visible(False)
#         self.ax.grid(True, color='#EFEFEF', linestyle='--', alpha=0.1)
#
#         self.ax.set_xlim(0, 10)
#         self.ax.set_ylim(0, 5)
#
#         self.toolbarLayout = QVBoxLayout(self)
#
#         self.navToolbarLayout = QHBoxLayout()
#
#         self.navToolbar = NavigationToolbar(self, parent)
#         self.navToolbar.setStyleSheet("background-color: transparent;")
#         self.navToolbar.setFixedHeight(25)
#         self.navToolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#
#         for action in self.navToolbar.actions():
#             if action.text() in ['Pan', 'Zoom']:
#                 action.setVisible(True)
#                 if action.text() == 'Pan':
#                     action.setIcon(QIcon('Assets/MatPlotToolBar/pan.png'))
#                 elif action.text() == 'Zoom':
#                     action.setIcon(QIcon('Assets/MatPlotToolBar/zoomIn.png'))
#             else:
#                 action.setVisible(False)
#
#         spacer = QSpacerItem(760, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
#         self.navToolbarLayout.addItem(spacer)
#
#         self.navToolbarLayout.addWidget(self.navToolbar)
#
#         self.zoomOutButton = QPushButton("", parent)
#         self.zoomOutButton.setIcon(QtGui.QIcon("Assets/MatPlotToolBar/zoomOut.png"))
#         self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
#         self.zoomOutButton.setFixedSize(25, 25)
#         self.zoomOutButton.clicked.connect(self.zoom_out)
#
#         self.navToolbarLayout.addWidget(self.zoomOutButton)
#
#         self.toolbarLayout.addLayout(self.navToolbarLayout)
#         self.toolbarLayout.addWidget(self)
#
#         self.toolbarLayout.setAlignment(self.navToolbarLayout, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
#
#
#
#         # self.toolbarLayout = QHBoxLayout()
#         # self.toolbarLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)
#
#         # # Toolbar buttons (Zoom, Pan)
#         # self.zoomInButton = QPushButton("", parent)
#         # self.zoomInButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/zoomIn.png"))
#         # self.zoomInButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
#         # self.zoomInButton.setFixedSize(25, 25)
#         # self.zoomInButton.clicked.connect(self.zoom_in)
#         # self.toolbarLayout.addWidget(self.zoomInButton)
#
#         # self.zoomOutButton = QPushButton("", parent)
#         # self.zoomOutButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/zoomOut.png"))
#         # self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
#         # self.zoomOutButton.setFixedSize(25, 25)
#         # self.zoomOutButton.clicked.connect(self.zoom_out)
#         # self.toolbarLayout.addWidget(self.zoomOutButton)
#
#         # self.panButton = QPushButton("", parent)
#         # self.panButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/pan.png"))
#         # self.panButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
#         # self.panButton.setFixedSize(25, 25)
#         # self.panButton.setCheckable(True)
#         # self.panButton.clicked.connect(self.toggle_pan_mode)
#         # self.toolbarLayout.addWidget(self.panButton)
#
#         self.mainLayout = QVBoxLayout(self)
#         self.mainLayout.addLayout(self.toolbarLayout)
#         self.mainLayout.addWidget(self)
#         self.mainLayout.setContentsMargins(0, 0, 0, 0)
#
#         # self.panning = False
#         # self.lastMouseX = None
#
#     def add_line(self, x_data, y_data, color='#D55877', linewidth=2):
#         """Add a new line to the canvas with specified properties."""
#         line, = self.ax.plot(x_data, y_data, color=color, lw=linewidth)
#         self.lines.append(line)
#         self.ax.relim()
#         self.ax.autoscale_view()
#         self.draw_idle()  # Defer drawing until idle
#
#     def update_line(self, line_index, x_data, y_data):
#         """Update an existing line with new data."""
#         if 0 <= line_index < len(self.lines):
#             line = self.lines[line_index]
#             line.set_data(x_data, y_data)
#             self.ax.relim()
#             self.ax.autoscale_view()
#             self.draw_idle()  # Defer drawing until idle
#
#     def clear_canvas(self):
#         """Clear the canvas but keep the current limits."""
#         self.ax.cla()  # Clear the axes
#         self.ax.set_facecolor('#242424')  # Reset background color
#         self.ax.tick_params(axis='x', colors='#EFEFEF')
#         self.ax.tick_params(axis='y', colors='#EFEFEF')
#         self.ax.spines['bottom'].set_color('#EFEFEF')
#         self.ax.spines['left'].set_color('#EFEFEF')
#         self.ax.spines['top'].set_visible(False)
#         self.ax.spines['right'].set_visible(False)
#         self.ax.grid(True, color='#EFEFEF', linestyle='--', alpha=0.1)
#         self.lines.clear()  # Clear stored lines
#         self.draw_idle()  # Defer drawing until idle
#
#     def update_plot(self, x_data, y_data):
#         """Update the plot with new data."""
#         self.clear_canvas()  # Clear previous lines if needed
#         self.add_line(x_data, y_data)
#         self.draw_idle()  # Defer drawing until idle
#
#     def zoom_in(self):
#         """Zoom in by adjusting the axis limits."""
#         xlim = self.ax.get_xlim()
#         ylim = self.ax.get_ylim()
#         new_xlim = [max(0, xlim[0]), max(0.5, xlim[1] - 0.5)]
#         new_ylim = [max(0, ylim[0] + 0.5), ylim[1] - 0.5]
#         self.ax.set_xlim(new_xlim)
#         self.ax.set_ylim(new_ylim)
#         self.draw_idle()  # Defer drawing until idle
#
#     def zoom_out(self):
#         """Zoom out by adjusting the axis limits."""
#
#         # Get current axis limits
#         xlim = self.ax.get_xlim()
#         ylim = self.ax.get_ylim()
#         print(f"Current xlim: {xlim}, Current ylim: {ylim}")  # Debug print
#
#         # Calculate new axis limits
#         new_xlim = [max(0, xlim[0]- 0.05), xlim[1] + 0.05]
#         new_ylim = [ ylim[0] - 0.05, ylim[1] + 0.05]
#         print(f"New xlim: {new_xlim}, New ylim: {new_ylim}")  # Debug print
#
#         # Set new axis limits
#         self.ax.set_xlim(new_xlim)
#         self.ax.set_ylim(new_ylim)
#
#         # Print to confirm the limits were set
#         print(f"Updated xlim: {self.ax.get_xlim()}, Updated ylim: {self.ax.get_ylim()}")  # Debug print
#
#         # Trigger deferred drawing
#         self.draw_idle()  # Defer drawing until idle

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, \
    QLineEdit
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
import numpy as np
from plotting import Plotting

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#242424')
        self.ax.set_facecolor('#242424')

        self.lines = []

        super(MplCanvas, self).__init__(fig)

        # Customize the plot appearance
        self.ax.tick_params(axis='x', colors='#EFEFEF')
        self.ax.tick_params(axis='y', colors='#EFEFEF')
        self.ax.xaxis.label.set_color('#EFEFEF')
        self.ax.yaxis.label.set_color('#EFEFEF')
        self.ax.spines['bottom'].set_color('#EFEFEF')
        self.ax.spines['left'].set_color('#EFEFEF')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.grid(True, color='#EFEFEF', linestyle='--', alpha=0.1)

        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 5)

        self.toolbarLayout = QVBoxLayout(self)

        self.navToolbarLayout = QHBoxLayout()

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(25)
        self.navToolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        for action in self.navToolbar.actions():
            # if action.text() in ['Pan', 'Zoom']:
            #     action.setVisible(True)
            #     if action.text() == 'Pan':
            #         action.setIcon(QIcon('Assets/MatPlotToolBar/pan.png'))
            #     elif action.text() == 'Zoom':
            #         action.setIcon(QIcon('Assets/MatPlotToolBar/zoomIn.png'))
            # else:
                action.setVisible(False)

        spacer = QSpacerItem(760, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.navToolbarLayout.addItem(spacer)

        self.navToolbarLayout.addWidget(self.navToolbar)

        self.zoomOutButton = QPushButton("", parent)
        self.zoomOutButton.setIcon(
            QtGui.QIcon("Assets/MatPlotToolBar/zoomOut.png"))
        self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomOutButton.setFixedSize(25, 25)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        self.navToolbarLayout.addWidget(self.zoomOutButton)
        # Create Zoom In Button
        self.zoomInButton = QPushButton("", self)
        self.zoomInButton.setIcon(QtGui.QIcon("Assets/MatPlotToolBar/zoomIn.png"))
        self.zoomInButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomInButton.setFixedSize(25, 25)
        self.zoomInButton.clicked.connect(self.zoom_in)

        self.panButton = QPushButton("", self)
        self.panButton.setIcon(QtGui.QIcon("Assets/MatPlotToolBar/pan.png"))  # Assuming you have a pan icon
        self.panButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.panButton.setFixedSize(25, 25)
        self.panButton.clicked.connect(self.toggle_pan)
        # Add buttons to the toolbar layout
        self.navToolbarLayout.addWidget(self.zoomInButton)
        self.navToolbarLayout.addWidget(self.panButton)

        self.toolbarLayout.addLayout(self.navToolbarLayout)
        self.toolbarLayout.addWidget(self)

        self.toolbarLayout.setAlignment(self.navToolbarLayout, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        # self.toolbarLayout = QHBoxLayout()
        # self.toolbarLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # # Toolbar buttons (Zoom, Pan)
        # self.zoomInButton = QPushButton("", parent)
        # self.zoomInButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/zoomIn.png"))
        # self.zoomInButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        # self.zoomInButton.setFixedSize(25, 25)
        # self.zoomInButton.clicked.connect(self.zoom_in)
        # self.toolbarLayout.addWidget(self.zoomInButton)

        # self.zoomOutButton = QPushButton("", parent)
        # self.zoomOutButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/zoomOut.png"))
        # self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        # self.zoomOutButton.setFixedSize(25, 25)
        # self.zoomOutButton.clicked.connect(self.zoom_out)
        # self.toolbarLayout.addWidget(self.zoomOutButton)

        # self.panButton = QPushButton("", parent)
        # self.panButton.setIcon(QIcon("NewGUI/Assets/MatPlotToolBar/pan.png"))
        # self.panButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        # self.panButton.setFixedSize(25, 25)
        # self.panButton.setCheckable(True)
        # self.panButton.clicked.connect(self.toggle_pan_mode)
        # self.toolbarLayout.addWidget(self.panButton)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.toolbarLayout)
        self.mainLayout.addWidget(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # self.panning = False
        # self.lastMouseX = None

    def add_line(self, x_data, y_data, color='#D55877', linewidth=2):
        """Add a new line to the canvas with specified properties."""
        line, = self.ax.plot(x_data, y_data, color=color, lw=linewidth)
        self.lines.append(line)
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw_idle()  # Defer drawing until idle

    def update_line(self, line_index, x_data, y_data):
        """Update an existing line with new data."""
        if 0 <= line_index < len(self.lines):
            line = self.lines[line_index]
            line.set_data(x_data, y_data)
            self.ax.relim()
            self.ax.autoscale_view()
            self.draw_idle()  # Defer drawing until idle

    def clear_canvas(self):
        """Clear the canvas but keep the current limits."""
        self.ax.cla()  # Clear the axes
        self.ax.set_facecolor('#242424')  # Reset background color
        self.ax.tick_params(axis='x', colors='#EFEFEF')
        self.ax.tick_params(axis='y', colors='#EFEFEF')
        self.ax.spines['bottom'].set_color('#EFEFEF')
        self.ax.spines['left'].set_color('#EFEFEF')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.grid(True, color='#EFEFEF', linestyle='--', alpha=0.1)
        self.lines.clear()  # Clear stored lines
        self.draw_idle()  # Defer drawing until idle

    def update_plot(self, x_data, y_data):
        """Update the plot with new data."""
        self.clear_canvas()  # Clear previous lines if needed
        self.add_line(x_data, y_data)
        self.draw_idle()  # Defer drawing until idle

    def zoom_in(self):
        """Zoom in by adjusting the axis limits."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        new_xlim = [max(0, xlim[0]), max(0.5, xlim[1] - 0.5)]
        new_ylim = [max(0, ylim[0] + 0.5), ylim[1] - 0.5]
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.draw_idle()  # Defer drawing until idle

    def zoom_out(self):
        """Zoom out by adjusting the axis limits."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        new_xlim = [max(0, xlim[0]), xlim[1] + 0.5]
        new_ylim = [max(0, ylim[0] - 0.5), ylim[1] + 0.5]
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.draw_idle()  # Defer drawing until idle

    def toggle_pan(self):
        """Toggle panning state."""
        if hasattr(self, 'dragging') and self.dragging:
            self.dragging = False
            self.panButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")  # Reset style
        else:
            self.dragging = True
            self.panButton.setStyleSheet(
                "background-color: #404040; color: #FFFFFF; border: none;")  # Change style to indicate active panning