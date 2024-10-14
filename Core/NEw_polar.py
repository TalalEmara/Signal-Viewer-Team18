import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QToolButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from Core import Data_load


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='polar')
        super(MplCanvas, self).__init__(fig)


class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        self.zoom_out_button = QToolButton(self)
        self.zoom_out_button.setIcon(QIcon('photos/zoomOut.png'))
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.addWidget(self.zoom_out_button)

    def zoom_out(self):
        rlim = self.canvas.ax.get_ylim()
        # Zoom out by a factor of 1.5
        self.canvas.ax.set_ylim([rlim[0] - (rlim[1] - rlim[0]) * 0.5, rlim[1] + (rlim[1] - rlim[0]) * 0.5])
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the data from CSV
        self.csv_file_path = '../signals_data/EMG_Abnormal.csv'
        self.data_loader = Data_load.DataLoader(self.csv_file_path)
        self.data_loader.load_data()
        self.data = self.data_loader.get_data()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.init_plot()

        self.toolbar = CustomToolbar(self.canvas, self)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_signal)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.running = True
        self.current_index = 0

        # Create a point in the plot
        self.polar_point, = self.canvas.ax.plot([], [], 'o', color='b')  # 'o' creates a single point

        # Start the animation
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, interval=10, blit=False)

    def init_plot(self):
        self.canvas.ax.set_title('Polar Plot of Signal Data')
        if self.data is not None:
            self.canvas.ax.set_ylim(self.data.iloc[:, 1].min(), self.data.iloc[:, 1].max()*1.1)

    def update_plot(self, frame):
        if self.running and self.data is not None:
            if self.current_index < len(self.data):
                theta = 2 * np.pi * self.data.iloc[self.current_index, 0]
                r = self.data.iloc[self.current_index, 1]

                # Update the position point
                self.polar_point.set_data(theta, r)

                self.current_index += 1


                self.canvas.draw()

    def stop_signal(self):
        self.running = False


# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

