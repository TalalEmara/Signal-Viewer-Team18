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
import requests
from datetime import datetime
import matplotlib.dates as mdates

def Live_signal_processing(url):
    response = requests.get(url)
    data = response.json()

    # Initialize lists for storing extracted data
    time_numbers = []  # For numerical time representation
    kp_values = []
    date = []

    for entry in data:
        # Extracting the full datetime object
        full_time = datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S')

        # Convert datetime to a numerical format (for plotting)
        time_number = mdates.date2num(full_time)  # Convert to numerical format

        # Extracting date part (y-m-d)
        date_part = full_time.date()

        # Appending results
        time_numbers.append(time_number)
        date.append(date_part)
        kp_values.append(entry['estimated_kp'])  # Appending the kp value

    # Return numerical time representation and kp values
    return time_numbers, kp_values


# print(Live_signal_processing("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"))