import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from SignalViewer import Viewer
from Core.Data_load import DataLoader
from selectorPanel import SelectorPanel  # Assuming you have a SelectorPanel class
from linkBar import ToolBar
from properties import Properties

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Load data from CSV
    csv_file_path = 'signals_data/ECG_Abnormal.csv'
    data_loader = DataLoader(csv_file_path)
    data_loader.load_data()

    # Get the loaded data
    data = data_loader.get_data()
    x_data = data[:, 0]
    y_data = data[:, 1]

    # Prepare two sets of plot data
    plot_data_list_1 = [{'x_data': x_data, 'y_data': y_data}]
    plot_data_list_2 = [{'x_data': np.linspace(0, 10, 1000), 'y_data': np.sinh(np.linspace(0, 10, 1000))}]

    # Create the main window
    main_window = QtWidgets.QWidget()
    main_window.setWindowTitle("Signal Viewer")

    # Create two viewers, passing channel names
    viewer1 = Viewer(plot_data_list_1, channel_name="Channel 1")  # Ensure correct parameter names
    viewer2 = Viewer(plot_data_list_2, channel_name="Channel 2")

    link_bar = ToolBar(viewer1, viewer2)

    # Create two selector panels, passing channel names
    selector_panel1 = SelectorPanel(channelName="Channel 1")
    selector_panel2 = SelectorPanel(channelName="Channel 2")

    # Set the minimum width for the selector panels
    selector_panel1.setMinimumWidth(250)  # Adjust width here
    selector_panel2.setMinimumWidth(250)

    # Create splitters to make the panels resizable
    splitter1 = QtWidgets.QSplitter(Qt.Horizontal)
    splitter1.addWidget(selector_panel1)
    splitter1.addWidget(viewer1)
    splitter1.setStretchFactor(0, 3)  # Give selector_panel1 more space
    splitter1.setStretchFactor(1, 1)  # viewer1 will take less space

    splitter2 = QtWidgets.QSplitter(Qt.Horizontal)
    splitter2.addWidget(selector_panel2)
    splitter2.addWidget(viewer2)
    splitter2.setStretchFactor(0, 3)  # Give selector_panel2 more space
    splitter2.setStretchFactor(1, 1)  # viewer2 will take less space

    # Create a vertical layout and add both splitters
    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(link_bar)
    vbox.addWidget(splitter1)
    vbox.addWidget(splitter2)

    # Set the layout for the main window
    main_window.setLayout(vbox)
    main_window.resize(1400, 800)
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
