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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.bind(ADDR)
client.connect(ADDR)

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
        msgSend = json.dumps(message)
        client.send(msgSend.encode())
        msgRecv = json.loads(client.recv(2048))
        return msgRecv

    def disconnect(self):
        disconnect = self.sendAndReceive({"action": "disconnect", "playerID": self.playerID})
        if disconnect:
            client.close()
            print("DISCONNECT")

    def createRoom(self, roomName: str):
        self.roomID = self.sendAndReceive({"action": "createRoom", "name": roomName, "playerID": self.playerID})
        print(self.roomID)

    def getRoomList(self):
        roomList = self.sendAndReceive({"action": "getRoomList"})
        print(roomList)
        return roomList

    def joinToRoom(self, roomID):
        result = self.sendAndReceive({"action": "joinToRoom", "roomID": roomID, "playerID": self.playerID })
        if result:
            self.roomID = roomID
        print(f'{self.roomID}: {result}')

if __name__ == "__main__":

    player = Client("PlayerXD")
    player.createRoom("ddddsfsdf")
    room = player.getRoomList()
    player.joinToRoom(room[0][1])
    player.disconnect()
