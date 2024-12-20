import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QLabel, QPushButton, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QLineEdit
import pandas as pd
from Styling.importWindowStyles import importButtonStyle, browseButtonStyle,tabStyle
from NewCore.Signal import SignalProperties
from NewCore.dataLoader import DataLoader
from NewCore.live_signals import Live_signal_processing
from SignalViewer import Viewer

class ImportWindow(QMainWindow):
    # fileSelected = QtCore.pyqtSignal(str)
    fileSelected = QtCore.pyqtSignal(str, str, int)

    def __init__(self):
        super().__init__()
        self.file_path = None
        self.channel = 0
        self.setWindowTitle("Import a Signal")
        self.resize(400,100)
        self.setStyleSheet("background-color:#2D2D2D; color:#EFEFEF; font-family: Sofia sans; font-weight: semiBold;")

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("color:#2D2D2D;")
        self.setCentralWidget(self.tabs)

        self.fileTab = QWidget()
        self.fileTab.setStyleSheet("background-color:#2D2D2D; color:#EFEFEF; font-family: Sofia sans; font-weight: "
                                   "semiBold;")
        self.fileTabLabel = QLabel("Upload Signal File")
        self.fileTabLabel.setStyleSheet("font-size:18px; color:#76D4D4;")


        self.signalName = QLabel("Signal has not been uploaded yet")
        self.signalName.setStyleSheet("font-size:12px; ")
        self.signalName.setFixedWidth(300)

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.open_file_dialog)
        self.browseButton.setStyleSheet(browseButtonStyle)

        self.channel1CheckBox = QCheckBox("Channel 1")
        self.channel2CheckBox = QCheckBox("Channel 2")
        self.importButton = QPushButton("Import")
        self.importButton.setFixedWidth(400)
        self.importButton.setStyleSheet(importButtonStyle)
        self.importButton.clicked.connect(lambda :self.importFile())

        #layouts
        self.fileMainLayout = QVBoxLayout()
        self.fileMainLayout.setAlignment(Qt.AlignCenter)
        self.browseLayout = QHBoxLayout()
        self.browseLayout.addWidget(self.signalName)
        self.browseLayout.addWidget(self.browseButton)

        self.checkBoxesLayout = QHBoxLayout()
        self.checkBoxesLayout.addWidget(self.channel1CheckBox)
        self.checkBoxesLayout.addWidget(self.channel2CheckBox)

        self.fileMainLayout.addWidget(self.fileTabLabel)
        self.fileMainLayout.addLayout(self.browseLayout)
        self.fileMainLayout.addLayout(self.checkBoxesLayout)
        self.fileMainLayout.addStretch()
        self.fileMainLayout.addWidget(self.importButton)


        self.fileTab.setLayout(self.fileMainLayout)
        self.tabs.addTab(self.fileTab,"File")


        self.liveTab = QWidget()
        self.liveTab.setStyleSheet("background-color:#2D2D2D; color:#EFEFEF; font-family: Sofia sans; font-weight: "
                                   "semiBold;")
        self.liveInput = QLineEdit()
        self.liveInput.setStyleSheet("font-size:13px; padding:2px; border: .5px solid #76D4D4;;")
        self.liveInput.setPlaceholderText("Put the link")

        self.plotButton = QPushButton("Plot")
        self.plotButton.setStyleSheet(importButtonStyle)
        self.plotButton.clicked.connect(lambda :self.plotLiveSignal())

        self.liveMainLayout= QVBoxLayout()
        self.liveMainLayout.addWidget(self.liveInput)
        self.liveMainLayout.addWidget(self.plotButton)

        self.liveTab.setLayout(self.liveMainLayout)


        self.tabs.addTab(self.liveTab,"Live")

    def checkbox_state_changed(self):
        # Get the state of both checkboxes
        channel1_checked = self.channel1CheckBox.isChecked()
        channel2_checked = self.channel2CheckBox.isChecked()
        if channel1_checked:
            self.channel = 1
        elif channel2_checked:
            self.channel = 2

    # def importFile(self):
    #     from selectorPanel import SelectorPanel
    #     if self.file_path:
    #         file_name = os.path.basename(self.file_path)
    #         signalData = DataLoader(self.file_path).get_data()
    #         signal = SignalProperties(file_name, self.file_path, signalData, self.channel)
    #         SelectorPanel.signal_map[signal.name] = signal
            
    #         SelectorPanel.update_signal_elements(SelectorPanel)

    #         print(signal.isOnChannel1)
    #         self.close()
    #         return signalData
    #     else: 
    #         print("No file selected")
    

        # # function to import csv file    
    # def open_file_dialog(self):
    #     # Open a file dialog restricted to .csv files
    #     file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")

    #     # Check if a file was selected
    #     if file_path:
    #         self.file_path = file_path
    #         self.signalName.setText(os.path.basename(self.file_path))
    #         # print(signal.name)
    #         # return Signal(file_name, file_path, signalData)

    #     else:
    #         print("No file selected.")

    def importFile(self):
        from selectorPanel import SelectorPanel
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            signalData = DataLoader(self.file_path).get_data()
            signal = SignalProperties(file_name, self.file_path, signalData, self.channel)
            self.fileSelected.emit(signal.name, self.file_path, self.channel) 
            self.close()
        else:
            print("No file selected")

    def open_file_dialog(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.file_path = file_path
            self.signalName.setText(os.path.basename(self.file_path))



    def plotLiveSignal(self):
        print("LiveSignal")
        # Get the text from the QLineEdit
        liveSignal = str(self.liveInput.text())
        if liveSignal:
            times, speeds = Live_signal_processing(liveSignal)  # Get data from processing function
            plot_data_list = [{'x_data': times, 'y_data': speeds}]  # Prepare data for plotting

            self.viewer = Viewer(plot_data_list, show_rewind_button=False)  # Create Viewer instance
            self.viewer.setWindowTitle("Live Signal Viewer")  # Set the window title
            self.viewer.show()  # Show the viewer window
            self.close()




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    importToChannelsWindow = ImportWindow()
    importToChannelsWindow.show()
    sys.exit(app.exec_())