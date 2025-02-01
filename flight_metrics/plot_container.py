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

        self._buttons: list[StateButton] = [] # the state button objects
        self._selected_states: list = [0, 1, 2, 3, 4] # the currently selected states
        # a list of the end row number of each state
        self._state_ranges: list[list[int]] = [
            [10000,],
            [14000,],
            [40000,],
            [200000,],
            [205000,],
            ]

        self._setup()


    def _setup(self) -> None:
        self._plot_layout = self.addLayout(row=0, col=0)
        self._toolbar_layout = self.addLayout(row=1, col=0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # graph setup
        self._graph = Graph()
        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(self._graph)
        self._plot_layout.addItem(proxy_widget)
        self._plot_layout.setBorder(100, 100, 100)
        self._plot_layout.setContentsMargins(0, 0, 0, 10)

        # toolbar setup
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
            self._buttons.append(state_button)
            self._toolbar_layout.addItem(state_button, row=0, col=i)

        self._slider = RangeSlider(
            parent=self,
            min_value=0,
            max_value=max(self._state_ranges[-1]),
            start_min=0,
            start_max=max(self._state_ranges[-1]),
            )
        self._toolbar_layout.addItem(self._slider, row=1, col=0, colspan=5)

    def check_new_state(self, state_id: int) -> None:
        """Determines if the newly selected state is valid. It is invalid if there are gaps in the
        selected states"""
        button = self._buttons[state_id].button

        # if a button is selected and there is nothing that is currently selected, this is
        # always a valid selection
        if not self._selected_states:
            button.setChecked(True)
            self._selected_states.append(state_id)
            self._quick_set_slider(state_id)
        else:
            # valid selections are only those that are the minimum or maximum of the selected state
            # list or minimum - 1, maximum + 1.
            allowable_selections = [
                min(self._selected_states)-1,
                min(self._selected_states),
                max(self._selected_states),
                max(self._selected_states)+1,
                ]
            if state_id in allowable_selections:
                button.setChecked(not button.isChecked())
                self._selected_states.remove(state_id) if state_id in self._selected_states else self._selected_states.append(state_id)
                self._quick_set_slider(state_id)

    def _quick_set_slider(self, state_id: int) -> None:
        """When a valid state button is selected, the range slider moves to the selected state"""

        low_val = self._slider.slider.low_value
        high_val = self._slider.slider.high_value

        if not self._selected_states:
            # If the list is empty, min() and max() will error, so instead just set the handles
            # to whatever the minimum value currently is.
            self._slider.slider.set_handles(low_val, low_val)
        else:
            # determine which slider should move. We don't want both to be set, becuase it will
            # override any fine-tuning on both sliders.
            if max(self._selected_states) == state_id or max(self._selected_states) + 1 == state_id:
                high_val = (max(self._selected_states) + 1) * (max(self._state_ranges[-1]) / 5)
            if min(self._selected_states) == state_id or min(self._selected_states) - 1 == state_id:
                low_val = min(self._selected_states) * (max(self._state_ranges[-1]) / 5)
            self._slider.slider.set_handles(low_val, high_val)

    def range_update(self, low: int, high: int) -> None:
        """called whenever the slider range updates"""
        self._graph.update_graph_limits(low, high)


