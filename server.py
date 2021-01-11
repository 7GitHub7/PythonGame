import json
import socket
import threading
from player import Player
from room import Room

HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

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
            data = conn.recv(1024)
            data = json.loads(data)
            if not self.route(conn, addr, data):
                connected = False
                print(f"[DISCONNECT] {addr}")

    def route(self,conn, addr, data):
        action = data['action']

        if action == 'disconnect':
            self.send(conn,True)
            conn.close()
            return False

        elif action == 'register':
            player = Player(data["name"], addr)
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
            result = room.addPlayer(self.playersMap[data["playerID"]])
            self.send(conn, result)

        elif action == "getRoomList":
            listRoom = []
            for room in self.roomsMap.values():
                listRoom.append([room.roomName, room.roomID])
            self.send(conn, listRoom)

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