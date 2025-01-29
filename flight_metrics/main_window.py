"""File that creates and handles the foundation and main window of the GUI"""

from pyqtgraph import GraphicsLayout, GraphicsView

from flight_metrics.data_selector import DataSelector
from flight_metrics.flight_selector import FlightSelector
from flight_metrics.plot_container import PlotContainer


class MainWindow(GraphicsView):
    """The main class that controls the window of the GUI"""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Flight Metrics")
        self.resize(1280, 720)

        layout = GraphicsLayout(border=(100, 100, 100))
        self.setCentralItem(layout)
        self._layout = layout
        self._set_layouts()

    def _set_layouts(self) -> None:
        # splitting layout into 3 columns
        left_layout = self._layout.addLayout(row=0, col=0)
        mid_layout = self._layout.addLayout(row=0, col=1)
        right_layout = self._layout.addLayout(row=0, col=2)

        # setting column widths
        left_layout.setFixedWidth(300)
        right_layout.setFixedWidth(300)

        # adding launch data selector on left side
        flight_selector = FlightSelector()
        left_layout.addItem(flight_selector)

        # adding plot container in middle
        plot_container = PlotContainer()
        mid_layout.addItem(plot_container)

        # adding data selector to right
        data_selector = DataSelector()
        right_layout.addItem(data_selector)
