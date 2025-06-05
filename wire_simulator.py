from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from GUI.grid import draw_grid
from GUI.led_widget import LEDWidget
from GUI.properties_dock import PropertiesDock
from GUI.menu_bar import MenuBar
from Components.wire import Wire

class GridScene(QGraphicsScene):
    """ Custom QGraphicsScene that draws a grid in the background. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawing_wire = False
        self.temp_wire = None

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        draw_grid(painter, rect)  # Call your grid drawing function

class MainWindow(QMainWindow):
    """ Main application window for the gate simulator. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wire Simulator")
        self.setGeometry(400, 200, 800, 400)

        self.scene = GridScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setSceneRect(0, 0, 1200, 600)
        self.setCentralWidget(self.view)

        # Create and set the menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create and set the properties dock
        self.properties_dock = PropertiesDock(self, self.scene)
        self.properties_dock.setObjectName("PropertiesDock")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)
        self.properties_dock.setMinimumWidth(200)

        # Create a Wire item for demonstration
        self.wire = Wire(100, 100, 200, 200)
        self.scene.addItem(self.wire)
        self.wire.setSelected(True)  # Select the wire

        # Show properties for the selected wire
        self.properties_dock.show_controls(True, self.wire)

        # Connect selection change to show/hide controls
        self.scene.selectionChanged.connect(self.on_selection_changed)

    def closeEvent(self, event):
        try:
            self.scene.selectionChanged.disconnect(self.on_selection_changed)
        except Exception:
            pass
        super().closeEvent(event)

    def on_selection_changed(self):
        """Show controls if a component is selected, hide if not."""
        if hasattr(self, "scene") and self.scene is not None:
            try:
                selected = self.scene.selectedItems()
                self.properties_dock.show_controls(bool(selected), selected[0] if selected else None)
            except RuntimeError:
                # Scene has been deleted, ignore
                pass

if __name__ == "__main__":
    """ Main entry point for the application. """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())