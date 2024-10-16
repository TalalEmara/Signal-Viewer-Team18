import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, \
    QLineEdit
from PyQt5.QtGui import QIcon
from Styles import boxStyle, signalControlButtonStyle, labelStyle, rewindOffButtonStyle, rewindOnButtonStyle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from matplotlib.animation import FuncAnimation
from PyQt5.QtCore import Qt
from channels import Channels
from importToChannelsWindow import ImportToChannelsWindow  # Adjust path accordingly
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader

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

        # Toolbar layout with zoom-out button
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(25)
        self.navToolbar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for action in self.navToolbar.actions():
            if action.text() == 'Home':
                action.setIcon(QIcon('photos/home.png'))
            elif action.text() == 'Pan':
                action.setIcon(QIcon('photos/pan.png'))
            elif action.text() == 'Zoom':
                action.setIcon(QIcon('photos/zoomIn.png'))
            elif action.text() == 'Save':
                action.setIcon(QIcon('photos/save.png'))
        
        # Add the navigation toolbar to the toolbar layout
        self.toolbarLayout.addWidget(self.navToolbar)

        # Zoom Out Button
        self.zoomOutButton = QPushButton("", parent)
        self.zoomOutButton.setIcon(QtGui.QIcon("photos/zoomOut.png"))
        self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomOutButton.setFixedSize(25, 25)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        # Add the zoom-out button to the toolbar layout
        self.toolbarLayout.addWidget(self.zoomOutButton)

        # Main layout for the canvas
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.toolbarLayout)  
        self.mainLayout.addWidget(self)  
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

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


