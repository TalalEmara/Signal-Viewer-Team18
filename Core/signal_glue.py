import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# glue with interpolation
def interpolation(signal1, signal2):
    """
    signal1, signal2 => two signals of [time, amplitude]
    returning:
      total_time => time of the new signal
      new_signal => signal after interpolation
    """

    overlapped_time = []
    for i in range(len(signal1[0])):
        if signal1[0][i] == signal2[0][0]:
            overlapped_time.extend([int(x) for x in signal1[0][i:]])
            break

    first_part = signal1[1][-(len(overlapped_time)):]
    second_part = signal2[1][:len(overlapped_time)]

    # interpolation
    interp_func = interp1d(first_part, second_part)
    interp_signal = interp_func(np.linspace(min(first_part), max(first_part), num=len(first_part)))

    # intepolated signal
    part1 = np.array(signal1[1][:(len(overlapped_time)+2)])
    part3 = np.array(signal2[1][-len(overlapped_time)-1:])
    new_signal = np.concatenate((part1, interp_signal, part3))
    
    # total time
    total_time = np.array([i for i in range(len(signal1[1])+len(signal2[1])-len(first_part))])
    
    return total_time, new_signal

# glue with ovelapping
def overlap(signal1, signal2):
    """
    signal1, signal2 => two signals of [time, amplitude]
    returning:
        new_time[:len(signal1[1])] => time of signal1
        signal1[1] => amplitude of signal1
        new_time[:len(signal2[1])] => time of signal2
        signal2[1] => amplitude of signal2
    """

    new_time = np.array([i for i in range(max(len(signal1[0]),  len(signal2[0])))])

    return new_time[:len(signal1[1])], signal1[1], new_time[:len(signal2[1])], signal2[1] 


# glue with a gap
def gap(signal1, signal2):
    """
    signal1, signal2 => two signals of [time, amplitude]
    returning:
        new_time[:len(signal1[1])] => time of signal1
        signal1[1] => amplitude of signal1
        new_time[len(signal1[1]):] => time of signal2
        signal2[1] => amplitude of signal2
    """
    
    new_time = np.array([i for i in range(len(signal1[0]) + len(signal2[0]))])

    return new_time[: len(signal1[1])], signal1[1], new_time[len(signal1[1]):], signal2[1] 

# General glue
def move_back(signal1, signal2):
    """
    assume that signal1 will be fixed
    signal2 will move left on each call
    """
    signal2[0] = signal2[0] - 1

    return signal1, signal2

def move_forward(signal1, signal2):
    """
    assume that signal1 will be fixed
    signal2 will move right on each call
    """
    signal2[0] = signal2[0] + 1

    return signal1, signal2


# Generate sample signals
# Signal 1
time1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # Time values for signal 1
signal_data1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 14])  # Signal data for signal 1
one = [time1, signal_data1]  # Tuple of signal data and time

# Signal 2
time2 = np.array([6, 7, 8, 9, 10, 11, 12, 13, 14])  # Time values for signal 2
signal_data2 = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2])  # Signal data for signal 2
two = [time2, signal_data2]  # Tuple of signal data and time

# print(interpolation(one, two))
time, signal = interpolation(one, two)
plt.plot(time, signal, color='green', label='Signal 2')
plt.legend()
plt.grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()
# Show the plots
plt.show()


# signal1, signal2 = move(one, two)
# plt.plot(signal1[0], signal1[1], color='red', label='Signal 1')
# plt.plot(signal2[0], signal2[1], color='green', label='Signal 2')
# plt.legend()
# plt.grid(True)

# # Adjust layout to prevent overlap
# plt.tight_layout()
# # Show the plots
# plt.show()

# # testing
# xi, yi = interpolation(one, two)
# xo1, yo1, xo2, yo2 = overlap(one, two)
# xg1, yg1, xg2, yg2 = gap(one, two)

# # Create a figure and 3 subplots (3 rows, 1 column)
# fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# # Plotting the interpolated signal
# axs[0].plot(xi, yi, color='green', label='Interpolation')
# axs[0].legend()
# axs[0].grid(True)

# # Plot the second overlapped signal
# axs[1].plot(xo1, yo1, label='Signal 1 overlapping', color='blue')
# axs[1].plot(xo2, yo2, label='Signal 2 overlapping', color='orange')
# axs[1].legend()
# axs[1].grid(True)

# # Plotting the gapped signal
# axs[2].plot(xg1, yg1, color='red', label='Signal 1 Gap')
# axs[2].plot(xg2, yg2, color='brown', label='Signal 2 Gap')
# axs[2].legend()
# axs[2].grid(True)

# # Adjust layout to prevent overlap
# plt.tight_layout()

# # Show the plots
# plt.show()
