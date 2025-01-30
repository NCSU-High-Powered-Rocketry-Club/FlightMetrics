"""."""

from pyqtgraph import GraphicsLayout
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget

from flight_metrics.graph import Graph
from flight_metrics.range_slider import RangeSlider
from flight_metrics.state_button import StateButton


class PlotContainer(GraphicsLayout):
    """."""

    def __init__(self):
        super().__init__()

        self._plot_layout = self.addLayout(row=0, col=0)
        self._toolbar_layout = self.addLayout(row=1, col=0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # graph setup
        graph = Graph()
        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(graph)
        self._plot_layout.addItem(proxy_widget)
        self._plot_layout.setBorder(100, 100, 100)
        self._plot_layout.setContentsMargins(0, 0, 0, 10)

        # toolbar setup
        self._selected_states: list = [0, 1, 2, 3, 4]
        self._setup_toolbar()

    def _setup_toolbar(self) -> None:
        """."""
        self._toolbar_layout.setFixedHeight(200)
        self._toolbar_layout.setBorder(100, 100, 100)
        self._toolbar_layout.setContentsMargins(0, 0, 0, 0)

        # adding buttons to layout
        button_names = ["Standby", "Motor Burn", "Coast", "Freefall", "Landed"]
        for i, name in enumerate(button_names):
            state_button = StateButton(self, name)
            state_button.setMinimumHeight(50)
            self._toolbar_layout.addItem(state_button, row=0, col=i)

        self._slider = RangeSlider(min_value=0, max_value=1000, start_min=0, start_max=1000)
        self._toolbar_layout.addItem(self._slider, row=1, col=0, colspan=5)

    def quick_set_slider(self, state_id: int):
        if state_id in self._selected_states:
            self._selected_states.remove(state_id)
        else:
            self._selected_states.append(state_id)
        if not self._selected_states:
            # If the list is empty, min() and max() will error, so instead just set the handles
            # to whatever the minimum value currently is.
            self._slider.slider.set_handles(
                self._slider.slider.low_value, self._slider.slider.low_value
            )
        else:
            low_val = min(self._selected_states) * 200
            high_val = (max(self._selected_states) + 1) * 200
            self._slider.slider.set_handles(low_val, high_val)
