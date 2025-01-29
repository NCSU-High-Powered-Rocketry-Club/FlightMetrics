"""."""

from pathlib import Path

from pyqtgraph.Qt.QtCore import Qt
from pyqtgraph import GraphicsLayout, LabelItem
from pyqtgraph.Qt.QtWidgets import QCheckBox, QGraphicsProxyWidget, QListWidget, QListWidgetItem


class FlightSelector(GraphicsLayout):
    """."""

    def __init__(self):
        super().__init__()

        self._get_flights()

        self.list_widget = QListWidget()
        self._make_checklist()

        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.list_widget)
        self.addItem(proxy_list)



    def _get_flights(self):
        log_dir = Path(__file__).parent.parent / "launch_logs"
        self._flights = ["   " + f.stem.replace("_", " ").title() for f in log_dir.glob("*.csv")]

    def _make_checklist(self):
        for flight_name in self._flights:
            list_item = QListWidgetItem(flight_name)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)