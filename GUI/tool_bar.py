from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle, linkedButtonOffStyle, linkedButtonOnStyle


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        # Signal controls and time
        self.timeLabel = QLabel("00:00")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet(labelStyle)

        # Signal controls and time
        self.timeLabel = QLabel("00:00")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet(labelStyle)

        self.pauseButton = QPushButton()
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseIcon = QIcon("Assets/ControlsButtons/pause.png")
        self.pauseButton.setIcon(self.pauseIcon)

        self.pauseButton.pressed.connect(lambda: self.handleButtonPress(self.pauseButton))
        self.pauseButton.released.connect(lambda: self.handleButtonRelease(self.pauseButton))

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playIcon = QIcon("Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)

        self.playButton.pressed.connect(lambda: self.handleButtonPress(self.playButton))
        self.playButton.released.connect(lambda: self.handleButtonRelease(self.playButton))

        self.stopButton = QPushButton()
        self.stopButton.setStyleSheet(signalControlButtonStyle)
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopIcon = QIcon("Assets/ControlsButtons/stop.png")
        self.stopButton.setIcon(self.stopIcon)


        self.stopButton.pressed.connect(lambda: self.handleButtonPress(self.stopButton))
        self.stopButton.released.connect(lambda: self.handleButtonRelease(self.stopButton))


        self.toStartButton = QPushButton()
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartIcon = QIcon("Assets/ControlsButtons/start.png")
        self.toStartButton.setIcon(self.toStartIcon)


        self.toStartButton.pressed.connect(lambda: self.handleButtonPress(self.toStartButton))
        self.toStartButton.released.connect(lambda: self.handleButtonRelease(self.toStartButton))


        self.toEndButton = QPushButton()
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndIcon = QIcon("Assets/ControlsButtons/end.png")
        self.toEndButton.setIcon(self.toEndIcon)


        self.toEndButton.pressed.connect(lambda: self.handleButtonPress(self.toEndButton))
        self.toEndButton.released.connect(lambda: self.handleButtonRelease(self.toEndButton))

        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindIcon = QIcon("Assets/ControlsButtons/rewindOff.png")
        self.rewindButton.setIcon(self.rewindIcon)

        self.isRewind = False
        self.rewindButton.clicked.connect(lambda: self.handleRewindClick())

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

        self.zoomButton = QPushButton()
        self.zoomButton.setStyleSheet(signalControlButtonStyle)
        self.zoomButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomIcon = QIcon("Assets/ToolBox/zoom.png")
        self.zoomButton.setIcon(self.zoomIcon)

        self.zoomButton.pressed.connect(lambda: self.handleButtonPress(self.zoomButton))
        self.zoomButton.released.connect(lambda: self.handleButtonRelease(self.zoomButton))


        self.glueButton = QPushButton()
        self.glueButton.setStyleSheet(signalControlButtonStyle)
        self.glueButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.glueIcon = QIcon("Assets/ToolBox/glue.png")
        self.glueButton.setIcon(self.glueIcon)


        self.glueButton.pressed.connect(lambda: self.handleButtonPress(self.glueButton))
        self.glueButton.released.connect(lambda: self.handleButtonRelease(self.glueButton))




        toolBox = QWidget()
        toolBox.setStyleSheet(boxStyle)
        toolBoxLayout = QHBoxLayout()
        toolBox.setLayout(toolBoxLayout)

        toolBoxLayout.addWidget(self.zoomButton)
        toolBoxLayout.addWidget(self.glueButton)
        toolBoxLayout.addStretch()

        #self.linkedLabel = QLabel("Linked")
        #self.linkedLabel.setStyleSheet(labelStyle)


        self.linkedButton = QPushButton("Linked")
        self.linkedButton.setStyleSheet(linkedButtonOnStyle)
        self.isLinked =True
        self.linkedButton.clicked.connect(lambda: self.handleLinkedClick())

        #self.channel2LinkOption = QPushButton("Channel 2")

        linkedGroup = QWidget()
        linkedGroup.setStyleSheet(boxStyle)
        linkedGroupLayout = QHBoxLayout()
        linkedGroup.setLayout(linkedGroupLayout)

        #linkedGroupLayout.addWidget(self.linkedLabel)
        #linkedGroupLayout.addWidget(self.channel1LinkOption)
        #linkedGroupLayout.addWidget(self.channel2LinkOption)

        linkedGroupLayout.addWidget(self.linkedButton)

        toolBarLayout = QHBoxLayout()
        toolBarLayout.addWidget(signalControl,30)
        toolBarLayout.addWidget(toolBox,30)
        toolBarLayout.addWidget(linkedGroup,10)

        self.setLayout(toolBarLayout)


    def handleRewindClick(self):
        if self.isRewind:
            self.isRewind = False
            self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        else:
            self.isRewind = True
            self.rewindButton.setStyleSheet(rewindOnButtonStyle)

    def handleLinkedClick(self):
        if self.isLinked:
            self.isLinked = False
            self.linkedButton.setText("Link")
            self.linkedButton.setStyleSheet(linkedButtonOffStyle)
        else:
            self.isLinked = True
            self.linkedButton.setText("Linked")
            self.linkedButton.setStyleSheet(linkedButtonOnStyle)


    def handleButtonPress(self, button):
        button.setStyleSheet("""
                        QPushButton{
                            background-color: #efefef;
                            border: 3px solid #76D4D4;
                            border-radius: 10px;
                            Opacity: .7;
                        }
                        """)

    def handleButtonRelease(self, button):
        button.setStyleSheet(signalControlButtonStyle)