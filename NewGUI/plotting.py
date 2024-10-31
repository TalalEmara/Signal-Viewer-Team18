# from PyQt5.QtCore import QObject, pyqtSignal
# from PyQt5.QtWidgets import QApplication
# from matplotlib.animation import FuncAnimation
# import numpy as np
# import sys

# class Plotting(QObject):
#     rewind_state_changed = pyqtSignal(bool)

#     def _init_(self, canvas):
#         super()._init_()
#         self.canvas = canvas
#         self.animation = None
#         self.is_paused = False
#         self.current_frame = 0
#         self.total_frames = 0
#         self.data_list = []
#         self.rewind_enabled = False
#         self.canvas.mpl_connect('scroll_event', self.on_scroll)

#     def init_plot(self, data_list):
#         self.data_list = data_list
#         self.total_frames = len(data_list[0]['x_data'])

#         self.animation = FuncAnimation(
#             self.canvas.figure,
#             self.animate_cine_mode,
#             frames=self.total_frames,
#             interval=100,
#             repeat=False
#         )

#     def animate_cine_mode(self, i):
#         self.current_frame = i
#         self.canvas.ax.clear()

#         # Determine the minimum and maximum x values for the current window
#         window_size = 20  # Number of data points to show at once
#         x_min, x_max = None, None

#         for idx, data in enumerate(self.data_list):
#             time = data['x_data']
#             amplitude = data['y_data']
#             self.canvas.ax.plot(time[:i + 1], amplitude[:i + 1], label=f'Signal {idx + 1}')

#             # Update x_min and x_max based on the data range in this window
#             if i < window_size:
#                 x_min, x_max = time[0], time[window_size] if x_max is None else max(x_max, time[window_size])
#             else:
#                 x_min, x_max = time[i - window_size], time[i]

#         # Set consistent x-axis limits for all signals
#         self.canvas.ax.set_xlim(x_min, x_max)

#         # Define the number of ticks and set the x-ticks with spacing
#         num_ticks = 10
#         tick_positions = np.linspace(x_min, x_max, num_ticks)
#         self.canvas.ax.set_xticks(tick_positions)

#         # Optionally format the tick labels for better readability
#         self.canvas.ax.set_xticklabels([f'{pos:.2f}' for pos in tick_positions])

#         self.canvas.draw()

#         # Check if it's the last frame
#         if i == self.total_frames - 1:
#             if self.rewind_enabled:
#                 self.reset_animation()
#             else:
#                 # If rewind is not enabled, check if the button was pressed after animation finished
#                 if not self.is_paused:
#                     self.is_paused = True  # Pause if rewind is not enabled

#     def reset_animation(self):
#         self.current_frame = 0
#         self.is_paused = False
#         self.animation.event_source.stop()
#         self.animation = FuncAnimation(
#             self.canvas.figure,
#             self.animate_cine_mode,
#             frames=self.total_frames,
#             interval=100,
#             repeat=False
#         )
#         self.animation.event_source.start()

#     def on_slider_change(self, value):
#         """Handle slider value change."""
#         # Assuming x_data is in the range of 0 to 10
#         x_data_range = self.canvas.ax.get_xlim()[1] - self.canvas.ax.get_xlim()[0]
#         new_xlim = [value, value + x_data_range]
#         self.canvas.ax.set_xlim(new_xlim)
#         self.canvas.draw_idle()  # Update the canvas

#     def pause(self):
#         self.is_paused = True
#         if self.animation:
#             self.animation.event_source.stop()

#     def play(self):
#         self.is_paused = False
#         if self.animation:
#             self.animation.event_source.start()

#     def to_start(self):
#         current_ylim = self.canvas.ax.get_ylim()
#         self.canvas.ax.set_xlim([0, 0])
#         self.canvas.ax.set_ylim(current_ylim)
#         self.canvas.draw()

