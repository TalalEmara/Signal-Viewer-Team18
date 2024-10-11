from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QSizePolicy, QSlider, \
    QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView,QHeaderView
from PyQt5.QtGui import QIcon, QPixmap, QColor
from right_panel_style import signalChooseStyle, labelStyle, titleStyle, colorSignalChooseStyle, sliderStyle, \
    valueBoxStyle, tableStyle, viewButtonOnStyle, viewButtonOffStyle
from stats_Card import StatsCard

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.signalNameInput = "ECG Signal"  

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #2E2E2E')


        self.signalChoose = QComboBox()
        self.signalChoose.setStyleSheet(signalChooseStyle)
        self.signalChoose.addItems(["ECG Signal", "EEG Signal", "Beta Signal"])

        signalTitlePanel = QHBoxLayout()

        signalTitlePanel.addWidget(self.signalChoose)

        # properties settings
        self.propertiesTitle = QLabel("Properties")
        self.propertiesTitle.setStyleSheet(titleStyle)

        self.signalColorLabel = QLabel("Signal Color")
        self.signalColorLabel.setStyleSheet(labelStyle)

        
        self.signalColorChoose = QComboBox()
        self.signalColorChoose.setStyleSheet(colorSignalChooseStyle)
        self.signalColorChoose.addItems(["Red", "Cyan", "Orange", "Add Color"])
        
        self.signalColorChoose.setItemIcon(0, QIcon("Assets/RightPanel/ColorsIcon/red.png"))
        self.signalColorChoose.setItemIcon(1, QIcon("Assets/RightPanel/ColorsIcon/cyan.png"))
        self.signalColorChoose.setItemIcon(2, QIcon("Assets/RightPanel/ColorsIcon/orange.png"))

        propertiesTitleRow = QHBoxLayout()
        propertiesTitleRow.addWidget(self.propertiesTitle)

        colorPropertyRow1 = QHBoxLayout()
        colorPropertyRow1.addWidget(self.signalColorLabel)

        colorPropertyRow2 = QHBoxLayout()
        
        colorPropertyRow2.addWidget(self.signalColorChoose)

        self.thicknessLabel = QLabel("Line thickness")
        self.thicknessLabel.setStyleSheet(labelStyle)

        self.thicknessSlider = QSlider(Qt.Horizontal)
        self.thicknessSlider.setStyleSheet(sliderStyle)
        self.thicknessSlider.setMinimum(0)
        self.thicknessSlider.setMaximum(30)
        self.thicknessSlider.setSingleStep(3)
        self.thicknessSlider.valueChanged.connect(self.updateThicknessValue)

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

        # Statistics setup
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

        self.statsListViewButton = QPushButton()
        self.statsCardsViewButton = QPushButton()
        self.statsListViewButton.setStyleSheet(viewButtonOnStyle)
        self.statsCardsViewButton.setStyleSheet(viewButtonOffStyle)

        self.listButtonIcon = QIcon("Assets/RightPanel/ViewButtons/list.png")
        self.cardsButtonIcon = QIcon("Assets/RightPanel/ViewButtons/cards.png")
        self.listBlackButtonIcon = QIcon("Assets/RightPanel/ViewButtons/listBlack.png")
        self.cardsBlackButtonIcon = QIcon("Assets/RightPanel/ViewButtons/cardsBlack.png")

        self.statsListViewButton.setIcon(self.listButtonIcon)
        self.statsCardsViewButton.setIcon(self.cardsButtonIcon)

        self.statsListViewButton.clicked.connect(self.toggle_view_mode)
        self.statsCardsViewButton.clicked.connect(self.toggle_view_mode)

       
        statsTitleRow = QHBoxLayout()
        statsTitleRow.addWidget(statsTitle)
        statsTitleRow.addStretch()
        statsTitleRow.addWidget(self.statsListViewButton)
        statsTitleRow.addWidget(self.statsCardsViewButton)

        self.statsPanel.addLayout(statsTitleRow)

        # Create the table view
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

        self.statsTable.setMinimumWidth(300)


        # Create the card view
        self.card1 = StatsCard("mean", "12")
        self.card2 = StatsCard("min", "2")
        self.card3 = StatsCard("max", "24")
        self.card4 = StatsCard("mean", "12")
        self.card5 = StatsCard("min", "2")
        self.card6 = StatsCard("max", "24")

        self.cardViewLayout = QVBoxLayout()
        cardRow1 = QHBoxLayout()
        cardRow2 = QHBoxLayout()

        cardRow1.addWidget(self.card1)
        cardRow1.addWidget(self.card2)
        cardRow1.addWidget(self.card3)
        cardRow2.addWidget(self.card4)
        cardRow2.addWidget(self.card5)
        cardRow2.addWidget(self.card6)

        self.cardViewLayout.addLayout(cardRow1)
        self.cardViewLayout.addLayout(cardRow2)

        
        self.statsPanel.addWidget(self.statsTable)
        self.cardViewLayoutWidget = QWidget()
        self.cardViewLayoutWidget.setLayout(self.cardViewLayout)
        self.cardViewLayoutWidget.hide()
        self.statsPanel.addWidget(self.cardViewLayoutWidget)

    def updateThicknessValue(self, value):
        self.thicknessValueBox.setText(str(value))

    def toggle_view_mode(self):
        if self.statsTable.isVisible():
            # Switch to card view
            self.statsTable.hide()
            self.cardViewLayoutWidget.show()
            self.statsListViewButton.setStyleSheet(viewButtonOffStyle)
            self.statsCardsViewButton.setStyleSheet(viewButtonOnStyle)
            self.statsListViewButton.setIcon(self.listBlackButtonIcon)
            self.statsCardsViewButton.setIcon(self.cardsButtonIcon)
        else:
            # Switch to list view
            self.cardViewLayoutWidget.hide()
            self.statsTable.show()
            self.statsListViewButton.setStyleSheet(viewButtonOnStyle)
            self.statsCardsViewButton.setStyleSheet(viewButtonOffStyle)
            self.statsListViewButton.setIcon(self.listButtonIcon)
            self.statsCardsViewButton.setIcon(self.cardsBlackButtonIcon)



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.right_panel = RightPanel()
        self.setCentralWidget(self.right_panel)

        
        self.setWindowTitle("Right Pane;")
        self.setGeometry(100, 100, 400, 600)  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
