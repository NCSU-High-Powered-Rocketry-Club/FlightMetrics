"""The main file"""

import sys
from pathlib import Path

import pyqtgraph as pg

from flight_metrics.main_window import MainWindow


def run_analyzer() -> None:
    """Entry point to run the analyzer. Starts when run with `uv run plot`."""
    app = pg.mkQApp("FlightMetrics")
    with Path.open("flight_metrics/style.qss") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_analyzer()
