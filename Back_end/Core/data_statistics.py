import statistics

def stat(signal):
    mean = statistics.mean(signal[1])          # Calculate mean
    maximum = max(signal[1])                   # Calculate max
    minimum = min(signal[1])                   # Calculate min
    std_dev = statistics.stdev(signal[1])      # Calculate standard deviation

    return [mean, maximum, minimum, std_dev]


signal = [[1, 3, 5, 6, 7], 
          [3, 4, 6, 2, 9]]

print(stat(signal))