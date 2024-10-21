import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
import time

# url_live = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'

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


# Function to live plot the solar wind data
def plot_live_data(url_live):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(10, 6))

    # Initialize empty lists to store time and kp index data
    times = []
    speeds = []

    # Continuous loop to update the plot
    try:

        while True:
            # Fetch the latest data
            new_times, new_speeds, _ = Live_signal_processing(url_live)  # Call the live signal function

            # Append new data to the lists
            times.extend(new_times)  # Extend the list with new time data
            speeds.extend(new_speeds)  # Extend the list with new kp index data

            ax.clear()  # Clear the plot for live updating
            ax.plot(times, speeds, label='Kp Index', color='blue')

            ax.xaxis.set_major_locator(MaxNLocator(nbins=10))  # Maximum of 10 ticks on the x-axis
            ax.set_xlabel('Time')
            ax.set_ylabel('Kp Index')
            ax.set_title('Real-time Kp Index Data')
            plt.xticks(rotation=90)
            plt.tight_layout()

            # Set y-limits dynamically based on data
            if speeds:  # Check if speeds has data
                ax.set_ylim(min(speeds) - 1, max(speeds) + 1)  # Adding a buffer to y-limits

            plt.pause(120)  # Pause for a brief moment to allow the plot to update
    except KeyboardInterrupt:
        print("Plotting stopped by user.")


# print(Live_signal_processing("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"))