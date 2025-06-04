from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp

class NotGate(Comp):
    """ NOT gate digital logic component """
    def __init__(self):
        super().__init__()

        self.points = [
            QPointF(0, 0),   # Top left
            QPointF(0, 40),  # Bottom left
            QPointF(40 - 2 * self.i_rad - self.c_rad, 20),  # Right (output)
            QPointF(0, 0),   # Top left
        ]

        self.conns = [
            {"name": "in", "type": "input", "pos": QPointF(0, 20), "state": False},
            {"name": "out", "type": "output", "pos": QPointF(40, 20), "state": True}
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
        """ Draws the NOT gate symbol """
        path = QPainterPath()

        # Triangle body
        path.moveTo(self.points[0])  # Top left
        for point in self.points:
            path.lineTo(point)
        painter.drawPath(path)

        # Draw the invert circle at the output
        point = self.points[2]  # Right point (output)
        painter.drawEllipse(QPointF(point.x() + self.i_rad, point.y()), self.i_rad, self.i_rad)

    def update_state(self):
        """ Updates the state of the NOT gate based on the input. """
        self.conns[1]["state"] = not self.conns[0]["state"]

    def to_dict(self):
        """ Save file JSON fields for the component """
        pos = self.pos()
        rect = self.boundingRect()
        conn_states = {conn["name"]: conn["state"] for conn in self.conns}
        return {
            "type": "not_gate",
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
