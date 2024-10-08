from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QSizePolicy, QSlider, \
    QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap, QColor
from right_panel_style import signalChooseStyle, labelStyle, titleStyle, colorSignalChooseStyle, sliderStyle, valueBoxStyle, tableStyle


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
        self.thicknessSlider.valueChanged.connect(self.update_thickness_value)

        self.thicknessValueBox = QLineEdit("0")
        self.thicknessValueBox.setStyleSheet(valueBoxStyle)
        self.thicknessValueBox.setFixedWidth(40)
        self.thicknessValueBox.setAlignment(Qt.AlignCenter)




        thicknessPropertyRow1 = QHBoxLayout()
        thicknessPropertyRow1.addWidget(self.thicknessLabel)

        thicknessPropertyRow2 = QHBoxLayout()
        thicknessPropertyRow2.addWidget(self.thicknessSlider)
        thicknessPropertyRow2.addWidget(self.thicknessValueBox)



        propertiesPanel = QVBoxLayout()
        propertiesPanel.addLayout(propertiesTitleRow)
        propertiesPanel.addLayout(colorPropertyRow1)
        propertiesPanel.addLayout(colorPropertyRow2)
        propertiesPanel.addLayout(thicknessPropertyRow1)
        propertiesPanel.addLayout(thicknessPropertyRow2)

        #Statistics
        self.statsTitle = QLabel("Statistics")
        self.statsTitle.setStyleSheet(titleStyle)
        #self.statsTitle.setStyleSheet("""border-top: 1px solid #242424;""")

        self.statsTable = QTableWidget()
        self.statsTable.setStyleSheet(tableStyle)
        self.statsTable.setColumnCount(2)
        self.statsTable.setRowCount(5)
        self.statsTable.horizontalHeader().setVisible(False)
        self.statsTable.verticalHeader().setVisible(False)
        self.statsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.statsTable.setEnabled(False)

        header = self.statsTable.horizontalHeader()
        header.setStretchLastSection(True)

        statsLabel =["Mean", "Std", "Duration", "Max", "Min"]
        stats =["12", "223", "22:45", "15", "-2"]

        for row in range(len(statsLabel)):

            self.statsTable.setItem(row,0, QTableWidgetItem(statsLabel[row]))
            statsValue = QTableWidgetItem(stats[row])
            statsValue.setTextAlignment(Qt.AlignCenter)
            self.statsTable.setItem(row, 1, statsValue)

        statsTitleRow = QHBoxLayout()
        statsTitleRow.addWidget(self.statsTitle)

        statsTableLayout = QHBoxLayout()
        statsTableLayout.addWidget(self.statsTable)

        #self.model = QStandardItemModel()
        #self.statsView = QTreeView()
        #self.statsView.setModel(self.model)

        #statsLabel = ["Mean", "Std", "Duration", "Max", "Min"]

        #for stat in range(len(statsLabel)):
         #   self.model.appendRow([QStandardItem(statsLabel[stat]), QStandardItem("55")])

        #statsTitleRow = QHBoxLayout()
        #statsTitleRow.addWidget(self.statsTitle)

        #statsTableLayout = QHBoxLayout()
        #statsTableLayout.addWidget(self.statsView)

        statsPanel = QVBoxLayout()
        statsPanel.addLayout(statsTitleRow)
        statsPanel.addLayout(statsTableLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(signalTitlePanel)
        mainLayout.addLayout(propertiesPanel)
        mainLayout.addLayout(statsPanel )
        mainLayout.addStretch()
        self.setLayout(mainLayout)

        # Set the size policy to expand horizontally
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def update_thickness_value(self, value):
        self.thicknessValueBox.setText(str(value))
