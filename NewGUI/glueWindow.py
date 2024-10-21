
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, \
    QFileDialog, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Styles import signalControlButtonStyle, labelStyle


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, signal_color="#D55877"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#242424')  # Set background color for plot area
        self.ax.set_facecolor('#242424')    # Set background color for axes

        self.line, = self.ax.plot([], [], color=signal_color, lw=2)  # Initialize empty line for plotting

        self.ax.tick_params(axis='x', colors='#EFEFEF')
        self.ax.tick_params(axis='y', colors='#EFEFEF')
        self.ax.xaxis.label.set_color('#EFEFEF')
        self.ax.yaxis.label.set_color('#EFEFEF')
        self.ax.spines['bottom'].set_color('#EFEFEF')
        self.ax.spines['left'].set_color('#EFEFEF')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.grid(True, color='#EFEFEF', linestyle='--', alpha=0.1)

        super(MplCanvas, self).__init__(fig)



class GlueWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glued signal")
        self.setStyleSheet("background-color:#242424;")
        self.setContentsMargins(10,10,10,10)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)



        self.mpl_canvas = MplCanvas(self)

        self.title = QLabel("Gluing signals")
        self.title.setStyleSheet(labelStyle)
        self.title.setFixedHeight(70)


        self.backwordButton = QPushButton("Backword")
        self.backwordButton.setStyleSheet(signalControlButtonStyle)
        self.backwordButton.setFixedSize(150, 70)
        self.backwordButton.pressed.connect(lambda: self.handleButtonPress(self.backwordButton))
        self.backwordButton.released.connect(lambda: self.handleButtonRelease(self.backwordButton))

        self.forwordButton = QPushButton("Forword")
        self.forwordButton.setStyleSheet(signalControlButtonStyle)
        self.forwordButton.setFixedSize(150, 70)
        self.forwordButton.pressed.connect(lambda: self.handleButtonPress(self.forwordButton))
        self.forwordButton.released.connect(lambda: self.handleButtonRelease(self.forwordButton))

        self.glueButton = QPushButton("Glue")
        self.glueButton.setStyleSheet(signalControlButtonStyle)
        self.glueButton.setFixedSize(150 ,70)
        self.glueButton.pressed.connect(lambda: self.handleButtonPress(self.glueButton))
        self.glueButton.released.connect(lambda: self.handleButtonRelease(self.glueButton))

        titleRow = QHBoxLayout()
        titleRow.addStretch()
        titleRow.addWidget(self.title)
        titleRow.addStretch()

        graphRow = QHBoxLayout()
        graphRow.addWidget(self.mpl_canvas)

        buttonRow = QHBoxLayout()
        buttonRow.addStretch()
        buttonRow.addWidget(self.backwordButton)
        buttonRow.addWidget(self.forwordButton)
        #buttonRow.addWidget(self.glueButton)
        buttonRow.addStretch()

        main_layout.addLayout(titleRow ,10)
        main_layout.addLayout(graphRow ,10)
        main_layout.addLayout(buttonRow ,80)




        # Set the window size and show it
        self.setMinimumSize(1000, 700)
        self.show()

    def update_plot(self, x, y):
        self.mpl_canvas.ax.clear()  # Clear the existing plot
        self.mpl_canvas.line.set_xdata(x)
        self.mpl_canvas.line.set_ydata(y)
        self.mpl_canvas.ax.set_xlim(min(x), max(x))  # Set X-axis limits
        self.mpl_canvas.ax.set_ylim(-1.2, 1.2)  # Set Y-axis limits (adjust as needed)
        self.mpl_canvas.ax.set_xlabel("X-axis")
        self.mpl_canvas.ax.set_ylabel("Y-axis")
        self.mpl_canvas.draw()  # Redraw the canvas to show the updated plot


    def handleButtonPress(self, button):
        button.setStyleSheet("""
                        QPushButton{
                            margin:10px;
                            background-color: #efefef;
                            border: 3px solid #76D4D4;
                            border-radius: 10px;
                            Opacity: .7;

                            color: #76D4D4;
                            font-family: Sofia sans;
                            font-weight: semiBold;
                            font-size: 18px;
                        }
                        """)

    def handleButtonRelease(self, button):
        button.setStyleSheet(signalControlButtonStyle)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = GlueWindow()
    sys.exit(app.exec_())