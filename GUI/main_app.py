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

from signals import SignalMainWindow
from PyQt5.QtCore import pyqtSignal
from NewGUI.selectorPanel import SelectorPanel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Demo UI")
        self.resize(2000, 980)
        self.setStyleSheet("background-color: #242424;")


        self.menuBar = MenuBar()
        self.menuBar.setStyleSheet(menuBarStyle)
        self.toolBar = ToolBar()
        self.properties = RightPanel()
        self.ImportSignal = SelectorPanel()
        self.properties.setMinimumWidth(int(.2*1440))
        self.signalViewer = SignalMainWindow()
        self.toolBar.signals=self.signalViewer


        self.signalListTest = QWidget()
        

        self.menuBarLayout = QHBoxLayout()
        self.menuBarLayout.addWidget(self.menuBar)

        self.workspace = QHBoxLayout()
        self.activeArea = QVBoxLayout()
        self.toolBarLayout = QHBoxLayout()
        self.toolBarLayout.addWidget(self.toolBar)
        self.signalShowLayout = QHBoxLayout()
        self.signalsListPanel = QVBoxLayout()
        self.signalsListPanel.addWidget(self.ImportSignal)
        self.channelsLayout = QVBoxLayout()
        self.channelsLayout.addWidget(self.signalViewer)
        self.propertiesPanel = QVBoxLayout()
        self.propertiesPanel.addWidget(self.properties)


        mainLayout = QVBoxLayout()
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