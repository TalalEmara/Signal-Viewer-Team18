
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QSpacerItem, QFrame, QFileDialog, QMainWindow
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from Styles import signalControlButtonStyle, labelStyle
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

        self.navToolbarLayout = QHBoxLayout()

        self.navToolbar = NavigationToolbar(self, parent)
        self.navToolbar.setStyleSheet("background-color: transparent;")
        self.navToolbar.setFixedHeight(25)  
        self.navToolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        for action in self.navToolbar.actions():
            if action.text() in ['Pan', 'Zoom']:
                action.setVisible(True)
                if action.text() == 'Pan':
                    action.setIcon(QIcon('E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/pan.png'))
                elif action.text() == 'Zoom':
                    action.setIcon(QIcon('E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/zoomIn.png'))
            else:
                action.setVisible(False)

       
        spacer = QSpacerItem(820, 20, QSizePolicy.Fixed, QSizePolicy.Minimum) 
        self.navToolbarLayout.addItem(spacer)

 
        self.navToolbarLayout.addWidget(self.navToolbar)

        self.zoomOutButton = QPushButton("", parent)
        self.zoomOutButton.setIcon(QtGui.QIcon("E:\Programming programs\Web dev\Signal-Viewer-Team18\GUI\photos/zoomOut.png"))
        self.zoomOutButton.setStyleSheet("background-color: #242424; color: #FFFFFF; border: none;")
        self.zoomOutButton.setFixedSize(25, 25)
        self.zoomOutButton.clicked.connect(self.zoom_out)

      
        self.navToolbarLayout.addWidget(self.zoomOutButton)

     
        self.toolbarLayout.addLayout(self.navToolbarLayout)
        self.toolbarLayout.addWidget(self)

      
        self.toolbarLayout.setAlignment(self.navToolbarLayout, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

    def update_plot(self, t, signal):
        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view()
        self.draw()

    def zoom_out(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] - 0.5, xlim[1] + 0.5])
        self.ax.set_ylim([ylim[0] - 0.5, ylim[1] + 0.5])
        self.draw()


class GlueWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glued signal")
        self.setStyleSheet("background-color:#242424;")
        self.setContentsMargins(10,10,10,10)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.snapshots = []  
        self.signal_data = None  



        self.mpl_canvas = MplCanvas(self)

        self.titleToolbarLayout = QHBoxLayout()
        self.title = QLabel("Gluing signals")
        self.title.setStyleSheet(labelStyle)
        self.title.setFixedHeight(70)
        self.titleToolbarLayout.addWidget(self.title)


        self.snapShotButton = QPushButton("SnapShot", self)
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

        self.exportPdfButton = QPushButton("Export to PDF", self)
        self.exportPdfButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exportPdfButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #EFEFEF;
                border-radius: 5px;
                background-color: #2D2D2D; 
                color: #EFEFEF;
                width:120px;
                font-size:17px;
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

        
        graphRow = QHBoxLayout()
        graphRow.addWidget(self.mpl_canvas)

        buttonRow = QHBoxLayout()
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

        buttonRow.addStretch()
        buttonRow.addWidget(self.backwordButton)
        buttonRow.addWidget(self.forwordButton)
        buttonRow.addStretch()


        main_layout.addLayout(self.titleToolbarLayout, 10)
        main_layout.addLayout(graphRow, 10)
        main_layout.addLayout(buttonRow, 80)


        self.setMinimumSize(1000, 700)
        self.show()

    def update_plot(self, x, y):
        self.mpl_canvas.ax.clear()  
        self.mpl_canvas.line.set_xdata(x)
        self.mpl_canvas.line.set_ydata(y)
        self.mpl_canvas.ax.set_xlim(min(x), max(x)) 
        self.mpl_canvas.ax.set_ylim(-1.2, 1.2)  
        self.mpl_canvas.ax.set_xlabel("X-axis")
        self.mpl_canvas.ax.set_ylabel("Y-axis")
        self.mpl_canvas.draw() 
    
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
        
       
        self.mpl_canvas.update_plot(t, signal)
        self.mpl_canvas.figure.savefig(snapshot['image_path'])  

    def export_to_pdf(self):
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")

        if save_path:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            table_col_width = 40 
            table_total_width = 2 * table_col_width  
            page_width = 210  
            x_offset = (page_width - table_total_width) / 2 
            image_width = 180  
            image_x_offset = (page_width - image_width) / 2  

            for idx, snapshot in enumerate(self.snapshots):
                pdf.add_page()

           
                pdf.set_font('Arial', 'B', 16)
                title_width = pdf.get_string_width(f'Snapshot {idx + 1}')
                pdf.set_x((page_width - title_width) / 2) 
                pdf.cell(0, 10, f'Snapshot {idx + 1}', ln=True)

                pdf.ln(10)

           
                pdf.set_font('Arial', 'B', 12)

               
                pdf.set_x(x_offset)  
                pdf.cell(table_col_width, 10, 'Statistic', 1, 0, 'C')
                pdf.cell(table_col_width, 10, 'Value', 1, 1, 'C')

              
                pdf.set_font('Arial', '', 12)

              
                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, 'Mean', 1)
                pdf.cell(table_col_width, 10, f'{snapshot["mean"]:.4f}', 1, 1)
                
                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, 'Std Dev', 1)
                pdf.cell(table_col_width, 10, f'{snapshot["std"]:.4f}', 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, 'Min', 1)
                pdf.cell(table_col_width, 10, f'{snapshot["min"]:.4f}', 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, 'Max', 1)
                pdf.cell(table_col_width, 10, f'{snapshot["max"]:.4f}', 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, 'Duration', 1)
                pdf.cell(table_col_width, 10, f'{snapshot["duration"]:.4f}', 1, 1)

              
                pdf.ln(10)

              
                pdf.image(snapshot['image_path'], x=image_x_offset, y=None, w=image_width)  

            pdf.output(save_path)
    

    def save_snapshot_image(self, filepath):
       
        self.figure.savefig(filepath)

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