class Signals(QtWidgets.QWidget):  # Inheriting from QWidget instead of object
    def __init__(self):
        super().__init__()
        self.signalViewerUi()

    def signalViewerUi(self):
        self.setObjectName("Signals")
        self.resize(1440, 1024)
        
        # Main layout for the widget
        mainLayout = QVBoxLayout(self)
        
        # Signal 1 Viewer
        self.signal1Viewer = QtWidgets.QFrame(self)
        self.signal1Viewer.setStyleSheet("background-color: #2D2D2D;border:none;")
        self.signal1Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        self.signal1PlotLayout = QVBoxLayout(self.signal1Viewer)
        self.signal1PlotLayout.setContentsMargins(5, 5, 5, 5)

        self.canvas1 = MplCanvas(self.signal1Viewer, width=5, height=4, dpi=100, signal_color="#D55877")
        
        self.titleToolbarLayout1 = QHBoxLayout()
        self.signal1Title = QLabel("Channel 1", self.signal1Viewer)
        self.signal1Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.titleToolbarLayout1.addWidget(self.signal1Title)
        
        self.signal1TitleEditButton = QPushButton(self.signal1Viewer)
        self.signal1TitleEditButton.setIcon(QtGui.QIcon("photos/edit.png"))
        self.signal1TitleEditButton.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signal1TitleEditButton.setFixedSize(20, 20)
        self.signal1TitleEditButton.clicked.connect(lambda: self.editTitle(self.signal1Title, self.titleToolbarLayout1))
        self.titleToolbarLayout1.addWidget(self.signal1TitleEditButton)

        
        self.signal1PlotLayout.addLayout(self.titleToolbarLayout1, stretch=1)  

       
        self.signal1PlotLayout.addWidget(self.canvas1, stretch=13)  

        spacer = QSpacerItem(1000, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout1.addSpacerItem(spacer)
        
       

        self.signal1PlotLayout.addLayout(self.titleToolbarLayout1)
        self.signal1PlotLayout.addWidget(self.canvas1)

        # Time labels and buttons
        self.Signal1buttonsLayout = QHBoxLayout()
        self.Signal1buttonsLayout .addStretch(1)
        self.Signal1buttonsLayout  = QHBoxLayout()
        self.Signal1buttonsLayout .addSpacing(30)
      
        self.timeLabel1 = QtWidgets.QLabel("00:00", self.signal1Viewer)
        self.timeLabel1.setStyleSheet(labelStyle)
        self.Signal1buttonsLayout.addWidget(self.timeLabel1)
        self.Signal1buttonsLayout .addSpacing(70)

        self.pauseButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.clicked.connect(self.pauseActionChannel1)
        self.Signal1buttonsLayout.addWidget(self.pauseButton)

        self.playButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.clicked.connect(self.playActionChannel1)
        self.Signal1buttonsLayout.addWidget(self.playButton)

        self.toStartButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toStartButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.toStartButton.setStyleSheet(signalControlButtonStyle)
        self.toStartButton.clicked.connect(self.toStartAction1)
        self.Signal1buttonsLayout.addWidget(self.toStartButton)

        self.toEndButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.toEndButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.toEndButton.setStyleSheet(signalControlButtonStyle)
        self.toEndButton.clicked.connect(self.toEndAction1)
        self.Signal1buttonsLayout.addWidget(self.toEndButton)

        self.rewindButton = QtWidgets.QPushButton(self.signal1Viewer)
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setCheckable(True)
        self.rewindButton.toggled.connect(self.toggleRewind)
        self.Signal1buttonsLayout.addWidget(self.rewindButton)

        self.Signal1buttonsLayout.addStretch(6)  
        self.signal1PlotLayout.addLayout(self.Signal1buttonsLayout)
        
        mainLayout.addWidget(self.signal1Viewer)
        spacer_between_signals = QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mainLayout.addSpacerItem(spacer_between_signals)
        
        self.signal2Viewer = QtWidgets.QFrame(self)
        self.signal2Viewer.setStyleSheet("background-color: #2D2D2D; border:none;")
        self.signal2Viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.signal2PlotLayout = QVBoxLayout(self.signal2Viewer)
        self.signal2PlotLayout.setContentsMargins(5, 5, 5, 5)

        self.canvas2 = MplCanvas(self.signal2Viewer, width=5, height=4, dpi=100, signal_color="#76D4D4")

        self.titleToolbarLayout2 = QHBoxLayout()
        self.signal2Title = QLabel("Channel 2", self.signal2Viewer)
        self.signal2Title.setStyleSheet("color: #87EDF1; font-size:15px;")
        self.titleToolbarLayout2.addWidget(self.signal2Title)

        self.signal2TitleEditButton = QPushButton(self.signal2Viewer)
        self.signal2TitleEditButton.setIcon(QtGui.QIcon("photos/edit.png"))
        self.signal2TitleEditButton.setStyleSheet("background-color: #2D2D2D; border: none;")
        self.signal2TitleEditButton.setFixedSize(20, 20)
        self.signal2TitleEditButton.clicked.connect(lambda: self.editTitle(self.signal2Title, self.titleToolbarLayout2))
        self.titleToolbarLayout2.addWidget(self.signal2TitleEditButton)

        spacer = QSpacerItem(1000, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.titleToolbarLayout2.addSpacerItem(spacer)
        
        self.signal2PlotLayout.addLayout(self.titleToolbarLayout2, stretch=1)  
        self.signal2PlotLayout.addWidget(self.canvas2, stretch=13)  

        self.Signal2buttonsLayout = QHBoxLayout()
        self.Signal2buttonsLayout .addStretch(1)
        self.Signal2buttonsLayout .addSpacing(30)

        self.timeLabel2 = QtWidgets.QLabel("00:00", self.signal2Viewer)
        self.timeLabel2.setStyleSheet(labelStyle)
        self.Signal2buttonsLayout.addWidget(self.timeLabel2)
        self.Signal2buttonsLayout.addSpacing(70)

        self.pauseButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.pauseButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.pauseButton2.setStyleSheet(signalControlButtonStyle)
        self.pauseButton2.clicked.connect(self.pauseActionChannel2)
        self.Signal2buttonsLayout.addWidget(self.pauseButton2)

        self.playButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.playButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.playButton2.setStyleSheet(signalControlButtonStyle)
        self.playButton2.clicked.connect(self.playActionChannel2)
        self.Signal2buttonsLayout.addWidget(self.playButton2)

        self.toStartButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toStartButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/start.png"))
        self.toStartButton2.setStyleSheet(signalControlButtonStyle)
        self.toStartButton2.clicked.connect(self.toStartAction2)
        self.Signal2buttonsLayout.addWidget(self.toStartButton2)

        self.toEndButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.toEndButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/end.png"))
        self.toEndButton2.setStyleSheet(signalControlButtonStyle)
        self.toEndButton2.clicked.connect(self.toEndAction2)
        self.Signal2buttonsLayout.addWidget(self.toEndButton2)

        self.rewindButton2 = QtWidgets.QPushButton(self.signal2Viewer)
        self.rewindButton2.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton2.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton2.setCheckable(True)
        self.rewindButton2.toggled.connect(self.toggleRewind2)
        self.Signal2buttonsLayout.addWidget(self.rewindButton2)

        self.Signal2buttonsLayout.addStretch(6)  
        self.signal2PlotLayout.addLayout(self.Signal2buttonsLayout)
        
        mainLayout.addWidget(self.signal2Viewer)

        
    def pauseActionChannel1(self):
        self.parent().anim1.event_source.stop()
        self.parent().is_paused1 = True

    def playActionChannel1(self):
        if self.parent().is_paused1:
            self.parent().anim1.event_source.start()
            self.parent().is_paused1 = False

    def toStartAction1(self):
        current_ylim = self.canvas1.ax.get_ylim()
        self.canvas1.ax.set_xlim([0, 0])  
        self.canvas1.ax.set_ylim(current_ylim)  
        self.canvas1.draw()  

    def toEndAction1(self):
        current_ylim = self.canvas1.ax.get_ylim()
        self.canvas1.ax.set_xlim([10, 10])  
        self.canvas1.ax.set_ylim(current_ylim) 
        self.canvas1.draw()  

    def toggleRewind(self, checked):
        self.parent().rewind_enabled1 = checked
        if checked:
            self.parent().reset_signal_animation(1) 
            self.rewindButton.setStyleSheet(rewindOnButtonStyle) 
        else:
            self.rewindButton.setStyleSheet(rewindOffButtonStyle) 



    def pauseActionChannel2(self):
        self.parent().anim2.event_source.stop()
        self.parent().is_paused2 = True

    def playActionChannel2(self):
        if self.parent().is_paused2:
            self.parent().anim2.event_source.start()
            self.parent().is_paused2 = False

    def toStartAction2(self):
        current_ylim = self.canvas2.ax.get_ylim()
        self.canvas2.ax.set_xlim([0, 0])  
        self.canvas2.ax.set_ylim(current_ylim)  
        self.canvas2.draw()  

    def toEndAction2(self):
        current_ylim = self.canvas2.ax.get_ylim()
        self.canvas2.ax.set_xlim([10, 10])  
        self.canvas2.ax.set_ylim(current_ylim) 
        self.canvas2.draw()  

    def toggleRewind2(self, checked):
        """Enable or disable the rewind functionality based on button toggle."""
        self.parent().rewind_enabled2 = checked
        if checked:
            self.parent().reset_signal_animation(2) 
            self.rewindButton2.setStyleSheet(rewindOnButtonStyle) 
        else:
            self.rewindButton2.setStyleSheet(rewindOffButtonStyle) 
    def editTitle(self, label, layout):
        edit_line = QLineEdit(label.text(), self.signal1Viewer)

        edit_line.setMaxLength(12)

        edit_line.setStyleSheet("color: #EFEFEF; font-size:15px; background-color:#2D2D2D;")

        def save_changes():
            new_text = edit_line.text()

            label.setText(new_text)

            layout.replaceWidget(edit_line, label)

            edit_line.deleteLater()

        edit_line.returnPressed.connect(save_changes)

        edit_line.setFocus()

        layout.replaceWidget(label, edit_line)

        # Add a focus out event handler to restore the QLabel state

        def on_focus_out(event):
            if event.reason() == QtCore.Qt.FocusReason.LostFocus:
                layout.replaceWidget(edit_line, label)

                edit_line.deleteLater()

        edit_line.focusOutEvent = on_focus_out


class SignalMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignalMainWindow, self).__init__()
        self.signals = Signals()
        self.setCentralWidget(self.signals)
        self.default_path = 'D:\Faculty\SBE 24-25\DSP\Final\Signal-Viewer-Team18\signals_data\ECG_Abnormal.csv'
        self.default_signal = DataLoader(self.default_path).get_data()
        self.init_plot(self.default_signal ,3)

    @QtCore.pyqtSlot(pd.DataFrame, int)    
    def init_plot(self, signal_data, selectedChannel):
        
        time = signal_data.iloc[:, 0]
        amplitude = signal_data.iloc[:, 1]

        print(signal_data, selectedChannel)
        
        if selectedChannel == 1:
            self.update_canvas(self.signals.canvas1, time, amplitude)
            self.anim1 = FuncAnimation(self.signals.canvas1.figure, self.animate_cine_mode, frames=len(time),
                                       interval=100, fargs=(self.signals.canvas1, time, amplitude))
        elif selectedChannel == 2:
            self.update_canvas(self.signals.canvas2, time, amplitude)
            self.anim2 = FuncAnimation(self.signals.canvas2.figure, self.animate_cine_mode, frames=len(time),
                                       interval=100, fargs=(self.signals.canvas2, time, amplitude))
        else:
            # If unspecified, update both canvases with the same signal
            self.update_canvas(self.signals.canvas1, time, amplitude)
            self.anim1 = FuncAnimation(self.signals.canvas1.figure, self.animate_cine_mode, frames=len(time),
                                       interval=100, fargs=(self.signals.canvas1, time, amplitude))
            self.update_canvas(self.signals.canvas2, time, amplitude)
            self.anim2 = FuncAnimation(self.signals.canvas2.figure, self.animate_cine_mode, frames=len(time),
                                       interval=100, fargs=(self.signals.canvas2, time, amplitude))

    def animate_cine_mode(self, i, canvas, time, amplitude):
        """Animate the signal in cine mode by looping over the data."""
        # Define a window size for the data (number of points to display at once)
        window_size = 100

        # Compute the start and end indices for the window
        start_idx = i % len(time)
        end_idx = (start_idx + window_size) % len(time)

        if start_idx < end_idx:
            t_window = time[start_idx:end_idx]
            amp_window = amplitude[start_idx:end_idx]
        else:
            # If the window wraps around the end of the signal
            t_window = np.concatenate((time[start_idx:], time[:end_idx]))
            amp_window = np.concatenate((amplitude[start_idx:], amplitude[:end_idx]))

        # Update the plot with the new window of data
        canvas.update_plot(t_window, amp_window)

    def update_canvas(self, canvas, t, signal):
        """Update the plot with the entire signal (initial plot)."""
        canvas.update_plot(t, signal)

    def update_signal1(self, frame):
        if not self.is_paused1:
            if self.rewind_enabled1:
                self.current_frame1 = (frame + 1) % self.total_frames
            else:
                self.current_frame1 = frame
                if self.current_frame1 >= self.total_frames - 1:  
                    self.is_paused1 = True

        
        self.signals_widget.canvas1.update_plot(self.t[:self.current_frame1], self.signal1[:self.current_frame1])

    def update_signal2(self, frame):
        if not self.is_paused2:
            if self.rewind_enabled2:
                self.current_frame2 = (frame + 1) % self.total_frames
            else:
                self.current_frame2 = frame
                if self.current_frame2 >= self.total_frames - 1:  
                    self.is_paused2 = True

   
        self.signals_widget.canvas2.update_plot(self.t[:self.current_frame2], self.signal2[:self.current_frame2])

    def reset_signal_animation(self, channel):
        """Resets the animation to start over for the specified channel."""
        if channel == 1:
            self.current_frame1 = 0  
            self.is_paused1 = False  
            self.anim1.event_source.stop()  
            self.anim1.event_source.start()  
        elif channel == 2:
            self.current_frame2 = 0  
            self.is_paused2 = False  
            self.anim2.event_source.stop()  
            self.anim2.event_source.start()  



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SignalMainWindow()
    window.show()
    sys.exit(app.exec_())
