"""."""
import re
from typing import TYPE_CHECKING

from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import Qt
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget, QListWidget, QListWidgetItem

if TYPE_CHECKING:
    from flight_metrics.main_window import MainWindow

class DataSelector(GraphicsLayout):
    """."""

    def __init__(self, parent: "MainWindow"):
        super().__init__()
        self._parent = parent

        self.list_widget = QListWidget()
        proxy_list = QGraphicsProxyWidget()
        proxy_list.setWidget(self.list_widget)
        self.addItem(proxy_list)
        self.list_widget.setObjectName("data_selector_list")
        self._checked_columns = []

    def format_headers(self, headers: list[str]) -> dict:
        """Takes in a list of unformatted headers and formats them to be title case"""
        header_dict = {}
        for string in headers:
            formatted_string = ""
            if "_" in string:
                formatted_string = string.replace("_", " ")
                formatted_string = formatted_string.title()
            elif bool(re.search(r"[A-Z]", string)):
                # caps in the string, it is in camel case
                formatted_string = re.sub(r"(?<=[a-z])(?=[A-Z])"," ", string)
                formatted_string = formatted_string[0].upper() + formatted_string[1:]
            else:
                # single word, no caps or underscores
                formatted_string = string.title()
            header_dict.update({formatted_string: string})
        return header_dict

    def update_headers(self, headers: set) -> None:
        """Updates the available y-axis options"""
        self._header_dict = self.format_headers(list(headers))
        self.list_widget.clear()

        for column in sorted(self._header_dict):
            list_item = QListWidgetItem(column)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)
        self.list_widget.itemChanged.connect(self.item_changed)

    def item_changed(self, item: QListWidgetItem):
        """When a box is ticked, update the internal list of ticked boxes, and call
        main window to update the plot"""
        if item.checkState() == Qt.CheckState.Checked:
            self._checked_columns.append(self._header_dict[item.text()])
        if item.checkState() == Qt.CheckState.Unchecked:
            self._checked_columns.remove(self._header_dict[item.text()])
        self._parent.data_selector_updated(self._checked_columns)
