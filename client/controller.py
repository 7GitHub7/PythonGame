from PyQt5.QtWidgets import (QStackedWidget,QFrame,QWidget, QApplication,QLabel ,QTabWidget,
                            QVBoxLayout,QCheckBox,QHBoxLayout,QPushButton,QLineEdit,QListWidget,QLabel,QGridLayout,QFormLayout)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette
from PyQt5.QtCore import QRect, Qt
from worker import ServerListener

import sys
import numpy as np
from client import *
import math
from game import Game

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Controller():

    def __init__(self, main):
        self.main = main
        self.player = Client()
        self.thread = ServerListener(self.player.client)
        self.thread.route.connect(self.routeGame)
        self.main.list.currentItemChanged.connect(self.selected_room)
        self.main.btn_add_room.clicked.connect(self.create_room)
        self.main.btn_get_rooms.clicked.connect(self.refreshList)
        self.main.btn_enter_room.clicked.connect(self.enterToRoom)


    def refreshList(self):
        self.main.rooms = self.player.getRoomList()
        self.main.rooms.sort(key=lambda x: x[0])
        self.main.list.clear()
        for room in self.main.rooms:
            self.main.list.addItem(f"{room[0]} The current number of players {room[2]}")

    def selected_room(self):
        if self.main.rooms:
            selectedRoom = self.main.rooms[self.main.list.currentRow()]
            self.main.selected_room_input.setText(selectedRoom[0])

    def create_room(self):
        if self.main.room_name_input.text():
            self.player.createRoom(self.main.room_name_input.text())
            self.refreshList()
            self.thread.start()
            self.main.info_label.setText(f"Stworzono pokój: {self.main.room_name_input.text()}. Poczekaj na drugiego gracza.")
            self.main.btn_add_room.setDisabled(True)
            self.main.btn_enter_room.setDisabled(True)
            self.main.btn_get_rooms.setDisabled(True)
            self.main.game.color = 1
        else:
            self.main.info_label.setText("Wpisz nazwę pokoju")

    def enterToRoom(self):
        if len(self.main.selected_room_input.text()) > 0:
            for room in self.main.rooms:
                if room[0] == self.main.selected_room_input.text():
                    if self.player.joinToRoom(room[1]):
                        self.routeGame({'action': 'startGame'})
                        self.main.game.color = 2
                        self.main.next_page()
                    else:
                        self.main.info_label.setText("Nie można wejść do pokoju")
                    break
            else:
                self.main.info_label.setText("Nie znaleziono pokoju")
        else:
            self.main.info_label.setText("Nie wybrano pokoju")

    def routeGame(self, data):

        action = data['action']

        if action == 'startGame':
            if not self.thread.isRunning():
                self.thread.start()
            self.player.getCurrentPlayer()
            self.main.game.player = self.player
            self.main.game.thread = self.thread
            self.main.game.resultTable = self.main.resultTable
            self.main.resultTable.startTimer()
            self.main.next_page()

        elif action == 'currentPlayer':
            self.main.resultTable.setCurrentPlayer(data['currentPlayer'][0])
            self.main.game.currentPlayer = data['currentPlayer']

        elif action == 'getBoard':
            self.main.game.board = np.asarray(data['board'])
            self.main.game.update()

        elif action == 'updateBoard':
            self.player.changePlayer()
            self.player.getCurrentPlayer()

        elif action == 'changePlayer':
            self.player.getCurrentPlayer()
            self.player.getBoard()

        elif action == 'endGame':
            time = self.main.resultTable.stopTimer()
            if data['reason'] == 'four':
                self.main.game.showDialog(f"Wygrał {self.main.game.currentPlayer[0]}\nCzas gry: {time}")
            else:
                self.main.game.showDialog(f"Gra została przerwana")