import sys
import numpy as np
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from Core import Data_load
from NewGUI.Styles import signalControlButtonStyle, boxStyle, rewindOffButtonStyle,rewindOnButtonStyle
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
        self.setStyleSheet("background-color:#2D2D2D; color: #efefef;")
        self.setWindowTitle("Polar view")
        self.rewind_active = False

        # Load the data from CSV
        self.csv_file_path = 'signals_data/EMG_Normal.csv'
        self.data_loader = Data_load.DataLoader(self.csv_file_path)
        self.data_loader.load_data()
        self.data = self.data_loader.get_data()

        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.init_plot()


        self.is_panning = False
        self.last_mouse_position = None

        # Connect mouse events
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)


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
        self.signalColorChooseList.addItem("#76D4D4", "#76D4D4")
        self.signalColorChooseList.addItem("#D55877", "#D55877")

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
        self.speedSlider.setValue(10)  # Default speed
        self.speedSlider.valueChanged.connect(self.updateSpeedValue)  # Uncomment this line

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
        self.pauseIcon = QIcon("NewGUI/Assets/ControlsButtons/pause.png")
        self.pauseButton.setIcon(self.pauseIcon)
        self.pauseButton.clicked.connect(self.pause)

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playIcon = QIcon("NewGUI/Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)
        self.playButton.clicked.connect(self.play)

        self.zoomInButton = QPushButton()
        self.zoomInButton.setStyleSheet(signalControlButtonStyle)
        self.zoomInButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomInIcon = QIcon("NewGUI/Assets/ControlsButtons/zoomInPolar.png")
        self.zoomInButton.setIcon(self.zoomInIcon)
        self.zoomInButton.clicked.connect(self.zoom_in)

        # Zoom Out Button
        self.zoomOutButton = QPushButton()
        self.zoomOutButton.setStyleSheet(signalControlButtonStyle)
        self.zoomOutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomOutIcon = QIcon("NewGUI/Assets/ControlsButtons/zoomOutPolar.png")
        self.zoomOutButton.setIcon(self.zoomOutIcon)
        self.zoomOutButton.clicked.connect(self.zoom_out)


        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindIcon = QIcon("NewGUI/Assets/ControlsButtons/rewindOff.png")
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

    def init_plot(self):
        """Initialize the polar plot."""
        self.polar_line, = self.canvas.ax.plot([], [], marker='.', color="#76D4D4")
        self.canvas.ax.set_title('Polar Plot of Signal Data')

        if self.data is not None:
            r_min = np.min(self.data[:, 1])
            r_max = np.max(self.data[:, 1])
            self.canvas.ax.set_ylim(r_min, r_max * 1.1)

    def update_plot(self, frame):
        """Update the plot with the current batch of data."""
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
            if self.current_index >= len(self.data):
                if self.rewind_active:
                    # Automatically rewind if the rewind button is active
                    self.current_index = 0  # Reset to the beginning
                    self.polar_line.set_data([], [])  # Clear the plot
                    self.canvas.draw()  # Redraw the canvas
                    self.running = True 

    def updateSpeedValue(self, value):
        """Update animation speed and batch size based on slider value."""
        self.speedValueBox.setText(str(value))

        # Calculate new interval and batch size
        speed_factor = value / 100  # Normalize the speed value
        new_interval = max(1, 50 - int(40 * speed_factor))  # Decrease interval as speed increases
        new_batch_size = max(1, int(10 + 90 * speed_factor))  # Increase batch size with speed

        self.batch_size = new_batch_size  # Update the batch size

        # Update the animation interval
        self.ani.event_source.interval = new_interval  # Update the existing animation interval
        self.ani.event_source.start()  # Restart the animation with the new interval 
   
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
        self.rewind_active = not self.rewind_active
        if self.rewind_active:
            self.rewindButton.setStyleSheet(rewindOnButtonStyle)
            # self.current_index = 0
            # self.polar_line.set_data([], [])  
            # self.canvas.draw() 
            # self.running = True 
        else:
            self.rewindButton.setStyleSheet(rewindOffButtonStyle)

    def on_mouse_press(self, event):
        """Handle mouse button press event."""
        if event.inaxes == self.canvas.ax:  # Use self.canvas.ax instead of self.ax
            self.is_panning = True
            self.last_mouse_position = (event.xdata, event.ydata)

    def on_mouse_move(self, event):
        """Handle mouse movement event."""
        if self.is_panning and event.inaxes == self.canvas.ax:  # Use self.canvas.ax instead of self.ax
            dx = event.xdata - self.last_mouse_position[0]
            dy = event.ydata - self.last_mouse_position[1]

            # Update the plot based on mouse movement
            self.canvas.ax.set_theta_offset(self.canvas.ax.get_theta_offset() + dx * 0.1)  # Adjust the angle offset
            self.canvas.ax.set_ylim(self.canvas.ax.get_ylim()[0] + dy * 0.1, self.canvas.ax.get_ylim()[1] + dy * 0.1)  # Adjust the radius

            self.last_mouse_position = (event.xdata, event.ydata)
            self.canvas.draw_idle()

    def on_mouse_release(self, event):
        """Handle mouse button release event."""
        self.is_panning = False
          
    def on_scroll(self, event):
        """Handle mouse scroll event for zooming."""
        if event.inaxes == self.canvas.ax:
            # Get current limits
            r_min, r_max = self.canvas.ax.get_ylim()

            
            zoom_factor = 0.2
            if event.button == 'up': 
                r_min *= (1 - zoom_factor)
                r_max *= (1 - zoom_factor)
            elif event.button == 'down':  
                r_min *= (1 + zoom_factor)
                r_max *= (1 + zoom_factor)

            
            r_min = max(r_min, 0)  
            r_max = min(r_max, np.max(self.data[:, 1]) * 1.5) 

            
            if r_min < r_max:
                self.canvas.ax.set_ylim(r_min, r_max)
                self.canvas.draw_idle()  

    def reset_zoom(self):
        """Reset the zoom to initial limits."""
        if self.data is not None:
            r_min = np.min(self.data[:, 1])
            r_max = np.max(self.data[:, 1]) * 1.1
            self.canvas.ax.set_ylim(r_min, r_max)
            self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NonRectangularWindow()
    window.show()
    sys.exit(app.exec_())
