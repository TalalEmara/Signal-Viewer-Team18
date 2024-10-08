from PyQt5 import QtCore, QtGui, QtWidgets

class Channels(object):
    def ChannelsLayout(self, centralwidget):
        self.channel1 = QtWidgets.QWidget(centralwidget)
        self.channel1.setGeometry(QtCore.QRect(10, 480, 291, 451))
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
        self.importChannel2Button = QtWidgets.QPushButton(self.channel1Frame)
        self.importChannel2Button.setEnabled(True)
        self.importChannel2Button.setGeometry(QtCore.QRect(220, 420, 53, 20))
        self.importChannel2Button.setStyleSheet("background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px; font-size: 11px; font-weight: normal;width: 52.8px; height: 20px;")
        self.importChannel2Button.setObjectName("importChannel2Button")
        self.channel2Title = QtWidgets.QLabel(self.channel1Frame)
        self.channel2Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.channel2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.channel2Title.setObjectName("channel2Title")
        self.line2 = QtWidgets.QFrame(self.channel1Frame)
        self.line2.setGeometry(QtCore.QRect(0, 50, 291, 21))
        self.line2.setStyleSheet("font-color:#76D4D4;")
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.signals2Title = QtWidgets.QLabel(self.channel1Frame)
        self.signals2Title.setGeometry(QtCore.QRect(20, 40, 55, 16))
        self.signals2Title.setStyleSheet("color:#D1D1D1;")
        self.signals2Title.setObjectName("signals2Title")
        self.signals2Location = QtWidgets.QLabel(self.channel1Frame)
        self.signals2Location.setGeometry(QtCore.QRect(160, 40, 55, 16))
        self.signals2Location.setStyleSheet("color:#D1D1D1;")
        self.signals2Location.setObjectName("signals2Location")
        
        # Set the QListView and hide borders
        self.channel2List = QtWidgets.QListView(self.channel1Frame)
        self.channel2List.setGeometry(QtCore.QRect(0, 60, 291, 351))
        self.channel2List.setObjectName("channel2List")
        self.channel2List.setFrameShape(QtWidgets.QFrame.NoFrame)  # Hide borders
        self.channel2List.setStyleSheet("border: none;")  # Remove any border from stylesheet
        
        self.channel1Layout.addWidget(self.channel1Frame)

        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 291, 451))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.frame_2 = QtWidgets.QFrame(self.horizontalLayoutWidget_4)
        self.frame_2.setStyleSheet("background-color:#2D2D2D;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.importChannel1Button = QtWidgets.QPushButton(self.frame_2)
        self.importChannel1Button.setEnabled(True)
        self.importChannel1Button.setGeometry(QtCore.QRect(220, 420, 53, 20))
        self.importChannel1Button.setStyleSheet("background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px; font-size: 11px; font-weight: normal; width: 52.8px; height: 20px; hover { background-color: #0D0D0D; color: #87EDF1; margin: 5px; }")

        self.importChannel1Button.setObjectName("importChannel1Button")
        self.channel1Title = QtWidgets.QLabel(self.frame_2)
        self.channel1Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.channel1Title.setStyleSheet("color: #87EDF1;\n"
                                         "font-size:15px;")
        self.channel1Title.setObjectName("channel1Title")
        self.line = QtWidgets.QFrame(self.frame_2)
        self.line.setGeometry(QtCore.QRect(0, 50, 291, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.signals1Title = QtWidgets.QLabel(self.frame_2)
        self.signals1Title.setGeometry(QtCore.QRect(20, 40, 55, 16))
        self.signals1Title.setStyleSheet("color:#D1D1D1;")
        self.signals1Title.setObjectName("signals1Title")
        self.signals1Location = QtWidgets.QLabel(self.frame_2)
        self.signals1Location.setGeometry(QtCore.QRect(160, 40, 55, 16))
        self.signals1Location.setStyleSheet("color:#D1D1D1;")
        self.signals1Location.setObjectName("signals1Location")
        
        # Set the QListView and hide borders
        self.channel1List = QtWidgets.QListView(self.frame_2)
        self.channel1List.setGeometry(QtCore.QRect(0, 60, 291, 351))
        self.channel1List.setObjectName("channel1List")
        self.channel1List.setFrameShape(QtWidgets.QFrame.NoFrame)  # Hide borders
        self.channel1List.setStyleSheet("border: none;")  # Remove any border from stylesheet

        self.hideButton = QtWidgets.QPushButton(self.frame_2)
        self.hideButton.setGeometry(QtCore.QRect(250, 70, 31, 28))
        self.hideButton.setStyleSheet("background-color: #2D2D2D;\n"
                                      "border: none;\n"
                                      "box-shadow: none;\n")
        self.hideButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:/downloads prog/visible.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton.setIcon(icon)
        self.hideButton.setObjectName("hideButton")

        self.hideButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.hideButton_2.setGeometry(QtCore.QRect(250, 100, 31, 28))
        self.hideButton_2.setStyleSheet("background-color: #2D2D2D;\n"
                                        "border: none;\n"
                                        "box-shadow: none;\n")
        self.hideButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("E:/downloads prog/hidden.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideButton_2.setIcon(icon1)
        self.hideButton_2.setObjectName("hideButton_2")
        self.horizontalLayout_4.addWidget(self.frame_2)

    def SetText(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.importChannel2Button.setText(_translate("MainWindow", "Import"))
        self.channel2Title.setText(_translate("MainWindow", "Channel 2"))
        self.signals2Title.setText(_translate("MainWindow", "Signals"))
        self.signals2Location.setText(_translate("MainWindow", "Location"))
        self.importChannel1Button.setText(_translate("MainWindow", "Import"))
        self.channel1Title.setText(_translate("MainWindow", "Channel 1"))
        self.signals1Title.setText(_translate("MainWindow", "Signals"))
        self.signals1Location.setText(_translate("MainWindow", "Location"))
