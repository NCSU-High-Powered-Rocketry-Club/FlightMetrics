"""."""
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from flight_metrics.constants import LAUNCH_PATHS

if TYPE_CHECKING:
    from flight_metrics.main_window import MainWindow


class DataManager:
    """Manages the data sets and what data is given to the plotter"""

    def __init__(self, parent: "MainWindow") -> None:
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
            self._datasets: list[pd.DataFrame] = [
                self._all_logs[name] for name in current_datasets if name in self._all_logs
            ]
            headers = [set(df.columns.to_list()) for df in self._datasets]
            unique_headers = headers[0]
            for header_index in range(len(headers) - 1):
                unique_headers.union(headers[header_index + 1])
            self._parent.update_data(unique_headers)

    def get_columns(self, x_axis: str, headers: list) -> list[list]:
        """Using the selected x axis and y axis data to plot, get the data and return as
        two or more (if multiple selected headers) lists in a list"""
        x_axis = "row_num" # default until I implement others
        x_list = []
        if x_axis == "row_num":
            max_len = max([len(df) for df in self._datasets])
            x_list = np.arange(max_len)
        y_list = []
        for num_header, header in enumerate(headers):
            y_list.append([])
            for num_df, df in enumerate(self._datasets):
                y_list[num_header].append([])
                y_list[num_header][num_df].append(df[header].tolist())
        return list[x_list,y_list]



