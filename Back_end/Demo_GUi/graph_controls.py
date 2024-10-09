import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QListWidget,
    QCheckBox
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Demo UI")
        self.resize(1440,1080)

        # Create layout for folder selection and list
        folder_layout = QVBoxLayout()

        self.select_folder_button = QPushButton("Select Folder")
        self.folder_list = QListWidget()

        folder_layout.addWidget(self.select_folder_button)
        folder_layout.addWidget(self.folder_list)

        # Create layout for audio player controls
        control_layout = QHBoxLayout()

        self.time_label = QLabel("00:00")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.rewind_button = QCheckBox("rewind")
        self.start_button = QPushButton("start")
        self.end_button = QPushButton("end")

        self.ch1linked_button = QCheckBox("ch1 linked ")
        self.ch2linked_button = QCheckBox("ch2 linked ")
        self.glue_button = QPushButton("glue")



        self.export = QPushButton("export")


        control_layout.addWidget(self.time_label)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.rewind_button)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.end_button)
        control_layout.addWidget(self.ch1linked_button)
        control_layout.addWidget(self.ch2linked_button)
        control_layout.addWidget(self.glue_button)

        control_layout.addWidget(self.export)

        # Create layout for the graph
        graph_layout = QVBoxLayout()

        # Generate dummy data
        x = np.linspace(0, 10, 100)  # 100 points between 0 and 10 (could represent time in seconds)
        y = np.sin(x) + np.random.normal(0, 0.1, x.shape)  # Sine wave with some noise        

        # Create a Matplotlib figure and plot data
        self.fig = Figure(figsize=(5, 3))  # Adjust figure size as needed
        ax = self.fig.add_subplot(111)
        ax.plot(x, y)

        # Create a Matplotlib canvas for embedding in the layout
        self.canvas = FigureCanvasQTAgg(self.fig)
        graph_layout.addWidget(self.canvas)

        # Combine all layouts
        main_layout = QHBoxLayout()
        # main_layout.addLayout(folder_layout)
        # main_layout.addLayout(control_layout)
        main_layout.addLayout(graph_layout)

        self.setLayout(main_layout)

        # Create a timer to update time label (replace with actual playback logic)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # Update time every second
        self.timer.timeout.connect(self.update_time_label)
        self.current_time = 0  # Placeholder for current playback time

        # Connect button functionality

    def update_time_label(self):
        # Update current time based on playback logic
        self.current_time += 1  # Placeholder for progress

        # Convert current time to a formatted string (e.g., MM:SS)
        minutes, seconds = divmod(self.current_time, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"

        # Update the time label text
        self.time_label.setText(time_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())