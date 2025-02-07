"""."""

from pathlib import Path

import numpy as np
import pandas as pd
from pyqtgraph.Qt.QtCore import QObject, pyqtSignal

from flight_metrics.constants import LAUNCH_PATHS


class DataManager(QObject):
    """Manages the data sets and what data is given to the plotter"""

    datasets_changed = pyqtSignal(list)
    data_ready = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self._all_logs: dict | None = None

    def _load_logs(self):
        self._all_logs = {}
        launch_log_folder = Path(__file__).parent.parent / "launch_logs"
        for path in LAUNCH_PATHS:
            # converting the default log_name.csv to "Log Name" so the dict key is nice
            name = Path(path).stem.replace("_", " ").title()
            df = pd.read_csv(launch_log_folder / path, dtype={"invalid_fields": str})
            self._all_logs.update({name: df})

    def update_flights(self, current_datasets: list[str]) -> None:
        """Called when flight selector updates. Will modify the selectable data
        that the user is able to plot, and update the necessary values for sliders and state
        buttons."""
        self._datasets: list[pd.DataFrame] = [
            self._all_logs[name] for name in current_datasets if name in self._all_logs
        ]
        self.datasets_changed.emit(self._datasets)

    def get_data(self, x_field, y_fields: list) -> None:
        """Updated when a field is selected/removed. Gets the data and updates
        the signal with the columns to plot"""
        if not x_field or not y_fields:
            self.data_ready.emit([[()]])
            return
        data_list = []
        for num_header, header in enumerate(y_fields):
            data_list.append([])
            for df in self._datasets:
                data_with_nan = np.array(df[header].tolist())
                x_unfiltered = (
                    np.arange(len(data_with_nan))
                    if x_field == "row_num"
                    else np.array(df[x_field].tolist())
                )

                plot_pair = (x_unfiltered, data_with_nan)
                data_list[num_header].append(plot_pair)
        self.data_ready.emit(data_list)
