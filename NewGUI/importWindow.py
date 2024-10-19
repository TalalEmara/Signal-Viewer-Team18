from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QLabel, QPushButton, QCheckBox, QVBoxLayout, \
    QHBoxLayout, QLineEdit
from Styling.importWindowStyles import importButtonStyle, browseButtonStyle,tabStyle
import Signal

class ImportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        print("importedSignal")
    def plotLiveSignal(self):
        print("LiveSignal")




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    importToChannelsWindow = ImportWindow()
    importToChannelsWindow.show()
    sys.exit(app.exec_())