from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp

class AndGate(Comp):
    """ 2-Input AND gate digital logic component """
    def __init__(self):
        super().__init__()

        self.radius = 3

        self.conns = [
            {"name": "in1", "type": "input", "pos": QPointF(0, 10), "state": False},
            {"name": "in2", "type": "input", "pos": QPointF(0, 30), "state": False},
            {"name": "out", "type": "output", "pos": QPointF(40, 20), "state": False}
        ]

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, 40, 40)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the NOT gate component """
        # Set the pen and brush colors based on the theme
        from GUI.theme_state import is_dark_mode
        self.pen_color = Qt.GlobalColor.white if is_dark_mode else Qt.GlobalColor.black
        painter.setPen(self.pen_color)
        self.brush_color = Qt.GlobalColor.black if is_dark_mode else Qt.GlobalColor.white
        painter.setBrush(self.brush_color)

        # Draw the NOT gate symbol and connectors
        self.draw_comp_symbol(painter)
        self.draw_conns(painter)

        # Draw selection outline if selected
        if option.state & QStyle.StateFlag.State_Selected:
            self.draw_selection_outline(painter)

    def draw_comp_symbol(self, painter: QPainter) -> None:
        """ Draws the component symbol """
        path = QPainterPath()
        # Left vertical line
        path.moveTo(0 + self.radius, 0)
        path.lineTo(0 + self.radius, 40)
        # Bottom line
        path.lineTo(20, 40)
        # Right semicircle (arc)
        rect = QRectF(0 + self.radius, 0, 34, 40)
        path.arcTo(rect, 270, 180)
        # Top line
        path.lineTo(0 + self.radius, 0)

        from GUI.theme_state import is_dark_mode
        self.pen_color = QColor(255, 255, 255) if is_dark_mode else QColor(0, 0, 0)
        painter.setPen(QPen(self.pen_color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

    def update_state(self):
        """ Updates the state of the component based on the inputs """
        self.conns[2]["state"] = self.conns[0]["state"] and self.conns[1]["state"]

    def to_dict(self):
        """ Save file JSON fields for the component """
        pos = self.pos()
        rect = self.boundingRect()
        conn_states = {conn["name"]: conn["state"] for conn in self.conns}
        return {
            "type": "and_gate",
            "x": rect.x(),
            "y": rect.y(),
            "width": rect.width(),
            "height": rect.height(),
            "rotation": self.rotation(),
            "pos_x": pos.x(),
            "pos_y": pos.y(),
            "conn_states": conn_states
        }

    @classmethod
    def from_dict(cls, data):
        """ Load file JSON fields for the component """
        obj = cls()
        obj.setRotation(data.get("rotation", 0))
        obj.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        # Restore connector states by name if present
        conn_states = data.get("conn_states", {})
        for conn in obj.conns:
            if conn["name"] in conn_states:
                conn["state"] = conn_states[conn["name"]]
        return obj
