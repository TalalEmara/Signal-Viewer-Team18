import requests
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime

# URL to the real-time solar wind data from NOAA
url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'

# Function to fetch and process the live solar wind data
def fetch_solar_wind_data():
    response = requests.get(url)
    data = response.json()

    # Extract time and relevant data (e.g., speed of solar wind)
    times = [datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S') for entry in data]
    kp = [entry['estimated_kp'] for entry in data]

    return times, kp

# Function to live plot the solar wind data
# def plot_live_data():
#     plt.ion()  # Interactive mode on for live updates
#     fig, ax = plt.subplots(figsize=(10, 6))

#     while True:
#         times, speeds = fetch_solar_wind_data()

#         ax.clear()  # Clear the plot for live updating
#         ax.plot(times, speeds, label='kp index', color='skyblue')
#         ax.set_xlabel('Time')
#         ax.set_ylabel('Kp Index')
#         ax.set_title('Real-time kp Index Data')
#         plt.xticks(rotation=45)
#         plt.tight_layout()

#         plt.pause(60)  # Update the plot every 60 seconds

# # Call the function to start live plotting
# plot_live_data()
