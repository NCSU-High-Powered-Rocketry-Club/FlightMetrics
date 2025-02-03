"""."""

import shutil
import subprocess
from pathlib import Path

from pyqtgraph.Qt.QtWidgets import QPushButton

from flight_metrics.constants import LAUNCH_PATHS


class PullDataButton(QPushButton):
    """."""

    def __init__(self):
        super().__init__()

        self.clicked.connect(self.button_clicked)
        self.set_style()
        self._is_running = False

    def set_style(self) -> None:
        self.setText("Pull")
        self.setFixedSize(40, 40)
        self.setCheckable(True)

    def button_clicked(self) -> None:
        """Run AirbrakesV2 (uv run mock -d -f -l -p [launch file path]). Then rename and move the
        resulting log files to this repo"""
        if not self._is_running:
            self._is_running = True
            self.setChecked(True)
            airbrakes_path = self._get_airbrakes_path()
            self._run_airbrakes(airbrakes_path)
            self._collect_files(airbrakes_path)

    def _get_airbrakes_path(self) -> Path:
        """gets the users path to AirbrakesV2 repo. It should always be in this repo's parent
        folder, but it will check one deeper if not."""
        parent_folder = Path(__file__).parent.parent.parent
        if Path.exists(parent_folder / "AirbrakesV2"):
            return Path(parent_folder / "AirbrakesV2")
        if Path.exists(parent_folder.parent / "AirbrakesV2"):
            return Path(parent_folder.parent / "AirbrakesV2")
        raise FileNotFoundError(
            "AirbrakesV2 repo should be located in the parent folder of this repository"
        ) from FileNotFoundError

    def _run_airbrakes(self, airbrakes_path: Path) -> None:
        for launch_log in LAUNCH_PATHS:
            airbrakes_launch_log_path = "launch_data/" + launch_log

            if not (airbrakes_path / Path(airbrakes_launch_log_path)).resolve().exists():
                raise FileNotFoundError(f"Launch file not found: {airbrakes_launch_log_path}")

            command = [
                "uv",
                "run",
                "--directory",
                str(airbrakes_path),  # Change working directory to AirbrakesV2 repo
                "mock",
                "-d",
                "-f",
                "-l",
                "-p",
                str((airbrakes_path / Path(airbrakes_launch_log_path)).resolve()),
            ]
            command = " ".join(command)
            try:
                # Run the command inside AirbrakesV2 directory
                process = subprocess.run(  # noqa: S602
                    command,
                    capture_output=True,
                    text=True,
                    shell=True,
                    check=True,
                )
                if process.stdout:
                    print(f"AirbrakesV2 Output:\n{process.stdout}")
                if process.stderr:
                    print(f"AirbrakesV2 Error Output:\n{process.stderr}")
            except subprocess.CalledProcessError as e:
                # Print error output if the command fails
                print(f"Error running AirbrakesV2:\n{e.stderr}")
            print(f"finished {airbrakes_launch_log_path}")

    def _collect_files(self, airbrakes_path: Path) -> None:
        """Collects log files from AirbrakesV2/logs, renames them, and moves them to
        FlightMetrics/launch_logs."""

        logs_dir = airbrakes_path / "logs"
        if not logs_dir.exists():
            raise FileNotFoundError(f"Logs directory not found: {logs_dir}")

        # Define destination folder (FlightMetrics repo)
        flight_metrics_path = Path(__file__).parent.parent
        launch_logs_dir = flight_metrics_path / "launch_logs"

        # Get all log files sorted alphabetically
        log_files = sorted(logs_dir.glob("log_*.csv"))

        # Take the last logs, same length as LAUNCH_PATHS
        latest_logs = log_files[len(log_files)-len(LAUNCH_PATHS) :]
        if len(latest_logs) < len(LAUNCH_PATHS):
            print(
                f"Warning: Only found {len(latest_logs)} log files, expected {len(LAUNCH_PATHS)}."
            )

        # Iterate through the logs and rename/move them
        for log_file, new_name in zip(latest_logs, LAUNCH_PATHS, strict=False):
            print(log_file)
            new_file = launch_logs_dir / new_name
            if not new_file.exists():
                with Path.open(new_file, "x"):
                    pass
            shutil.copy(log_file, new_file)  # Move and overwrite existing files
        print("Done!")
        self._is_running = False
        self.setChecked(False)
