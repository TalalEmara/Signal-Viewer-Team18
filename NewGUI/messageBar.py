from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

class MessageBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #242424')
        self.setContentsMargins(10,0,0,0)

        self.message = QLabel("")
        self.message.setStyleSheet("""color: #EFEFEF;
                                    font-family: Sofia sans;
                                    font-weight: semiBold;
                                    font-size: 15px;  
        """)

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addStretch()
        mainLayout.addWidget(self.message)
        mainLayout.addStretch()

    def showMessage(self,message = None, type = None):
        self.message.setText (message)
        if type == "alert":
            self.setStyleSheet('background-color: #D55877')  # Correct color value
        else:
            self.setStyleSheet('background-color: #242424')  # Set 