from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.signalNameInput = "ECG Signal" # variable

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #2E2E2E')

        self.signalName = QLabel(self.signalNameInput)
        self.signalName.setStyleSheet("")

        signalTitlePanel = QHBoxLayout()
        signalTitlePanel.addWidget(self.signalName)

        propertiesPanel = QHBoxLayout()
        statsPanel = QHBoxLayout()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(signalTitlePanel)
        mainLayout.addLayout(propertiesPanel)
        mainLayout.addLayout(statsPanel)
        self.setLayout(mainLayout)

        # Set the size policy to expand horizontally
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)