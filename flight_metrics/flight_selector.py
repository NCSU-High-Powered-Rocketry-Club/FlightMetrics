"""."""

from pathlib import Path

from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import Qt
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget, QListWidget, QListWidgetItem


class FlightSelector(GraphicsLayout):
    """."""

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._checked_flights: list = []

        self.list_widget = QListWidget()
        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.list_widget)
        self.addItem(proxy_list)

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
            self._checked_flights.append(item.text())
        if item.checkState() == Qt.CheckState.Unchecked:
            self._checked_flights.remove(item.text())

        self._parent.update_data(sorted(self._checked_flights))

