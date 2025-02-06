"""The Flight Selector contains the list of all available flight data"""

from pathlib import Path

from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import Qt, pyqtSignal
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget, QListWidget, QListWidgetItem

from flight_metrics.settings import SettingsButton


class FlightSelector(GraphicsLayout):
    """Pulls data from launch_logs folder and creates a checklist of all available flight data."""

    # signal that emits whenever a flight is checked or unchecked. Emits the list of currently
    # selected flights
    flight_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._checked_flights: list = []

        self.list_widget = QListWidget()
        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.list_widget)
        self.addItem(proxy_list)
        self.list_widget.setObjectName("flight_selector_list")

        # make small container for settings at bottom
        self._settings_layout = self.addLayout(row=1, col=0)
        self._settings_layout.setFixedHeight(50)
        self._settings_button = SettingsButton()
        self._settings_layout.addItem(self._settings_button)

        flights = self._get_flights()
        self._make_checklist(flights)

    def _get_flights(self) -> list[str]:
        """Gets the names of all flight data in launch_logs folder"""
        log_dir = Path(__file__).parent.parent / "launch_logs"
        return [f.stem.replace("_", " ").title() for f in log_dir.glob("*.csv")]

    def _make_checklist(self, flights: list[str]) -> None:
        """Creates the flight selector checklist"""
        for flight_name in flights:
            # checkbox size is big, and without adding whitespace, the text gets overlapped
            # on the gui
            list_item = QListWidgetItem("   " + flight_name)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)
        self.list_widget.itemChanged.connect(self.fs_item_changed)

    def fs_item_changed(self, item: QListWidgetItem):
        """When a flight checkbox is checked or unchecked, emit to the signal with the
        currently selected flights"""
        if item.checkState() == Qt.CheckState.Checked:
            # removing the whitespace before the name
            self._checked_flights.append(item.text().strip())
        if item.checkState() == Qt.CheckState.Unchecked:
            self._checked_flights.remove(item.text().strip())
        self.flight_changed.emit(self._checked_flights)
