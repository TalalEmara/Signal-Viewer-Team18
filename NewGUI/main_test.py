from PyQt5 import QtWidgets
from importWindow import ImportWindow
from selectorPanel import SelectorPanel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Create instances of the two UI classes
        self.first_ui = ImportWindow()
        self.second_ui = SelectorPanel()

        # Add the two UI widgets to the main window's layout
        layout.addWidget(self.first_ui)
        layout.addWidget(self.second_ui)

        # Set the main window properties
        self.setWindowTitle("Main Window with Two UIs")
        self.setGeometry(100, 100, 400, 300)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
