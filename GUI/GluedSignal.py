import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QFileDialog
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from fpdf import FPDF  # Add fpdf library for PDF creation


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

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(30)  
        self.navToolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.toolbarLayout = QVBoxLayout(self)
        self.toolbarLayout.addWidget(self.navToolbar)
        self.toolbarLayout.addWidget(self)

        self.toolbarLayout.setAlignment(self.navToolbar, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

    def update_plot(self, t, signal):
        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()

    def save_snapshot_image(self, filepath):
        """Save the current figure as an image."""
        self.figure.savefig(filepath)


class Signals(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.snapshots = []  # List to store snapshots
        self.signal_data = None  # Store current signal data

    def signalViewerUi(self, Signals):
        Signals.setObjectName("Signals")
        Signals.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(Signals)
        self.centralwidget.setObjectName("centralwidget")
        Signals.setCentralWidget(self.centralwidget)

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
        self.snapShotButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 5px; background-color: #2D2D2D; color: #76D4D4; width:100px; font-size:17px;")
        self.snapShotButton.clicked.connect(self.take_snapshot)
        self.titleToolbarLayout.addWidget(self.snapShotButton)

        self.exportPdfButton = QPushButton("Export to PDF", self.GluedSignal)
        self.exportPdfButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exportPdfButton.setStyleSheet("border: 2px solid #EFEFEF; border-radius: 5px; background-color: #2D2D2D; color: #EFEFEF; width:120px;font-size:17px;")
        self.exportPdfButton.clicked.connect(self.export_to_pdf)
        self.titleToolbarLayout.addWidget(self.exportPdfButton)

        self.GluedSignalPlotLayout.addLayout(self.titleToolbarLayout, stretch=1)  
        self.GluedSignalPlotLayout.addWidget(self.canvas1, stretch=13)  

        self.GluedSignalbuttonsLayout = QHBoxLayout()
        self.GluedSignalbuttonsLayout.addSpacing(10)  

                # Time Label
        self.timeLabel = QtWidgets.QLabel("00:00", self.GluedSignal)
        self.timeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeLabel.setStyleSheet("color: #EFEFEF")
        self.GluedSignalbuttonsLayout.addWidget(self.timeLabel)

        self.GluedSignalbuttonsLayout.addSpacing(123)

        # Buttons
        self.pauseButton = QtWidgets.QPushButton(self.GluedSignal)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.pauseButton.clicked.connect(self.pause_signal)
        self.GluedSignalbuttonsLayout.addWidget(self.pauseButton)

        self.playButton = QtWidgets.QPushButton(self.GluedSignal)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.playButton.clicked.connect(self.play_signal)
        self.GluedSignalbuttonsLayout.addWidget(self.playButton)

        self.stopButton = QtWidgets.QPushButton(self.GluedSignal)
        self.stopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stopButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.stopButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/stop.png"))
        self.stopButton.clicked.connect(self.stop_signal)
        self.GluedSignalbuttonsLayout.addWidget(self.stopButton)

        self.toStartButton = QtWidgets.QPushButton(self.GluedSignal)
        self.toStartButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toStartButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.toStartButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.toStartButton.clicked.connect(self.to_start_signal)
        self.GluedSignalbuttonsLayout.addWidget(self.toStartButton)

        self.toEndButton = QtWidgets.QPushButton(self.GluedSignal)
        self.toEndButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toEndButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.toEndButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.toEndButton.clicked.connect(self.to_end_signal)
        self.GluedSignalbuttonsLayout.addWidget(self.toEndButton)

        self.rewindButton = QtWidgets.QPushButton(self.GluedSignal)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindButton.setStyleSheet("border: 2px solid #76D4D4; border-radius: 10px; background-color: #2D2D2D;")
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton.clicked.connect(self.rewind_signal)
        self.GluedSignalbuttonsLayout.addWidget(self.rewindButton)

        self.GluedSignalbuttonsLayout.addStretch()
        self.GluedSignalPlotLayout.addLayout(self.GluedSignalbuttonsLayout, stretch=6)

        GluedSignalLayout = QVBoxLayout(self.GluedSignal)
        GluedSignalLayout.setContentsMargins(0, 0, 0, 0)
        GluedSignalLayout.addWidget(self.GluedSignalPlot)
        self.GluedSignal.setLayout(GluedSignalLayout)

        # Initialize default signal plot
        self.initialize_signal()

    def initialize_signal(self):
        """Initialize the signal plot with default data."""
        t = np.linspace(0, 10, 100)
        signal = np.sin(t)
        self.signal_data = {'time': t, 'signal': signal}
        self.canvas1.update_plot(t, signal)

    def play_signal(self):
        """Play the signal."""
        self.playing = True
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_signal)
        self.timer.start(100)

    def pause_signal(self):
        """Pause the signal."""
        self.playing = False
        if hasattr(self, 'timer'):
            self.timer.stop()

    def stop_signal(self):
        """Stop the signal and reset."""
        self.pause_signal()
        self.time = 0
        self.timeLabel.setText("00:00")
        self.canvas1.update_plot(self.signal_data['time'], self.signal_data['signal'])

    def to_start_signal(self):
        """Move to the start of the signal."""
        self.time = 0
        self.timeLabel.setText("00:00")

    def to_end_signal(self):
        """Move to the end of the signal."""
        self.time = len(self.signal_data['time']) - 1
        self.timeLabel.setText(f"{self.time:02d}:00")

    def rewind_signal(self):
        """Rewind the signal."""
        self.time = max(0, self.time - 10)
        self.timeLabel.setText(f"{self.time:02d}:00")

    def update_signal(self):
        """Update the signal dynamically."""
        if self.playing:
            self.time += 1
            if self.time < len(self.signal_data['time']):
                new_signal = self.signal_data['signal'][:self.time]
                new_time = self.signal_data['time'][:self.time]
                self.canvas1.update_plot(new_time, new_signal)
                self.timeLabel.setText(f"{self.time:02d}:00")
            else:
                self.pause_signal()


        self.GluedSignalPlotLayout.addLayout(self.GluedSignalbuttonsLayout, stretch=6)

        GluedSignalLayout = QVBoxLayout(self.GluedSignal)
        GluedSignalLayout.setContentsMargins(0, 0, 0, 0) 
        GluedSignalLayout.addWidget(self.GluedSignalPlot)
        self.GluedSignal.setLayout(GluedSignalLayout)

    def take_snapshot(self):
       
        t = np.linspace(0, 10, 100)  
        signal = np.sin(t)  

        snapshot = {
            'time': t,
            'signal': signal,
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

                # Add title for the snapshot
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, f'Snapshot {idx + 1}', ln=True, align='C')

                # Add signal statistics
                pdf.set_font('Arial', '', 12)
                pdf.cell(200, 10, f'Mean: {snapshot["mean"]}', ln=True)
                pdf.cell(200, 10, f'Std Dev: {snapshot["std"]}', ln=True)
                pdf.cell(200, 10, f'Min: {snapshot["min"]}', ln=True)
                pdf.cell(200, 10, f'Max: {snapshot["max"]}', ln=True)
                pdf.cell(200, 10, f'Duration: {snapshot["duration"]}', ln=True)

                # Add snapshot image
                pdf.image(snapshot['image_path'], x=10, y=80, w=180)  # Positioning the image in the PDF

            # Save the PDF to the chosen file
            pdf.output(save_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SignalsApp = Signals()
    SignalsApp.signalViewerUi(SignalsApp)
    SignalsApp.show()
    sys.exit(app.exec_())
