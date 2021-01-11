import json
import threading
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.56.1"
SERVER = "localhost"
ADDR = (SERVER, PORT)

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

class Client:

    def __init__(self, playerName: str):
        self.playerName = playerName
        self.playerID = None
        self.roomID = None
        self.register()

    def register(self):
        self.playerID = self.sendAndReceive({"action": "register", "name": self.playerName})
        print(self.playerID)

    def sendAndReceive(self, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        msgSend = json.dumps(message)
        client.send(msgSend.encode())
        msgRecv = json.loads(client.recv(2048))
        client.close()
        return msgRecv

    def createRoom(self, roomName: str):
        self.roomID = self.sendAndReceive({"action": "createRoom", "name": roomName, "playerID": self.playerID})
        print(self.roomID)


if __name__ == "__main__":

    player = Client("PlayerXD")
    player.createRoom("ddddsfsdf")
