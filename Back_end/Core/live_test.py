import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from websocket import WebSocketApp


class WebSocketClient(QThread):
    # Signal to send data to the main GUI thread
    data_received = pyqtSignal(dict)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.ws = WebSocketApp(url, on_message=self.on_message)

    def run(self):
        self.ws.run_forever()  # Start the WebSocket client

    def on_message(self, ws, message):
        data = json.loads(message)  # Assuming the message is in JSON format
        self.data_received.emit(data)  # Emit the signal with the data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Signal Display")
        self.setGeometry(100, 100, 600, 400)

        # Create a layout and a label to display the signal
        layout = QVBoxLayout()
        self.label = QLabel("Waiting for data...", self)
        layout.addWidget(self.label)

        # Create a central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Start the WebSocket client
        self.websocket_client = WebSocketClient("ws://localhost:5000/socket.io/?EIO=4&transport=websocket")
        self.websocket_client.data_received.connect(self.update_signal)
        self.websocket_client.start()  # Start the thread

    def update_signal(self, data):
        # Update the label with the received signal data
        self.label.setText(f"Received Signal: {data['signal_value']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
