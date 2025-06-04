from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

GRID_SIZE = 10
GRID_COLOR = QColor(125, 125, 125)
GRID_ENABLED = True

def draw_grid(painter, rect):
    if not GRID_ENABLED:
        return
    painter.save()
    painter.setPen(QPen(GRID_COLOR, 1))
    left = int(rect.left()) - (int(rect.left()) % GRID_SIZE)
    top = int(rect.top()) - (int(rect.top()) % GRID_SIZE)
    right = int(rect.right())
    bottom = int(rect.bottom())
    x = left
    while x <= right:
        painter.drawLine(x, top, x, bottom)
        x += GRID_SIZE
    y = top
    while y <= bottom:
        painter.drawLine(left, y, right, y)
        y += GRID_SIZE
    painter.restore()

def set_grid_color(color):
    global GRID_COLOR
    GRID_COLOR = color

def snap_to_grid(x, y):
    if not GRID_ENABLED:
        return x, y
    return round(x / GRID_SIZE) * GRID_SIZE, round(y / GRID_SIZE) * GRID_SIZE