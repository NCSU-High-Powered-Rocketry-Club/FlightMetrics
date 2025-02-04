"""."""

from pathlib import Path
from typing import TYPE_CHECKING

from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import Qt
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget, QListWidget, QListWidgetItem

from flight_metrics.settings import SettingsButton

if TYPE_CHECKING:
    from flight_metrics.main_window import MainWindow


class FlightSelector(GraphicsLayout):
    """."""

    def __init__(self, parent: "MainWindow"):
        super().__init__()
        self._parent = parent
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

        self._get_flights()
        self._make_checklist()

    def _get_flights(self):
        log_dir = Path(__file__).parent.parent / "launch_logs"
        self._flights = ["   " + f.stem.replace("_", " ").title() for f in log_dir.glob("*.csv")]

    def _make_checklist(self):
        for flight_name in self._flights:
            list_item = QListWidgetItem(flight_name)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)
        self.list_widget.itemChanged.connect(self.item_changed)

    def item_changed(self, item: QListWidgetItem):
        if item.checkState() == Qt.CheckState.Checked:
            self._checked_flights.append(item.text().strip())
        if item.checkState() == Qt.CheckState.Unchecked:
            self._checked_flights.remove(item.text().strip())
        self._parent.update_data_manager(sorted(self._checked_flights))


