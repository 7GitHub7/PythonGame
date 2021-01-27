from PyQt5.QtWidgets import (QStackedWidget,QFrame,QWidget, QApplication,QLabel ,QTabWidget,
                            QVBoxLayout,QCheckBox,QHBoxLayout,QPushButton,QLineEdit,QListWidget,QLabel,QGridLayout,QFormLayout)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette
from PyQt5.QtCore import QRect, Qt, QTime, QTimer
from worker import ServerListener
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import QSize


import sys
import numpy as np
from client import *
import math
from Game import Game
from Controller import Controller


class ResulTable(QWidget):

    def __init__(self):
        super().__init__()
        self.__createTable()
        self.setFixedSize(500,200)

    def __createTable(self):
        vBox = QVBoxLayout(self)

        self.curr_time = QTime(00, 00, 00)
        self.timer = QTimer()
        self.timer.timeout.connect(self.__time)

        self.current_player_label = QLabel()
        self.current_player_label.setStyleSheet("font: 20pt Century Gothic")
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font: 15pt Century Gothic")

        vBox.addWidget(self.current_player_label)
        vBox.addWidget(QHLine())
        vBox.addWidget(self.time_label)
        vBox.addWidget(QHLine())

    def setCurrentPlayer(self, playerName):
        self.current_player_label.setText(f"Ruch gracza: {playerName}")

    def startTimer(self):
        self.timer.start(1000)

    def stopTimer(self):
        self.timer.stop()
        self.curr_time = QTime(00, 00, 00)
        self.time_label.setText(f"Czas: {self.curr_time.toString('hh:mm:ss')}")
        return self.curr_time.toString('hh:mm:ss')

    def __time(self):
        self.curr_time = self.curr_time.addSecs(1)
        self.time_label.setText(f"Czas: {self.curr_time.toString('hh:mm:ss')}")


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.setGeometry(150, 150, 700, 500)
        self.mouse_clik_counter = 0
        self.controller = None
 

    def closeEvent(self, event):
        if self.controller:
            self.controller.player.disconnect()

    def initUI(self):

        self.stacked_widget = QStackedWidget()

        hbox = QHBoxLayout()
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.stacked_widget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def set_button_state(self, index):
        n_pages = len(self.stacked_widget)
        self.next_button.setEnabled( index % n_pages < n_pages - 1)

    def insert_page(self, widget, index=-1):
        self.stacked_widget.insertWidget(index, widget)
        self.set_button_state(self.stacked_widget.currentIndex())

    def next_page(self):
        new_index = self.stacked_widget.currentIndex()+1
        if new_index < len(self.stacked_widget):
            self.stacked_widget.setCurrentIndex(new_index)

        if self.mouse_clik_counter == 0:
            self.resize(600, 650)
            self.update()
            self.mouse_clik_counter += 1
            self.controller = Controller(self)
            self.controller.player.register(self.player_name_input.text())
            self.controller.refreshList()

        if self.mouse_clik_counter == 2:
            self.game.setFixedSize(700,750)
            self.update()

        if self.mouse_clik_counter == 1:
            self.mouse_clik_counter += 1

    def back_page(self):
        try:
            self.game.board = np.zeros((6, 7))
            self.mouse_clik_counter -= 1
            self.resize(600, 650)
            self.stacked_widget.setCurrentIndex(1)
            self.btn_add_room.setDisabled(False)
            self.btn_enter_room.setDisabled(False)
            self.btn_get_rooms.setDisabled(False)
            self.selected_room_input.clear()
            self.room_name_input.clear()
            self.info_label.clear()
            self.update()
            self.controller.refreshList()
        except Exception as e:
            print(e)

    def quit_game(self):
        if not self.controller.thread.isRunning():
            self.controller.thread.start()
        self.controller.player.endGame("quit")

        self.back_page()
        self.controller.player.roomID = None

    def welcomeTabUI(self):
        """Strona pierwsza, z nazwą gracza i tekstem powitalnym"""
        self.grid = QFormLayout()
        
        self.grid.setFormAlignment(Qt.AlignTop|Qt.AlignTop|Qt.AlignTop) 
        self.next_button = QPushButton('Potwierdz')
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.next_page)
        
        self.verticalSpacer = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Expanding)

    
        self.player_name_input = QLineEdit('Player')

        self.player_name_label = QLabel("Podaj swoją nazwę gracza", self)
        self.title_label = QLabel("Witaj w Connect4", self)
        self.title_label.setStyleSheet("font: 22pt Century Gothic")
        self.player_name_label.setStyleSheet("font: 15pt Century Gothic")
        self.title_label.setAlignment(Qt.AlignLeading|Qt.AlignCenter|Qt.AlignCenter)
        self.player_name_label.setAlignment(Qt.AlignCenter|Qt.AlignCenter|Qt.AlignCenter)
        self.player_name_input.setAlignment(Qt.AlignCenter|Qt.AlignCenter|Qt.AlignCenter)
        self.grid.addWidget(self.title_label)
        self.grid.addItem(self.verticalSpacer)
        self.grid.addWidget(self.player_name_label)
        self.grid.addWidget(self.player_name_input)
        self.grid.addItem(self.verticalSpacer)
        self.grid.addWidget(self.next_button)

        generalTab = QWidget()
        generalTab.setLayout(self.grid)
      
        return generalTab

    def networkTabUI(self):
        """Strona druga - ustawienia"""

        """init boxes"""
        self.networkTab = QWidget()
        self.layout_main = QVBoxLayout()
        self.layout_create_room = QHBoxLayout()


        """Create room layout"""
        self.room_name_input = QLineEdit(self)
        self.room_name_label = QLabel("Nazwa", self)
        self.layout_create_room.addWidget(self.room_name_label)
        self.layout_create_room.addWidget(self.room_name_input)

        """Main layout"""
        self.list = QListWidget()
        self.btn_add_room = QPushButton('Dodaj pokój')
        self.btn_get_rooms = QPushButton('Odśwież listę pokoi')
        self.selected_room_input = QLineEdit()
        self.btn_enter_room = QPushButton('Wejdź do pokoju')
        self.btn_enter_room.clicked.connect(self.next_page)
        self.info_label = QLabel()
        self.info_label.setStyleSheet("font: 15pt Century Gothic; color: red")
        self.layout_main.addWidget(QLabel("Stwórz nowy pokój", self))
        self.layout_main.addLayout(self.layout_create_room)
        self.layout_main.addWidget(self.btn_add_room)
        self.layout_main.addWidget(self.btn_get_rooms)
        self.layout_main.addWidget(QHLine())
        self.layout_main.addWidget(QLabel("Wybierz pokój", self))
        self.layout_main.addWidget(self.list)
        self.layout_main.addWidget(self.selected_room_input)
        self.layout_main.addWidget(self.btn_enter_room)
        self.layout_main.addWidget(self.info_label)
        self.networkTab.setLayout(self.layout_main)

        return self.networkTab    

    def gameTabUI(self):
        """Strona trzecia - gra"""
        generalTab = QWidget()
        self.resultTable = ResulTable()
        self.game = Game(self)
        self.btn_quit_game = QPushButton("Opuść grę")
        self.btn_quit_game.clicked.connect(self.quit_game)

        vBox = QVBoxLayout()

        layout = QHBoxLayout()
        layout.addWidget(self.game)
        layout.addLayout(vBox)
        vBox.addWidget(self.btn_quit_game)

        vBox.addWidget(self.resultTable)

        generalTab.setLayout(layout)

        return generalTab

if __name__ == '__main__':
     app = QApplication(sys.argv)
     palette = QPalette()
     palette.setBrush(QPalette.Background, QBrush(QPixmap("image.png")))
     app.setPalette(palette)
     ex = Main()
     ex.show()
     ex.insert_page(ex.welcomeTabUI())
     ex.insert_page(ex.networkTabUI())
     ex.insert_page(ex.gameTabUI())
     sys.exit(app.exec_())
