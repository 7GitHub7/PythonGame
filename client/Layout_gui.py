from PyQt5.QtWidgets import (QStackedWidget,QFrame,QWidget, QApplication,QLabel ,QTabWidget,
                            QVBoxLayout,QCheckBox,QHBoxLayout,QPushButton,QLineEdit,QListWidget,QLabel,QGridLayout,QFormLayout)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPalette
from PyQt5.QtCore import QRect, Qt
from worker import ServerListener
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import QSize


import sys
import numpy as np
from client import *
import math
from Game import Game
from Controller import Controller

ROW_COUNT = 6
COLUMN_COUNT = 7 
SQUARESIZE = 100
board = np.zeros((ROW_COUNT,COLUMN_COUNT))
board[0][6] = 2
board[1][6] = 2

controller = None

class ResulTable(QWidget):

    def __init__(self):
        super().__init__()
        self.__createTable()
        # self.size(QSize(100,100))
        self.setFixedSize(500,200)

    def __createTable(self):
        vBox = QVBoxLayout(self)
        self.current_player_label = QLabel()
        self.current_player_label.setStyleSheet("font: 20pt Century Gothic")

        vBox.addWidget(self.current_player_label)

    def setCurrentPlayer(self, playerName):
        self.current_player_label.setText(f"Ruch gracza: {playerName}")


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
        # self.next_button.clicked.connect(self.next_page)
        self.setGeometry(150, 150, 700, 500)
        self.mouse_clik_counter = 0
 

    def closeEvent(self, event):
        if self.player.playerID:
            self.player.disconnect()

    def initUI(self):

        # self.next_button = QPushButton('Dalej')
        # self.next_button.setEnabled(False)
        self.stacked_widget = QStackedWidget()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # hbox.addWidget(self.next_button)

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
            self.next_button.setText("Graj!")
            self.mouse_clik_counter += 1
            controller.player.register(self.player_name_input.text())
            controller.refreshList()

        if self.mouse_clik_counter == 2:
            self.game.setFixedSize(700,750)
            self.update()

        if self.mouse_clik_counter == 1:
            self.mouse_clik_counter += 1


    def welcomeTabUI(self):
        """Strona pierwsza, z nazwą gracza i tekstem powitalnym"""
        self.grid = QFormLayout()
        
        self.grid.setFormAlignment(Qt.AlignTop|Qt.AlignTop|Qt.AlignTop) 
        self.next_button = QPushButton('Potwierdz')
        self.next_button.setEnabled(False)
        # self.next_button.setGeometry(200, 150, 100, 40) 
        # self.next_button.resize(150, 50) 
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
        # self.list.currentItemChanged.connect(self.selected_room)
        self.btn_add_room = QPushButton('Dodaj pokój')
        # self.btn_add_room.clicked.connect(self.create_room)
        self.btn_get_rooms = QPushButton('Odśwież listę pokoi')
        # self.btn_get_rooms.clicked.connect(self.refreshList)
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
        self.game = Game() 
        
        layout = QHBoxLayout()
        player_panel_vbox = QVBoxLayout()
        player_active_hbox = QHBoxLayout()
        player_buttons_hbox = QHBoxLayout()

        moves_list = QListWidget()
        moves_list.addItem("1. Gracz XYZ. Kolumna 2, Wiersz: 1 ")
        moves_list.addItem("2. Gracz Szymon. Kolumna 6, Wiersz: 1 ")
        moves_list_label = QLabel(f"Przebieg spotkania")
        room_name_label = QLabel(f"Pokój: test")
        room_name_label.setStyleSheet("font: 15pt Century Gothic; color: black")
        time_label = QLabel(f"Czas: 00:00:00")
        btn_player_active_1 = QPushButton('PLayer 1')
        btn_player_active_2 = QPushButton('PLayer 2')
        btn_player_active_2.setEnabled(False)
        btn_end_game = QPushButton('rezygnuję')
        btn_undo_move = QPushButton('cofnij ruch')
        btn_player_active_1.setFixedSize(150,50)
        btn_player_active_2.setFixedSize(150,50)

        layout.addWidget(self.game)
        layout.addLayout(player_panel_vbox)
        
        player_panel_vbox.addWidget(room_name_label)
        player_panel_vbox.addLayout(player_active_hbox)

        player_active_hbox.addWidget(btn_player_active_1)
        player_active_hbox.addWidget(btn_player_active_2)
        
        # layout.addWidget(self.resultTable)
        player_panel_vbox.addWidget(time_label)
        player_panel_vbox.addWidget(QHLine())
        
        player_panel_vbox.addWidget(moves_list_label)
        player_panel_vbox.addWidget(moves_list)

        player_panel_vbox.addLayout(player_buttons_hbox)
        player_buttons_hbox.addWidget(btn_end_game)
        player_buttons_hbox.addWidget(btn_undo_move)



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
     controller = Controller(ex)
     sys.exit(app.exec_())
     board = np.zeros((ROW_COUNT,COLUMN_COUNT))    