#     def to_end(self):
#         current_ylim = self.canvas.ax.get_ylim()
#         self.canvas.ax.set_xlim([10, 10])
#         self.canvas.ax.set_ylim(current_ylim)
#         self.canvas.draw()

#     def toggle_rewind(self, checked):
#         self.rewind_enabled = checked
#         self.rewind_state_changed.emit(checked)


#         if self.rewind_enabled and self.current_frame == self.total_frames - 1:
#             self.reset_animation()

#     def update_canvas(self, canvas, t, signal):
#         canvas.update_plot(t, signal)

#     def update_plot(self, frame):
#         if not self.is_paused:
#             if self.rewind_enabled:
#                 self.current_frame = (frame + 1) % self.total_frames
#             else:
#                 self.current_frame = frame
#                 if self.current_frame >= self.total_frames - 1:
#                     self.is_paused = True

#         # Ensure self.signals_widget and its canvas are initialized
#         if hasattr(self, 'signals_widget') and hasattr(self.signals_widget, 'canvas'):
#             self.signals_widget.canvas.update_plot(self.data_list[0]['x_data'][:self.current_frame],
#                                                     self.data_list[0]['y_data'][:self.current_frame])


#     def get_current_data(self):
#         """Return the currently visible x and y data based on the x-axis limits."""
#         if self.canvas.ax:
#             x_min, x_max = self.canvas.ax.get_xlim()  # Get current x-axis limits
#             current_x_data = self.data_list[0]['x_data']
#             current_y_data = self.data_list[0]['y_data']

#             # Get indices of x data that fall within the current x limits
#             indices = np.where((current_x_data >= x_min) & (current_x_data <= x_max))[0]

#             # Return the corresponding x and y data
#             return current_x_data[indices], current_y_data[indices]

#         return None, None  # No data available yet

#     def on_scroll(self, event):
#         if event.inaxes == self.canvas.ax:
#             # Get current y-axis limits
#             r_min, r_max = self.canvas.ax.get_ylim()

#             # Define a zoom factor
#             zoom_factor = 0.2
#             if event.button == 'up':  # Zoom in
#                 r_min *= (1 - zoom_factor)
#                 r_max *= (1 - zoom_factor)
#             elif event.button == 'down':  # Zoom out
#                 r_min *= (1 + zoom_factor)
#                 r_max *= (1 + zoom_factor)

#             # Ensure y limits are valid
#             r_min = max(r_min, 0)  # Prevent going below 0
#             if self.data_list:  # Check if there's data available
#                 y_data = np.concatenate([data['y_data'] for data in self.data_list])
#                 r_max = min(r_max, np.max(y_data) * 1.5)  # Use the maximum y value from the data

#             # Set the new limits if valid
#             if r_min < r_max:
#                 self.canvas.ax.set_ylim(r_min, r_max)
#                 self.canvas.draw_idle()  # Update the canvas

#     def reset_zoom(self):
#         if self.data is not None:
#             r_min = np.min(self.data[:, 1])
#             r_max = np.max(self.data[:, 1]) * 1.1
#             self.canvas.ax.set_ylim(r_min, r_max)
#             self.canvas.draw()


from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QLabel
import numpy as np


