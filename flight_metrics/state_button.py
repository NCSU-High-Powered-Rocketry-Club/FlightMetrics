"""."""

from PyQt6.QtWidgets import QGraphicsProxyWidget
from pyqtgraph.Qt.QtWidgets import QPushButton


class ButtonProxy(QGraphicsProxyWidget):
    """."""

    def __init__(self):
        super().__init__()
        self.button = QPushButton()


class StateButton(ButtonProxy):
    """."""

    def __init__(self, state_identifier):
        super().__init__()
        self.setWidget(self.button)
        self.button.setText(state_identifier)
