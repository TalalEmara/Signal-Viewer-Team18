from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from matplotlib.animation import FuncAnimation
import sys
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle

  

from PyQt5.QtCore import QObject
from matplotlib.animation import FuncAnimation
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib.animation import FuncAnimation
import numpy as np

class Plotting(QObject):
    rewind_state_changed = pyqtSignal(bool)

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.animation = None
        self.is_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.data_list = []  # List of signal data
        self.x_data = []  # X-axis data
        self.y_data = []  # Y-axis data
        self.rewind_enabled = False  # Flag for rewind mode

    def init_plot(self, data_list):
        """ Initializes the plot for the given signal data. """
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


        for idx, data in enumerate(self.data_list):
            time = data['x_data']
            amplitude = data['y_data']
            self.canvas.ax.plot(time[:i + 1], amplitude[:i + 1], label=f'Signal {idx + 1}')

        self.canvas.draw()

        if i == self.total_frames - 1:
            if self.rewind_enabled:
                self.reset_animation()  
            else:
                self.animation.event_source.stop()  

         # Check if it is the last frame for live signal
        if i == self.total_frames - 1 and self.rewind_enabled:
            self.reset_animation()  # Reset live animation if rewind is enabled


    def reset_animation(self):
        """ Resets the animation back to the first frame and restarts it. """
        self.current_frame = 0  # Reset to the first frame
        if self.animation:
            self.animation.event_source.stop()  # Stop current animation

        # Restart the animation from the first frame
        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_cine_mode,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )
        self.animation.event_source.start()  # Start the new animation

    def pause(self):
        """ Pause the current animation. """
        self.is_paused = True
        if self.animation:
            self.animation.event_source.stop()

    def play(self):
        """ Resume the current animation. """
        self.is_paused = False
        if self.animation:
            self.animation.event_source.start()

    def to_start(self):
        """ Reset the animation to the first frame and pause it. """
        self.current_frame = 0  # Reset frame
        self.update_plot()  # Update plot with the first frame
        self.pause()  # Pause the animation

    def to_end(self):
        """ Jump to the last frame and pause the animation. """
        self.current_frame = self.total_frames - 1  # Jump to the last frame
        self.update_plot()  # Update plot with the last frame
        self.pause()  # Pause the animation

    def toggle_rewind(self, checked):
        """ Toggle rewind mode. """
        self.rewind_enabled = checked
        self.rewind_state_changed.emit(checked)

        # If rewind is enabled and we're at the last frame, restart the animation
        if self.rewind_enabled and self.current_frame == self.total_frames - 1:
            self.reset_animation()

    def update_plot(self):
        """ Update the plot from the current frame. """
        self.animate_cine_mode(self.current_frame)


    def plot_live_signal(self, x_data, y_data):
        """
        Plot live signal data. This method will create an animation for live data.
        """
        self.x_data = x_data  
        self.y_data = y_data  
        self.total_frames = len(x_data)

        # Create a new animation for live signal data
        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_live_signal,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )

    def animate_live_signal(self, i):
        """
        Animate live signal by plotting the data incrementally.
        """
        self.canvas.ax.clear()
        self.canvas.ax.plot(self.x_data[:i + 1], self.y_data[:i + 1], label='Live Signal')
        
        # Adjust x-axis if the total frames exceed a certain threshold (e.g., 60)
        if self.total_frames > 60:
            minute_ticks = np.arange(0, self.total_frames, 60)  
            minute_labels = [f'Minute {j}' for j in range(len(minute_ticks))]
            self.canvas.ax.set_xticks(minute_ticks)  
            self.canvas.ax.set_xticklabels(minute_labels)
        
        # Adjust the x-axis limit to keep displaying the incoming data
        self.canvas.ax.set_xlim(0, self.total_frames)
        self.canvas.ax.set_xlabel('Time (Frames)')
        self.canvas.ax.set_ylabel('KP Values')
        self.canvas.ax.legend()
        self.canvas.draw()

        # Check if it is the last frame for live signal
        if i == self.total_frames - 1 and self.rewind_enabled:
            self.reset_animation()  # Reset live animation if rewind is enabled
