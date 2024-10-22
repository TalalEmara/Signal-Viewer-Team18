import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QToolButton, QSizePolicy, \
    QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from Core import Data_load
from NewGUI.Styles import signalControlButtonStyle, boxStyle, rewindOffButtonStyle,rewindOnButtonStyle



class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='polar')
        fig.patch.set_facecolor('#242424')
        self.ax.set_facecolor('#242424')
        self.ax.set_title("Polar Plot", color='#EFEFEF')
        self.ax.spines['polar'].set_color('#EFEFEF')
        self.ax.grid(color='#EFEFEF', linestyle='dashed', linewidth=0.2)
        self.ax.tick_params(axis='x', colors='#EFEFEF')
        self.ax.tick_params(axis='y', colors='#EFEFEF')



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

        self.setStyleSheet("background-color:#242424; color: #efefef;")
        self.setWindowTitle("Polar view")

        # Load the data from CSV
        self.csv_file_path = '..\signals_data\EMG_Normal.csv'
        self.data_loader = Data_load.DataLoader(self.csv_file_path)
        self.data_loader.load_data()
        self.data = self.data_loader.get_data()  # Convert to NumPy array


        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.init_plot()


        self.toolbar = CustomToolbar(self.canvas, self)


        #self.stop_button = QPushButton("Stop")
        #self.stop_button.clicked.connect(self.stop_signal)

        self.pauseButton = QPushButton()
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseIcon = QIcon(
            "E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets\ControlsButtons\pause.png")
        self.pauseButton.setIcon(self.pauseIcon)

        self.pauseButton.pressed.connect(lambda: self.handleButtonPress(self.pauseButton))
        self.pauseButton.released.connect(lambda: self.handleButtonRelease(self.pauseButton))

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playIcon = QIcon(
            "E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)

        self.playButton.pressed.connect(lambda: self.handleButtonPress(self.playButton))
        self.playButton.released.connect(lambda: self.handleButtonRelease(self.playButton))

        self.toStartButton = QPushButton()
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartIcon = QIcon(
            "E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/start.png")
        self.toStartButton.setIcon(self.toStartIcon)

        self.toStartButton.pressed.connect(lambda: self.handleButtonPress(self.toStartButton))
        self.toStartButton.released.connect(lambda: self.handleButtonRelease(self.toStartButton))

        self.toEndButton = QPushButton()
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndIcon = QIcon(
            "E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/end.png")
        self.toEndButton.setIcon(self.toEndIcon)

        self.toEndButton.pressed.connect(lambda: self.handleButtonPress(self.toEndButton))
        self.toEndButton.released.connect(lambda: self.handleButtonRelease(self.toEndButton))

        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindIcon = QIcon(
            "E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/rewindOff.png")
        self.rewindButton.setIcon(self.rewindIcon)

        self.isRewind = False
        self.rewindButton.clicked.connect(lambda: self.handleRewindClick())

        signalControl = QWidget()
        signalControl.setStyleSheet(boxStyle)
        signalControlLayout = QHBoxLayout()
        signalControl.setLayout(signalControlLayout)

        signalControlLayout.addWidget(self.pauseButton)
        signalControlLayout.addWidget(self.playButton)
        signalControlLayout.addWidget(self.toStartButton)
        signalControlLayout.addWidget(self.toEndButton)
        signalControlLayout.addWidget(self.rewindButton)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.stop_button)
        layout.addWidget(signalControl)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.running = True
        self.current_index = 0
        self.batch_size = 10  # Number of points to update
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, interval=100, blit=False)

    def init_plot(self):
        self.polar_line, = self.canvas.ax.plot([], [], marker='.')
        self.canvas.ax.set_title('Polar Plot of Signal Data')

        if self.data is not None:
            r_min = np.min(self.data[:, 1])
            r_max = np.max(self.data[:, 1])
            self.canvas.ax.set_ylim(r_min, r_max * 1.1)

    def update_plot(self, frame):
        if self.running and self.data is not None:
            # Avoiding index errors
            end_index = min(self.current_index + self.batch_size, len(self.data))

            batch_data = self.data[self.current_index:end_index]

            # Transform time to theta
            time = batch_data[:, 0]  # Assuming the first column is time
            max_time = self.data[:, 0].max()  # Get the maximum time value for normalization
            theta = 2 * np.pi * time / max_time  # Map time to the range [0, 2π]

            r = batch_data[:, 1]  # Second column for radius (amplitude)

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
