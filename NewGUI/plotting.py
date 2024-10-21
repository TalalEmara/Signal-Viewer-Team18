from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from matplotlib.animation import FuncAnimation
import sys

from NewCore.live_signals import Live_signal_processing


# class Plotting(QObject):
#     plot_selected = pyqtSignal(int, str, int, int)
#
#     def __init__(self, canvas, plot_data_list=None):
#         super().__init__()
#         self.canvas = canvas
#         self.plot_data_list = plot_data_list if plot_data_list else []
#         self.animations = []
#         self.is_paused = False
#         self.selected_plot_index = None
#
#         if self.plot_data_list:
#             self.init_plot(self.plot_data_list)
#
#     def init_plot(self, plot_data_list):
#         for index, plot_data in enumerate(plot_data_list):
#             self.add_plot(plot_data['x_data'], plot_data['y_data'],
#                           color=plot_data.get('color', '#D55877'),
#                           thickness=plot_data.get('thickness', 2),
#                           speed=plot_data.get('speed', 100))
#
#     def add_plot(self, x_data, y_data, color='#D55877', thickness=2, speed=100):
#         """
#         Adds a new plot with the specified x and y data, color, thickness, and animation speed.
#         """
#         plot_data = {
#             'x_data': x_data,
#             'y_data': y_data,
#             'color': color,
#             'thickness': thickness,
#             'speed': speed
#         }
#         self.plot_data_list.append(plot_data)
#
#         # Plot the data on the canvas
#         self.canvas.add_line(x_data, y_data, color=color, linewidth=thickness)
#
#         # Create an animation for the new plot
#         anim = FuncAnimation(self.canvas.figure, self.animate_line,
#                              frames=len(x_data), interval=speed, repeat=True,
#                              fargs=(len(self.plot_data_list) - 1, x_data, y_data))
#         self.animations.append(anim)
#
#     def select_plot(self, index):
#         self.selected_plot_index = index
#         plot_data = self.plot_data_list[index]
#         self.plot_selected.emit(index, plot_data['color'], plot_data['thickness'], plot_data['speed'])
#
#     def update_plot_properties(self, index, color, thickness, speed):
#         self.plot_data_list[index]['color'] = color
#         self.plot_data_list[index]['thickness'] = thickness
#         self.plot_data_list[index]['speed'] = speed
#         self.canvas.update_line(index, self.plot_data_list[index]['x_data'],
#                                 self.plot_data_list[index]['y_data'], color=color, linewidth=thickness)
#         self.animations[index].event_source.interval = speed
#
#     def animate_line(self, i, line_index, x_data, y_data):
#         if not self.is_paused:
#             self.canvas.update_line(line_index, x_data[:i], y_data[:i])
#
#     def play(self):
#         self.is_paused = False
#         for anim in self.animations:
#             anim.event_source.start()
#
#     def pause(self):
#         self.is_paused = True
#         for anim in self.animations:
#             anim.event_source.stop()
#
#     def to_start(self):
#         self.current_frame = 0
#         for index, plot_data in enumerate(self.plot_data_list):
#             x_data = plot_data['x_data']
#             y_data = plot_data['y_data']
#             self.canvas.update_line(index, x_data[:1], y_data[:1])
#         self.pause()
#
#     def to_end(self):
#         for index, plot_data in enumerate(self.plot_data_list):
#             x_data = plot_data['x_data']
#             y_data = plot_data['y_data']
#             self.current_frame = len(x_data) - 1
#             self.canvas.update_line(index, x_data, y_data)
#         self.pause()
#
#     def toggle_rewind(self):
#         self.rewind_enabled = not self.rewind_enabled
# from PyQt5.QtCore import QObject
# from matplotlib.animation import FuncAnimation
# import numpy as np
#
# class Plotting(QObject):
#     def __init__(self, canvas):
#         super().__init__()
#         self.canvas = canvas
#         self.animation = None
#         self.is_paused = False
#         self.rewind_enabled = False
#         self.current_frame = 0
#         self.total_frames = 0
#         self.time = None
#         self.amplitude = None
#
#     def init_plot(self, time, amplitude):
#         """
#         Initializes the plot for the given signal data (time and amplitude).
#         Parameters:
#         - time: Array-like, the x-axis data.
#         - amplitude: Array-like, the y-axis data.
#         """
#         self.total_frames = len(time)
#         self.time = time
#         self.amplitude = amplitude
#
#         # Initialize the canvas with the first frame of data
#         self.canvas.update_plot(time, amplitude)
#
#         # Create the animation for the plot
#         self.animation = FuncAnimation(
#             self.canvas.figure,
#             self.animate_cine_mode,
#             frames=self.total_frames,
#             interval=100,
#             repeat=False
#         )
#
#     def animate_cine_mode(self, i):
#         """
#         Animate the signal in cine mode by looping over the data.
#         """
#         # Display the entire signal
#         self.canvas.update_plot(self.time[:i + 1], self.amplitude[:i + 1])
#
#     def pause(self):
#         """
#         Pauses the animation.
#         """
#         self.is_paused = True
#         if self.animation:
#             self.animation.event_source.stop()
#
#     def play(self):
#         """
#         Resumes the animation.
#         """
#         self.is_paused = False
#         if self.animation:
#             self.animation.event_source.start()
#
#     def to_start(self):
#         """
#         Resets the plot to the beginning.
#         """
#         self.current_frame = 0
#         self.canvas.update_plot(self.time[:1], self.amplitude[:1])
#         self.pause()
#
#     def to_end(self):
#         """
#         Sets the plot to the end.
#         """
#         self.current_frame = self.total_frames - 1
#         self.canvas.update_plot(self.time, self.amplitude)
#         self.pause()
from PyQt5.QtCore import QObject
from matplotlib.animation import FuncAnimation
import numpy as np

