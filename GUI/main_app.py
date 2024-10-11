import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from menu_bar import MenuBar  # Import the panel class
from tool_bar import ToolBar  # Import the panel class
from right_panel import RightPanel
from Styles import menuBarStyle, toolBarStyle
from channels import Channels
#from signals import SignalsMainWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Demo UI")
        self.resize(1440, 1080)

        self.menuBar = MenuBar()
        self.menuBar.setStyleSheet(menuBarStyle)
        self.toolBar = ToolBar()
        self.properties = RightPanel()
        self.properties.setMinimumWidth(int(.2*1440))
#       self.signalViewer = SignalsMainWindow()

        self.signalListTest = QWidget()
        self.signalListTest.setStyleSheet("background-color: #FFD700;")  # Gold


        self.channels = QWidget()
        self.channels.setStyleSheet("background-color: #00FFFF;")  # Cyan

        self.propTest = QWidget()
        self.propTest.setStyleSheet("background-color: #90EE90;")  # Light Green

        self.menBar = QWidget()
        self.menBar.setStyleSheet("background-color: #FF0000;")  # Red

        self.tlBar = QWidget()
        self.tlBar.setStyleSheet("background-color: #808080;")  # Gray

        self.menuBarLayout = QHBoxLayout()
        self.menuBarLayout.addWidget(self.menuBar)

        self.workspace = QHBoxLayout()
        self.activeArea = QVBoxLayout()
        self.toolBarLayout = QHBoxLayout()
        self.toolBarLayout.addWidget(self.toolBar)
        self.signalShowLayout = QHBoxLayout()
        self.signalsListPanel = QVBoxLayout()
        self.signalsListPanel.addWidget(self.signalListTest)
        self.channelsLayout = QVBoxLayout()
        self.channelsLayout.addWidget(self.channels)
        self.propertiesPanel = QVBoxLayout()
        self.propertiesPanel.addWidget(self.properties)


        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.menuBarLayout,2)
        mainLayout.addLayout(self.workspace,98)
        self.workspace.addLayout(self.activeArea,80)
        self.workspace.addLayout(self.propertiesPanel,20)
        self.activeArea.addLayout(self.toolBarLayout,5)
        self.activeArea.addLayout(self.signalShowLayout,95)
        self.signalShowLayout.addLayout(self.signalsListPanel,25)
        self.signalShowLayout.addLayout(self.channelsLayout,75)

        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())