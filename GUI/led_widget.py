from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class LEDWidget(QWidget):
    clicked = pyqtSignal()
    def __init__(self, state=False, parent=None):
        super().__init__(parent)
        self.state = state
        self.setFixedSize(30, 30)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def set_state(self, state: bool):
        self.state = state
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        color = Qt.GlobalColor.yellow if self.state else Qt.GlobalColor.darkYellow
        painter.setPen(QPen(Qt.GlobalColor.darkRed, 3))
        painter.setBrush(color)
        painter.drawEllipse(5, 5, 15, 15)