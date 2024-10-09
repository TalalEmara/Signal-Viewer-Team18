import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QToolButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        # Add a zoom out button
        self.zoom_out_button = QToolButton(self)
        self.zoom_out_button.setIcon(QIcon('photos/zoomOut.png'))  # Path to your zoom out icon
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.addWidget(self.zoom_out_button)

    def zoom_out(self):
        """Zoom out the plot."""
        xlim = self.canvas.ax.get_xlim()
        ylim = self.canvas.ax.get_ylim()
        # Zoom out by a factor of 1.5
        self.canvas.ax.set_xlim([xlim[0] - (xlim[1] - xlim[0]) * 0.5, xlim[1] + (xlim[1] - xlim[0]) * 0.5])
        self.canvas.ax.set_ylim([ylim[0] - (ylim[1] - ylim[0]) * 0.5, ylim[1] + (ylim[1] - ylim[0]) * 0.5])
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define initial x-axis and y-axis limits
        self.initial_xlim = [0, 10]  # Adjusted initial x limit
        self.initial_ylim = [-2, 2]

        # Create a canvas to hold the plot
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.init_plot()

        # Create a customized toolbar for zooming and panning
        self.toolbar = CustomToolbar(self.canvas, self)

        # Create a Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_signal)

        # Layout to arrange widgets
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)  # Add toolbar to the layout
        layout.addWidget(self.canvas)
        layout.addWidget(self.stop_button)  # Add stop button to the layout

        # Set the central widget with layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Start the animation (real-time plot)
        self.running = True
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, interval=100, blit=False)

        # Initialize variables for dragging
        self.dragging = False
        self.last_mouse_pos = None

        # Connect mouse events
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def init_plot(self):
        """ Initialize the plot with the first signal """
        t = np.linspace(0, 10, 100)  # Adjusted time range
        self.signal_line, = self.canvas.ax.plot(t, self.generate_signal(t))
        self.canvas.ax.set_xlim(self.initial_xlim)
        self.canvas.ax.set_ylim(self.initial_ylim)

    def generate_signal(self, t):
        """ Generate synthetic noisy signal """
        return np.sin(2 * np.pi * t) + 0.5 * np.random.normal(size=len(t))

    def update_plot(self, frame):
        """ Update plot in real-time """
        if self.running:
            t_new = np.linspace(frame, frame + 10, 100)  # Keep within 10 seconds
            y_new = self.generate_signal(t_new)

            # Update line with new data
            self.signal_line.set_data(t_new, y_new)

            # Keep the limits up to date (use pan/zoom to control manually)
            self.canvas.ax.set_xlim(t_new[0], t_new[-1])
            self.canvas.draw()

    def stop_signal(self):
        """ Stop the real-time updating of the plot """
        self.running = False

    def on_press(self, event):
        """ Handle mouse press event """
        if event.button == 1:  # Left mouse button
            self.dragging = True
            self.last_mouse_pos = event.xdata

    def on_release(self, event):
        """ Handle mouse release event """
        self.dragging = False
        self.last_mouse_pos = None

    def on_motion(self, event):
        """ Handle mouse motion event """
        if self.dragging and event.xdata is not None:
            # Calculate how far to drag
            dx = event.xdata - self.last_mouse_pos
            new_xlim = self.canvas.ax.get_xlim()
            new_xlim[0] += dx
            new_xlim[1] += dx

            # Prevent dragging below zero
            if new_xlim[0] < 0:
                new_xlim[0] = 0
                new_xlim[1] = new_xlim[0] + (self.initial_xlim[1] - self.initial_xlim[0])  # Keep the width constant

            self.canvas.ax.set_xlim(new_xlim)
            self.last_mouse_pos = event.xdata  # Update last position
            self.canvas.draw()

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
