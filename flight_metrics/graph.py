"""."""

import numpy as np
from pyqtgraph import PlotItem, PlotWidget, ScatterPlotItem, TextItem, mkBrush


class Graph(PlotWidget):
    """."""

    def __init__(self):
        super().__init__()

        self._x, self._y = self._test_data()
        self._plot_item: PlotItem = self.plot(self._x, self._y, pen="w")

        # Create scatter plot item for hover detection
        self.scatter = ScatterPlotItem(
            self._x, self._y, size=5, brush=mkBrush(255, 0, 0, 120), hoverable=True
        )
        self.addItem(self.scatter)
        self.scatter.sigHovered.connect(self.on_hover)

        self.scatter.setOpacity(0.001)
        self.scatter.setSize(5)

        # Create a text label to show coordinates
        self.label = TextItem("", anchor=(0, 1), color="g")
        self.label.hide()
        self.addItem(self.label)

    def _test_data(self):
        x = np.arange(205000)
        y = np.power(x, 2) / 1e8
        y = y + (y / 2) * np.sin(x / 4000)
        return x, y

    def on_hover(self, _event, points: list):
        """Show the coordinates of the hovered point."""
        if len(points) > 0:
            point = points[0]
            x, y = point.pos()
            self.label.setText(f"({x:.1f}, {y:.1f})")
            self.label.setPos(x, y)
            self.label.show()

    def update_graph_limits(self, min_x: int, max_x: int):
        self._x_lim = self._x[min_x:max_x]
        self._y_lim = self._y[min_x:max_x]
        self._plot_item.setData(self._x_lim, self._y_lim)

        # if you just hide and show the scatter plot when moving the slider, the x and y limits of
        # the graph have very small jumps that don't look clean. By only setting min and maxs of x
        # and y points of the scatter, performance is still good, but no jumpy limits when moving
        if len(self._x_lim) > 0:
            self.scatter.setData(
                [self._x_lim[0], self._x_lim[-1]], [min(self._y_lim), max(self._y_lim)]
            )

    def _get_visible_data_points(self) -> int:
        """Returns the number of data points currently visible on the screen."""
        mask = 0
        if len(self._x_lim) > 0:
            mask = (self._x >= self._x_lim[0]) & (self._x <= self._x_lim[-1])
        return np.count_nonzero(mask)

    def update_scatter_limits(self, option: int):
        """updates the scatter plot. Because scatter plot is incredibly slow, and the only
        purpose is to assist the coordinate labeling, it is hidden while sliding, and only
        updates at the end of the slide, when it is released"""
        if option == 0:
            self.label.hide()
        if option == 1:
            self.scatter.setData(self._x_lim, self._y_lim)
            num_points_on_screen = self._get_visible_data_points()
            self.scatter.setOpacity(
                0.5
            ) if num_points_on_screen <= 200 else self.scatter.setOpacity(0.001)

    def set_graph_data(self, x: list, y: list[list]):
        """plots the data"""

        #self._x = x
        #self._y = y[0][0]

