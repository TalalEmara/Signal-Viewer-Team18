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
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QSizePolicy, QSlider, \
    QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QColorDialog
from PyQt5.QtGui import QColor

from NewGUI.properties_style import signalChooseStyle, labelStyle, titleStyle, colorSignalChooseStyle, sliderStyle, \
    valueBoxStyle, tableStyle, viewButtonOnStyle, viewButtonOffStyle



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

        self.colorChoosen = "#76D4D4"
        self.signalColorLabel = QLabel("Signal Color")
        self.signalColorLabel.setStyleSheet(labelStyle)

        self.signalColorChooseSquare = QPushButton()
        self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
        self.signalColorChooseSquare.setFixedHeight(20)
        self.signalColorChooseSquare.setFixedWidth(20)
        self.signalColorChooseSquare.clicked.connect(self.openColorDialog)

        self.signalColorChooseList = QComboBox()
        self.signalColorChooseList.setStyleSheet(colorSignalChooseStyle)
        self.signalColorChooseList.addItem("Blue", "#76D4D4")
        self.signalColorChooseList.addItem("Red", "#D55877")

        self.signalColorChooseList.addItem("Add New Color")
        self.signalColorChooseList.currentIndexChanged.connect(self.changeSignalColor)

        # Thickness Control
        self.thicknessLabel = QLabel("Line Thickness")
        self.thicknessLabel.setStyleSheet(labelStyle)

        self.thicknessSlider = QSlider(Qt.Horizontal)
        self.thicknessSlider.setStyleSheet(sliderStyle)
        self.thicknessSlider.setMinimum(1)
        self.thicknessSlider.setMaximum(10)
        self.thicknessSlider.setSingleStep(1)
        self.thicknessSlider.setValue(2)  # Default thickness
        self.thicknessSlider.valueChanged.connect(self.updateThicknessValue)

        self.thicknessValueBox = QLineEdit("2")
        self.thicknessValueBox.setStyleSheet(valueBoxStyle)
        self.thicknessValueBox.setFixedWidth(40)
        self.thicknessValueBox.setAlignment(Qt.AlignCenter)

        # Speed Control
        self.speedLabel = QLabel("Animation Speed")
        self.speedLabel.setStyleSheet(labelStyle)

        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setStyleSheet(sliderStyle)
        self.speedSlider.setMinimum(5)
        self.speedSlider.setMaximum(100)
        self.speedSlider.setSingleStep(5)
        self.speedSlider.setValue(10)
        #self.ani.event_source.interval = 10
        #self.speedSlider.valueChanged.connect(self.updateSpeedValue)

        self.speedValueBox = QLineEdit("10")
        self.speedValueBox.setStyleSheet(valueBoxStyle)
        self.speedValueBox.setFixedWidth(40)
        self.speedValueBox.setAlignment(Qt.AlignCenter)

        # Layout for the color, thickness, and speed properties
        propertiesPanel = QVBoxLayout()

        colorPropertyRow1 = QHBoxLayout()
        colorPropertyRow1.addWidget(self.signalColorLabel)
        colorPropertyRow2 = QHBoxLayout()
        colorPropertyRow2.addWidget(self.signalColorChooseSquare)
        colorPropertyRow2.addWidget(self.signalColorChooseList)

        thicknessPropertyRow1 = QHBoxLayout()
        thicknessPropertyRow1.addWidget(self.thicknessLabel)
        thicknessPropertyRow2 = QHBoxLayout()
        thicknessPropertyRow2.addWidget(self.thicknessSlider)
        thicknessPropertyRow2.addWidget(self.thicknessValueBox)

        speedPropertyRow1 = QHBoxLayout()
        speedPropertyRow1.addWidget(self.speedLabel)
        speedPropertyRow2 = QHBoxLayout()
        speedPropertyRow2.addWidget(self.speedSlider)
        speedPropertyRow2.addWidget(self.speedValueBox)

        propertiesPanel.addLayout(colorPropertyRow1)
        propertiesPanel.addLayout(colorPropertyRow2)
        propertiesPanel.addLayout(thicknessPropertyRow1)
        propertiesPanel.addLayout(thicknessPropertyRow2)
        propertiesPanel.addLayout(speedPropertyRow1)
        propertiesPanel.addLayout(speedPropertyRow2)

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
        layout.addLayout(propertiesPanel)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.running = True
        self.current_index = 0
        self.batch_size = 10
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, interval=100, blit=False)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorChoosen = color.name()  # Get the color hex code
            self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")

            # Check if the color is already in the list
            color_exists = False
            for i in range(self.signalColorChooseList.count()):
                if self.signalColorChooseList.itemText(i) == self.colorChoosen:  # Corrected the condition
                    color_exists = True
                    break

            # If the color is not in the list, add it
            if not color_exists:
                self.signalColorChooseList.insertItem(self.signalColorChooseList.count() - 1, self.colorChoosen,
                                                      self.colorChoosen)  # Add hex color as both text and data

            # Set the current index to the new color
            self.signalColorChooseList.setCurrentIndex(self.signalColorChooseList.count() - 2)

            self.changeSignalColor()

    def changeSignalColor(self):
        # Avoid re-triggering color dialog on "Add New Color"
        if self.signalColorChooseList.currentText() == "Add New Color":
            # Temporarily block signals to prevent recursive calls
            self.signalColorChooseList.blockSignals(True)

            # Open the color dialog and reset the selection after
            self.openColorDialog()

            # Reset to the last selected color or the first item
            self.signalColorChooseList.setCurrentIndex(self.signalColorChooseList.count() - 2)

            # Unblock signals after resetting the index
            self.signalColorChooseList.blockSignals(False)
        else:
            # Get the color associated with the selected item
            self.colorChoosen = self.signalColorChooseList.currentData()
            if self.colorChoosen:  # Ensure valid color is selected
                self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
                self.polar_line.set_color(self.colorChoosen)
                self.canvas.draw()

    def updateThicknessValue(self, value):
        self.thicknessValueBox.setText(str(value))
        self.polar_line.set_linewidth(value)
        self.canvas.draw()

    def updateSpeedValue(self, value):
        self.speedValueBox.setText(str(value))
        self.ani.event_source.interval = value  # Update the animation interval directly

    def init_plot(self):
        self.polar_line, = self.canvas.ax.plot([], [], marker='.', color="#76D4D4")
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
