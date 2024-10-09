from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QSizePolicy, QSlider
from PyQt5.QtGui import QIcon, QPixmap, QColor
from right_panel_style import signalChooseStyle, labelStyle, titleStyle, colorSignalChooseStyle, sliderStyle


class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.signalNameInput = "ECG Signal"  # variable

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #2E2E2E')

        # self.signalName = QLabel(self.signalNameInput)
        # self.signalName.setStyleSheet("")

        self.signalChoose = QComboBox()
        self.signalChoose.setStyleSheet(signalChooseStyle)
        self.signalChoose.addItems(["ECG Signal", "EEG Signal", "Beta Signal"])

        signalTitlePanel = QHBoxLayout()
        # signalTitlePanel.addWidget(self.signalName)
        signalTitlePanel.addWidget(self.signalChoose)

        # properties settings
        self.propertiesTitle = QLabel("Properties")
        self.propertiesTitle.setStyleSheet(titleStyle)

        self.signalColorLabel = QLabel("Signal Color")
        self.signalColorLabel.setStyleSheet(labelStyle)

        #self.colorSquare = QLabel()
        #self.square = QPixmap(30, 30)
        #self.square.fill(QColor("#EFEFEF"))
        #self.colorSquare.setPixmap(self.square)

        self.signalColorChoose = QComboBox()
        self.signalColorChoose.setStyleSheet(colorSignalChooseStyle)
        self.signalColorChoose.addItems(["Red", "Cyan", "Orange", "Add Color"])
        #Setting Color Icons
        self.signalColorChoose.setItemIcon(0, QIcon("Assets/RightPanel/ColorsIcon/red.png"))
        self.signalColorChoose.setItemIcon(1, QIcon("Assets/RightPanel/ColorsIcon/cyan.png"))
        self.signalColorChoose.setItemIcon(2, QIcon("Assets/RightPanel/ColorsIcon/orange.png"))

        propertiesTitleRow = QHBoxLayout()
        propertiesTitleRow.addWidget(self.propertiesTitle)


        colorPropertyRow1 = QHBoxLayout()
        colorPropertyRow1.addWidget(self.signalColorLabel)

        colorPropertyRow2 = QHBoxLayout()
        #propertiesRow2.addWidget(self.colorSquare)
        colorPropertyRow2.addWidget(self.signalColorChoose)


        self.thicknessLabel =QLabel("Line thickness")
        self.thicknessLabel.setStyleSheet(labelStyle)

        self.thicknessSlider = QSlider(Qt.Horizontal)
        self.thicknessSlider.setStyleSheet(sliderStyle)
        self.thicknessSlider.setMinimum(0)
        self.thicknessSlider.setMaximum(30)
        self.thicknessSlider.setSingleStep(3)

        thicknessPropertyRow1 = QHBoxLayout()
        thicknessPropertyRow1.addWidget(self.thicknessLabel)

        thicknessPropertyRow2 = QHBoxLayout()
        thicknessPropertyRow2.addWidget(self.thicknessSlider)



        propertiesPanel = QVBoxLayout()
        propertiesPanel.addLayout(propertiesTitleRow)
        propertiesPanel.addLayout(colorPropertyRow1)
        propertiesPanel.addLayout(colorPropertyRow2)
        propertiesPanel.addLayout(thicknessPropertyRow1)
        propertiesPanel.addLayout(thicknessPropertyRow2)
        propertiesPanel.addStretch()

        statsPanel = QHBoxLayout()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(signalTitlePanel)
        mainLayout.addLayout(propertiesPanel)
        mainLayout.addLayout(statsPanel)
        self.setLayout(mainLayout)

        # Set the size policy to expand horizontally
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
