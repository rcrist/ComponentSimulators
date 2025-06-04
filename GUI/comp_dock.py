from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Components.and_gate import AndGate
from Components.or_gate import OrGate
from Components.not_gate import NotGate
from Components.nand_gate import NandGate
from Components.nor_gate import NorGate
from Components.xor_gate import XorGate
from Components.xnor_gate import XnorGate

class ComponentDock(QDockWidget):
    """ Component widget for selecting and displaying components """
    def __init__(self, parent=None, scene=None):
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        
        # Custom title bar to allow styling
        title = QLabel("Components")
        title.setObjectName("ComponentsDockTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setContentsMargins(10, 0, 0, 0)  # Add 10px left margin
        self.setTitleBarWidget(title)

        self.scene = scene
        
        self.properties_widget = QWidget()
        self.layout = QVBoxLayout(self.properties_widget)

        # Add gate buttons
        self.gate_buttons = {}
        gates = ["And", "Or", "Not", "Nand", "Nor", "Xor", "Xnor"]
        for gate in gates:
            btn = QPushButton(gate)
            btn.clicked.connect(lambda checked, g=gate: self.add_gate(g))
            self.layout.addWidget(btn)
            self.gate_buttons[gate] = btn

        self.layout.addStretch()
        self.setWidget(self.properties_widget)

    def add_gate(self, gate_type):
        """Create the associated gate on the canvas/scene """
        if self.scene is not None:
            # You may need to adapt this to your scene's API
            if gate_type == "And":
                gate = AndGate()
            elif gate_type == "Or":
                gate = OrGate()
            elif gate_type == "Not":
                gate = NotGate()
            elif gate_type == "Nand":
                gate = NandGate()
            elif gate_type == "Nor":
                gate = NorGate()
            elif gate_type == "Xor":
                gate = XorGate()
            elif gate_type == "Xnor":
                gate = XnorGate()
            else:
                return

            gate.setPos(100, 100)
            self.scene.addItem(gate)