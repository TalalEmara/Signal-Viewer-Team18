from PyQt5.QtCore import QObject, pyqtSignal 
from PyQt5.QtWidgets import QApplication
from matplotlib.animation import FuncAnimation
import numpy as np
import sys

class Plotting(QObject):
    rewind_state_changed = pyqtSignal(bool)

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.animation = None
        self.is_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.data_list = []  
        self.rewind_enabled = False 
        self.canvas.mpl_connect('scroll_event', self.on_scroll) 

    def init_plot(self, data_list):
        self.data_list = data_list
        self.total_frames = max(len(data['x_data']) for data in data_list)

        self.canvas.ax.clear()  # Clear the previous plots

        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_cine_mode,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )
        self.canvas.draw()


    def animate_cine_mode(self, i):
        self.current_frame = i
        self.canvas.ax.clear()

        # Determine the minimum and maximum x values for the current window
        window_size = 20  # Number of data points to show at once
        x_min, x_max = None, None

        for idx, data in enumerate(self.data_list):
            time = data['x_data']
            amplitude = data['y_data']
            self.canvas.ax.plot(time[:i + 1], amplitude[:i + 1], label=f'Signal {idx + 1}')

            # Update x_min and x_max based on the data range in this window
            if i < window_size:
                x_min, x_max = time[0], time[window_size] if x_max is None else max(x_max, time[window_size])
            else:
                x_min, x_max = time[i - window_size], time[i]

        # Set consistent x-axis limits for all signals
        self.canvas.ax.set_xlim(x_min, x_max)

        # Define the number of ticks and set the x-ticks with spacing
        num_ticks = 10
        tick_positions = np.linspace(x_min, x_max, num_ticks)
        self.canvas.ax.set_xticks(tick_positions)

        # # Optionally format the tick labels for better readability
        # self.canvas.ax.set_xticklabels([f'{pos:.2f}' for pos in tick_positions])

        self.canvas.draw()


        # Check if it's the last frame
        if i == self.total_frames - 1:
            if self.rewind_enabled:
                self.reset_animation()
            else:
                # If rewind is not enabled, check if the button was pressed after animation finished
                if not self.is_paused:
                    self.is_paused = True  # Pause if rewind is not enabled

    def reset_animation(self):
        self.current_frame = 0  
        self.is_paused = False  
        self.animation.event_source.stop()  
        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_cine_mode,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )
        self.animation.event_source.start()

    def on_slider_change(self, value):
        """Handle slider value change."""
        # Assuming x_data is in the range of 0 to 10
        x_data_range = self.canvas.ax.get_xlim()[1] - self.canvas.ax.get_xlim()[0]
        new_xlim = [value, value + x_data_range]
        self.canvas.ax.set_xlim(new_xlim)
        self.canvas.draw_idle()  # Update the canvas

    def pause(self):
        self.is_paused = True
        if self.animation:
            self.animation.event_source.stop()

    def play(self):
        self.is_paused = False
        if self.animation:
            self.animation.event_source.start()

    def to_start(self):
        current_ylim = self.canvas.ax.get_ylim()
        self.canvas.ax.set_xlim([0, 0])  
        self.canvas.ax.set_ylim(current_ylim)  
        self.canvas.draw() 

    def to_end(self):
        current_ylim = self.canvas.ax.get_ylim()
        self.canvas.ax.set_xlim([10, 10])  
        self.canvas.ax.set_ylim(current_ylim) 
        self.canvas.draw()

    def toggle_rewind(self, checked):
        self.rewind_enabled = checked
        self.rewind_state_changed.emit(checked)

       
        if self.rewind_enabled and self.current_frame == self.total_frames - 1:
            self.reset_animation()

    def update_canvas(self, canvas, t, signal):
        canvas.update_plot(t, signal)

    def update_plot(self, frame):
        if not self.is_paused:
            if self.rewind_enabled:
                self.current_frame = (frame + 1) % self.total_frames
            else:
                self.current_frame = frame
                if self.current_frame >= self.total_frames - 1:  
                    self.is_paused = True

        # Ensure self.signals_widget and its canvas are initialized
        if hasattr(self, 'signals_widget') and hasattr(self.signals_widget, 'canvas'):
            self.signals_widget.canvas.update_plot(self.data_list[0]['x_data'][:self.current_frame], 
                                                    self.data_list[0]['y_data'][:self.current_frame])


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

    def on_scroll(self, event):
        if event.inaxes == self.canvas.ax:
            # Get current y-axis limits
            r_min, r_max = self.canvas.ax.get_ylim()

            # Define a zoom factor
            zoom_factor = 0.2
            if event.button == 'up':  # Zoom in
                r_min *= (1 - zoom_factor)
                r_max *= (1 - zoom_factor)
            elif event.button == 'down':  # Zoom out
                r_min *= (1 + zoom_factor)
                r_max *= (1 + zoom_factor)

            # Ensure y limits are valid
            r_min = max(r_min, 0)  # Prevent going below 0
            if self.data_list:  # Check if there's data available
                y_data = np.concatenate([data['y_data'] for data in self.data_list])
                r_max = min(r_max, np.max(y_data) * 1.5)  # Use the maximum y value from the data

            # Set the new limits if valid
            if r_min < r_max:
                self.canvas.ax.set_ylim(r_min, r_max)
                self.canvas.draw_idle()  # Update the canvas

    def reset_zoom(self):
        if self.data is not None:
            r_min = np.min(self.data[:, 1])
            r_max = np.max(self.data[:, 1]) * 1.1
            self.canvas.ax.set_ylim(r_min, r_max)
            self.canvas.draw()