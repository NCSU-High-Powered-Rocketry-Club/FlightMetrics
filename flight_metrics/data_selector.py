"""."""

import re

import pandas as pd
from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import Qt, pyqtSignal
from pyqtgraph.Qt.QtWidgets import (
    QGraphicsProxyWidget,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DataSelector(GraphicsLayout):
    """
    Retrieves current dataset from FlightSelector and creates two checklists for selecting
    flight data: one for the X-axis (single selection) and one for the Y-axis (multiple selection).
    """

    fields_changed = pyqtSignal(str, list)

    def __init__(self):
        super().__init__()

        self._header_dict = {}
        self._checked_y_columns = []
        self._checked_x_column = None

        self._set_layout()

        self.x_list_widget.itemChanged.connect(self._x_item_changed)
        self.y_list_widget.itemChanged.connect(self._y_item_changed)

    def _set_layout(self) -> None:
        """Sets up the layout and UI components"""
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        # X-axis selection list (single checkable item)
        self.x_list_widget = QListWidget()
        self.x_list_widget.setObjectName("data_selector_list")
        layout.addWidget(self.x_list_widget)

        # Y-axis selection list (multiple checkable items)
        self.y_list_widget = QListWidget()
        self.y_list_widget.setObjectName("data_selector_list")
        layout.addWidget(self.y_list_widget)

        # Set proxy for embedding
        proxy_container = QGraphicsProxyWidget()
        proxy_container.setWidget(container)
        self.addItem(proxy_container)

    def format_headers(self, headers: list[str]) -> dict:
        """Formats headers into title case"""
        header_dict = {}
        for string in headers:
            formatted_string = ""
            if "_" in string:
                formatted_string = string.replace("_", " ").title()
            elif bool(re.search(r"[A-Z]", string)):
                # caps in the string, it is in camel case
                formatted_string = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", string)
                formatted_string = formatted_string[0].upper() + formatted_string[1:]
            else:
                # single word, no caps or underscores
                formatted_string = string.title()
            header_dict[formatted_string] = string
        return header_dict

    def update_fields(self, datasets: list[pd.DataFrame]) -> None:
        """Updates the available fields to plot, called whenever a new dataset is added or
        removed"""
        # making a set of the headers in each dataset
        headers = [set(df.columns.to_list()) for df in datasets]
        unique_headers = set.union(*headers) if headers else set()
        self._header_dict = self.format_headers(list(unique_headers))

        self.fields_changed.emit(self._checked_x_column, self._checked_y_columns)

        self.x_list_widget.clear()
        self.y_list_widget.clear()

        if datasets:
            # Add "Row Number" as the first item in the X-axis list
            self._header_dict["Row Number"] = "row_num"
            row_num_item = QListWidgetItem("Row Number")
            row_num_item.setFlags(row_num_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            row_num_item.setCheckState(Qt.CheckState.Unchecked)
            self.x_list_widget.addItem(row_num_item)

        for column in sorted(self._header_dict):
            # X-axis selection (single checkable item)
            if column != "Row Number":
                x_item = QListWidgetItem(column)
                x_item.setFlags(x_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                x_item.setCheckState(Qt.CheckState.Unchecked)
                self.x_list_widget.addItem(x_item)

            # Y-axis selection (multiple checkable items)
            y_item = QListWidgetItem(column)
            y_item.setFlags(y_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            y_item.setCheckState(Qt.CheckState.Unchecked)
            self.y_list_widget.addItem(y_item)

    def _x_item_changed(self, item: QListWidgetItem) -> None:
        """Ensures only one X-axis field is selected at a time."""
        if item.checkState() == Qt.CheckState.Checked:
            if (
                self._checked_x_column
                and self._checked_x_column != self._header_dict[item.text()]
            ):
                # Uncheck previously selected X-axis item
                for i in range(self.x_list_widget.count()):
                    prev_item = self.x_list_widget.item(i)
                    if prev_item.text() == self._checked_x_column:
                        prev_item.setCheckState(Qt.CheckState.Unchecked)
                        break

            self._checked_x_column = self._header_dict[item.text()]
        else:
            self._checked_x_column = None

        self.fields_changed.emit(self._checked_x_column, self._checked_y_columns)

    def _y_item_changed(self, item: QListWidgetItem) -> None:
        """When a box is ticked, update the internal list of ticked boxes, and call
        main window to update the plot"""
        field = self._header_dict[item.text()]
        if item.checkState() == Qt.CheckState.Checked:
            self._checked_y_columns.append(field)
        if item.checkState() == Qt.CheckState.Unchecked:
            self._checked_y_columns.remove(field)

        self.fields_changed.emit(self._checked_x_column, self._checked_y_columns)
