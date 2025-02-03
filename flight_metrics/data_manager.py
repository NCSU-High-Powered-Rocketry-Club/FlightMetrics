"""."""

from pathlib import Path

import pandas as pd

from flight_metrics.constants import LAUNCH_PATHS


class DataManager:
    """Manages the data sets and what data is given to the plotter"""

    def __init__(self, parent) -> None:
        self._all_logs: dict | None = None
        self._parent = parent

    def _load_logs(self):
        self._all_logs = {}
        launch_log_folder = Path(__file__).parent.parent / "launch_logs"
        for path in LAUNCH_PATHS:
            # converting the default log_name.csv to "Log Name" so the dict key is nice
            name = Path(path).stem.replace("_", " ").title()
            df = pd.read_csv(launch_log_folder / path, dtype={"invalid_fields": str})
            self._all_logs.update({name: df})

    def refresh_data(self, current_datasets: list):
        """Called when the current data set(s) change. Will modify the selectable data
        that the user is able to plot, and update the necessary values for sliders and state
        buttons."""
        if current_datasets:
            datasets: list[pd.DataFrame] = [
                self._all_logs[name] for name in current_datasets if name in self._all_logs
            ]
            state_cols = [df["state_letter"] for df in datasets]

