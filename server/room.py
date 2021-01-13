import uuid, random
import numpy as np
from player import Player

class Room:

    def __init__(self, roomName: str):
        self.__roomName = roomName
        self.__roomID = str(uuid.uuid4())
        self.__playerList = []
        self.__numberOfPlayers = 0
        self.__currentPlayer = None
        self.__board = np.zeros((6,7))

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board):
        self.__board = board

    @property
    def roomName(self):
        return self.__roomName

    @property
    def roomID(self):
        return self.__roomID

    @property
    def playerList(self):
        return self.__playerList
    @property
    def currentPlayer(self):
        return self.__currentPlayer

    @property
    def numberOfPlayers(self):
        return self.__numberOfPlayers

    def addPlayer(self, player: Player):
        if self.__numberOfPlayers < 2:
            self.__playerList.append(player)
            self.__numberOfPlayers += 1
            if self.__numberOfPlayers == 2:
                self.__selectFirstPlayer()
            return True
        return False

    def __selectFirstPlayer(self):
        self.__currentPlayer = self.__playerList[random.randint(0,1)]

    def changePlayer(self):
        if self.__currentPlayer == self.__playerList[0]:
            self.__currentPlayer = self.__playerList[1]
        else:
            self.__currentPlayer = self.__playerList[0]

    def __str__(self):
        return f"{self.__roomName} ID: {self.__roomID} Players: {self.__numberOfPlayers}"

    def __repr__(self):
        return f"{self.__roomName} ID: {self.__roomID} Players: {self.__numberOfPlayers}"
