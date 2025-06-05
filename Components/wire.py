from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid

class Wire(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

        self.default_line_color = Qt.GlobalColor.white
        self.line_width = 3
        self.setPen(QPen(self.default_line_color, self.line_width))

        self._dragging_point = None  # None, 0 (p1), or 1 (p2)
        self._drag_offset = QPointF(0, 0)

        self.state = False

    def paint(self, painter, option, widget=None):
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)

        from GUI.theme_state import is_dark_mode
        self.default_line_color = Qt.GlobalColor.white if is_dark_mode else Qt.GlobalColor.black
        color = Qt.GlobalColor.green if self.state else self.default_line_color
        painter.setPen(QPen(color, self.line_width))
        painter.drawLine(self.line())

        # If selected, draw blue rectangles at endpoints
        if self.isSelected():
            rect_size = 10
            half = rect_size / 2
            line = self.line()
            for pt in [line.p1(), line.p2()]:
                rect = QRectF(pt.x() - half, pt.y() - half, rect_size, rect_size)
                painter.setBrush(QBrush(Qt.GlobalColor.blue))
                painter.setPen(Qt.GlobalColor.blue)
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        if self.isSelected():
            rect_size = 10
            half = rect_size / 2
            line = self.line()
            mouse_pos = event.pos()
            for idx, pt in enumerate([line.p1(), line.p2()]):
                rect = QRectF(pt.x() - half, pt.y() - half, rect_size, rect_size)
                if rect.contains(mouse_pos):
                    self._dragging_point = idx
                    self._drag_offset = mouse_pos - pt
                    event.accept()
                    return
        self._dragging_point = None
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging_point is not None:
            line = self.line()
            new_pt = event.pos() - self._drag_offset
            snapped_x, snapped_y = snap_to_grid(new_pt.x(), new_pt.y())
            if self._dragging_point == 0:
                self.setLine(snapped_x, snapped_y, *snap_to_grid(line.x2(), line.y2()))
            else:
                self.setLine(*snap_to_grid(line.x1(), line.y1()), snapped_x, snapped_y)
            event.accept()
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging_point = None
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Get the new position as x, y
            x, y = value.x(), value.y()
            snapped_x, snapped_y = snap_to_grid(x, y)
            return QPointF(snapped_x, snapped_y)
        return super().itemChange(change, value)
    
    def update_state(self):
        self.state = not self.state  # Toggle state
        self.update()
    
    def to_dict(self):
        pos = self.pos()
        line = self.line()
        pen = self.pen()
        return {
            "type": "wire",
            "x1": line.x1(),
            "y1": line.y1(),
            "x2": line.x2(),
            "y2": line.y2(),
            "rotation": self.rotation(),
            "pos_x": pos.x(),
            "pos_y": pos.y()
        }

    @classmethod
    def from_dict(cls, data):
        rect = cls(
            data.get("x1", 0),
            data.get("y1", 0),
            data.get("x2", 100),
            data.get("y2", 100)
        )
        rect.setRotation(data.get("rotation", 0))
        pen = QPen(
            QColor(data.get("border_color", "#000000")),
            data.get("border_width", 3)
        )
        rect.setPen(pen)
        # Set the scene position after creation
        rect.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        return rect