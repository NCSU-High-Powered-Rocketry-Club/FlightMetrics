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

    def __init__(self, state_identifier):
        super().__init__()
        self.state = state_identifier
        self.set_style()


    def set_style(self) -> None:
        self.button.setText(self.state)
        self.button.setCheckable(True)
