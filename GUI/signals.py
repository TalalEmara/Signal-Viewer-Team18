from PyQt5 import QtCore, QtGui, QtWidgets
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindButtonStyle, linkedButtonStyle, signalButtonZooming
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon

class Ui_Signals(object):
    def setupUi(self, Signals):
        Signals.setObjectName("Signals")
        Signals.resize(1440, 1024)
        self.centralwidget = QtWidgets.QWidget(Signals)
        self.centralwidget.setObjectName("centralwidget")

        # First signal box
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(350, 85, 791, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.signal1Viewer = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.signal1Viewer.setStyleSheet("background-color:#2D2D2D;")
        self.signal1Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signal1Viewer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.signal1Viewer.setObjectName("signal1Viewer")

        self.signal1Title = QtWidgets.QLabel(self.signal1Viewer)
        self.signal1Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.signal1Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.signal1Title.setObjectName("signal1Title")
        self.signal1TitleEdit = QtWidgets.QPushButton(self.signal1Viewer)
        self.signal1TitleEdit.setGeometry(QtCore.QRect(80, 0, 21, 31))
        self.signal1TitleEdit.setStyleSheet("background-color: #2D2D2D; border: none; box-shadow: none;")
        self.signal1TitleEdit.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("photos/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.signal1TitleEdit.setIcon(icon)
        self.signal1TitleEdit.setObjectName("signal1TitleEdit")

        # Zoom, capture buttons on top-right
        self.captureButton1 = QtWidgets.QPushButton(self.signal1Viewer)
        self.captureButton1.setGeometry(QtCore.QRect(693, 10, 30, 30))  # Positioned next to zoom out
        self.captureButton1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.captureButton1.setStyleSheet(signalButtonZooming)
        self.captureButton1.setIcon(QtGui.QIcon("photos/capture.png"))

        self.zoomInButton1 = QtWidgets.QPushButton(self.signal1Viewer)
        self.zoomInButton1.setGeometry(QtCore.QRect(757, 10, 30, 30))  # Positioned 593px from the left
        self.zoomInButton1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomInButton1.setStyleSheet(signalButtonZooming)
        self.zoomInButton1.setIcon(QtGui.QIcon("photos/zoomIn.png"))

        self.zoomOutButton1 = QtWidgets.QPushButton(self.signal1Viewer)
        self.zoomOutButton1.setGeometry(QtCore.QRect(725, 10, 30, 30))  # Positioned next to zoom in
        self.zoomOutButton1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomOutButton1.setStyleSheet(signalButtonZooming)
        self.zoomOutButton1.setIcon(QtGui.QIcon("photos/zoomOut.png"))

        # Buttons for signal1Viewer (existing buttons)
        self.timeLabel1 = QtWidgets.QLabel("00:00", self.signal1Viewer)
        self.timeLabel1.setGeometry(QtCore.QRect(23, 401, 100, 30))  # Positioning time label
        self.timeLabel1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel1.setStyleSheet(labelStyle)

        self.pauseButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.pauseButton.setGeometry(QtCore.QRect(124, 401, 30, 30))
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))

        self.playButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.playButton.setGeometry(QtCore.QRect(157, 401, 30, 30))  # 1px gap
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))

        self.stopButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.stopButton.setGeometry(QtCore.QRect(189, 401, 30, 30))
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton.setStyleSheet(signalControlButtonStyle)
        self.stopButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))

        self.toStartButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toStartButton.setGeometry(QtCore.QRect(221, 401, 30, 30))
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))

        self.toEndButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toEndButton.setGeometry(QtCore.QRect(253, 401, 30, 30))
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))

        self.rewindButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.rewindButton.setGeometry(QtCore.QRect(285, 401, 30, 30))
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton.setStyleSheet(rewindButtonStyle)
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))

        self.verticalLayout.addWidget(self.signal1Viewer)

        # Second signal box (similar layout to signal1Viewer)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(350, 540, 791, 451))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.signal2Viewer = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.signal2Viewer.setStyleSheet("background-color:#2D2D2D;")
        self.signal2Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signal2Viewer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.signal2Viewer.setObjectName("signal2Viewer")

        self.signal2Title = QtWidgets.QLabel(self.signal2Viewer)
        self.signal2Title.setGeometry(QtCore.QRect(10, 0, 91, 31))
        self.signal2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.signal2Title.setObjectName("signal2Title")
        self.signal2TitleEdit = QtWidgets.QPushButton(self.signal2Viewer)
        self.signal2TitleEdit.setGeometry(QtCore.QRect(80, 0, 21, 31))
        self.signal2TitleEdit.setStyleSheet("background-color: #2D2D2D; border: none; box-shadow: none;")
        self.signal2TitleEdit.setIcon(icon)
        self.signal2TitleEdit.setObjectName("signal2TitleEdit")

        # Zoom, capture buttons for signal2Viewer
        self.captureButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.captureButton2.setGeometry(QtCore.QRect(693, 10, 30, 30))  # Positioned next to zoom out
        self.captureButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.captureButton2.setStyleSheet(signalButtonZooming)
        self.captureButton2.setIcon(QtGui.QIcon("photos/capture.png"))

        self.zoomInButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.zoomInButton2.setGeometry(QtCore.QRect(757, 10, 30, 30))  # Positioned next to zoom out
        self.zoomInButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomInButton2.setStyleSheet(signalButtonZooming)
        self.zoomInButton2.setIcon(QtGui.QIcon("photos/zoomIn.png"))

        self.zoomOutButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.zoomOutButton2.setGeometry(QtCore.QRect(725, 10, 30, 30))  # Positioned next to zoom in
        self.zoomOutButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomOutButton2.setStyleSheet(signalButtonZooming)
        self.zoomOutButton2.setIcon(QtGui.QIcon("photos/zoomOut.png"))

        # Time label for signal2Viewer
        self.timeLabel2 = QtWidgets.QLabel("00:00", self.signal2Viewer)
        self.timeLabel2.setGeometry(QtCore.QRect(23, 401, 100, 30))  # Positioning time label
        self.timeLabel2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel2.setStyleSheet(labelStyle)

        # Control buttons for signal2Viewer
        self.pauseButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.pauseButton2.setGeometry(QtCore.QRect(124, 401, 30, 30))
        self.pauseButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton2.setStyleSheet(signalControlButtonStyle)
        self.pauseButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))

        self.playButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.playButton2.setGeometry(QtCore.QRect(157, 401, 30, 30))  # 1px gap
        self.playButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton2.setStyleSheet(signalControlButtonStyle)
        self.playButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))

        self.stopButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.stopButton2.setGeometry(QtCore.QRect(189, 401, 30, 30))
        self.stopButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton2.setStyleSheet(signalControlButtonStyle)
        self.stopButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))

        self.toStartButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toStartButton2.setGeometry(QtCore.QRect(221, 401, 30, 30))
        self.toStartButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton2.setStyleSheet(signalControlButtonStyle)
        self.toStartButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))

        self.toEndButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toEndButton2.setGeometry(QtCore.QRect(253, 401, 30, 30))
        self.toEndButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton2.setStyleSheet(signalControlButtonStyle)
        self.toEndButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))

        self.rewindButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.rewindButton2.setGeometry(QtCore.QRect(285, 401, 30, 30))
        self.rewindButton2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton2.setStyleSheet(rewindButtonStyle)
        self.rewindButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))

        self.verticalLayout_2.addWidget(self.signal2Viewer)

        Signals.setCentralWidget(self.centralwidget)

        self.retranslateUi(Signals)
        QtCore.QMetaObject.connectSlotsByName(Signals)

    def retranslateUi(self, Signals):
        _translate = QtCore.QCoreApplication.translate
        Signals.setWindowTitle(_translate("Signals", "MainWindow"))
        self.signal1Title.setText(_translate("Signals", "Channel 1"))
        self.signal2Title.setText(_translate("Signals", "Channel 2"))
