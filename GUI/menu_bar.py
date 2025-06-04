from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import json

from Components.not_gate import NotGate
from Components.and_gate import AndGate
from Components.or_gate import OrGate
from Components.nand_gate import NandGate
from Components.nor_gate import NorGate
from Components.xor_gate import XorGate
from Components.xnor_gate import XnorGate
from GUI.grid import set_grid_color

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # File Menu
        file_menu = self.addMenu("File")
        new_action = file_menu.addAction("New")
        new_action.triggered.connect(self.new_file)
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        print_action = file_menu.addAction("Print")
        print_action.triggered.connect(self.print_diagram)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)

        # Settings Menu
        settings_menu = self.addMenu("Settings")
        toggle_grid_action = settings_menu.addAction("Toggle Grid")
        toggle_grid_action.triggered.connect(self.toggle_grid)
        toggle_theme_action = settings_menu.addAction("Toggle Theme")
        toggle_theme_action.triggered.connect(self.toggle_theme)

        self.apply_dark_theme()

    def toggle_theme(self):
        import GUI.theme_state as theme_module
        theme_module.toggle_dark_mode()

        if theme_module.is_dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        app = QApplication.instance()
        app.setStyleSheet("""
            QMainWindow, QGraphicsView, QGraphicsScene {
                background: #000;
                color: #fff;
            }
            QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                background: #000;
                color: #fff;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background: #2a82da;
            }
            QDockWidget#PropertiesDock {
                background: #000;
                color: #fff;
            }
            QDockWidget#PropertiesDock QLabel {
                background: #000;
                color: #fff;
            }
        """)
        set_grid_color(QColor(60, 60, 60))  # Set grid color for dark mode
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.update()
        if hasattr(main_window, "view"):
            main_window.view.viewport().update()

    def apply_light_theme(self):
        app = QApplication.instance()
        app.setStyleSheet("""
            QMainWindow, QGraphicsView, QGraphicsScene {
                background: #fff;
                color: #000;
            }
            QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                background: #f0f0f0;
                color: #000;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background: #d0d0d0;
            }
            QDockWidget#PropertiesDock {
                background: #fff;
            }
            QDockWidget#PropertiesDock::title {
                color: #000;
                background: #fff;
            }
            QDockWidget#PropertiesDock * {
                color: #000;
                background: #fff;
            }
            QSlider {
                background: transparent;
            }
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #eee;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #2a82da;
                border: 1px solid #5c5c5c;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """)
        set_grid_color(QColor(200, 200, 200))  # Set grid color for light mode
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.update()
        if hasattr(main_window, "view"):
            main_window.view.viewport().update()

    def toggle_grid(self):
        import GUI.grid as grid_module
        grid_module.GRID_ENABLED = not grid_module.GRID_ENABLED
        # Optionally, update the view to refresh the grid
        main_window = self.parent()
        if hasattr(main_window, "view"):
            main_window.view.viewport().update()

    def new_file(self):
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.clear()
        else:
            QMessageBox.information(self, "New", "Scene clearing is not implemented.")

    def open_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Open", "Scene loading is not implemented.")
            return
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    items_data = json.load(f)
                main_window.scene.clear()
                for item_data in items_data:
                    item = self.deserialize_item(item_data)
                    if item:
                        main_window.scene.addItem(item)
            except Exception as e:
                QMessageBox.warning(self, "Open", f"Failed to open file:\n{e}")

    def save_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Save", "Scene saving is not implemented.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                items_data = [self.serialize_item(item) for item in main_window.scene.items()]
                # Remove None items (if any)
                items_data = [item for item in items_data if item is not None]
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(items_data, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Save", f"Failed to save file:\n{e}")

    def serialize_item(self, item):
        if isinstance(item, NotGate):
            return item.to_dict()
        if isinstance(item, AndGate):
            return item.to_dict()
        if isinstance(item, OrGate):
            return item.to_dict()
        if isinstance(item, NandGate):
            return item.to_dict()
        if isinstance(item, NorGate):
            return item.to_dict()
        if isinstance(item, XorGate):
            return item.to_dict()
        if isinstance(item, XnorGate):
            return item.to_dict()
        return None

    def deserialize_item(self, data):
        if not data:
            return None
        t = data.get("type", "")
        if t == "not_gate":
            return NotGate.from_dict(data)
        if t == "and_gate":
            return AndGate.from_dict(data)
        if t == "or_gate":
            return OrGate.from_dict(data)
        if t == "nand_gate":
            return NandGate.from_dict(data)
        if t == "nor_gate":
            return NorGate.from_dict(data)
        if t == "xor_gate":
            return XorGate.from_dict(data)
        if t == "xnor_gate":
            return XnorGate.from_dict(data)
        return None

    def print_diagram(self):
        main_window = self.parent()
        if not hasattr(main_window, "view"):
            QMessageBox.information(self, "Print", "Nothing to print.")
            return

        view = getattr(main_window, "view", None)
        scene = getattr(main_window, "scene", None)

        # Hide grid before printing if it exists
        import GUI.grid as grid_module
        if grid_module.GRID_ENABLED:
            old_grid_enabled = grid_module.GRID_ENABLED
            grid_module.GRID_ENABLED = False
        else:
            old_grid_enabled = None

        # --- Fix: update the global theme state variable before printing ---
        import GUI.theme_state as theme_state
        old_dark_mode = theme_state.is_dark_mode
        if theme_state.is_dark_mode:
            theme_state.is_dark_mode = False
            self.apply_light_theme()
            if scene:
                scene.update()
            if view:
                view.viewport().update()

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec():
            painter = QPainter(printer)
            main_window.view.render(painter)
            painter.end()

        # Restore theme state after printing
        if old_dark_mode:
            theme_state.is_dark_mode = True
            self.apply_dark_theme()
            if scene:
                scene.update()
            if view:
                view.viewport().update()

        # Restore grid visibility
        if old_grid_enabled is not None:
            grid_module.GRID_ENABLED = old_grid_enabled