import os
import time
from datetime import datetime
import pandas as pd
import psutil
from from_root import from_root
import os

# =========================
# CONFIG
# =========================
CSV_FILE = os.path.join(from_root(),"notebooks/Data/system_metrics_binary.csv")
LOG_INTERVAL_SEC = 1

CPU_STRESS = 0.85
RAM_STRESS = 0.80
DISK_STRESS = 0.90

# =========================
# INIT CSV
# =========================
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "timestamp_ms",
        "datetime_utc",
        "cpu_ratio",
        "ram_ratio",
        "disk_ratio",
        "label"   # 0 = normal, 1 = stress
    ]).to_csv(CSV_FILE, index=False)

# =========================
# LABEL DECIDER (BINARY)
# =========================
def decide_label(cpu, ram, disk):
    if cpu > CPU_STRESS or ram > RAM_STRESS or disk > DISK_STRESS:
        return 1
    return 0

# =========================
# METRIC LOOP
# =========================
def log_metrics():
    while True:
        ts = int(time.time() * 1000)
        dt = datetime.utcnow().isoformat()

        cpu = psutil.cpu_percent(interval=None) / 100.0

        vm = psutil.virtual_memory()
        ram = vm.used / vm.total

        disk = psutil.disk_usage("/")
        disk_ratio = disk.used / disk.total

        label = decide_label(cpu, ram, disk_ratio)

        row = pd.DataFrame([{
            "timestamp_ms": ts,
            "datetime_utc": dt,
            "cpu_ratio": round(cpu, 4),
            "ram_ratio": round(ram, 4),
            "disk_ratio": round(disk_ratio, 4),
            "label": label
        }])

        row.to_csv(CSV_FILE, mode="a", index=False, header=False)
        time.sleep(LOG_INTERVAL_SEC)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    log_metrics()
