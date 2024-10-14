import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
from datetime import datetime
import time
import requests


url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'

response = requests.get(url)
data = response.json()


# Lists to store the times and kp_index for the plot
times = []
kp_indices = []

# Function to update the plot
def update_plot(frame):
    # Simulating live data stream by accessing one entry at a time
    if frame < len(data):
        entry = data[frame]
        time_tag = entry['time_tag']
        kp_index = entry['kp_index']
        
        # Convert time_tag to datetime object and store the time (as hh:mm:ss)
        time_obj = datetime.strptime(time_tag, '%Y-%m-%dT%H:%M:%S')
        times.append(time_obj)
        kp_indices.append(kp_index)
        
        # Clear and re-plot
        plt.cla()
        plt.plot(times, kp_indices, color='b', marker='o')
        
        # Format the x-axis for better readability
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xlabel('Time (hh:mm:ss)')
        plt.ylabel('KP Index')
        plt.title('Live KP Index Signal')
        plt.grid(True)
    
    # Dynamically set x-limits and y-limits
    if len(times) > 0:
        plt.xlim([times[0], times[-1]])
        plt.ylim([min(kp_indices)-1, max(kp_indices)+1])

# Creating the figure and setting the update interval
fig = plt.figure()
ani = FuncAnimation(fig, update_plot, frames=len(data), interval=1000)  # Update every second

# Show the plot
plt.show()
