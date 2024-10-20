import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel, QPushButton
)
from NewGUI.Styling.selectorStyles import channelLabelStyle
from NewGUI.Signal import Signal


class SignalElement(QWidget):
    def __init__(self, signal):
        super().__init__()

        self.name= signal.name
        self.signalColor = signal.colorinChannel1
        self.location=signal.location
        self.isShown = signal.isShown


        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            color: #EFEFEF;
            font-family: Sofia sans;
            font-size: 10px;
            border: none;
            border-bottom: 2px solid #2d2d2d;
        """)

        self.name = QLabel(self.name)
        self.color = QPushButton("")
        self.color.setFixedWidth(3)
        self.color.setFixedHeight(14)
        self.color.setEnabled(False)


        self.location = QLabel(self.location)
        self.hiddenIcon = QIcon("Assets/Selector/hidden.png")
        self.shownIcon = QIcon("NewGUI/Assets/Selector/hidden.png")
        self.switchIcon = QIcon("Assets/Selector/swap.png")

        self.hideButton = QPushButton("")
        self.hideButton.setFixedSize(16,16)
        self.hideButton.setIcon(QIcon("NewGUI/Assets/Selector/hidden.png"))
        self.hideButton.clicked.connect(lambda: toogleHidden())

        self.switchButton = QPushButton("")
        self.switchButton.setFixedSize(16,16)
        self.switchButton.setIcon(self.switchIcon)

        self.name.setStyleSheet("border:none;")
        self.color.setStyleSheet(f"border:none; background-color:{self.signalColor};")
        self.location.setStyleSheet("border:none;")
        self.hideButton.setStyleSheet("border:none; background-color:red; ")
        self.switchButton.setStyleSheet("border:none;background-color:blue;")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.color,3)
        self.layout.addWidget(self.name,17)
        self.layout.addWidget(self.location,50)
        self.layout.addWidget(self.hideButton,15)
        self.layout.addWidget(self.switchButton,15)

        self.setLayout(self.layout)


        def toogleHidden():
            if self.isShown:
                print("now is hidden")
                self.hideButton.setIcon(self.hiddenIcon)
                self.isShown = False
            else:
                print("now is shown")
                self.hideButton.setIcon(self.shownIcon)
                self.isShown = True

        def switchChannels():
            print("switched")

class SelectorPanel(QWidget):
    def __init__(self, channelName ="Channel 1"):
        super().__init__()

        self.signals = [Signal(), Signal(), Signal()]

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#222222; font-family: Sofia sans; font-weight: semiBold;")

        self.channelLabel = QLabel(channelName)
        self.channelLabel.setStyleSheet(channelLabelStyle)

        self.nameHeader = QLabel("Name")
        self.nameHeader.setStyleSheet("font-size:12px; color:#7c7c7c; padding-left:5px;")
        self.locationHeader = QLabel("Location")
        self.locationHeader.setStyleSheet("font-size:12px; color:#7c7c7c;")

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.nameHeader,25)
        self.headerLayout.addWidget(self.locationHeader,65)



        self.activeArea = QWidget()
        self.activeArea.setStyleSheet("border-top: 1px solid #76D4D4;")
        self.activeLayout = QVBoxLayout()

        for signal in self.signals:
            signal_element = SignalElement(signal)
            self.activeLayout.addWidget(signal_element)

        self.activeLayout.addStretch()

        self.activeArea.setLayout(self.activeLayout)



        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.channelLabel,7)
        self.mainLayout.addLayout(self.headerLayout,3)
        self.mainLayout.addWidget(self.activeArea,90)

        self.setLayout(self.mainLayout)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectorPanel()
    window.show()
    sys.exit(app.exec_())