class Plotting(QObject):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.animation = None
        self.is_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.data_list = []  # List to hold multiple datasets

    def init_plot(self, data_list):
        """
        Initializes the plot for the given signal data.
        Parameters:
        - data_list: List of dictionaries containing 'time' and 'amplitude' for each signal.
        """
        self.data_list = data_list
        self.total_frames = len(data_list[0]['x_data'])  # Assuming all signals have the same length

        # Initialize the canvas with the first frame of data for all signals
        self.update_plot()

        # Create the animation for the plot
        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_cine_mode,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )

    def animate_cine_mode(self, i):
        """
        Animate all signals in cine mode by looping over the data.
        """
        # Clear the current axes
        self.canvas.ax.clear()

        # Plot all signals for the current frame
        for idx, data in enumerate(self.data_list):
            time = data['x_data']
            amplitude = data['y_data']
            self.canvas.ax.plot(time[:i + 1], amplitude[:i + 1], label=f'Signal {idx + 1}')

        # Update the canvas
        self.canvas.draw()

    def plot_live_signal(self, x_data, y_data):
        """
        Updates the existing plot with live signal data.
        Parameters:
        - x_data: Array-like, the x-axis data (time).
        - y_data: Array-like, the y-axis data (amplitude).
        """
        self.x_data = x_data  # Store the live signal's x_data
        self.y_data = y_data  # Store the live signal's y_data
        self.total_frames = len(x_data)  # Set total frames based on x_data length

        # Create the animation for the live plot
        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_live_signal,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )

    def animate_live_signal(self, i):
        """
        Animate the live signal by plotting the time series data.
        Parameters:
        - i: Current frame index.
        """
        # Clear the current axes
        self.canvas.ax.clear()

        # Plot the current frame of the live signal
        self.canvas.ax.plot(self.x_data[:i + 1], self.y_data[:i + 1], label='Live Signal')

        # Set x-ticks to display every minute, but do not limit the x-axis
        # Set x-ticks only if there are enough frames
        if self.total_frames > 60:
            minute_ticks = np.arange(0, self.total_frames, 60)  # Ticks for every minute
            minute_labels = [f'Minute {j}' for j in range(len(minute_ticks))]
            self.canvas.ax.set_xticks(minute_ticks)  # Set x-ticks
            self.canvas.ax.set_xticklabels(minute_labels)  # Set x-tick labels

        # Set the x-axis limits to adapt to the current frame
        self.canvas.ax.set_xlim(0, self.total_frames)  # Dynamic x-axis limits

        # Label the axes
        self.canvas.ax.set_xlabel('Time (Frames)')  # Changed from 'Time (Minutes)'
        self.canvas.ax.set_ylabel('KP Values')

        # Add a legend
        self.canvas.ax.legend()

        # Update the canvas
        self.canvas.draw()

    def pause(self):
        """
        Pauses the animation.
        """
        self.is_paused = True
        if self.animation:
            self.animation.event_source.stop()

    def play(self):
        """
        Resumes the animation.
        """
        self.is_paused = False
        if self.animation:
            self.animation.event_source.start()

    def to_start(self):
        """
        Resets the plot to the beginning.
        """
        self.current_frame = 0
        self.update_plot()  # Show only the first frame of all signals
        self.pause()

    def to_end(self):
        """
        Sets the plot to the end.
        """
        self.current_frame = self.total_frames - 1
        self.update_plot()  # Show the full signals
        self.pause()

    def update_plot(self):
        """
        Updates the plot with the current frame for all datasets.
        """
        self.animate_cine_mode(self.current_frame)  # Update plot for current frame
