import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QFileDialog
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from fpdf import FPDF 

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, signal_color="#D55877"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#242424')  
        self.ax.set_facecolor('#242424')    

        self.line, = self.ax.plot([], [], color=signal_color, lw=2)  

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
        
        self.toolbarLayout = QVBoxLayout(self)

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(30)  
        self.navToolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        for action in self.navToolbar.actions():
            if action.text() == 'Home':
                action.setIcon(QIcon('E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/home.png'))
            elif action.text() == 'Pan':
                action.setIcon(QIcon('E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/pan.png'))
            elif action.text() == 'Zoom':
                action.setIcon(QIcon('E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos\zoomIn.png'))
            elif action.text() == 'Save':
                action.setIcon(QIcon('E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/save.png'))

        # Add the zoom-out button to the toolbar layout, right beside the toolbar
        self.zoomOutButton = QPushButton("", parent)
        self.zoomOutButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/zoomOut.png"))
        self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomOutButton.setFixedSize(25, 25)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        # Add the zoom-out button directly to the navigation toolbar layout
        self.navToolbar.layout().addWidget(self.zoomOutButton)

        self.toolbarLayout.addWidget(self.navToolbar)
        self.toolbarLayout.addWidget(self)
        self.toolbarLayout.setAlignment(self.navToolbar, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
    
    def zoom_out(self):
        """Zoom out by adjusting the x and y axis limits."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] - 0.5, xlim[1] + 0.5])
        self.ax.set_ylim([ylim[0] - 0.5, ylim[1] + 0.5])
        self.draw()


    def update_plot(self, t, signal):
        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()

    def save_snapshot_image(self, filepath):
        """Save the current figure as an image."""
        self.figure.savefig(filepath)


class GluedSignals(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.snapshots = []  # List to store snapshots
        self.signal_data = None  # Store current signal data

    def signalViewerUi(self, GluedSignals):
        GluedSignals.setObjectName("GluedSignals")
        GluedSignals.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(GluedSignals)
        self.centralwidget.setObjectName("centralwidget")
        GluedSignals.setCentralWidget(self.centralwidget)

        mainLayout = QVBoxLayout(self.centralwidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.GluedSignal = QFrame(self.centralwidget)
        self.GluedSignal.setStyleSheet("background-color: #2D2D2D;")  
        self.GluedSignal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        mainLayout.addWidget(self.GluedSignal)

        self.GluedSignalPlot = QFrame(self.GluedSignal)
        self.GluedSignalPlot.setStyleSheet("background-color: #2D2D2D;")
        self.GluedSignalPlotLayout = QVBoxLayout(self.GluedSignalPlot)
        self.GluedSignalPlotLayout.setContentsMargins(5, 5, 5, 5)
        self.GluedSignalPlotLayout.setObjectName("GluedSignalPlotLayout")

        self.canvas1 = MplCanvas(self.GluedSignal, width=5, height=4, dpi=100, signal_color="#D55877")

        self.titleToolbarLayout = QHBoxLayout()
        self.GluedsignalTitle = QLabel("Glued Signal", self.GluedSignal)
        self.GluedsignalTitle.setStyleSheet("color: #87EDF1; font-size:15px;")  
        self.titleToolbarLayout.addWidget(self.GluedsignalTitle)

        self.snapShotButton = QPushButton("SnapShot", self.GluedSignal)
        self.snapShotButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.snapShotButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #76D4D4;
                border-radius: 5px;
                background-color: #2D2D2D;
                color: #76D4D4;
                width: 100px;
                font-size: 17px;
            }
            QPushButton:hover {
                background-color: #76D4D4;
                color: #2D2D2D;
            }
            QPushButton:pressed {
                background-color: #2D2D2D;
                color: #76D4D4;
            }
        """)
        self.snapShotButton.clicked.connect(self.take_snapshot)
        self.titleToolbarLayout.addWidget(self.snapShotButton)

        self.exportPdfButton = QPushButton("Export to PDF", self.GluedSignal)
        self.exportPdfButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exportPdfButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #EFEFEF;
                border-radius: 5px;
                background-color: #2D2D2D; 
                color: #EFEFEF;
                width:120px;
                font-size:17px
            }
            QPushButton:hover {
                background-color: #EFEFEF;
                color: #2D2D2D;
            }
            QPushButton:pressed {
                background-color: #EFEFEF;
                color: #2D2D2D;
            }
        """)
        self.exportPdfButton.clicked.connect(self.export_to_pdf)
        self.titleToolbarLayout.addWidget(self.exportPdfButton)

        self.GluedSignalPlotLayout.addLayout(self.titleToolbarLayout, stretch=1)  
        self.GluedSignalPlotLayout.addWidget(self.canvas1, stretch=13)  

        self.GluedSignalbuttonsLayout = QHBoxLayout()
        self.GluedSignalbuttonsLayout.addSpacing(10)  

        # Time Label
        self.timeLabel = QtWidgets.QLabel("00:00", self.GluedSignal)
        self.timeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel.setStyleSheet(labelStyle)
        self.GluedSignalbuttonsLayout.addWidget(self.timeLabel)

        self.GluedSignalbuttonsLayout.addSpacing(123)

        # Buttons
        self.pauseButton = QtWidgets.QPushButton(self.GluedSignal)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/pause.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.pauseButton)

        self.playButton = QtWidgets.QPushButton(self.GluedSignal)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/play.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.playButton)

        self.stopButton = QtWidgets.QPushButton(self.GluedSignal)
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton.setStyleSheet(signalControlButtonStyle)
        self.stopButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/stop.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.stopButton)

        self.toStartButton = QtWidgets.QPushButton(self.GluedSignal)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/start.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.toStartButton)

        self.toEndButton = QtWidgets.QPushButton(self.GluedSignal)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets\ControlsButtons\end.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.toEndButton)

        self.rewindButton = QtWidgets.QPushButton(self.GluedSignal)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\Assets/ControlsButtons/rewindOff.png"))
        self.GluedSignalbuttonsLayout.addWidget(self.rewindButton)

        self.GluedSignalbuttonsLayout.addStretch()
        self.GluedSignalPlotLayout.addLayout(self.GluedSignalbuttonsLayout, stretch=6)

        GluedSignalLayout = QVBoxLayout(self.GluedSignal)
        GluedSignalLayout.setContentsMargins(0, 0, 0, 0)
        GluedSignalLayout.addWidget(self.GluedSignalPlot)
        self.GluedSignal.setLayout(GluedSignalLayout)

        # Generate initial signal to show when the app starts
        t = np.linspace(0, 2 * np.pi, 400)
        signal = np.sin(t)  # Example initial signal
        self.canvas1.update_plot(t, signal)

    def take_snapshot(self):
        t = np.linspace(0, 2 * np.pi, 400)
        signal = np.sin(t)

        snapshot = {
            'mean': np.mean(signal),
            'std': np.std(signal),
            'min': np.min(signal),
            'max': np.max(signal),
            'duration': t[-1] - t[0],
            'image_path': f'snapshot_{len(self.snapshots)}.png'  
        }

        self.snapshots.append(snapshot)
        self.canvas1.update_plot(t, signal)
        self.canvas1.save_snapshot_image(snapshot['image_path']) 

    def export_to_pdf(self):
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")

        if save_path:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            for idx, snapshot in enumerate(self.snapshots):
                pdf.add_page()

                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, f'Snapshot {idx + 1}', ln=True, align='C')

                pdf.set_font('Arial', '', 12)
                pdf.cell(200, 10, f'Mean: {snapshot["mean"]}', ln=True)
                pdf.cell(200, 10, f'Std Dev: {snapshot["std"]}', ln=True)
                pdf.cell(200, 10, f'Min: {snapshot["min"]}', ln=True)
                pdf.cell(200, 10, f'Max: {snapshot["max"]}', ln=True)
                pdf.cell(200, 10, f'Duration: {snapshot["duration"]}', ln=True)

                pdf.image(snapshot['image_path'], x=10, y=80, w=180)  

            pdf.output(save_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GluedSignalsApp = GluedSignals()
    GluedSignalsApp.signalViewerUi(GluedSignalsApp)
    GluedSignalsApp.show()
    sys.exit(app.exec_())
