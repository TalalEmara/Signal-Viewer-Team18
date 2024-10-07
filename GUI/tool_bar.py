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

        signalControl = QWidget()
        signalControlLayout = QHBoxLayout()
        signalControl.setLayout(signalControlLayout)

        signalControlLayout.addWidget(self.timeLabel)
        signalControlLayout.addWidget(self.pauseButton)
        signalControlLayout.addWidget(self.pauseButton)
        signalControlLayout.addWidget(self.startButton)
        signalControlLayout.addWidget(self.stopButton)
        signalControlLayout.addWidget(self.toStartButton)
        signalControlLayout.addWidget(self.toEndButton)



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
        toolBarLayout.addWidget(signalControl)
        toolBarLayout.addLayout(toolGroup)
        toolBarLayout.addLayout(linkedGroup)
        self.setLayout(toolBarLayout)
