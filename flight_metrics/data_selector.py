"""."""

from pyqtgraph import GraphicsLayout, LabelItem


class DataSelector(GraphicsLayout):
    """."""

    def __init__(self):
        super().__init__()

        label = LabelItem(text="Data Selector", size="14pt")
        self.addItem(label)
