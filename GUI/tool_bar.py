from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, timeLabelStyle, rewindButtonStyle


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        # Signal controls and time
        self.timeLabel = QLabel("00:00")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet(timeLabelStyle)

        self.pauseButton = QPushButton()
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseIcon = QIcon("Assets/ControlsButtons/pause.png")
        self.pauseButton.setIcon(self.pauseIcon)
        self.pauseButton.resize(25, 25)

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playIcon = QIcon("Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)
        self.playButton.resize(25, 25)

        self.stopButton = QPushButton()
        self.stopButton.setStyleSheet(signalControlButtonStyle)
        self.stopIcon = QIcon("Assets/ControlsButtons/stop.png")
        self.stopButton.setIcon(self.stopIcon)
        self.stopButton.resize(25, 25)

        self.toStartButton = QPushButton()
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartIcon = QIcon("Assets/ControlsButtons/start.png")
        self.toStartButton.setIcon(self.toStartIcon)
        self.toStartButton.resize(25, 25)

        self.toEndButton = QPushButton()
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndIcon = QIcon("Assets/ControlsButtons/end.png")
        self.toEndButton.setIcon(self.pauseIcon)
        self.toEndButton.resize(25, 25)

        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindButtonStyle)
        self.rewindIcon = QIcon("Assets/ControlsButtons/rewindOff.png")
        self.rewindButton.setIcon(self.rewindIcon)
        self.rewindButton.resize(25, 25)

        signalControl = QWidget()
        signalControl.setStyleSheet(boxStyle)
        signalControlLayout = QHBoxLayout()
        signalControl.setLayout(signalControlLayout)

        signalControlLayout.addWidget(self.timeLabel)
        signalControlLayout.addWidget(self.pauseButton)
        signalControlLayout.addWidget(self.playButton)
        signalControlLayout.addWidget(self.stopButton)
        signalControlLayout.addWidget(self.toStartButton)
        signalControlLayout.addWidget(self.toEndButton)
        signalControlLayout.addWidget(self.rewindButton)

        self.zoomButton = QPushButton("Z")
        self.glueButton = QPushButton("G")

        toolGroup = QHBoxLayout()
        toolGroup.addWidget(self.zoomButton)
        toolGroup.addWidget(self.glueButton)

        self.linkedLabel = QLabel("Linked")
        self.channel1LinkOption = QPushButton("Channel 1")
        self.channel2LinkOption = QPushButton("Channel 2")

        linkedGroup = QHBoxLayout()
        toolGroup.addWidget(self.linkedLabel)
        toolGroup.addWidget(self.channel1LinkOption)
        toolGroup.addWidget(self.channel2LinkOption)

        toolBarLayout = QHBoxLayout()
        toolBarLayout.addWidget(signalControl)
        toolBarLayout.addLayout(toolGroup)
        toolBarLayout.addLayout(linkedGroup)
        self.setLayout(toolBarLayout)
