from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from properties_style import cardLabelStyle, cardValueStyle
from PyQt5.QtCore import Qt  # Import Qt for alignment flags

class StatsCard(QWidget):
    def __init__(self, label, value):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #242424;")

        self.statLabel = QLabel(label)
        self.statLabel.setStyleSheet(cardLabelStyle)

        self.statValue = QLabel(value)
        self.statValue.setStyleSheet(cardValueStyle)

        layout = QVBoxLayout()
        # stats_Card.py


        layout.addWidget(self.statLabel, alignment=Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.statValue, alignment=Qt.AlignHCenter | Qt.AlignVCenter)

        self.setLayout(layout)