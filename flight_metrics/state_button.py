"""."""
from PyQt6.QtWidgets import QGraphicsProxyWidget
from pyqtgraph.Qt.QtWidgets import QPushButton


class ButtonProxy(QGraphicsProxyWidget):
    """."""

    def __init__(self):
        super().__init__()
        self.button = QPushButton()
        self.setWidget(self.button)


class StateButton(ButtonProxy):
    """."""

    def __init__(self, parent, state_identifier):
        super().__init__()
        self._parent = parent
        self.state = state_identifier
        self._state_id = self._set_id()
        self.button.clicked.connect(self.button_changed)
        self.set_style()

    def set_style(self) -> None:
        self.button.setText(self.state)
        self.button.setCheckable(True)
        self.button.setChecked(True)

    def _set_id(self) -> int:
        match self.state:
            case "Standby":
                return 0
            case "Motor Burn":
                return 1
            case "Coast":
                return 2
            case "Freefall":
                return 3
            case "Landed":
                return 4

    def button_changed(self) -> None:
        """When button is clicked, send its ID to the parent container so that it
        can update the slider"""
        self._parent.quick_set_slider(self._state_id)
