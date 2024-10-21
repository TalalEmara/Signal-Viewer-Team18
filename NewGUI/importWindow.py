import os
import sys
sys.path.append(os.path.abspath('Signal-Viewer-Team18'))

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QLabel, QPushButton, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QLineEdit
import pandas as pd
from Styling.importWindowStyles import importButtonStyle, browseButtonStyle,tabStyle
from NewCore.Signal import Signal
from NewCore.dataLoader import DataLoader
from selectorPanel import SelectorPanel

from NewCore.live_signals import plot_live_data, Live_signal_processing
from plotting import Plotting
from SignalViewer import Viewer
class ImportWindow(QMainWindow):
    fileSelected = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file_path = None
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

    def importFile(self):
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            signalData = DataLoader(self.file_path).get_data()
            signal = Signal(file_name, self.file_path, signalData)
            SelectorPanel.signal_map[signal.name] = signal
            
            # self.fileSelected.emit(self.file_path)
            SelectorPanel.update_signal_dict(SelectorPanel)

            print("importedSignal")
            self.close()
        else: 
            print("No file selected")

    def plotLiveSignal(self):
        print("LiveSignal")
        # Get the text from the QLineEdit
        liveSignal = str(self.liveInput.text())
        if liveSignal:
            times, speeds, _ = Live_signal_processing(liveSignal)
            Plotting.plot_live_signal(self,times, speeds)
        self.close()

    # function to import csv file    
    def open_file_dialog(self):
        # Open a file dialog restricted to .csv files
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")

        # Check if a file was selected
        if file_path:
            self.file_path = file_path
            # print(signal.name)
            # return Signal(file_name, file_path, signalData)

        else:
            print("No file selected.")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    importToChannelsWindow = ImportWindow()
    importToChannelsWindow.show()
    sys.exit(app.exec_())