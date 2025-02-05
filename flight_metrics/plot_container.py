"""."""

import pandas as pd
from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtCore import pyqtSignal
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget

from flight_metrics.data_manager import DataManager
from flight_metrics.graph import Graph
from flight_metrics.range_slider import RangeSlider
from flight_metrics.state_button import StateButton


class PlotContainer(GraphicsLayout):
    """."""
    button_clicked = pyqtSignal(int, int)

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self._data_manager: DataManager = data_manager
        self._buttons: list[StateButton] = []  # the state button objects
        self._selected_states: list = [0, 1, 2, 3, 4]  # the currently selected states
        self._state_ranges: tuple[list] = ([0],[0],[0],[0],[0])
        self._setup()

        self.button_clicked.connect(self._slider.slider.state_button_update)

    def _setup(self) -> None:
        self._plot_layout = self.addLayout(row=0, col=0)
        self._toolbar_layout = self.addLayout(row=1, col=0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # graph setup
        self._graph = Graph()
        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(self._graph)
        self._plot_layout.addItem(proxy_widget)
        self._plot_layout.setBorder(100, 100, 100)
        self._plot_layout.setContentsMargins(0, 0, 0, 10)

        # toolbar setup
        self._setup_toolbar()

    def _setup_toolbar(self) -> None:
        """."""
        self._toolbar_layout.setFixedHeight(200)
        self._toolbar_layout.setBorder(100, 100, 100)
        self._toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # adding buttons to layout
        button_names = ["Standby", "Motor Burn", "Coast", "Freefall", "Landed"]
        for i, name in enumerate(button_names):
            state_button = StateButton(self, name)
            state_button.setMinimumHeight(50)
            self._buttons.append(state_button)
            self._toolbar_layout.addItem(state_button, row=0, col=i)

        self._slider = RangeSlider(
            parent=self,
            min_value=0,
            max_value=1,
            start_min=0,
            start_max=1,
        )
        self._toolbar_layout.addItem(self._slider, row=1, col=0, colspan=5)

    def check_new_state(self, button_id: int) -> None:
        """Determines if the newly selected state is valid. It is invalid if there are gaps in the
        selected states"""
        button = self._buttons[button_id].button

        # if a button is selected and there is nothing that is currently selected, this is
        # always a valid selection
        if not self._selected_states:
            button.setChecked(True)
            self._selected_states.append(button_id)
        else:
            # valid selections are only those that are the minimum or maximum of the selected state
            # list or minimum - 1, maximum + 1.
            allowable_selections = [
                min(self._selected_states) - 1,
                min(self._selected_states),
                max(self._selected_states),
                max(self._selected_states) + 1,
            ]
            if button_id in allowable_selections:
                button.setChecked(not button.isChecked())
                self._selected_states.remove(
                    button_id
                ) if button_id in self._selected_states else self._selected_states.append(button_id)

        # determining what the low and high handle should be on the slider
        if not self._selected_states:
            # If the list is empty, the low and high will be 0 and 0. The slider will be manually
            # overriden so that both handles aren't on top of eachother though
            self.button_clicked.emit(0,0)
        else:
            low_val = self._slider.slider.low_value
            high_val = self._slider.slider.high_value
            max_state = max(self._selected_states)
            min_state = min(self._selected_states)

            if button_id in (max_state, max_state + 1):
                # indicates that the high value should be the one moving
                high_val = max(self._state_ranges[max_state])
            if button_id in (min_state, min_state - 1):
                # indicates that the low value should be the one moving
                low_val = 0 if min_state == 0 else min(self._state_ranges[min_state - 1])
            print(f"low: {low_val}, high: {high_val}")
            self.button_clicked.emit(low_val, high_val)

    def update_state_rows(self, datasets: list[pd.DataFrame]) -> None:
        """When a new dataset is selected, update the row number range of each flight state
        for each dataset."""
        state_cols = [df["state_letter"] for df in datasets]
        # list of tuples, tuples have row # of each state
        dataset_state_ranges = [
            tuple(state_col.index[state_col != state_col.shift(-1)]) for state_col in state_cols
        ]
        # tuple of lists, each list is the row # for a specific state, list length is # of datasets
        self._state_ranges = tuple(map(list, zip(*dataset_state_ranges, strict=False)))

