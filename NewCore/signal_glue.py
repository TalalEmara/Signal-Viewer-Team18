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
    # getting total time
    total_time = signal1[0]
    # print(len(total_time))
    for i in signal2[0]:
        if np.all(i > total_time):
            total_time = np.concatenate((total_time, [i]))

    # print(total_time)

    signal_time = [i for i in signal1[0]]                 

    for i in signal2[0]:
        if i not in signal_time:
            signal_time.append(i)

    if len(total_time) > len(signal_time):
        signal_data = [int(i) for i in signal1[1]]
        signal_data.extend(int(i) for i in signal2[1])
        new_signal = np.interp(total_time, signal_time, signal_data)

    else:
        overlapped_time = []
        for i in range(len(signal1[0])):
            if signal1[0][i] == signal2[0][0]:
                overlapped_time.extend([float(x) for x in signal1[0][i:]])
                break

        interpolated_signal1 = np.interp(overlapped_time, signal1[0], signal1[1])
        interpolated_signal2 = np.interp(overlapped_time, signal2[0], signal2[1])
        combined_overlap = (interpolated_signal1 + interpolated_signal2) / 2
        new_signal = np.concatenate((signal1[1][:-len(overlapped_time)], combined_overlap, signal2[1][len(overlapped_time):]))

        # print(len(total_time), len(overlapped_time), len(new_signal))

    return total_time, new_signal

def move_backward(signal1, signal2):
    """
    assume that signal1 will be fixed
    signal2 will move left on each call
    """
    signal2[0] = signal2[0] - 1

    return interpolation(signal1, signal2)

def move_forward(signal1, signal2):
    """
    assume that signal1 will be fixed
    signal2 will move right on each call
    """
    signal2[0] = signal2[0] + 1

    return interpolation(signal1, signal2)


# # Generate sample signals
# time1 = np.linspace(0, 30, 100)
# signal1 = np.sin(2 * np.pi * 10 * time1)
# one = [time1, signal1]

# time2 = np.linspace(20, 50, 100)
# signal2 = np.exp(0.1 * time2)
# two = [time2, signal2]
# # print(interpolation(one, two))
# # print(time1, time2)
# time, signal = interpolation(one, two)

# plt.plot(time1, signal1, color='red')
# plt.plot(time2, signal2, color='blue')
# plt.plot(time, signal, color='green')
# plt.legend()
# plt.grid(True)

# # Adjust layout to prevent overlap
# plt.tight_layout()
# # Show the plots
# plt.show()
