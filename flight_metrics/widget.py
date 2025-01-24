"""File that creates and handles the foundation and main window of the GUI"""
from PyQt6.QtWidgets import QApplication, QWidget


class MetricsApp:
    """The main class that controls the window of the GUI"""

    def __init__(self) -> None:
        self._metric_app = QApplication([])
        self._window = QWidget()
        self._window.show()
        self._metric_app.exec()
