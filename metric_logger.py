import os
import time
from datetime import datetime
import pandas as pd
import psutil
from from_root import from_root


# =========================
# CONFIGURATION
# =========================
CSV_FILE = os.path.join(
    from_root(),
    "notebooks",
    "Data",
    "system_metrics_binary.csv"
)

LOG_INTERVAL_SEC = 1


# =========================
# CSV INITIALIZATION
# =========================
CSV_COLUMNS = [
    "timestamp_ms",
    "datetime_utc",
    "cpu_ratio",
    "ram_ratio",
    "disk_ratio"
]


def initialize_csv(file_path: str):
    """
    Ensure CSV exists with correct schema.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if not os.path.exists(file_path):
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(
            file_path,
            index=False
        )


# =========================
# METRIC LOGGER
# =========================
def log_metrics():
    """
    Log system metrics to CSV at fixed intervals.
    Output is append-only and pipeline-compatible.
    """
    initialize_csv(CSV_FILE)

    while True:
        ts = int(time.time() * 1000)
        dt = datetime.utcnow().isoformat()

        cpu = psutil.cpu_percent(interval=None) / 100.0

        vm = psutil.virtual_memory()
        ram = vm.used / vm.total

        disk = psutil.disk_usage("/")
        disk_ratio = disk.used / disk.total

        row = {
            "timestamp_ms": ts,
            "datetime_utc": dt,
            "cpu_ratio": round(cpu, 4),
            "ram_ratio": round(ram, 4),
            "disk_ratio": round(disk_ratio, 4),
        }

        pd.DataFrame([row]).to_csv(
            CSV_FILE,
            mode="a",
            index=False,
            header=False
        )

        time.sleep(LOG_INTERVAL_SEC)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    log_metrics()
