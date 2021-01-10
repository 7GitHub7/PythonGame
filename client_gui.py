from PyQt5.QtWidgets import QWidget, QApplication,QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys
import numpy as np
import math

ROW_COUNT = 6
COLUMN_COUNT = 7 
SQUARESIZE = 100
board = np.zeros((ROW_COUNT,COLUMN_COUNT))
board[0][6] = 2


class Example(QWidget):
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

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = Example()
     sys.exit(app.exec_())
     board = np.zeros((ROW_COUNT,COLUMN_COUNT))    