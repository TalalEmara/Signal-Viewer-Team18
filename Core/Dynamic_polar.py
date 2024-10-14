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
        self.zoom_out_button.setIcon(QIcon('photos/zoomOut.png'))  # Path to your zoom out icon
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
        self.csv_file_path = '../signals_data/EMG_Normal.csv'
        self.data_loader = Data_load.DataLoader(self.csv_file_path)
        self.data_loader.load_data()
        self.data = self.data_loader.get_data().values  # Convert to NumPy array


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
        self.batch_size = 10  # Number of points to update
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, interval=100, blit=False)

    def init_plot(self):
        self.polar_line, = self.canvas.ax.plot([], [], marker='o')
        self.canvas.ax.set_title('Polar Plot of Signal Data')
        if self.data is not None:
            r_min = np.min(self.data[:, 1])
            r_max = np.max(self.data[:, 1])
            self.canvas.ax.set_ylim(r_min, r_max*1.1)
    def update_plot(self, frame):
        if self.running and self.data is not None:
            # avoiding index errors.
            end_index = min(self.current_index + self.batch_size, len(self.data))

            batch_data = self.data[self.current_index:end_index]
            theta = 2 * np.pi * batch_data[:, 0]  # First column for theta
            r = batch_data[:, 1]  # Second column for radius

            if self.current_index == 0:
                self.polar_line.set_data(theta, r)  # Initial plot
            else:
                self.polar_line.set_data(
                    np.concatenate((self.polar_line.get_xdata(), theta)),
                    np.concatenate((self.polar_line.get_ydata(), r))
                )

            self.current_index += self.batch_size



            self.canvas.draw()

    def stop_signal(self):
        self.running = False


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

