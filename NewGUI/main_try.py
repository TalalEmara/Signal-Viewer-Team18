import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget  
import numpy as np
from SignalViewer import Viewer
from right_panel import RightPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signal Viewer with Right Panel")
        self.setGeometry(100, 100, 1200, 600)

        # Example plot data
        x_data = np.linspace(0, 10, 1000)
        plot_data_list = [
            {'x_data': x_data, 'y_data': np.sin(x_data), 'color': '#FF5733', 'thickness': 2, 'speed': 50},
            {'x_data': x_data, 'y_data': np.cos(x_data), 'color': '#33FF57', 'thickness': 3, 'speed': 100},
            {'x_data': x_data, 'y_data': np.sin(2 * x_data), 'color': '#3357FF', 'thickness': 4, 'speed': 150}
        ]

       
        self.SignalViewer = Viewer(plot_data_list)

        
        self.right_panel = RightPanel()
        self.SignalViewer.set_right_panel(self.right_panel)

        
        self.viewer.plotting_instance.plot_selected.connect(self.right_panel.update_properties)
        self.right_panel.signal_properties_changed.connect(self.viewer.plotting_instance.update_plot_properties)

        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(self.SignalViewer, stretch=3)  
        main_layout.addWidget(self.right_panel, stretch=1)  

        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
