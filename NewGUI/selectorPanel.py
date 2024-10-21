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
from PyQt5.QtCore import pyqtSignal
from Styling.selectorStyles import channelLabelStyle
# import os

# # Add the root project directory to the system path
# sys.path.append(os.path.abspath('Signal-Viewer-Team18'))

# from NewCore.Signal import Signal
# from importWindow import ImportWindow

class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Signal to be emitted when the label is clicked

    def mousePressEvent(self, event):
        # Emit the clicked signal when the label is clicked
        self.clicked.emit()
        super().mousePressEvent(event)

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

        self.name = ClickableLabel(self.name)
        self.color = QPushButton("")
        self.color.setFixedWidth(3)
        self.color.setFixedHeight(14)
        self.color.setEnabled(False)


        self.location = ClickableLabel(self.location)
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

        # Connect the clicked signals to custom methods
        self.name.clicked.connect(self.get_signal_name)
        self.location.clicked.connect(self.get_signal_location)

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

    def get_signal_name(self):
        # Retrieve the signal name when name label is clicked
        print("Signal Name:", self.name.text())

    def get_signal_location(self):
        # Retrieve the signal location when location label is clicked
        print("Signal Location:", self.location.text())

class SelectorPanel(QWidget):    

    signal_map = {}

    def __init__(self, channelName ="Channel 1"):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#222222; font-family: Sofia sans; font-weight: semiBold;")

        self.channelLabel = QLabel(channelName)
        self.channelLabel.setStyleSheet(channelLabelStyle)
       
        self.nameHeader = QLabel("Name")
        self.nameHeader.setStyleSheet("font-size:12px; color:#7c7c7c;")
        self.locationHeader = QLabel("Location")
        self.locationHeader.setStyleSheet("font-size:12px; color:#7c7c7c;")

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.nameHeader,25)
        self.headerLayout.addWidget(self.locationHeader,65)

        self.activeArea = QWidget()
        self.activeArea.setStyleSheet("border-top: 1px solid #76D4D4;")
        self.activeLayout = QVBoxLayout()

        self.activeLayout.addStretch()

        self.activeArea.setLayout(self.activeLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.channelLabel,7)
        self.mainLayout.addLayout(self.headerLayout,3)
        self.mainLayout.addWidget(self.activeArea,90)

        self.setLayout(self.mainLayout)

    def update_signal_dict(self):
        self.update_signal_elements(self)

    def update_signal_elements(self):
        self.activeLayout = QVBoxLayout()
        self.activeArea = QWidget()
        self.activeArea.setStyleSheet("border-top: 1px solid #76D4D4;")
        self.mainLayout = QVBoxLayout()

        # self.setLayout(self.mainLayout)

        # Clear existing widgets
        for i in reversed(range(self.activeLayout.count())):
            widget = self.activeLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Properly delete the widget

        # Add updated signal elements
        for signal_name, signal_data in SelectorPanel.signal_map.items():
            signal_element = SignalElement(signal_data)
            print(signal_element)
            self.activeLayout.addWidget(signal_element)
        
        self.activeLayout.addStretch()  # Add stretch to keep layout neat  
        self.activeArea.setLayout(self.activeLayout)
        self.mainLayout.addWidget(self.activeArea,90)








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectorPanel()
    window.show()
    sys.exit(app.exec_())