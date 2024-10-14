import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from Back_end import Data_load



def plot_spiral_coordinates(data):
    """Plot EMG data in spiral coordinates."""
    # Extract time (t) and signal value (v) from the DataFrame
    t = data.iloc[:, 0]  # First column for time
    v = data.iloc[:, 1]  # Second column for signal value

    # Normalize the signal values for better visualization
    v_normalized = (v - np.min(v)) / (np.max(v) - np.min(v))  # Normalize to [0, 1]

    # Create a spiral by adjusting the radius based on normalized signal values
    theta = np.linspace(0, 4 * np.pi, len(t))  # Increase the angle for the spiral
    z = np.linspace(0, 1, len(t))  # Linear space for height
    r = v_normalized  # Radius corresponds to normalized signal values

    # Convert to Cartesian coordinates for 3D plot
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Create a 3D plot for the spiral
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, c='b', alpha=0.8)

    ax.set_title('Spiral Plot of EMG Signal Data')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def plot_cylindrical_coordinates(data):
    """Plot EMG data in cylindrical coordinates."""
    # Extract time (t) and signal value (v) from the DataFrame
    t = data.iloc[:, 0]  # First column for time
    v = data.iloc[:, 1]  # Second column for signal value

    # Normalize the signal values for better visualization
    v_normalized = (v - np.min(v)) / (np.max(v) - np.min(v))  # Normalize to [0, 1]

    # Convert time to a theta (angle in radians)
    theta = 2 * np.pi * (t - np.min(t)) / (np.max(t) - np.min(t))  # Normalize time to [0, 2*pi]

    # Set z as the normalized signal value
    z = v_normalized

    # Convert cylindrical to Cartesian coordinates
    x = z * np.cos(theta)
    y = z * np.sin(theta)

    # Create a 3D plot for the cylinder
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, c='b', alpha=0.8)

    ax.set_title('Cylindrical Plot of EMG Signal Data')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# Usage Example
if __name__ == "__main__":
    # Path to your CSV file
    file_path = '../signals_data/ECG_Abnormal.csv'

    # Load data
    data_loader = Data_load.DataLoader(file_path)
    data_loader.load_data()

    # Get loaded data
    data = data_loader.get_data()

    # Ensure data has the required two columns before plotting
    if data is not None:  # Check for exactly 2 columns
        # Plot spiral coordinates
        plot_spiral_coordinates(data)

        # Plot cylindrical coordinates
        plot_cylindrical_coordinates(data)
    else:
        print("Data does not have the required two columns for plotting.")