class Plotting(QObject):
    rewind_state_changed = pyqtSignal(bool)

    def __init__(self, canvas, timer_label: QLabel):
        super().__init__()
        self.canvas = canvas
        self.ax = self.canvas.ax
        self.timer_label = timer_label

        # Real-time data and animation attributes
        self.animation_timer = QTimer()
        self.is_paused = False
        self.current_frame = 0
        self.window_size_x = 10
        self.interval = 50  # Time in milliseconds between frames
        self.rewind_enabled = False
        self.data_list = []

        # Panning attributes
        self.dragging = False
        self.start_press_event = None
        self.previous_state_was_playing = False  # New attribute to track previous state


        # Zoom attributes
        self.default_window_size_x = self.window_size_x
        self.zoom_value = 50  # Default zoom value
        self.current_zoom_x = self.default_window_size_x

        # Connect timer to update function and start animation
        self.animation_timer.timeout.connect(self.update_graph)
        self.animation_timer.start(self.interval)

        # Timer for resuming after zoom
        self.zoom_resume_timer = QTimer()
        self.zoom_resume_timer.setSingleShot(True)  # Run only once
        self.zoom_resume_timer.timeout.connect(self.play)  # Connect to play method

        # Enable scroll event for zooming on y-axis
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

    def init_plot(self, data_list):
        self.data_list = data_list
        self.total_frames = len(data_list[0]['x_data']) if data_list else 0
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.ax.clear()
        self.ax.set_xlim(0, self.window_size_x)
        self.ax.set_ylim(-1.5, 1.5)
        self.canvas.draw()

    def on_slider_change(self, value):
        """Handle slider value change."""
        # Calculate the new x-axis limits based on the slider value
        x_data_range = self.canvas.ax.get_xlim()[1] - self.canvas.ax.get_xlim()[0]
        new_xlim = [value, value + x_data_range]
        self.canvas.ax.set_xlim(new_xlim)
        self.canvas.draw_idle()  # Update the canvas

    def update_graph(self):
        if not self.is_paused and self.data_list:
            # Increment the current frame
            self.current_frame += 1

            # Check if current_frame exceeds the total frames
            if self.current_frame >= self.total_frames:
                if self.rewind_enabled:
                    self.current_frame = 0
                else:
                    self.current_frame = self.total_frames - 1  # Prevent going out of bounds
                    self.animation_timer.stop()

            self.update_plot(self.current_frame)
            self.update_timer_label()

    def update_plot(self, frame):
        """Update plot data for the current frame."""
        self.ax.clear()

        # Ensure frame does not exceed the total length
        frame = min(frame, self.total_frames - 1)

        for idx, data in enumerate(self.data_list):
            x_data, y_data = data['x_data'], data['y_data']

            # Determine x-axis limits, clamping x_min to 0 if it goes negative
            if frame < self.window_size_x:
                x_min, x_max = max(0, x_data[0]), x_data[min(frame, len(x_data) - 1)]
            else:
                x_min, x_max = max(0, x_data[frame - self.window_size_x]), x_data[frame]

            # Set y-axis limits based on the visible portion of the data up to the current frame
            visible_y_data = y_data[:frame + 1]
            y_min = np.min(visible_y_data) * 1.1
            y_max = np.max(visible_y_data) * 1.1

            # Plot the data for the current frame and set axis limits
            self.ax.plot(x_data[:frame + 1], y_data[:frame + 1], label=f'Signal {idx + 1}')
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)

        self.ax.legend()
        self.canvas.draw_idle()

    def update_timer_label(self):
        """Update the timer label with the current time."""
        if self.data_list and self.current_frame < len(self.data_list[0]['x_data']):
            current_time = self.data_list[0]['x_data'][self.current_frame]
            self.timer_label.setText(f"Time: {current_time:.2f} s")

    # def on_scroll(self, event):
    #     """Zoom y-axis with mouse scroll."""
    #     # Pause the animation when zooming
    #     self.pause()
    #
    #     y_min, y_max = self.ax.get_ylim()
    #     zoom_factor = 0.2
    #     if event.button == 'up':
    #         y_min, y_max = y_min * (1 - zoom_factor), y_max * (1 - zoom_factor)
    #     elif event.button == 'down':
    #         y_min, y_max = y_min * (1 + zoom_factor), y_max * (1 + zoom_factor)
    #
    #     y_data = np.concatenate([data['y_data'] for data in self.data_list])
    #     self.ax.set_ylim(max(y_min, np.min(y_data) * 1.1), min(y_max, np.max(y_data) * 1.1))
    #
    #     self.canvas.draw_idle()
    #
    #     # Resume the animation after zooming
    #     self.play()
    def set_zoom_x(self, value):
        """Set zoom level for the x-axis."""
        zoom_ratio = value / self.zoom_value
        self.zoom_graph_x(zoom_ratio)
        self.zoom_value = value  # Update zoom_value to the current one

    def zoom_graph_x(self, zoom_ratio):
        """Zoom x-axis based on the zoom ratio."""
        # Calculate the current x-axis limits
        x_min, x_max = self.ax.get_xlim()
        x_center = (x_min + x_max) / 2

        # Calculate the new limits based on zooming in or out
        new_width = (x_max - x_min) / zoom_ratio
        self.current_xlim = [x_center - new_width / 2, x_center + new_width / 2]

        # Set new x-axis limits
        self.ax.set_xlim(self.current_xlim)
        self.canvas.draw_idle()

    def on_press(self, event):
        """Handle mouse press event for panning."""
        if event.inaxes == self.canvas.ax:
            self.dragging = True
            self.start_press_event = event.xdata

            # Track whether the graph was playing before the drag started
            self.previous_state_was_playing = not self.is_paused

            # Pause the animation when starting to pan
            self.pause()

    def on_release(self, event):
        """Handle mouse release event for panning."""
        self.dragging = False

        # Only resume the animation if it was playing before the pan started
        if self.previous_state_was_playing:
            self.play()  # Resume if the graph was playing

    def on_scroll(self, event):
        """Zoom y-axis with mouse scroll and pause the animation for 2 seconds."""
        if event.inaxes == self.ax:
            self.pause_for_zoom()

            y_min, y_max = self.ax.get_ylim()
            zoom_factor = 0.2

            if event.button == 'up':
                y_min, y_max = y_min * (1 - zoom_factor), y_max * (1 - zoom_factor)
            elif event.button == 'down':
                y_min, y_max = y_min * (1 + zoom_factor), y_max * (1 + zoom_factor)

            # Adjust y limits while ensuring it stays within data bounds
            y_data = np.concatenate([data['y_data'] for data in self.data_list])
            self.ax.set_ylim(max(y_min, np.min(y_data) * 1.1), min(y_max, np.max(y_data) * 1.1))
            self.canvas.draw_idle()

    def pause_for_zoom(self):
        """Pause the graph, wait for 2 seconds, then resume."""
        self.pause()  # Pause the animation
        self.zoom_resume_timer.start(2000)  # Start the timer to resume after 2 seconds

    def on_motion(self, event):
        """Handle mouse motion event for panning."""
        if self.dragging and event.inaxes == self.canvas.ax:
            # Calculate the amount to pan
            dx = event.xdata - self.start_press_event
            self.start_press_event = event.xdata  # Update the starting point for the next movement
            xlim = self.canvas.ax.get_xlim()
            self.canvas.ax.set_xlim([xlim[0] - dx, xlim[1] - dx])
            self.canvas.draw_idle()  # Update the canvas
    def play(self):
        self.is_paused = False
        self.animation_timer.start()

    def pause(self):
        self.is_paused = True
        self.animation_timer.stop()

    def reset_animation(self):
        self.current_frame = 0
        self.update_plot(self.current_frame)
        self.animation_timer.start()

    def toggle_rewind(self, enabled):
        self.rewind_enabled = enabled

        if enabled and self.current_frame >= self.total_frames - 1:  # Animation has stopped at the end
            self.current_frame = 0  # Reset to the beginning
            self.update_plot(self.current_frame)  # Update the plot to show the reset state
        self.rewind_state_changed.emit(enabled)

    def get_current_data(self):
        """Return the currently visible x and y data based on the x-axis limits."""
        if self.canvas.ax:
            x_min, x_max = self.canvas.ax.get_xlim()  # Get current x-axis limits
            current_x_data = self.data_list[0]['x_data']
            current_y_data = self.data_list[0]['y_data']

            # Get indices of x data that fall within the current x limits
            indices = np.where((current_x_data >= x_min) & (current_x_data <= x_max))[0]

            # Return the corresponding x and y data
            return current_x_data[indices], current_y_data[indices]

        return None, None  # No data available yet




