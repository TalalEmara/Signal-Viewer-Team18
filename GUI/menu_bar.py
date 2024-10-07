
from PyQt5.QtWidgets import  QMenuBar, QMenu, QAction


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.fileMenu = QMenu("File")

        self.importSignal = QAction("Import", self)
        self.exportSignal = QAction("Export", self)

        self.fileMenu.addAction(self.importSignal)
        self.fileMenu.addAction(self.exportSignal)

        self.aboutMenu = QMenu("About")

        self.addMenu(self.fileMenu)
        self.addMenu(self.aboutMenu)
