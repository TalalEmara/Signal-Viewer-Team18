from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QListView
from importToChannelsWindow import ImportToChannelsWindow  

class Channels(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        
        self.setGeometry(100, 100, 700, 1000)  
        self.setWindowTitle("Channels Interface")

       
        self.ChannelsLayout()
        self.SetText()

    def ChannelsLayout(self):
       
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

        self.channel1List = QListView(self.channel1Frame)
        self.channel1List.setGeometry(QtCore.QRect(0, 60, 350, 315))
        self.channel1List.setObjectName("channel1List")
        self.channel1List.setStyleSheet("border: none; color: #EFEFEF;")
        self.channel1Model = QStringListModel()
        self.channel1List.setModel(self.channel1Model)

        self.channel1Layout.addWidget(self.channel1Frame)


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

        self.channel2List = QListView(self.channel2Frame)
        self.channel2List.setGeometry(QtCore.QRect(0, 60, 350, 315))
        self.channel2List.setObjectName("channel2List")
        self.channel2List.setStyleSheet("border: none; color: #EFEFEF;")
        self.channel2Model = QStringListModel()
        self.channel2List.setModel(self.channel2Model)

        self.channel2Layout.addWidget(self.channel2Frame)

    def SetText(self):
        _translate = QtCore.QCoreApplication.translate
        self.channel1Title.setText(_translate("Channels", "Channel 1"))
        self.importChannel1Button.setText(_translate("Channels", "Import"))
        self.channel2Title.setText(_translate("Channels", "Channel 2"))
        self.importChannel2Button.setText(_translate("Channels", "Import"))

    def openImportWindowForChannel1(self):
        self.importWindow = ImportToChannelsWindow(default_channel=1)  
        self.importWindow.fileSelected.connect(self.handleFileSelection)
        self.importWindow.show()

    def openImportWindowForChannel2(self):
        self.importWindow = ImportToChannelsWindow(default_channel=2)  
        self.importWindow.fileSelected.connect(self.handleFileSelection)
        self.importWindow.show()

    def handleFileSelection(self, filePath, selectedChannel):
        if selectedChannel == 1:
            currentList = self.channel1Model.stringList()
            currentList.append(filePath)
            self.channel1Model.setStringList(currentList)
            
        
            if self.importWindow.checkBoxChannel2.isChecked():
                currentList2 = self.channel2Model.stringList()
                currentList2.append(filePath)
                self.channel2Model.setStringList(currentList2)

        elif selectedChannel == 2:
            currentList = self.channel2Model.stringList()
            currentList.append(filePath)
            self.channel2Model.setStringList(currentList)
            
          
            if self.importWindow.checkBoxChannel1.isChecked():
                currentList1 = self.channel1Model.stringList()
                currentList1.append(filePath)
                self.channel1Model.setStringList(currentList1)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    channelsWindow = Channels()
    channelsWindow.show()

    sys.exit(app.exec_())
