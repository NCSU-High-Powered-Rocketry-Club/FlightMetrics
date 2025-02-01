"""."""
import numpy as np
from pyqtgraph import PlotItem, PlotWidget


class Graph(PlotWidget):
    """."""

    def __init__(self):
        super().__init__()

        self._x,self._y = self._test_data()
        self._plot_item: PlotItem = self.plot(self._x, self._y)

    def _test_data(self):
        x = np.arange(205000)
        y = np.power(x, 2) / 1e8
        y = y + (y / 2) * np.sin(x / 4000)
        return x,y

    def update_graph_limits(self, min_x: int, max_x: int):
        x_lim = self._x[min_x : max_x]
        y_lim = self._y[min_x : max_x]
        self._plot_item.setData(x_lim, y_lim)
