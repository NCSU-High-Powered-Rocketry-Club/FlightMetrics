"""File that creates and handles the foundation and main window of the GUI"""

from pyqtgraph import GraphicsLayout, GraphicsView

from flight_metrics.data_manager import DataManager
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
        self._data_manager = DataManager()

    def _set_layouts(self) -> None:
        # splitting layout into 3 columns
        left_layout = self._layout.addLayout(row=0, col=0, rowspan=1)
        mid_layout = self._layout.addLayout(row=0, col=1, rowspan=1)
        right_layout = self._layout.addLayout(row=0, col=2, rowspan=1)

        # setting column widths
        left_layout.setFixedWidth(300)
        right_layout.setFixedWidth(300)

        # adding launch data selector on left side
        flight_selector = FlightSelector(self)
        left_layout.addItem(flight_selector)

        # adding plot container in middle
        plot_container = PlotContainer()
        mid_layout.addItem(plot_container)

        # adding data selector to right
        data_selector = DataSelector()
        right_layout.addItem(data_selector)

    def update_data(self, log_names: list[str]) -> None:
        # log names is a list of the names of the logs, in title case with spaces instead of
        # underscores, and some leading whitespace.
        log_files = [name.lower().strip().replace(" ", "_") + ".csv" for name in log_names]
