import json

from PyQt5.QtCore import QThread, pyqtSignal

class ServerListener(QThread):

    route = pyqtSignal(dict)
    def __init__(self, client, parent=None):
        QThread.__init__(self, parent)
        self.client = client

    def run(self):
        data = json.loads(self.client.recv(2048))
        print(data)
        self.route.emit(data)

