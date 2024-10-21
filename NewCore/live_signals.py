import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.animation import FuncAnimation
import numpy as np
# from NewGUI.SignalViewer import Viewer
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    # plot_data_list = [{'x_data': time_strings, 'y_data': kp_values}]
    # viewer = Viewer(plot_data_list)
    # viewer.setWindowTitle("Live Signal Viewer")
    # viewer.show()
    print(data)
    return time_strings, kp_values


# print(Live_signal_processing("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"))