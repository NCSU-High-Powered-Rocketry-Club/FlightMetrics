"""."""

from pyqtgraph.Qt.QtGui import QFont
from pyqtgraph.Qt.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from flight_metrics.pull_data_button import PullDataButton
from flight_metrics.state_button import ButtonProxy


class SettingsButton(ButtonProxy):
    """."""

    def __init__(self):
        super().__init__()

        self._settings_window: SettingsWindow | None = None

        self.button.clicked.connect(self.button_clicked)
        self.set_style()

    def set_style(self) -> None:
        self.button.setText("Settings")

    def button_clicked(self) -> None:
        """When button is clicked, open settings panel"""
        if self._settings_window is None:
            self._settings_window = SettingsWindow(self)
            self._settings_window.show()

        self._settings_window.raise_()


class SettingsWindow(QWidget):
    """A separate settings window."""

    def __init__(self, parent):
        super().__init__()
        self._parent_button = parent

        self._set_style()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 300, 600, 400)

    def _set_style(self):
        """sets the style and layout for the settings window"""
        main_layout = QVBoxLayout()
        self._pull_data_layout = QHBoxLayout()
        self._add_pull_data_setting()
        self._pull_data_layout.addStretch()  # spacing so the label presses up against the button

        # adding the "pull data" layout to the main layout, and adding space below
        # so the pull_data_layout doesn't take up the whole menu
        main_layout.addLayout(self._pull_data_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _add_pull_data_setting(self):
        """adds the button and label to be able to pull data from AirbrakesV2"""
        pull_data_button = PullDataButton()
        label = QLabel("Pull launch data from AirbrakesV2")
        label.setFont(QFont("default", 16))
        # This orders the layout so the button is on the left of the label
        self._pull_data_layout.addWidget(pull_data_button)
        self._pull_data_layout.addWidget(label)

    def closeEvent(self, event):
        self._parent_button._settings_window = None
        # event.accept() is used to indicate that the closing event is handled
        event.accept()
