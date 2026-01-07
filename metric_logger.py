import os
import time
from datetime import datetime
import pandas as pd
import psutil
from from_root import from_root  # Ensure this is implemented correctly


# =========================
# CONFIGURATION
# =========================
CSV_FILE = os.path.join(from_root(), "notebooks", "Data", "system_metrics_binary.csv")
LOG_INTERVAL_SEC = 1  # Interval between metric recordings in seconds


# =========================
# INITIALIZE CSV
# =========================
def initialize_csv(file_path: str):
    """
    Create the CSV file with proper headers if it does not already exist.

    Args:
        file_path (str): Path to the CSV file to create.
    """
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=[
            "timestamp_ms",
            "datetime_utc",
            "cpu_ratio",
            "ram_ratio",
            "disk_ratio"
        ])
        df.to_csv(file_path, index=False)
        print(f"CSV file created at: {file_path}")
    else:
        print(f"CSV file already exists: {file_path}")


# =========================
# METRIC LOGGING LOOP
# =========================
def log_metrics():
    """
    Continuously monitor system metrics (CPU, RAM, Disk) and append them to the CSV file.

    - Records timestamp in milliseconds and UTC datetime.
    - CPU, RAM, and Disk usage ratios are stored as floats between 0.0 and 1.0.
    - Sleeps for LOG_INTERVAL_SEC between measurements.
    """
    while True:
        ts = int(time.time() * 1000)          # Timestamp in milliseconds
        dt = datetime.utcnow().isoformat()    # ISO UTC datetime

        # CPU usage ratio
        cpu = psutil.cpu_percent(interval=None) / 100.0

        # RAM usage ratio
        vm = psutil.virtual_memory()
        ram = vm.used / vm.total

        # Disk usage ratio
        disk = psutil.disk_usage("/")
        disk_ratio = disk.used / disk.total

        # Create a single-row DataFrame
        row = pd.DataFrame([{
            "timestamp_ms": ts,
            "datetime_utc": dt,
            "cpu_ratio": round(cpu, 4),
            "ram_ratio": round(ram, 4),
            "disk_ratio": round(disk_ratio, 4),
        }])

        # Append to CSV
        row.to_csv(CSV_FILE, mode="a", index=False, header=False)
        time.sleep(LOG_INTERVAL_SEC)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    initialize_csv(CSV_FILE)
    print("Starting system metrics logging...")
    log_metrics()
