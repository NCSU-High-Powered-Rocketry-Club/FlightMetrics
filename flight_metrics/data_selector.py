"""."""

import re
from typing import TYPE_CHECKING

import pandas as pd
from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import Qt, pyqtSignal
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget, QListWidget, QListWidgetItem

if TYPE_CHECKING:
    from flight_metrics.main_window import MainWindow


class DataSelector(GraphicsLayout):
    """Retrieves current dataset from FlightSelector and creates a checklist of all available
    flight data."""

    fields_changed = pyqtSignal(list)

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
                formatted_string = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", string)
                formatted_string = formatted_string[0].upper() + formatted_string[1:]
            else:
                # single word, no caps or underscores
                formatted_string = string.title()
            header_dict.update({formatted_string: string})
        return header_dict

    def update_fields(self, datasets: list[pd.DataFrame]) -> None:
        """Updates the available fields to plot, called whenever a new dataset is added or
        removed"""
        # making a set of the headers in each dataset
        headers = [set(df.columns.to_list()) for df in datasets]
        # combining all the sets into one set
        if headers:
            unique_headers = headers[0]
            for header_index in range(len(headers) - 1):
                unique_headers.union(headers[header_index + 1])
            self._header_dict = self.format_headers(list(unique_headers))
        else:
            self._header_dict = {}
        self.list_widget.clear()

        for column in sorted(self._header_dict):
            list_item = QListWidgetItem(column)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)
        self.list_widget.itemChanged.connect(self.item_changed)

    def item_changed(self, item: QListWidgetItem) -> None:
        """When a box is ticked, update the internal list of ticked boxes, and call
        main window to update the plot"""
        if item.checkState() == Qt.CheckState.Checked:
            self._checked_columns.append(self._header_dict[item.text()])
        if item.checkState() == Qt.CheckState.Unchecked:
            self._checked_columns.remove(self._header_dict[item.text()])
        self.fields_changed.emit(self._checked_columns)
