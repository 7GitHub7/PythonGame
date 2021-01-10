from PyQt5.QtWidgets import QWidget, QApplication,QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100


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
        self.label = QLabel(self)
        self.label.move(100, 100)
        self.label.setStyleSheet("border: 1px solid black;")
        self.label.setText("Sdafdfdafdsfsdfgsdasdasdasdasd") 
        self.show()

    def mouseMoveEvent(self,e):
        self.label.setText(f'{e.x()}{e.y()}')
        self.X_Circle = e.x() 
        self.Y_Circle = e.y() 
        self.update()    


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        qp.setPen(col)
        qp.setBrush(QColor(200, 0, 0))
        print(COLUMN_COUNT)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                qp.setBrush(QColor(0, 0, 0))
                qp.drawRect(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE) 
                qp.setBrush(QColor(200, 0, 0)) 
                qp.drawEllipse(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE-5, SQUARESIZE-5)
        qp.drawEllipse(self.X_Circle, self.Y_Circle, SQUARESIZE-5, SQUARESIZE-5)  


if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = Example()
     sys.exit(app.exec_())    