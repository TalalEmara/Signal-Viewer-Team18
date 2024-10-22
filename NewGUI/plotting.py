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

        for idx, data in enumerate(self.data_list):
            time = data['x_data']
            amplitude = data['y_data']
            self.canvas.ax.plot(time[:i + 1], amplitude[:i + 1], label=f'Signal {idx + 1}')

        # self.canvas.ax.set_xlim(min(self.data_list[0]['x_data']), max(self.data_list[0]['x_data']))
        # self.canvas.ax.set_ylim(min(np.min([data['y_data'] for data in self.data_list])), max(np.max([data['y_data'] for data in self.data_list])))
        self.canvas.draw()

        if i == self.total_frames - 1:
            if self.rewind_enabled:
                self.reset_animation()  
            else:
                self.animation.event_source.stop()

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
        self.current_frame = 0  
        self.update_plot() 
        self.pause()  

    def to_end(self):
        self.current_frame = self.total_frames - 1 
        self.update_plot() 
        self.pause() 

    def toggle_rewind(self, checked):
        self.rewind_enabled = checked
        self.rewind_state_changed.emit(checked)

        if self.rewind_enabled and self.current_frame == self.total_frames - 1:
            self.reset_animation()

    def update_plot(self):
        self.animate_cine_mode(self.current_frame)

    def plot_live_signal(self, x_data, y_data):
        self.x_data = x_data  
        self.y_data = y_data  
        self.total_frames = len(x_data)

        self.animation = FuncAnimation(
            self.canvas.figure,
            self.animate_live_signal,
            frames=self.total_frames,
            interval=100,
            repeat=False
        )

    def animate_live_signal(self, i):
        self.canvas.ax.clear()
        self.canvas.ax.plot(self.x_data[:i + 1], self.y_data[:i + 1], label='Live Signal')

        if self.total_frames > 60:
            minute_ticks = np.arange(0, self.total_frames, 60)  
            minute_labels = [f'Minute {j}' for j in range(len(minute_ticks))]
            self.canvas.ax.set_xticks(minute_ticks)  
            self.canvas.ax.set_xticklabels(minute_labels)

        self.canvas.ax.set_xlim(0, self.total_frames)
        self.canvas.ax.set_xlabel('Time (Frames)')
        self.canvas.ax.set_ylabel('KP Values')
        self.canvas.ax.legend()
        self.canvas.draw()

        if i == self.total_frames - 1 and self.rewind_enabled:
            self.reset_animation()  


