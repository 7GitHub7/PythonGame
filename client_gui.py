from PyQt5.QtWidgets import QStackedWidget,QFrame,QWidget, QApplication,QLabel ,QTabWidget,QVBoxLayout,QCheckBox,QHBoxLayout,QPushButton,QLineEdit,QListWidget,QLabel
# from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys
import numpy as np
from client import *
import math

ROW_COUNT = 6
COLUMN_COUNT = 7 
SQUARESIZE = 100
board = np.zeros((ROW_COUNT,COLUMN_COUNT))
board[0][6] = 2
board[1][6] = 2

class Game(QWidget):
    X_Circle = 0
    Y_Circle = 0

    def __init__(self):
        super().__init__()
        self.X_Circle = 0
        self.Y_Circle = 0

        self.initUI()  

    def initUI(self):
        self.setGeometry(300, 300, 900, 900)
        self.setMouseTracking(True)
        self.setWindowTitle('PyQt window') 

        self.show()

    def mouseMoveEvent(self,e):
        self.X_Circle = e.x() 
        self.Y_Circle = e.y() 
        self.update()

    def get_next_open_row(self,board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r        

    def update_board(self,board, row, col, player):
	    board[row][col] = player    

    def mouseDoubleClickEvent(self,e):
        print("click")
        pos_col = int(math.floor(e.x()/100))
        if pos_col > 700:
            pos_col = 6
        pos_row = self.get_next_open_row(board,pos_col)
        print(pos_col)     
        print(pos_row)     
        self.update_board(board,pos_row,pos_col,1)
        np.flip(board, 0)
        print(board)
        self.update()
  

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp,board)
        qp.end()

    def drawRectangles(self, qp, board):
        col = QColor(0, 0, 0)
        qp.setPen(col)
        qp.setBrush(QColor(200, 0, 0))
        r_index =0 
        c_index =0
        board_display = np.rot90(np.transpose(board))
        print(board_display)
        for c in board_display:
            for r in c:
                qp.setBrush(QColor(0, 0, 0))
                qp.drawRect(r_index*SQUARESIZE, c_index*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)
                if r == 1:
                    qp.setBrush(QColor(200, 0, 0))
                elif r == 2:
                    qp.setBrush(QColor(100, 0, 200))
                elif r == 0:
                    qp.setBrush(QColor(100, 100, 0))         
                qp.drawEllipse(r_index*SQUARESIZE, c_index*SQUARESIZE+SQUARESIZE, SQUARESIZE-5, SQUARESIZE-5)
                r_index = r_index + 1
            r_index =0     
            c_index = c_index + 1
        qp.setBrush(QColor(200, 0, 0))        
        qp.drawEllipse(self.X_Circle-15, int(SQUARESIZE/10), SQUARESIZE-5, SQUARESIZE-5)


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
        self.next_button.clicked.connect(self.next_page)
        self.setGeometry(300, 300, 750, 800)
        self.mouse_clik_counter = 0
        self.player = None

    def initUI(self):

        self.next_button = QPushButton('Dalej')
        self.next_button.setEnabled(False)
        self.stacked_widget = QStackedWidget()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.next_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.stacked_widget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def set_button_state(self, index):
        n_pages = len(self.stacked_widget)
        self.next_button.setEnabled( index % n_pages < n_pages - 1)

    def insert_page(self, widget, index=-1):
        self.stacked_widget.insertWidget(index, widget)
        print(index)
        self.set_button_state(self.stacked_widget.currentIndex())

    def next_page(self):
        new_index = self.stacked_widget.currentIndex()+1
        if new_index < len(self.stacked_widget):
            self.stacked_widget.setCurrentIndex(new_index)

        if self.mouse_clik_counter == 0:
            self.next_button.setText("Graj!")
            self.mouse_clik_counter += 1
            self.player = Client(self.player_name_input.text())
            self.rooms = self.player.getRoomList()
            self.list.clear()
            for room in self.rooms:
                self.list.addItem(str(room))
            self.update()

        elif self.mouse_clik_counter == 1:
            pass


    def welcomeTabUI(self):
        """Create the Welcome page UI."""
        self.layout_welcome = QVBoxLayout()
        self.player_name_input = QLineEdit(self)
        self.player_name_label = QLabel("Podaj swoją nazwę gracza", self)
        self.title_label = QLabel("Witaj w Connect4", self)
        self.layout_welcome.addWidget(self.title_label)
        self.layout_welcome.addWidget(self.player_name_label)
        self.layout_welcome.addWidget(self.player_name_input)
        
        generalTab = QWidget()
        layout = QVBoxLayout()
        layout.addLayout(self.layout_welcome)
        
        generalTab.setLayout(layout)
        return generalTab


    def gameTabUI(self):
        """Create the Game page UI."""
        generalTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(Game())
        generalTab.setLayout(layout)
        return generalTab

    def networkTabUI(self):
        
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
        self.btn_add_room.clicked.connect(self.create_room)
        self.layout_main.addWidget(QLabel("Stwórz nowy pokój", self))
        self.layout_main.addLayout(self.layout_create_room)
        self.layout_main.addWidget(self.btn_add_room)
        self.layout_main.addWidget(QHLine())
        self.layout_main.addWidget(QLabel("Wybierz pokój", self))
        self.layout_main.addWidget(self.list)
        self.networkTab.setLayout(self.layout_main)

        return self.networkTab

    def create_room(self):
        if self.room_name_label.text():
            self.player.createRoom(self.room_name_label.text())
            self.rooms = self.player.getRoomList()
            self.list.clear()
            for room in self.rooms:
                self.list.addItem(str(room))
        self.update()    

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = Main()
     ex.show()
     ex.insert_page(ex.welcomeTabUI())
     ex.insert_page(ex.networkTabUI())
     ex.insert_page(ex.gameTabUI())
     sys.exit(app.exec_())
     board = np.zeros((ROW_COUNT,COLUMN_COUNT))    