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
        self._data_manager = DataManager(self)
        self._set_layouts()

    def _set_layouts(self) -> None:
        """Configures the main window's layout and initializes the plot, flight selector, and
        data selector"""
        # splitting layout into 3 columns
        left_layout = self._layout.addLayout(row=0, col=0, rowspan=1)
        mid_layout = self._layout.addLayout(row=0, col=1, rowspan=1)
        right_layout = self._layout.addLayout(row=0, col=2, rowspan=1)

        # setting column widths
        left_layout.setFixedWidth(300)
        right_layout.setFixedWidth(300)

        # adding launch data selector on left side
        self.flight_selector = FlightSelector(self)
        left_layout.addItem(self.flight_selector)

        # adding plot container in middle
        self._plot_container = PlotContainer(data_manager=self._data_manager)
        mid_layout.addItem(self._plot_container)

        # adding data selector to right
        self._data_selector = DataSelector(self)
        right_layout.addItem(self._data_selector)

    def update_data_manager(self, log_names: list[str]) -> None:
        """when a new flight is selected or removed in flight selector, this method is called
        which tells the data manager to refresh the available data sets"""
        # log names is a list of the names of the logs, in title case with spaces instead of
        # underscores, and some leading whitespace.
        self._data_manager.refresh_data(log_names)

    def update_data(self, unique_headers: set) -> None:
        """Using the unique headers from data manager, updates the data selector with the
        available headers"""
        self._data_selector.update_headers(unique_headers)

    def update_plot(self, columns_to_plot: list) -> None:
        """Updates the plot with the currently selected data."""
        data = self._data_manager.get_columns(self, columns_to_plot)
        print(data)
        #self._plot_container._graph.set_graph_data(data[0], data[1])
