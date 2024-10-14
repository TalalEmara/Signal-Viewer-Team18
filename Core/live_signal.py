import requests
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import MaxNLocator

# URL to the real-time solar wind data from NOAA
url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'
# url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'


# Function to fetch and process the live solar wind data
def fetch_solar_wind_data():
    response = requests.get(url)
    data = response.json()

    # # Extract time and solar wind speed from the data
    # times = [
    #     ((str(datetime.strptime(entry[0], '%Y-%m-%d %H:%M:%S.%f') - 
    #     datetime.strptime(entry[0][:10], '%Y-%m-%d')))) 
    #     for entry in data[1:]
    # ]

    # # Extract speed and handle None values by skipping them or replacing with 0
    # speed = [
    #     float(entry[2]) if entry[2] is not None else 0  # Set speed to 0 if it's None
    #     for entry in data[1:]
    # ]

    # Extracting time in hour:min:sec format and saving the date
    time = []
    time_string = []
    date = []
    for entry in data:
        # Extracting the full datetime object
        full_time = datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S')
        
        # Extracting time in seconds since midnight and formatting it as hh:mm:ss
        time_in_seconds = (full_time - full_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        formatted_time = str(full_time.time())  # This gives hh:mm:ss
        
        # Extracting the date part (y-m-d)
        date_part = full_time.date()

        # Appending results
        time_string.append(formatted_time)
        time.append(full_time)
        date.append(date_part)

        # times = [((datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S') - 
                # datetime.strptime(entry['time_tag'][:10], '%Y-%m-%d')).total_seconds()) for entry in data]
    kp = [entry['estimated_kp'] for entry in data]

    return time_string, kp, date

# # Function to live plot the solar wind data
# def plot_live_data():
#     plt.ion()  # Interactive mode on for live updates
#     fig, ax = plt.subplots(figsize=(10, 6))

#     while True:
#         times, speeds = fetch_solar_wind_data()

#         ax.clear()  # Clear the plot for live updating
#         ax.plot(times, speeds, label='kp index', color='blue')
        
#         ax.xaxis.set_major_locator(MaxNLocator(nbins=100))  # Maximum of 10 ticks on the x-axis

#         ax.set_xlabel('Time')
#         ax.set_ylabel('Kp Index')
#         ax.set_title('Real-time kp Index Data')
#         plt.xticks(rotation=90)
#         plt.tight_layout()

#         plt.pause(20)  # Update the plot every 60 seconds

# # Call the function to start live plotting
# plot_live_data()
