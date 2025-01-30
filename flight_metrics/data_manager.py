"""."""

from flight_metrics.constants import LAUNCH_PATHS
import pandas as pd
from pathlib import Path


class DataManager:
    """Manages the data sets and what data is given to the plotter"""

    def __init__(self) -> None:
        self._all_logs: dict | None = None
        self._load_logs()

    def _load_logs(self):
        self._all_logs = {}
        launch_log_folder = Path(__file__).parent.parent / "launch_logs"
        for path in LAUNCH_PATHS:
            # converting the default log_name.csv to "Log Name" so the dict key is nice
            name = Path(path).stem.replace("_", " ").title()
            df = pd.read_csv(launch_log_folder / path, dtype={"invalid_fields": str})
            self._all_logs.update({"name": df})
