from PyQt5.QtCore import QObject, pyqtSignal
from matplotlib.animation import FuncAnimation

class Plotting(QObject):
   
    plot_selected = pyqtSignal(int, str, int, int)  

    def __init__(self, canvas, plot_data_list=None):
        super().__init__()
        self.canvas = canvas
        self.plot_data_list = plot_data_list if plot_data_list else []
        self.animations = [] 
        self.is_paused = False
        self.selected_plot_index = None

        if self.plot_data_list:
            self.init_plot(self.plot_data_list)

    def init_plot(self, plot_data_list):
        for index, plot_data in enumerate(plot_data_list):
            x_data = plot_data['x_data']
            y_data = plot_data['y_data']
            color = plot_data.get('color', '#D55877')
            thickness = plot_data.get('thickness', 2)

            self.canvas.add_line(x_data, y_data, color=color, linewidth=thickness)

            speed = plot_data.get('speed', 100)  # Default speed is 100ms per frame
            anim = FuncAnimation(self.canvas.figure, self.animate_line,
                                 frames=len(x_data), interval=speed, repeat=True,
                                 fargs=(index, x_data, y_data))
            self.animations.append(anim)

    def select_plot(self, index):
        
        self.selected_plot_index = index
        plot_data = self.plot_data_list[index]
        self.plot_selected.emit(index, plot_data['color'], plot_data['thickness'], plot_data['speed'])

    def update_plot_properties(self, index, color, thickness, speed):
        
        self.plot_data_list[index]['color'] = color
        self.plot_data_list[index]['thickness'] = thickness
        self.plot_data_list[index]['speed'] = speed
        self.canvas.update_line(index, self.plot_data_list[index]['x_data'], 
                                self.plot_data_list[index]['y_data'], color=color, linewidth=thickness)
        self.animations[index].event_source.interval = speed

    def animate_line(self, i, line_index, x_data, y_data):
        
        if not self.is_paused:
            self.canvas.update_line(line_index, x_data[:i], y_data[:i])

    def play(self):
       
        self.is_paused = False
        for anim in self.animations:
            anim.event_source.start()

    def pause(self):
       
        self.is_paused = True
        for anim in self.animations:
            anim.event_source.stop()
        anim.event_source.stop()

    def to_start(self):
       
        self.current_frame = 0
        for index, plot_data in enumerate(self.plot_data_list):
            x_data = plot_data['x_data']
            y_data = plot_data['y_data']
            self.canvas.update_line(index, x_data[:1], y_data[:1])
        self.pause()  

    def to_end(self):
        
        for index, plot_data in enumerate(self.plot_data_list):
            x_data = plot_data['x_data']
            y_data = plot_data['y_data']
            self.current_frame = len(x_data) - 1
            self.canvas.update_line(index, x_data, y_data)
        self.pause() 

    def toggle_rewind(self):
       
        self.rewind_enabled = not self.rewind_enabled


