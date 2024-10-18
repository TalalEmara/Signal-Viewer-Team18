from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle, linkedButtonOffStyle, linkedButtonOnStyle
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Dynamic_polar import MainWindow as NonRectangularWindow
from signals import Signals
from messageBar import MessageBar

class ToolBar(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Signals()
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
        self.pauseIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets\ControlsButtons\pause.png")
        self.pauseButton.setIcon(self.pauseIcon)
        
       

        self.pauseButton.pressed.connect(lambda: self.handleButtonPress(self.pauseButton))
        self.pauseButton.released.connect(lambda: self.handleButtonRelease(self.pauseButton))

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)
        

        self.playButton.pressed.connect(lambda: self.handleButtonPress(self.playButton))
        self.playButton.released.connect(lambda: self.handleButtonRelease(self.playButton))

       

        self.toStartButton = QPushButton()
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/start.png")
        self.toStartButton.setIcon(self.toStartIcon)
        
        


        self.toStartButton.pressed.connect(lambda: self.handleButtonPress(self.toStartButton))
        self.toStartButton.released.connect(lambda: self.handleButtonRelease(self.toStartButton))


        self.toEndButton = QPushButton()
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/end.png")
        self.toEndButton.setIcon(self.toEndIcon)
        


        self.toEndButton.pressed.connect(lambda: self.handleButtonPress(self.toEndButton))
        self.toEndButton.released.connect(lambda: self.handleButtonRelease(self.toEndButton))

        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/rewindOff.png")
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
        signalControlLayout.addWidget(self.toStartButton)
        signalControlLayout.addWidget(self.toEndButton)
        signalControlLayout.addWidget(self.rewindButton)

        self.zoomButton = QPushButton()
        self.zoomButton.setStyleSheet(signalControlButtonStyle)
        self.zoomButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ToolBox/zoom.png")
        self.zoomButton.setIcon(self.zoomIcon)

        self.zoomButton.pressed.connect(lambda: self.handleButtonPress(self.zoomButton))
        self.zoomButton.released.connect(lambda: self.handleButtonRelease(self.zoomButton))


        self.glueButton = QPushButton()
        self.glueButton.setStyleSheet(signalControlButtonStyle)
        self.glueButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.glueIcon = QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ToolBox/glue.png")
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

       
        self.linkedButton = QPushButton("Linked")
        self.linkedButton.setStyleSheet(linkedButtonOnStyle)
        self.isLinked = True
        self.linkedButton.clicked.connect(lambda: self.handleLinkedClick())
        
        self.nonRectangleButton = QPushButton("Non-Rectangular View")
        self.nonRectangleButton.setStyleSheet(linkedButtonOnStyle)
        self.nonRectangleButton.clicked.connect(lambda: self.handleNonRectangularClick())
        self.nonRectangleButton.pressed.connect(lambda: self.nonRectangleButton.setStyleSheet("background-color: #efefef; font-family: Sofia sans; font-weight: semiBold;font-size: 20px;"))
        self.nonRectangleButton.released.connect(lambda: self.nonRectangleButton.setStyleSheet(linkedButtonOnStyle))

       
        linkedGroup = QWidget()
        linkedGroup.setStyleSheet(boxStyle)
        linkedGroupLayout = QHBoxLayout()
        linkedGroup.setLayout(linkedGroupLayout)

        #linkedGroupLayout.addWidget(self.linkedLabel)
        #linkedGroupLayout.addWidget(self.channel1LinkOption)
        #linkedGroupLayout.addWidget(self.channel2LinkOption)

        linkedGroupLayout.addWidget(self.linkedButton)
        linkedGroupLayout.addWidget(self.nonRectangleButton)

        toolBarLayout = QHBoxLayout()
        toolBarLayout.addWidget(signalControl,30)
        toolBarLayout.addWidget(toolBox,20)
        toolBarLayout.addWidget(linkedGroup,20)

        self.setLayout(toolBarLayout)


        self.pauseButton.clicked.connect(self.pauseAction if self.isLinked else self.handleButtonPress)
        self.pauseButton.clicked.connect(self.pauseAction) 
        self.playButton.clicked.connect(self.playAction)    
        self.toStartButton.clicked.connect(self.toStartAction)
        self.toEndButton.clicked.connect(self.toEndAction)
        self.rewindButton.clicked.connect(self.handleRewindClick)

    def pauseAction(self):
        if self.isLinked:
            self.signals.pause_both()
    

    def playAction(self):
        if self.isLinked:
            self.signals.play_both()  

    def toStartAction(self):
        if self.isLinked:
            self.signals.to_start()  

    def toEndAction(self):
        if self.isLinked:
            self.signals.to_end() 

    def handleRewindClick(self):
        if self.isLinked:
            self.signals.rewind_both()  


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

    def handleNonRectangularClick(self):
        nonRectangularView = NonRectangularWindow()
        nonRectangularView.show()

    
    def handleLinkedClick(self):
        if self.isLinked:
            self.isLinked = False
            self.linkedButton.setText("Link")
            self.linkedButton.setStyleSheet(linkedButtonOffStyle)
        else:
            self.isLinked = True
            self.linkedButton.setText("Linked")
            self.linkedButton.setStyleSheet(linkedButtonOnStyle)
