import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from Core import Data_load
from NewGUI.Styles import signalControlButtonStyle, boxStyle, rewindOffButtonStyle


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


class NonRectangularWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:#242424; color: #efefef;")
        self.setWindowTitle("Polar view")

        # Load the data from CSV
        self.csv_file_path = '..\signals_data\EMG_Normal.csv'
        self.data_loader = Data_load.DataLoader(self.csv_file_path)
        self.data_loader.load_data()
        self.data = self.data_loader.get_data()

        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.init_plot()

        # Create buttons
        self.pauseButton = QPushButton()
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseIcon = QIcon("../Assets/ControlsButtons/pause.png")
        self.pauseButton.setIcon(self.pauseIcon)
        self.pauseButton.clicked.connect(self.pause)

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playIcon = QIcon("../Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)
        self.playButton.clicked.connect(self.play)

        # Zoom In Button
        self.zoomInButton = QPushButton("Zoom In")
        self.zoomInButton.setStyleSheet(signalControlButtonStyle)
        self.zoomInButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomInButton.clicked.connect(self.zoom_in)

        # Zoom Out Button
        self.zoomOutButton = QPushButton("Zoom Out")
        self.zoomOutButton.setStyleSheet(signalControlButtonStyle)
        self.zoomOutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomOutButton.clicked.connect(self.zoom_out)


        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindIcon = QIcon("../Assets/ControlsButtons/rewindOff.png")
        self.rewindButton.setIcon(self.rewindIcon)
        self.rewindButton.clicked.connect(self.rewind)

        signalControl = QWidget()
        signalControl.setStyleSheet(boxStyle)
        signalControlLayout = QHBoxLayout()
        signalControl.setLayout(signalControlLayout)

        signalControlLayout.addWidget(self.pauseButton)
        signalControlLayout.addWidget(self.playButton)
        signalControlLayout.addWidget(self.zoomInButton)
        signalControlLayout.addWidget(self.zoomOutButton)
        signalControlLayout.addWidget(self.rewindButton)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(signalControl)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.running = True
        self.current_index = 0
        self.batch_size = 10
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
            end_index = min(self.current_index + self.batch_size, len(self.data))
            batch_data = self.data[self.current_index:end_index]

            time = batch_data[:, 0]
            max_time = self.data[:, 0].max()
            theta = 2 * np.pi * time / max_time
            r = batch_data[:, 1]

            if self.current_index == 0:
                self.polar_line.set_data(theta, r)
            else:
                self.polar_line.set_data(
                    np.concatenate((self.polar_line.get_xdata(), theta)),
                    np.concatenate((self.polar_line.get_ydata(), r))
                )

            self.current_index += self.batch_size
            self.canvas.draw()

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def zoom_in(self):
        current_ylim = self.canvas.ax.get_ylim()
        new_ylim = (current_ylim[0] / 2, current_ylim[1] / 2)  # Zoom in by half

        # Adjust the radial limits of the polar plot
        r_min, r_max = new_ylim
        self.canvas.ax.set_ylim(r_min, r_max)
        self.canvas.ax.set_yticks(np.linspace(r_min, r_max, num=5))  # Update y-ticks

        self.canvas.draw()  # Update the canvas with the new zoom level

    def zoom_out(self):
        current_ylim = self.canvas.ax.get_ylim()
        new_ylim = (current_ylim[0] * 2, current_ylim[1] * 2)  # Zoom out by doubling the range

        # Adjust the radial limits of the polar plot
        r_min, r_max = new_ylim
        self.canvas.ax.set_ylim(r_min, r_max)
        self.canvas.ax.set_yticks(np.linspace(r_min, r_max, num=5))  # Update y-ticks

        self.canvas.draw()  # Update the canvas with the new zoom level

    def rewind(self):
        self.current_index = 0
        self.polar_line.set_data([], [])  # Clear existing plot data
        self.canvas.draw()  # Update the canvas to reflect changes
        self.running = True  # Resume the animation after rewinding


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NonRectangularWindow()
    window.show()
    sys.exit(app.exec_())
