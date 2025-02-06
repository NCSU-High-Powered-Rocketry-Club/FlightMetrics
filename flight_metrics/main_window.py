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
        self.data_manager = DataManager()
        self._set_layouts()

        self.flight_selector.flight_changed.connect(self.data_manager.update_flights)
        self.data_manager.datasets_changed.connect(self.data_selector.update_fields)
        self.data_manager.datasets_changed.connect(self.plot_container.update_state_rows)
        self.data_manager.datasets_changed.connect(self.plot_container._slider.slider.set_range)
        self.data_selector.fields_changed.connect(self.data_manager.get_data)
        self.data_manager.data_ready.connect(self.plot_container.graph.set_data)

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
        self.flight_selector = FlightSelector()
        left_layout.addItem(self.flight_selector)

        # adding plot container in middle
        self.plot_container = PlotContainer(data_manager=self.data_manager)
        mid_layout.addItem(self.plot_container)

        # adding data selector to right
        self.data_selector = DataSelector(self)
        right_layout.addItem(self.data_selector)

    def data_selector_updated(self, columns: list) -> None:
        """Updates the plot with the currently selected data."""
        data = self.data_manager.get_data(self, columns)
        if data[1]:
            self.plot_container._graph.set_graph_data(data[0], data[1])
        else:
            self.plot_container._graph.set_graph_data([], [])
        slider = self.plot_container._slider.slider
        slider.high_value = min(slider.high_value, len(data[0]))
        slider.low_value = 1 if slider.low_value > len(data[0]) else slider.low_value
        slider.max_value = len(data[0])
        slider.update()
