"""."""

from pyqtgraph import GraphicsLayout, LabelItem


class FlightSelector(GraphicsLayout):
    """."""

    def __init__(self):
        super().__init__()

        label = LabelItem(text="Flight Selector", size="14pt")
        self.addItem(label)
