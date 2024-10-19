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


class SignalElement(QWidget):
    def __init__(self, name = "Untitled" , color = "red" , location = "///" ):
        super().__init__()
        isShown = True
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            color: #EFEFEF;
            font-family: Sofia sans;
            font-size: 10px;
            border: none;
            border-bottom: 2px solid #2d2d2d;
        """)

        self.name = QLabel(name)
        self.color = QPushButton("")
        self.color.setFixedWidth(3)
        self.color.setFixedHeight(14)
        self.color.setEnabled(False)


        self.location = QLabel(location)
        self.hiddenIcon = QIcon("Assets/Selector/hidden.png")
        self.shownIcon = QIcon("Assets/Selector/shown.png")
        self.switchIcon = QIcon("Assets/Selector/swap.png")

        self.hideButton = QPushButton("")
        self.hideButton.setFixedSize(60,60)
        self.hideButton.setIcon(self.shownIcon)
        self.hideButton.clicked.connect(lambda: toogleHidden())

        self.switchButton = QPushButton("sss")
        self.switchButton.setIcon(self.switchIcon)

        self.name.setStyleSheet("border:none;")
        self.color.setStyleSheet(f"border:none; background-color:{color};")
        self.location.setStyleSheet("border:none;")
        self.hideButton.setStyleSheet("border:none; background:red;")
        self.switchButton.setStyleSheet("border:none;")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.color)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.location)
        self.layout.addWidget(self.hideButton)
        self.layout.addWidget(self.switchButton)

        self.setLayout(self.layout)


        def toogleHidden():
            if isShown:
                print("now is hidden")
                self.hideButton.setIcon(self.hiddenIcon)
            else:
                print("now is shown")
                self.hideButton.setIcon(self.shownIcon)

class SelectorPanel(QWidget):
    def __init__(self, channelName ="Channel 1"):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#222222; font-family: Sofia sans; font-weight: semiBold;")

        self.channelLabel = QLabel(channelName)
        self.channelLabel.setStyleSheet(channelLabelStyle)

        self.nameHeader = QLabel("Name")
        self.nameHeader.setStyleSheet("font-size:12px; color:#7c7c7c; padding-left:5px;")
        self.locationHeader = QLabel("Location")
        self.locationHeader.setStyleSheet("font-size:12px; color:#7c7c7c;")

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.nameHeader,20)
        self.headerLayout.addWidget(self.locationHeader,80)

        self.activeArea = QWidget()
        self.activeArea.setStyleSheet("border-top: 1px solid #76D4D4;")
        self.activeLayout = QVBoxLayout()
        self.activeLayout.addWidget(SignalElement())
        self.activeLayout.addWidget(SignalElement())
        self.activeLayout.addWidget(SignalElement())
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