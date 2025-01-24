"""The main file """

from flight_metrics.widget import MetricsApp


def run_analyzer() -> None:
    """Entry point to run the analyzer. Starts when run with `uv run plot`."""
    metrics_app = MetricsApp()



if __name__ == "__main__":
    run_analyzer()
