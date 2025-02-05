"""."""

import numpy as np
from pyqtgraph import PlotItem, PlotWidget


class Graph(PlotWidget):
    """."""

    def __init__(self):
        super().__init__()

        self._x, self._y = [], []
        self._plot_item: PlotItem = self.plot(self._x, self._y, pen="w")

    def update_graph_limits(self, min_x: int, max_x: int):
        self._x_lim = self._x[min_x:max_x]
        self._y_lim = self._y[min_x:max_x]
        self._plot_item.setData(self._x_lim, self._y_lim)

    def set_graph_data(self, x: list, y: list):
        """plots the data"""
        self._x = x
        self._y = y
        self.update_graph_limits(0, len(self._y))
