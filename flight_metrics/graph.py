"""."""

from pyqtgraph import PlotWidget


class Graph(PlotWidget):
    """."""

    def __init__(self):
        super().__init__()
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 15, 30, 25]
        self.plot(x, y)
