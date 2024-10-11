from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QFileDialog, QListView

class Channels(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the geometry and main layout for the widget
        self.setGeometry(100, 100, 700, 1000)  # Adjust the size and position as needed
        self.setWindowTitle("Channels Interface")
        
        # Call the layout methods to create the channels
        self.ChannelsLayout()
        self.SetText()

    def ChannelsLayout(self):
        # Channel 1 Layout and Components (Height set to 415px, width increased to 350px)
        self.channel1 = QtWidgets.QWidget(self)
        self.channel1.setGeometry(QtCore.QRect(0, 0, 350, 415))  # Width updated to 350px
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

        # Adjust button position based on the new width
        self.importChannel1Button = QtWidgets.QPushButton(self.channel1Frame)
        self.importChannel1Button.setEnabled(True)
        self.importChannel1Button.setGeometry(QtCore.QRect(280, 385, 53, 20))  # X-position updated for 350px width
        self.importChannel1Button.setStyleSheet(
            "background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px; font-size: 11px; font-weight: normal;width: 52.8px; height: 20px;"
        )
        self.importChannel1Button.setObjectName("importChannel1Button")
        self.importChannel1Button.clicked.connect(self.importChannel1)

        self.channel1Title = QtWidgets.QLabel(self.channel1Frame)
        self.channel1Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.channel1Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.channel1Title.setObjectName("channel1Title")

        self.line1 = QtWidgets.QFrame(self.channel1Frame)
        self.line1.setGeometry(QtCore.QRect(0, 50, 350, 21))  # Width updated to 350px
        self.line1.setStyleSheet("font-color:#76D4D4;")
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setObjectName("line1")

        self.signals1Title = QtWidgets.QLabel(self.channel1Frame)
        self.signals1Title.setGeometry(QtCore.QRect(20, 40, 55, 16))
        self.signals1Title.setStyleSheet("color:#D1D1D1;")
        self.signals1Title.setObjectName("signals1Title")

        self.signals1Location = QtWidgets.QLabel(self.channel1Frame)
        self.signals1Location.setGeometry(QtCore.QRect(200, 40, 55, 16))  # Adjusted for the wider width
        self.signals1Location.setStyleSheet("color:#D1D1D1;")
        self.signals1Location.setObjectName("signals1Location")

        self.channel1List = QListView(self.channel1Frame)
        self.channel1List.setGeometry(QtCore.QRect(0, 60, 350, 315))  # Width updated to 350px
        self.channel1List.setObjectName("channel1List")
        self.channel1List.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.channel1List.setStyleSheet("border: none; color: #EFEFEF;")

        self.channel1Model = QStringListModel()
        self.channel1List.setModel(self.channel1Model)

        self.channel1Layout.addWidget(self.channel1Frame)

        # Channel 2 Layout and Components (Height set to 415px, width increased to 350px)
        self.channel2 = QtWidgets.QWidget(self)
        self.channel2.setGeometry(QtCore.QRect(0, 427, 350, 415))  # Width updated to 350px
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

        # Adjust button position based on the new width
        self.importChannel2Button = QtWidgets.QPushButton(self.channel2Frame)
        self.importChannel2Button.setEnabled(True)
        self.importChannel2Button.setGeometry(QtCore.QRect(280, 385, 53, 20))  # X-position updated for 350px width
        self.importChannel2Button.setStyleSheet(
            "background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px; font-size: 11px; font-weight: normal;width: 52.8px; height: 20px;"
        )
        self.importChannel2Button.setObjectName("importChannel2Button")
        self.importChannel2Button.clicked.connect(self.importChannel2)

        self.channel2Title = QtWidgets.QLabel(self.channel2Frame)
        self.channel2Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.channel2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.channel2Title.setObjectName("channel2Title")

        self.line2 = QtWidgets.QFrame(self.channel2Frame)
        self.line2.setGeometry(QtCore.QRect(0, 50, 350, 21))  # Width updated to 350px
        self.line2.setStyleSheet("font-color:#76D4D4;")
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")

        self.signals2Title = QtWidgets.QLabel(self.channel2Frame)
        self.signals2Title.setGeometry(QtCore.QRect(20, 40, 55, 16))
        self.signals2Title.setStyleSheet("color:#D1D1D1;")
        self.signals2Title.setObjectName("signals2Title")

        self.signals2Location = QtWidgets.QLabel(self.channel2Frame)
        self.signals2Location.setGeometry(QtCore.QRect(200, 40, 55, 16))  # Adjusted for the wider width
        self.signals2Location.setStyleSheet("color:#D1D1D1;")
        self.signals2Location.setObjectName("signals2Location")

        self.channel2List = QListView(self.channel2Frame)
        self.channel2List.setGeometry(QtCore.QRect(0, 60, 350, 315))  # Width updated to 350px
        self.channel2List.setObjectName("channel2List")
        self.channel2List.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.channel2List.setStyleSheet("border: none; color: #EFEFEF;")

        self.channel2Model = QStringListModel()
        self.channel2List.setModel(self.channel2Model)

        self.channel2Layout.addWidget(self.channel2Frame)

    def SetText(self):
        _translate = QtCore.QCoreApplication.translate
        self.importChannel1Button.setText(_translate("Channels", "Import"))
        self.channel1Title.setText(_translate("Channels", "Channel 1"))
        self.signals1Title.setText(_translate("Channels", "Signals"))
        self.signals1Location.setText(_translate("Channels", "Location"))

        self.importChannel2Button.setText(_translate("Channels", "Import"))
        self.channel2Title.setText(_translate("Channels", "Channel 2"))
        self.signals2Title.setText(_translate("Channels", "Signals"))
        self.signals2Location.setText(_translate("Channels", "Location"))

    def importChannel1(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File for Channel 1", "", "All Files (*);;Text Files (*.txt)", options=options)
        if filePath:
            currentList = self.channel1Model.stringList()
            currentList.append(filePath)
            self.channel1Model.setStringList(currentList)

    def importChannel2(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File for Channel 2", "", "All Files (*);;Text Files (*.txt)", options=options)
        if filePath:
            currentList = self.channel2Model.stringList()
            currentList.append(filePath)
            self.channel2Model.setStringList(currentList)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Channels()
    widget.show()
    sys.exit(app.exec_())
