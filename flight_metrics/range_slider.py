"""."""
from pyqtgraph.Qt.QtCore import QPoint, Qt, pyqtSignal
from pyqtgraph.Qt.QtGui import QBrush, QColor, QPainter, QPen
from pyqtgraph.Qt.QtWidgets import QGraphicsProxyWidget, QWidget


class RangeSlider(QGraphicsProxyWidget):
    """A QGraphicsProxyWidget containing the range slider widget."""
    def __init__(self, min_value=0, max_value=100, start_min=20, start_max=80):
        super().__init__()
        self.slider = SliderWidget(min_value, max_value, start_min, start_max)
        self.setWidget(self.slider)

class SliderWidget(QWidget):
    """Custom QWidget to handle painting and events."""
    rangeChanged = pyqtSignal(int, int)

    def __init__(self, min_value=0, max_value=100, start_min=20, start_max=80):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.low_value = start_min
        self.high_value = start_max
        self.handle_radius = 8  # Size of draggable handles
        self.bar_height = 6  # Thickness of the bar
        self.setMinimumSize(300, 40)
        self.setMouseTracking(True)
        self.dragging = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        margin = self.handle_radius

        low_x = margin + (self.low_value - self.min_value) / (self.max_value - self.min_value) * (width - 2 * margin)
        high_x = margin + (self.high_value - self.min_value) / (self.max_value - self.min_value) * (width - 2 * margin)

        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRect(margin, height // 2 - self.bar_height // 2, width - 2 * margin, self.bar_height)

        painter.setBrush(QBrush(QColor(100, 150, 255)))
        painter.drawRect(int(low_x), height // 2 - self.bar_height // 2, int(high_x - low_x), self.bar_height)

        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.drawEllipse(QPoint(int(low_x), height // 2), self.handle_radius, self.handle_radius)
        painter.drawEllipse(QPoint(int(high_x), height // 2), self.handle_radius, self.handle_radius)

    def mousePressEvent(self, event):
        x = event.position().x()
        low_x = self._value_to_x(self.low_value)
        high_x = self._value_to_x(self.high_value)

        if abs(x - low_x) <= self.handle_radius:
            self.dragging = "low"
        elif abs(x - high_x) <= self.handle_radius:
            self.dragging = "high"

    def mouseMoveEvent(self, event):
        if self.dragging is None:
            return

        x = event.position().x()
        value = self._x_to_value(x)

        if self.dragging == "low":
            value = max(value, self.min_value)
            if value >= self.high_value:
                value = self.high_value - 1
            self.low_value = value
        elif self.dragging == "high":
            value = min(value, self.max_value)
            if value <= self.low_value:
                value = self.low_value + 1
            self.high_value = value

        self.rangeChanged.emit(self.low_value, self.high_value)
        self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = None

    def _value_to_x(self, value):
        width = self.width()
        margin = self.handle_radius
        return margin + (value - self.min_value) / (self.max_value - self.min_value) * (width - 2 * margin)

    def _x_to_value(self, x):
        width = self.width()
        margin = self.handle_radius
        x = max(margin, min(x, width - margin))
        return round(self.min_value + (x - margin) / (width - 2 * margin) * (self.max_value - self.min_value))


