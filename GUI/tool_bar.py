from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        # Signal controls and time
        self.timeLabel = QLabel("00:00")
        self.pauseButton = QPushButton("||")
        self.startButton = QPushButton(">")
        self.stopButton = QPushButton("0")
        self.toStartButton = QPushButton("|<")
        self.toEndButton = QPushButton(">|")

        signalControl = QHBoxLayout()
        signalControl.addWidget(self.timeLabel)
        signalControl.addWidget(self.pauseButton)
        signalControl.addWidget(self.pauseButton)
        signalControl.addWidget(self.startButton)
        signalControl.addWidget(self.stopButton)
        signalControl.addWidget(self.toStartButton)
        signalControl.addWidget(self.toEndButton)



        self.zoomButton = QPushButton("Z")
        self.glueButton = QPushButton("G")

        toolGroup = QHBoxLayout()
        toolGroup.addWidget(self.zoomButton)
        toolGroup.addWidget(self.glueButton)

        self.linkedLabel =QLabel("Linked")
        self.channel1LinkOption = QPushButton("Channel 1")
        self.channel2LinkOption = QPushButton("Channel 2")

        linkedGroup = QHBoxLayout()
        toolGroup.addWidget(self.linkedLabel)
        toolGroup.addWidget(self.channel1LinkOption)
        toolGroup.addWidget(self.channel2LinkOption)

        toolBarLayout = QHBoxLayout()
        toolBarLayout.addLayout(signalControl)
        toolBarLayout.addLayout(toolGroup)
        toolBarLayout.addLayout(linkedGroup)
        self.setLayout(toolBarLayout)
