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
        self._plot_container = PlotContainer(parent=self, data_manager=self._data_manager)
        mid_layout.addItem(self._plot_container)

        # adding data selector to right
        self._data_selector = DataSelector(self)
        right_layout.addItem(self._data_selector)

    def flight_selector_updated(self, log_names: list[str]) -> None:
        """when a new flight is selected or removed in flight selector, this method is called
        which tells the data manager to refresh the available data sets"""
        # log names is a list of the names of the logs, in title case with spaces instead of
        # underscores, and some leading whitespace.
        self._data_manager.refresh_data(log_names)

    def data_selector_updated(self, columns: list) -> None:
        """Updates the plot with the currently selected data."""
        data = self._data_manager.get_data(self, columns)
        if data[1]:
            self._plot_container._graph.set_graph_data(data[0], data[1])
        else:
            self._plot_container._graph.set_graph_data([], [])
        slider = self._plot_container._slider.slider
        slider.high_value = min(slider.high_value, len(data[0]))
        slider.low_value = 1 if slider.low_value > len(data[0]) else slider.low_value
        slider.max_value = len(data[0])
        slider.update()

    def state_button_updated(self, selected_states: list, new_state: int) -> None:
        """When a valid state button is selected, this moves the slider"""
        slider = self._plot_container._slider.slider

        low_val = slider.low_value
        high_val = slider.high_value

        if not selected_states:
            # If the list is empty, min() and max() will error, so instead just set the handles
            # to whatever the minimum value currently is.
            slider.set_handles(low_val, low_val)
        else:
            # determine which slider should move. We don't want both to be set, becuase it will
            # override any fine-tuning on both sliders.
            if max(selected_states) == new_state or max(selected_states) + 1 == new_state:
                high_val = (max(selected_states) + 1) * (max(state_ranges[-1]) / 5)
            if min(selected_states) == new_state or min(selected_states) - 1 == new_state:
                low_val = min(selected_states) * (max(state_ranges[-1]) / 5)
            slider.set_handles(low_val, high_val)
