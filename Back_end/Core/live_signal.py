import requests
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import MaxNLocator

# URL to the real-time solar wind data from NOAA
url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'

# Function to fetch and process the live solar wind data
def fetch_solar_wind_data():
    response = requests.get(url)
    data = response.json()

    # Extract time and relevant data (e.g., speed of solar wind)
    times = [((datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S') - 
            datetime.strptime(entry['time_tag'][:10], '%Y-%m-%d')).total_seconds()) for entry in data]
    kp = [entry['estimated_kp'] for entry in data]

    return times, kp

# Function to live plot the solar wind data
def plot_live_data():
    plt.ion()  # Interactive mode on for live updates
    fig, ax = plt.subplots(figsize=(10, 6))

    while True:
        times, speeds = fetch_solar_wind_data()

        ax.clear()  # Clear the plot for live updating
        ax.plot(times, speeds, label='kp index', color='blue')
        
        ax.xaxis.set_major_locator(MaxNLocator(nbins=70))  # Maximum of 10 ticks on the x-axis

        ax.set_xlabel('Time')
        ax.set_ylabel('Kp Index')
        ax.set_title('Real-time kp Index Data')
        plt.xticks(rotation=90)
        plt.tight_layout()

        plt.pause(20)  # Update the plot every 60 seconds

# Call the function to start live plotting
plot_live_data()

# import time
# import requests
# from datetime import datetime

# NOAA_API_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

# def check_real_time_data():
#     response = requests.get(NOAA_API_URL)
#     data = response.json()[-1]  # Get the latest data
    
#     # Extract the timestamp from the data (assuming it is in ISO format)
#     signal_time_str = data['time_tag']  # Example: '2024-10-08T15:21:00'
    
#     # Convert to datetime object
#     signal_time = datetime.strptime(signal_time_str, '%Y-%m-%dT%H:%M:%S')
    
#     # Get the current time
#     current_time = datetime.utcnow()  # Assuming UTC for both the signal and system time

#     # Check if the time difference is small, indicating real-time data
#     time_difference = current_time - signal_time
#     print(f"Signal Time: {signal_time}, Current Time: {current_time}")
#     print(f"Time Difference: {time_difference.seconds} seconds")

#     # If the time difference is small, it's real-time
#     if time_difference.seconds < 120:  # Example: allowing up to 2 minutes delay
#         print("The signal is real-time!")
#     else:
#         print("The signal is delayed or not real-time.")

# if __name__ == "__main__":
#     check_real_time_data()
