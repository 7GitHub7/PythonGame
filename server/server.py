import json
import socket
import threading
from player import Player
from room import Room

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)

class Server():

    playersMap = {}
    roomsMap = {}

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            data = conn.recv(2048)
            data = json.loads(data)
            print(data)
            if not self.route(conn, addr, data):
                connected = False
                print(f"[DISCONNECT] {addr}")

    def route(self, conn, addr, data):
        action = data['action']

        if action == 'disconnect':
            player = self.playersMap[data["playerID"]]
            if player.roomID:
                del self.roomsMap[player.roomID]
            del self.playersMap[data["playerID"]]
            self.send(conn,True)
            conn.close()
            return False

        elif action == 'register':
            player = Player(data["name"], addr, conn)
            print(f"[NEW PLAYER] {player}")
            self.playersMap[player.playerID] = player
            self.send(conn, player.playerID)

        elif action == "createRoom":
            room = Room(data["name"])
            self.roomsMap[room.roomID] = room
            room.addPlayer(self.playersMap[data["playerID"]])
            print(f"[NEW ROOM] {room}")
            self.send(conn, room.roomID)

        elif action == "joinToRoom":
            room = self.roomsMap[data['roomID']]
            if room:
                player = self.playersMap[data["playerID"]]
                result = room.addPlayer(player)
                if result:
                    player.roomID = room.roomID
                    self.send(room.playerList[0].conn, {'action' : 'startGame'})
            else:
                result = False
            self.send(conn, result)

        elif action == "getRoomList":
            listRoom = []
            for room in self.roomsMap.values():
                listRoom.append([room.roomName, room.roomID, room.numberOfPlayers])
            self.send(conn, listRoom)

        elif action == 'currentPlayer':
            room = self.roomsMap[data['roomID']]
            self.send(conn, {'action': "currentPlayer", "currentPlayer": [room.currentPlayer.playerName, room.currentPlayer.playerID]})

        elif action == "updateBoard":
            room = self.roomsMap[data['roomID']]
            room.board = data['board']
            self.send(conn, {'action': 'updateBoard'})

        elif action == 'getBoard':
            room = self.roomsMap[data['roomID']]
            self.send(conn, {'action': 'getBoard', 'board': room.board})

        elif action == 'endGame':
            if data['roomID'] in self.roomsMap.keys():
                room = self.roomsMap[data['roomID']]
                for playerRoom in room.playerList:
                    self.send(playerRoom.conn, {'action': 'endGame', 'reason': data['reason']})
                    playerRoom.roomID = None

        elif action == 'changePlayer':
            room = self.roomsMap[data['roomID']]
            room.changePlayer()
            self.send(room.currentPlayer.conn, {'action' : 'changePlayer'})

        return True


    def send(self, conn, data):
        message = json.dumps(data)
        conn.send(message.encode())

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    server = Server()
    print("[STARTING] server is starting...")
    server.start()