import json

from PyQt5.QtCore import QThread, pyqtSignal

class ServerListener(QThread):

    route = pyqtSignal(dict)
    def __init__(self, client, parent=None):
        QThread.__init__(self, parent)
        self.client = client

    def run(self):
        while True:
            data = json.loads(self.client.recv(2048))
            self.route.emit(data)
            if data['action'] == 'endGame':
                break

