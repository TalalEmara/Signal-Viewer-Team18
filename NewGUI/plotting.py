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

    def init_plot(self, data_list):
        self.data_list = data_list
        self.total_frames = len(data_list[0]['x_data'])  
      
        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_cine_mode,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )

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

        # Optionally format the tick labels for better readability
        self.canvas.ax.set_xticklabels([f'{pos:.2f}' for pos in tick_positions])

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
  