import json
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)

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

    def send(self, message):
        msgSend = json.dumps(message)
        self.client.send(msgSend.encode())

    def disconnect(self):
        disconnect = self.sendAndReceive({"action": "disconnect", "playerID": self.playerID})
        if disconnect:
            self.client.close()
            print("DISCONNECT")

    def createRoom(self, roomName: str):
        self.roomID = self.sendAndReceive({"action": "createRoom", "name": roomName, "playerID": self.playerID})

    def getRoomList(self):
        return self.sendAndReceive({"action": "getRoomList"})

    def joinToRoom(self, roomID):
        result = self.sendAndReceive({"action": "joinToRoom", "roomID": roomID, "playerID": self.playerID })
        if result:
            self.roomID = roomID
            return True
        return False

    def getCurrentPlayer(self):
        return self.sendAndReceive({"action": "currentPlayer", "roomID": self.roomID})

    def updateBoard(self, board):
        return self.sendAndReceive({"action": "updateBoard", "board": board, "roomID": self.roomID})

    def getBoard(self):
        return self.sendAndReceive({"action": "getBoard", "roomID": self.roomID})

    def changePlayer(self):
        self.send({"action": "changePlayer", "roomID": self.roomID})

    def endGame(self, reason):
        self.send({"action": "endGame", "roomID": self.roomID, "reason": reason})

