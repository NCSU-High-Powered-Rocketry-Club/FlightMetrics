"""."""

import numpy as np
from pyqtgraph import PlotItem, PlotWidget

from flight_metrics.constants import GRAPH_COLORS


class Graph(PlotWidget):
    """."""

    def __init__(self):
        super().__init__()

        self._data = [[()]]
        self._plot_item: PlotItem = self.plot(self._data[0][0], self._data[0][0], pen="w")

    def update_graph_limits(self, min_x: int, max_x: int):
        self.setXRange(min_x, max_x)

    def set_graph_state_data(self, state_range: tuple[list], current_states: list):
        """Called when a valid state button is clicked. Takes the current data, and limits the
        range"""
        self.clear()
        i = 0
        for header_data_list in self._data:
            for idx, xy_data in enumerate(header_data_list):
                x_min = 0 if min(current_states) == 0 else state_range[min(current_states) - 1][idx]
                x_max = state_range[max(current_states)][idx]
                filtered_data = self.filter_nan_values(
                    (xy_data[0][x_min:x_max], xy_data[1][x_min:x_max])
                )

                self.plot(filtered_data[0], filtered_data[1], pen=self.colors[i])
                i += 1

    def filter_nan_values(self, data_points: tuple[list]) -> tuple[list]:
        mask = ~np.isnan(data_points[1])
        return (data_points[0][mask].tolist(), data_points[1][mask].tolist())

    def set_data(self, data: list[list[tuple]]):
        """Called whenever new fields are selected"""
        self._data = data
        self.clear()
        self.colors = self._set_colors(data)
        i = 0
        for header_data_list in data:
            for xy_data in header_data_list:
                filtered_data = self.filter_nan_values(xy_data)
                self.plot(filtered_data[0], filtered_data[1], pen=self.colors[i])
                i += 1

    def _set_colors(self, data: list[list[tuple]]) -> list:
        num_data = sum(len(header_data_list) for header_data_list in data)  # Count total entries
        return [GRAPH_COLORS[i % len(GRAPH_COLORS)] for i in range(num_data)]
