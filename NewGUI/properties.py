from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QSizePolicy, QSlider, \
    QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QColorDialog
from PyQt5.QtGui import QColor
from properties_style import signalChooseStyle, labelStyle, titleStyle, colorSignalChooseStyle, sliderStyle, \
    valueBoxStyle, tableStyle, viewButtonOnStyle, viewButtonOffStyle
from stats_Card import StatsCard


class Properties(QWidget):
    signal_properties_changed = pyqtSignal(str, int, int)  # Emit color, thickness, and speed

    def __init__(self):
        super().__init__()

        self.signalNameInput = "ECG Signal"
        self.colorChoosen = "#D55877"  # Default color

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #2E2E2E')

        self.signalChoose = QComboBox()
        self.signalChoose.setStyleSheet(signalChooseStyle)
        self.signalChoose.addItems(["ECG Signal", "EEG Signal", "Beta Signal"])

        signalTitlePanel = QHBoxLayout()
        signalTitlePanel.addWidget(self.signalChoose)

        # Properties settings
        self.propertiesTitle = QLabel("Properties")
        self.propertiesTitle.setStyleSheet(titleStyle)

        self.signalColorLabel = QLabel("Signal Color")
        self.signalColorLabel.setStyleSheet(labelStyle)

        self.signalColorChooseSquare = QPushButton()
        self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
        self.signalColorChooseSquare.setFixedHeight(20)
        self.signalColorChooseSquare.setFixedWidth(20)
        self.signalColorChooseSquare.clicked.connect(self.openColorDialog)  # Open color dialog when square is clicked

        self.signalColorChooseList = QComboBox()
        self.signalColorChooseList.setStyleSheet(colorSignalChooseStyle)
        self.signalColorChooseList.addItem("Red", "#D55877")
        self.signalColorChooseList.addItem("Blue", "#76D4D4")
        self.signalColorChooseList.addItem("Add New Color")
        self.signalColorChooseList.setItemData("Add New Color")
        self.signalColorChooseList.currentIndexChanged.connect(self.changeSignalColor)

        propertiesTitleRow = QHBoxLayout()
        propertiesTitleRow.addWidget(self.propertiesTitle)

        colorPropertyRow1 = QHBoxLayout()
        colorPropertyRow1.addWidget(self.signalColorLabel)

        colorPropertyRow2 = QHBoxLayout()
        colorPropertyRow2.addWidget(self.signalColorChooseSquare)
        colorPropertyRow2.addWidget(self.signalColorChooseList)

        self.thicknessLabel = QLabel("Line thickness")
        self.thicknessLabel.setStyleSheet(labelStyle)

        self.thicknessSlider = QSlider(Qt.Horizontal)
        self.thicknessSlider.setStyleSheet(sliderStyle)
        self.thicknessSlider.setMinimum(5)
        self.thicknessSlider.setMaximum(30)
        self.thicknessSlider.setSingleStep(3)
        self.thicknessSlider.valueChanged.connect(self.updateThicknessValue)

        self.thicknessValueBox = QLineEdit("0")
        self.thicknessValueBox.setStyleSheet(valueBoxStyle)
        self.thicknessValueBox.setFixedWidth(40)
        self.thicknessValueBox.setAlignment(Qt.AlignCenter)

        self.speedLabel = QLabel("Animation Speed")
        self.speedLabel.setStyleSheet(labelStyle)

        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setStyleSheet(sliderStyle)
        self.speedSlider.setMinimum(5)
        self.speedSlider.setMaximum(100)
        self.speedSlider.setSingleStep(10)
        self.speedSlider.setValue(10)  
        self.speedSlider.valueChanged.connect(self.updateSpeedValue)

        self.speedValueBox = QLineEdit("10")
        self.speedValueBox.setStyleSheet(valueBoxStyle)
        self.speedValueBox.setFixedWidth(40)
        self.speedValueBox.setAlignment(Qt.AlignCenter)

        thicknessPropertyRow1 = QHBoxLayout()
        thicknessPropertyRow1.addWidget(self.thicknessLabel)

        thicknessPropertyRow2 = QHBoxLayout()
        thicknessPropertyRow2.addWidget(self.thicknessSlider)
        thicknessPropertyRow2.addWidget(self.thicknessValueBox)

        speedPropertyRow1 = QHBoxLayout()
        speedPropertyRow1.addWidget(self.speedLabel)

        speedPropertyRow2 = QHBoxLayout()
        speedPropertyRow2.addWidget(self.speedSlider)
        speedPropertyRow2.addWidget(self.speedValueBox)

        propertiesPanel = QVBoxLayout()
        propertiesPanel.addLayout(propertiesTitleRow)
        propertiesPanel.addLayout(colorPropertyRow1)
        propertiesPanel.addLayout(colorPropertyRow2)
        propertiesPanel.addLayout(thicknessPropertyRow1)
        propertiesPanel.addLayout(thicknessPropertyRow2)
        propertiesPanel.addLayout(speedPropertyRow1)  
        propertiesPanel.addLayout(speedPropertyRow2)

       
        self.statsPanel = QVBoxLayout()
        self.statsPanel.setAlignment(Qt.AlignTop)
        self.setupStatistics()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(signalTitlePanel)
        mainLayout.addLayout(propertiesPanel)
        mainLayout.addLayout(self.statsPanel)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def setupStatistics(self):
        statsTitle = QLabel("Statistics")
        statsTitle.setStyleSheet(titleStyle)

        self.statsTable = QTableWidget()
        self.statsTable.setStyleSheet(tableStyle)
        self.statsTable.setColumnCount(2)
        self.statsTable.setRowCount(5)
        self.statsTable.horizontalHeader().setVisible(False)
        self.statsTable.verticalHeader().setVisible(False)
        self.statsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        statsLabels = ["Mean", "Std", "Duration", "Max", "Min"]
        statsValues = ["12", "223", "22:45", "15", "-2"]

        for row, (label, value) in enumerate(zip(statsLabels, statsValues)):
            self.statsTable.setItem(row, 0, QTableWidgetItem(label))
            statsValueItem = QTableWidgetItem(value)
            statsValueItem.setTextAlignment(Qt.AlignCenter)
            self.statsTable.setItem(row, 1, statsValueItem)
        self.statsTable.horizontalHeader().setStretchLastSection(True)
        self.statsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.statsPanel.addWidget(self.statsTable)

    def updateThicknessValue(self, value):
        self.thicknessValueBox.setText(str(value))
        self.emit_properties_change()

    def updateSpeedValue(self, value):
        self.speedValueBox.setText(str(value))
        self.emit_properties_change()

    def changeSignalColor(self, index):
        if index == 2:
            self.openColorDialog() 
        else:
            self.colorChoosen = self.signalColorChooseList.itemData(index)
            self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
            self.emit_properties_change()

    def openColorDialog(self):
        
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorChoosen = color.name()
            self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
            self.emit_properties_change()

    def emit_properties_change(self):
        
        thickness = self.thicknessSlider.value()
        speed = self.speedSlider.value()
        self.signal_properties_changed.emit(self.colorChoosen, thickness, speed)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Right Panel")
        self.setGeometry(100, 100, 400, 600)

       
        self.properties = Properties()
        self.setCentralWidget(self.properties)

        
        self.properties.signal_properties_changed.connect(self.on_properties_changed)

    def on_properties_changed(self, color, thickness, speed):
        print(f"Color: {color}, Thickness: {thickness}, Speed: {speed}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())