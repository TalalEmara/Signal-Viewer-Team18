import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from importWindow import ImportWindow
from SignalViewer import Viewer
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader
from selectorPanel import SelectorPanel
from linkBar import ToolBar
from properties import Properties
from Styling.importWindowStyles import importButtonStyle

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Load data from CSV
    csv_file_path = 'signals_data/ECG_Normal.csv'
    data_loader = DataLoader(csv_file_path)
    data_loader.load_data()

    data = data_loader.get_data()
    x_data = data[:, 0]
    y_data = data[:, 1]

    # Prepare two sets of plot data
    plot_data_list_1 = [{'x_data': x_data, 'y_data': y_data}]
    plot_data_list_2 = [{'x_data': np.linspace(0, 10, 1000), 'y_data': np.sinh(np.linspace(0, 10, 1000))}]

    main_window = QtWidgets.QWidget()
    main_window.setAttribute(Qt.WA_StyledBackground, True)
    main_window.setStyleSheet("background-color:#242424;")
    main_window.setWindowTitle("Signal Viewer")

    properties = Properties()

    viewer1 = Viewer(plot_data_list_1, channel_name="Channel 1", show_rewind_button=True)
    viewer2 = Viewer(plot_data_list_2, channel_name="Channel 2", show_rewind_button=True)

    toolBar = ToolBar(viewer1, viewer2)

    # Create two selector panels, passing channel names
    selector_panel1 = SelectorPanel(channelName="Channel 1")
    #selector_panel1.importButton.clicked.connect(lambda: handleImportClick(importWindow))
    selector_panel2 = SelectorPanel(channelName="Channel 2")

    mainLayout = QHBoxLayout()
    propertiesPanle = QVBoxLayout()
    activeArea = QVBoxLayout()

    toolBarLayout = QHBoxLayout()
    messageBarLayout = QHBoxLayout()

    channel1Layout = QHBoxLayout()
    channel2Layout = QHBoxLayout()

    selectorChannel1Layout = QVBoxLayout()
    viewerChannel1Layout = QVBoxLayout()

    selectorChannel2Layout = QVBoxLayout()
    viewerChannel2Layout = QVBoxLayout()

    propertiesPanle.addWidget(properties)
    toolBarLayout.addWidget(toolBar)
    selectorChannel1Layout.addWidget(selector_panel1)
    selectorChannel2Layout.addWidget(selector_panel2)
    viewerChannel1Layout.addWidget(viewer1)
    viewerChannel2Layout.addWidget(viewer2)

    buttonLayout = QHBoxLayout()
    importButton = QPushButton("Import")
    importButton.setStyleSheet(importButtonStyle)
    importButton.setFixedWidth(200)
    importButton.setFixedHeight(50)
    importButton.clicked.connect(lambda :handleImportClick())

    buttonLayout.addWidget(importButton)
    buttonLayout.addStretch()

    mainLayout.addLayout(activeArea,80)
    mainLayout.addLayout(propertiesPanle,20)
    activeArea.addLayout(toolBarLayout,10)
    activeArea.addLayout(messageBarLayout,2)
    activeArea.addLayout(channel1Layout,45)
    activeArea.addLayout(channel2Layout,45)
    activeArea.addLayout(buttonLayout,8)
    channel1Layout.addLayout(selectorChannel1Layout,30)
    channel1Layout.addLayout(viewerChannel1Layout,70)
    channel2Layout.addLayout(selectorChannel2Layout,30)
    channel2Layout.addLayout(viewerChannel2Layout,70)

    # Set the layout for the main window
    main_window.setLayout(mainLayout)
    main_window.resize(1400, 800)
    main_window.show()

    sys.exit(app.exec_())

def handleImportClick():
    importWindow = ImportWindow()
    importWindow.show()

if __name__ == "__main__":
    main()
