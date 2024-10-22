import sys
import numpy as np
from PyQt5 import QtWidgets
from SignalViewer import Viewer
from Core.Data_load import DataLoader

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    csv_file_path = 'Signal-Viewer-Team18\signals_data\ECG_Abnormal.csv'
    data_loader = DataLoader(csv_file_path)
    data_loader.load_data()

    # Get the loaded data
    data = data_loader.get_data()
    print(data)
    x_data = data[:, 0]
    y_data = data[:, 1]
    plot_data_list = [{'x_data': x_data, 'y_data': y_data},
                      {'x_data': np.linspace(0, 10, 1000), 'y_data': np.sinh(np.linspace(0, 10, 1000))}]

    viewer = Viewer(plot_data_list)
    viewer.setWindowTitle("Signal Viewer")
    viewer.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
