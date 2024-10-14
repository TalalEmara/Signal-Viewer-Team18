import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Back_end import Data_load


def plot_polar(data):
    """Plot the data on a polar graph."""
    theta = 2 * np.pi * data.iloc[:, 0]  # First column for theta
    r = data.iloc[:, 1]  # Second column for radius

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection='polar')
    ax.plot(theta, r, marker='o', linestyle='-')

    ax.set_title('Polar Plot of Signal Data')
    ax.set_xlabel('Angle (radians)')
    ax.set_ylabel('Signal Value')

    plt.show()


def main():
    """Main function to run the data loading and plotting."""
    # Replace 'your_file.csv' with the path to your CSV file
    csv_file_path = '../signals_data/EMG_Normal.csv'

    # Create a DataLoader instance and load data
    data_loader = Data_load.DataLoader(csv_file_path)
    data_loader.load_data()

    # Get the loaded data
    data = data_loader.get_data()
    plot_polar(data)

if __name__ == '__main__':
    main()

