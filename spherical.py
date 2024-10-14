import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from Back_end import Data_load


def plot_spherical_coordinates(data):
    """Plot EMG data in spherical coordinates."""
    # Extract time (t) and signal value (v) from the DataFrame
    t = data.iloc[:, 0]  # First column for time
    v = data.iloc[:, 1]  # Second column for signal value

    # Normalize the signal values for better visualization in spherical coordinates
    v_normalized = (v - np.min(v)) / (np.max(v) - np.min(v))  # Normalize to [0, 1]

    # Convert time to a polar angle (theta) in radians
    theta = 2 * np.pi * (t - np.min(t)) / (np.max(t) - np.min(t))  # Normalize time to [0, 2*pi]

    # Set azimuthal angle (phi) to a constant value (0 for simplicity)
    phi = np.zeros_like(v_normalized)  # Constant azimuthal angle

    # Convert spherical to Cartesian coordinates
    x = v_normalized * np.sin(theta) * np.cos(phi)
    y = v_normalized * np.sin(theta) * np.sin(phi)
    z = v_normalized * np.cos(theta)

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='b', marker='o', alpha=0.6)

    ax.set_title('Spherical Plot of EMG Signal Data')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# Usage Example
if __name__ == "__main__":
    # Path to your CSV file
    file_path = 'signals_data/ECG_Abnormal.csv'

    # Load data
    data_loader = Data_load.DataLoader(file_path)
    data_loader.load_data()

    # Get loaded data
    data = data_loader.get_data()

    # Ensure data has the required two columns before plotting
    if data is not None:  # Check for exactly 2 columns
        plot_spherical_coordinates(data)
    else:
        print("Data does not have the required two columns for plotting.")
