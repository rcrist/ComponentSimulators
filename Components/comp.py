from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid

class Comp(QGraphicsItem):
    """ Base class for all components. """
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.c_rad = 2  # Radius for connector circles
        self.i_rad = 4   # Radius for invert symbol circle

    def draw_selection_outline(self, painter: QPainter) -> None:
        """ Draws a selection outline around the item """
        pen = QPen(Qt.GlobalColor.blue)
        pen.setStyle(Qt.PenStyle.DotLine)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.boundingRect())

    def draw_conns(self, painter: QPainter):
        """ Draws the connections for the NOT gate. """
        for conn in self.conns:
            if conn["type"] == "input":
                painter.setPen(Qt.GlobalColor.green)
                painter.setBrush(Qt.GlobalColor.green)
            else:
                painter.setPen(Qt.GlobalColor.red)
                painter.setBrush(Qt.GlobalColor.red)
            painter.drawRect(QRectF(conn["pos"].x() - self.c_rad, conn["pos"].y() - self.c_rad,
                             self.c_rad * 2, self.c_rad * 2))
            
    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        """ Handle item changes, such as position changes """
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Snap the new position to the grid before moving
            snapped = snap_to_grid(value.x(), value.y())
            return QPointF(snapped[0], snapped[1])
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            scene = self.scene()
            if scene is not None:
                scene.invalidate(self.boundingRect(), QGraphicsScene.SceneLayer.ItemLayer)
                scene.update()
        return super().itemChange(change, value)
