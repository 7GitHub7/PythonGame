from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QWidget, QMessageBox

import numpy as np
import math

ROW_COUNT = 6
COLUMN_COUNT = 7 
SQUARESIZE = 100
# board = np.zeros((ROW_COUNT,COLUMN_COUNT))

class Game(QWidget):

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.X_Circle = 0
        self.Y_Circle = 0
        self.currentPlayer = None
        self.player = None
        self.thread = None
        self.resultTable = None
        self.color = None
        self.initUI()
        self.board = np.zeros((ROW_COUNT,COLUMN_COUNT))

    def initUI(self):
        
        self.setMouseTracking(True)
        self.setWindowTitle('PyQt window')
        self.show()

    def mouseMoveEvent(self, e):
        self.X_Circle = e.x() 
        self.Y_Circle = e.y()
        self.update()

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r        

    def update_board(self, row, col, player):
        if row is not None and col is not None:
            self.board[row][col] = player

    def winning_move(self, player):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == player and self.board[r][c+1] == player and self.board[r][c+2] == player and self.board[r][c+3] == player:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] == player and self.board[r+3][c] == player:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == player and self.board[r+1][c+1] == player and self.board[r+2][c+2] == player and self.board[r+3][c+3] == player:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == player and self.board[r-1][c+1] == player and self.board[r-2][c+2] == player and self.board[r-3][c+3] == player:
                    return True        

    def mousePressEvent(self,e):
        if self.currentPlayer[1] == self.player.playerID:
            if e.button() == Qt.LeftButton:
                pos_col = int(math.floor(e.x()/100))
                if pos_col > 700:
                    pos_col = 6
                pos_row = self.get_next_open_row(pos_col)
                if pos_row is not None:
                    self.update_board(pos_row,pos_col, self.color)
                    if self.winning_move(self.color):
                        self.player.endGame('four')
                    else:
                        self.player.updateBoard(self.board.tolist())
                        self.player.changePlayer()
                        self.currentPlayer = self.player.getCurrentPlayer()
                        self.resultTable.setCurrentPlayer(self.currentPlayer[0])
                        self.update()
                    self.thread.start()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp, self.board)
        qp.end()

    def drawRectangles(self, qp, board):
        col = QColor(0, 0, 0)
        qp.setPen(col)
        qp.setBrush(QColor(200, 0, 0))
        r_index = 0
        c_index = 0
        board_display = np.rot90(np.transpose(board))
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
        if self.color == 1:
            qp.setBrush(QColor(200, 0, 0))
        else:
            qp.setBrush(QColor(100, 0, 200))
        qp.drawEllipse(self.X_Circle-15, int(SQUARESIZE/100), SQUARESIZE-5, SQUARESIZE-5)


    def showDialog(self, text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Koniec gry")

        returnValue = msgBox.exec()
        # if returnValue == QMessageBox.Ok:
        #     # self.main.back_page()


