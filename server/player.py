import uuid

class Player:

    def __init__(self, playerName: str, addr, conn):
        self.__playerName = playerName
        self.__playerID = str(uuid.uuid4())
        self.__addr = addr
        self.__conn = conn
        self.__roomID = None

    @property
    def playerName(self):
        return self.__playerName

    @property
    def playerID(self):
        return self.__playerID

    @property
    def addr(self):
        return self.__addr

    @property
    def conn(self):
        return self.__conn

    @property
    def roomID(self):
        return self.__roomID

    @roomID.setter
    def roomID(self, roomID):
        self.__roomID = roomID

    def __str__(self):
        return f"{self.__playerName} ID: {self.__playerID}"

    def __repr__(self):
        return f"{self.__playerName} ID: {self.__playerID}"