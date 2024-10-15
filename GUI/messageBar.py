from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

class MessageBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #2E2E2E')

        self.message = QLabel()

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.message)