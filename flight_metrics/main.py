"""The main file"""

import sys
from pathlib import Path

import pyqtgraph as pg

from flight_metrics.main_window import MainWindow


def run_analyzer() -> None:
    """Entry point to run the analyzer. Starts when run with `uv run plot`."""
    app = pg.mkQApp("FlightMetrics")
    win = MainWindow()
    win.show()

    # We want to load the data after everything is shown, so it feels more responsive
    win.data_manager._load_logs()
    with Path.open("flight_metrics/style.qss") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    sys.exit(app.exec())


if __name__ == "__main__":
    run_analyzer()
