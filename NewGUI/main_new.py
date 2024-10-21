import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from plotting import Plotting  # Import your Plotting class
from matplotlibFig import MplCanvas  # Import your MplCanvas class
from SignalViewer import Viewer
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader
import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from importWindow import ImportWindow
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Signal Viewer")
#         self.setGeometry(100, 100, 800, 600)
#
#         # Create the MplCanvas instance
#         self.canvas = MplCanvas(self)
#
#         # Create the Plotting instance and pass the canvas to it
#         self.plotting_instance = Plotting(self.canvas)
#
#         # Set up the main layout
#         main_widget = QWidget()
#         main_layout = QVBoxLayout(main_widget)
#         main_layout.addWidget(self.canvas)
#
#         # Add control buttons
#         self.play_button = QPushButton("Play")
#         self.play_button.clicked.connect(self.plotting_instance.play)
#         main_layout.addWidget(self.play_button)
#
#         self.pause_button = QPushButton("Pause")
#         self.pause_button.clicked.connect(self.plotting_instance.pause)
#         main_layout.addWidget(self.pause_button)
#
#         self.reset_button = QPushButton("Reset")
#         self.reset_button.clicked.connect(self.reset_plot)
#         main_layout.addWidget(self.reset_button)
#
#         self.setCentralWidget(main_widget)
#
#         # Example plot data
#         self.initialize_plot_data()
#
#     def initialize_plot_data(self):
#         # Generate some example signal data
#         x_data = np.linspace(0, 10, 1000)
#         y_data = np.sin(2 * x_data)
#
#         # Initialize the plot with the example data
#         self.plotting_instance.init_plot(x_data, y_data)
#
#     def reset_plot(self):
#         self.plotting_instance.to_start()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())
url_live = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'

# Function to fetch and process the live solar wind data
def Live_signal_processing(url):
    response = requests.get(url)
    data = response.json()

    # Initialize lists for storing extracted data
    time_strings = []
    kp_values = []
    date = []

    for entry in data:
        # Extracting the full datetime object
        full_time = datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S')

        # Formatting time as hh:mm:ss
        formatted_time = str(full_time.time())

        # Extracting the date part (y-m-d)
        date_part = full_time.date()

        # Appending results
        time_strings.append(formatted_time)
        date.append(date_part)
        kp_values.append(entry['estimated_kp'])  # Appending the kp value

    return time_strings, kp_values, date
def main():
    app = QtWidgets.QApplication(sys.argv)
    x_data = np.linspace(0, 10, 1000)

    # plot_data_list = [
    #     {'x_data': x_data, 'y_data': np.sin(x_data)},
    #     {'x_data': x_data, 'y_data': np.cos(x_data)},
    #     {'x_data': x_data, 'y_data': np.sin(2 * x_data)}
    # ]
    # y_data = np.sin(x_data)
    csv_file_path = 'signals_data/ECG_Abnormal.csv'
    data_loader = DataLoader(csv_file_path)
    data_loader.load_data()

    # Get the loaded data
    data = data_loader.get_data()
    x_data = data[:, 0]
    y_data = data[:, 1]
    plot_data_list = [{'x_data': x_data, 'y_data': y_data},{'x_data': np.linspace(0, 10, 1000), 'y_data': np.sinh(np.linspace(0, 10, 1000))}]
    # x_data,y_data,_ = Live_signal_processing(url_live)
    # plot_data_list = [{'x_data': x_data, 'y_data': y_data}]
    print(x_data)
    viewer = Viewer(plot_data_list)
    viewer.setWindowTitle("Signal Viewer")
    viewer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()