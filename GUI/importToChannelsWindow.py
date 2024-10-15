from PyQt5 import QtCore, QtWidgets
# from ..Core import Data_load

class ImportToChannelsWindow(QtWidgets.QMainWindow):
    fileSelected = QtCore.pyqtSignal(str, int)  
    signalAdded = QtCore.pyqtSignal(str, int)   
    
    def __init__(self, default_channel=1, parent=None):
        super().__init__(parent)
        self.default_channel = default_channel
        self.setupImportUI()

    def setupImportUI(self):
        self.setObjectName("importToChannelsWindow")
        self.setWindowTitle("Import Signal")
        self.resize(312, 250)
        self.setStyleSheet("background-color:#2D2D2D;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.ImportTab = QtWidgets.QTabWidget(self.centralwidget)
        self.ImportTab.setGeometry(QtCore.QRect(10, 10, 291, 221))
        self.ImportTab.setStyleSheet("background-color:#2D2D2D;")

        self.fileTab = QtWidgets.QWidget()
        self.fileTab.setObjectName("fileTab")

        self.chooseToImportLabel = QtWidgets.QLabel(self.fileTab)
        self.chooseToImportLabel.setGeometry(QtCore.QRect(50, 20, 191, 16))
        self.chooseToImportLabel.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.chooseToImportLabel.setText("Choose where to import from")

        self.importFromFiles = QtWidgets.QPushButton(self.fileTab)
        self.importFromFiles.setGeometry(QtCore.QRect(80, 50, 131, 20))
        self.importFromFiles.setStyleSheet("background-color: #87EDF1; color: #0D0D0D; border: none; border-radius: 5px;")
        self.importFromFiles.setText("Files")
        self.importFromFiles.clicked.connect(self.importFromFile)

        self.importedInLabel = QtWidgets.QLabel(self.fileTab)
        self.importedInLabel.setGeometry(QtCore.QRect(80, 100, 121, 20)) 
        self.importedInLabel.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.importedInLabel.setText("To be imported in ")

        self.checkBoxChannel1 = QtWidgets.QCheckBox(self.fileTab)
        self.checkBoxChannel1.setGeometry(QtCore.QRect(110, 130, 100, 20)) 
        self.checkBoxChannel1.setStyleSheet("color: #87EDF1;")
        self.checkBoxChannel1.setText("Channel 1")

        self.checkBoxChannel2 = QtWidgets.QCheckBox(self.fileTab)
        self.checkBoxChannel2.setGeometry(QtCore.QRect(110, 160, 100, 20))  
        self.checkBoxChannel2.setStyleSheet("color: #87EDF1;")
        self.checkBoxChannel2.setText("Channel 2")

        self.ImportTab.addTab(self.fileTab, "File")

        self.liveTab = QtWidgets.QWidget()
        self.liveTab.setObjectName("liveTab")

        self.chooseToImportLabel_2 = QtWidgets.QLabel(self.liveTab)
        self.chooseToImportLabel_2.setGeometry(QtCore.QRect(70, 20, 151, 16))
        self.chooseToImportLabel_2.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.chooseToImportLabel_2.setText("Write link of live signal")

        self.ImportLiveSignal = QtWidgets.QTextEdit(self.liveTab)
        self.ImportLiveSignal.setGeometry(QtCore.QRect(32, 50, 231, 21))  
        self.ImportLiveSignal.setStyleSheet("background-color:white; border: none;")  
        self.ImportLiveSignal.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  

        self.importedInLabel_2 = QtWidgets.QLabel(self.liveTab)
        self.importedInLabel_2.setGeometry(QtCore.QRect(80, 100, 121, 20))  
        self.importedInLabel_2.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.importedInLabel_2.setText("To be imported in ")

        self.checkBoxChannel1_2 = QtWidgets.QCheckBox(self.liveTab)
        self.checkBoxChannel1_2.setGeometry(QtCore.QRect(110, 130, 100, 20)) 
        self.checkBoxChannel1_2.setStyleSheet("color: #87EDF1;")
        self.checkBoxChannel1_2.setText("Channel 1")

        self.checkBoxChannel2_2 = QtWidgets.QCheckBox(self.liveTab)
        self.checkBoxChannel2_2.setGeometry(QtCore.QRect(110, 160, 100, 20)) 
        self.checkBoxChannel2_2.setStyleSheet("color: #87EDF1;")
        self.checkBoxChannel2_2.setText("Channel 2")

        self.ImportTab.addTab(self.liveTab, "Live")

        if self.default_channel == 1:
            self.checkBoxChannel1.setChecked(True)
            self.checkBoxChannel1_2.setChecked(True)
        elif self.default_channel == 2:
            self.checkBoxChannel2.setChecked(True)
            self.checkBoxChannel2_2.setChecked(True)

    def importFromFile(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import File", "", "All Files (*)", options=options)

        selectedChannel = 1 if self.checkBoxChannel1.isChecked() else 2

        if filePath:
            self.fileSelected.emit(filePath, selectedChannel)
            return filePath, selectedChannel

    def handleLiveSignalImport(self):
        liveSignal = self.ImportLiveSignal.toPlainText() 

        selectedChannel = 1 if self.checkBoxChannel1_2.isChecked() else 2

        if liveSignal:
            self.signalAdded.emit(liveSignal, selectedChannel)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    importToChannelsWindow = ImportToChannelsWindow()
    importToChannelsWindow.show()
    sys.exit(app.exec_())
