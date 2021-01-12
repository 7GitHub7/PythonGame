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
# # client.bind(ADDR)
# client.connect(ADDR)

class Client:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.playerName = None
        self.playerID = None
        self.roomID = None

    def register(self, playerName):
        self.playerName = playerName
        self.playerID = self.sendAndReceive({"action": "register", "name": self.playerName})
        print(self.playerID)

    def sendAndReceive(self, message):
        msgSend = json.dumps(message)
        self.client.send(msgSend.encode())
        msgRecv = json.loads(self.client.recv(2048))
        return msgRecv

    def disconnect(self):
        disconnect = self.sendAndReceive({"action": "disconnect", "playerID": self.playerID})
        if disconnect:
            self.client.close()
            print("DISCONNECT")

    def createRoom(self, roomName: str):
        self.roomID = self.sendAndReceive({"action": "createRoom", "name": roomName, "playerID": self.playerID})

    def getRoomList(self):
        roomList = self.sendAndReceive({"action": "getRoomList"})
        return roomList

    def joinToRoom(self, roomID):
        result = self.sendAndReceive({"action": "joinToRoom", "roomID": roomID, "playerID": self.playerID })
        if result:
            self.roomID = roomID
            return True
        return False

# if __name__ == "__main__":

    # player = Client("PlayerXD")
    # player.createRoom("ddddsfsdf")
    # room = player.getRoomList()
    # player.joinToRoom(room[0][1])
    # player.disconnect()
