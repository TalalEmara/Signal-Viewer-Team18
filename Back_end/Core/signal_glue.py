import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def interpolation(signal1, signal2):
    first_part = signal1[1][-2:]
    second_part = signal2[1][:2]

    # interpolation
    interp_func = interp1d(first_part, second_part)
    interp_signal = interp_func(np.linspace(min(first_part), max(first_part), num=len(first_part)))

    # intepolated signal
    part1 = np.array(signal1[1][:-2])
    part3 = np.array(signal2[1][2:])
    new_signal = np.concatenate((part1, interp_signal, part3))
    
    # total time
    total_time = np.array([i for i in range(len(signal1[1])+len(signal2[1])-len(first_part))])
    
    return np.vstack((total_time, new_signal))

# Generate sample signals
# Signal 1
time1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # Time values for signal 1
signal_data1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Signal data for signal 1
one = (time1, signal_data1)  # Tuple of signal data and time

# Signal 2
time2 = np.array([5, 6, 7, 8, 9, 10, 11, 12, 13])  # Time values for signal 2
signal_data2 = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2])  # Signal data for signal 2
two = (time2, signal_data2)  # Tuple of signal data and time


new_signal = interpolation(one, two)

# Create a figure and 3 subplots (3 rows, 1 column)
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# Plotting the first graph
axs[0].plot(new_signal[0][:len(one[1])], one[1], color='blue', label='First Signal')
axs[0].set_title('First Signal')
# axs[0].set_xlabel('X-axis')
# axs[0].set_ylabel('Y-axis')
axs[0].legend()
axs[0].grid(True)

# Plotting the second graph
axs[1].plot(new_signal[0][:len(two[1])], two[1], color='orange', label='Second Signal')
axs[1].set_title('Second Signal')
# axs[1].set_xlabel('X-axis')
# axs[1].set_ylabel('Y-axis')
axs[1].legend()
axs[1].grid(True)

# Plotting the third graph
axs[2].plot(new_signal[0], new_signal[1], color='green', label='Interpolated Signal')
axs[2].set_title('Interpotated Signal')
# axs[2].set_xlabel('X-axis')
# axs[2].set_ylabel('Y-axis')
axs[2].legend()
axs[2].grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()

