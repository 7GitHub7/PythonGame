import json

from PyQt5.QtCore import QObject, QThread, pyqtSignal

class ServerListener(QThread):

    def __init__(self, client, parent=None):
        QThread.__init__(self, parent)
        self.client = client

    def run(self):
        while True:
            print(json.loads(self.client.recv(2048)))
