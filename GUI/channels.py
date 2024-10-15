from PyQt5 import QtCore, QtWidgets, QtGui
import os

import pandas as pd
from importToChannelsWindow import ImportToChannelsWindow  # Adjust path accordingly
from PyQt5.QtCore import pyqtSignal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader

class Channels(QtWidgets.QWidget):
    signal_data_ready = pyqtSignal(pd.DataFrame, int) 

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 700, 1000)  
        self.setWindowTitle("Channels Interface")

        # Global checkboxes to track selection for both channels
        self.ChannelsLayout()
        self.SetText()

    def ChannelsLayout(self):
        # Channel 1 Layout and Components
        self.channel1 = QtWidgets.QWidget(self)
        self.channel1.setGeometry(QtCore.QRect(0, 0, 350, 415))
        self.channel1.setObjectName("channel1")
        self.channel1Layout = QtWidgets.QHBoxLayout(self.channel1)
        self.channel1Layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.channel1Layout.setContentsMargins(0, 0, 0, 0)
        self.channel1Layout.setObjectName("channel1Layout")

        self.channel1Frame = QtWidgets.QFrame(self.channel1)
        self.channel1Frame.setStyleSheet("background-color:#2D2D2D;")
        self.channel1Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.channel1Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.channel1Frame.setObjectName("channel1Frame")

        self.importChannel1Button = QtWidgets.QPushButton(self.channel1Frame)
        self.importChannel1Button.setEnabled(True)
        self.importChannel1Button.setGeometry(QtCore.QRect(280, 385, 53, 20))
        self.importChannel1Button.setStyleSheet(
            "background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px; font-size: 11px; font-weight: normal;width: 52.8px; height: 20px;"
        )
        self.importChannel1Button.setObjectName("importChannel1Button")
        self.importChannel1Button.clicked.connect(self.openImportWindowForChannel1)

        self.channel1Title = QtWidgets.QLabel(self.channel1Frame)
        self.channel1Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.channel1Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.channel1Title.setObjectName("channel1Title")

        self.line_1 = QtWidgets.QFrame(self.channel1Frame)
        self.line_1.setGeometry(QtCore.QRect(0, 50, 350, 21))
        self.line_1.setStyleSheet("font-color:#76D4D4;")
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")

        self.signals1Name = QtWidgets.QLabel(self.channel1Frame)
        self.signals1Name.setGeometry(QtCore.QRect(20, 40, 55, 16))
        self.signals1Name.setStyleSheet("color:#D1D1D1;")
        self.signals1Name.setObjectName("signals1Title")
        self.signals1Location = QtWidgets.QLabel(self.channel1Frame)
        self.signals1Location.setGeometry(QtCore.QRect(160, 40, 55, 16))
        self.signals1Location.setStyleSheet("color:#D1D1D1;")
        self.signals1Location.setObjectName("signals1Location")

        # Create the QListWidget for Channel 1
        self.channel1List = QtWidgets.QListWidget(self.channel1Frame)
        self.channel1List.setGeometry(QtCore.QRect(0, 60, 350, 315))
        self.channel1List.setObjectName("channel1List")
        self.channel1List.setStyleSheet("border: none; color: #EFEFEF;")

        self.channel1Layout.addWidget(self.channel1Frame)

        # Channel 2 Layout and Components
        self.channel2 = QtWidgets.QWidget(self)
        self.channel2.setGeometry(QtCore.QRect(0, 427, 350, 415))
        self.channel2.setObjectName("channel2")
        self.channel2Layout = QtWidgets.QHBoxLayout(self.channel2)
        self.channel2Layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.channel2Layout.setContentsMargins(0, 0, 0, 0)
        self.channel2Layout.setObjectName("channel2Layout")

        self.channel2Frame = QtWidgets.QFrame(self.channel2)
        self.channel2Frame.setStyleSheet("background-color:#2D2D2D;")
        self.channel2Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.channel2Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.channel2Frame.setObjectName("channel2Frame")

        self.importChannel2Button = QtWidgets.QPushButton(self.channel2Frame)
        self.importChannel2Button.setEnabled(True)
        self.importChannel2Button.setGeometry(QtCore.QRect(280, 385, 53, 20))
        self.importChannel2Button.setStyleSheet(
            "background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px; font-size: 11px; font-weight: normal;width: 52.8px; height: 20px;"
        )
        self.importChannel2Button.setObjectName("importChannel2Button")
        self.importChannel2Button.clicked.connect(self.openImportWindowForChannel2)

        self.channel2Title = QtWidgets.QLabel(self.channel2Frame)
        self.channel2Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.channel2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.channel2Title.setObjectName("channel2Title")

        self.line_2 = QtWidgets.QFrame(self.channel2Frame)
        self.line_2.setGeometry(QtCore.QRect(0, 50, 350, 21))
        self.line_2.setStyleSheet("font-color:#76D4D4;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.signals2Name = QtWidgets.QLabel(self.channel2Frame)
        self.signals2Name.setGeometry(QtCore.QRect(20, 35, 55, 16))
        self.signals2Name.setStyleSheet("color:#D1D1D1;")
        self.signals2Name.setObjectName("signals1Title")
        self.signals2Location = QtWidgets.QLabel(self.channel2Frame)
        self.signals2Location.setGeometry(QtCore.QRect(160, 35, 55, 16))
        self.signals2Location.setStyleSheet("color:#D1D1D1;")
        self.signals2Location.setObjectName("signals1Location")

        # Create the QListWidget for Channel 2
        self.channel2List = QtWidgets.QListWidget(self.channel2Frame)
        self.channel2List.setGeometry(QtCore.QRect(0, 60, 350, 315))
        self.channel2List.setObjectName("channel2List")
        self.channel2List.setStyleSheet("border: none; color: #EFEFEF;")
        self.channel2Layout.addWidget(self.channel2Frame)

    def SetText(self):
        _translate = QtCore.QCoreApplication.translate
        self.channel1Title.setText(_translate("Channels", "Channel 1"))
        self.importChannel1Button.setText(_translate("Channels", "Import"))
        self.channel2Title.setText(_translate("Channels", "Channel 2"))
        self.importChannel2Button.setText(_translate("Channels", "Import"))
        self.signals1Name.setText(_translate("Channels", "Name"))
        self.signals1Location.setText(_translate("Channels", "Location"))
        self.signals2Name.setText(_translate("Channels", "Name"))
        self.signals2Location.setText(_translate("Channels", "Location"))

    def openImportWindowForChannel1(self):
        self.importWindow = ImportToChannelsWindow(default_channel=1)
        self.importWindow.fileSelected.connect(self.handleFileSelection)
        self.importWindow.show()

    def openImportWindowForChannel2(self):
        self.importWindow = ImportToChannelsWindow(default_channel=2)
        self.importWindow.fileSelected.connect(self.handleFileSelection)
        self.importWindow.show()

    def createFileItemWidget(self, file_name, file_location):
        
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        widget.setFixedHeight(20)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        fileLabel = QtWidgets.QLabel(file_name)
        fileLabel.setStyleSheet("color:#D1D1D1;")
        layout.addWidget(fileLabel)

        # File Location Label
        locationLabel = QtWidgets.QLabel(file_location)
        locationLabel.setStyleSheet("color:#D1D1D1;")
        layout.addWidget(locationLabel)

        # "Hide" button
        hideButton = QtWidgets.QPushButton()
        hideButton.setFixedSize(31, 28)
        hideButton.setStyleSheet("background-color: #2D2D2D; border: none;")
        hideButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:/downloads prog/visible.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        hideButton.setIcon(icon)
        hideButton.clicked.connect(lambda: self.toggleVisibility(fileLabel, hideButton))
        layout.addWidget(hideButton)

        widget.setLayout(layout)
        return widget

    def toggleVisibility(self, label, button):
       
        if label.isVisible():
            label.hide()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("E:/downloads prog/hidden.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
        else:
            label.show()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("E:/downloads prog/visible.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)

    def handleFileSelection(self, filePath, selectedChannel):
        file_name = os.path.basename(filePath)
        file_location = filePath

     
        fileWidget = self.createFileItemWidget(file_name, file_location)
        print(filePath)
        self.data_loader = DataLoader(filePath)

        signal_data = self.data_loader.get_data()
        self.signal_data_ready.emit(signal_data, selectedChannel)

    
        if selectedChannel == 1:
            
            listItem1 = QtWidgets.QListWidgetItem()
            listItem1.setSizeHint(fileWidget.sizeHint())
            self.channel1List.addItem(listItem1)
            self.channel1List.setItemWidget(listItem1, fileWidget)

            
            if self.importWindow.checkBoxChannel2.isChecked():
                listItem2 = QtWidgets.QListWidgetItem()
                listItem2.setSizeHint(fileWidget.sizeHint())
                self.channel2List.addItem(listItem2)
                self.channel2List.setItemWidget(listItem2, fileWidget)

        elif selectedChannel == 2:
            
            listItem2 = QtWidgets.QListWidgetItem()
            listItem2.setSizeHint(fileWidget.sizeHint())
            self.channel2List.addItem(listItem2)
            self.channel2List.setItemWidget(listItem2, fileWidget)

            
            if self.importWindow.checkBoxChannel1.isChecked():
                listItem1 = QtWidgets.QListWidgetItem()
                listItem1.setSizeHint(fileWidget.sizeHint())
                self.channel1List.addItem(listItem1)
                self.channel1List.setItemWidget(listItem1, fileWidget)

    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Channels()
    widget.show()
    app.exec_()
