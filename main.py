import os
import time
from datetime import datetime
import pandas as pd
import psutil
import joblib

from from_root import from_root


# =========================
# CONFIGURATION
# =========================
OUTPUT_DIR = os.path.join(from_root(), "output")
LOG_DIR = os.path.join(OUTPUT_DIR, "test_results")

INFERENCE_CSV = os.path.join(LOG_DIR, "system_inference_log.csv")

LOG_INTERVAL_SEC = 1
FEATURES = ["cpu_ratio", "ram_ratio", "disk_ratio"]

PIPELINE_FILE = os.path.join(
    from_root(),
    "models",
    "supervised_pipeline_simple.joblib"
)


# =========================
# CSV SCHEMA
# =========================
CSV_COLUMNS = [
    "timestamp_ms",
    "datetime_utc",
    "cpu_ratio",
    "ram_ratio",
    "disk_ratio",
    "predicted_stress"
]


# =========================
# INITIALIZATION
# =========================
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(INFERENCE_CSV):
    pd.DataFrame(columns=CSV_COLUMNS).to_csv(
        INFERENCE_CSV,
        index=False
    )

if not os.path.exists(PIPELINE_FILE):
    raise FileNotFoundError(f"Pipeline not found: {PIPELINE_FILE}")

pipeline = joblib.load(PIPELINE_FILE)
preprocessor = pipeline.named_steps["preprocess"]
model = pipeline.named_steps["clf"]


# =========================
# ALERT
# =========================
def beep():
    """
    Emit an audible alert to signal an anomaly detection event.

    On Windows systems, this uses the `winsound.Beep` API.
    On non-Windows systems, it falls back to emitting a
    terminal bell character, which may or may not produce sound
    depending on terminal configuration.
    """
    try:
        import winsound
        winsound.Beep(1000, 500)
    except ImportError:
        print("\a")


# =========================
# MONITORING LOOP
# =========================
def monitor_system():
    """
    Continuously monitor system resource usage and detect anomalies.

    This function:
    - Samples CPU, RAM, and disk usage at a fixed interval
    - Transforms metrics using a pre-trained preprocessing pipeline
    - Predicts system stress using a trained supervised model
    - Logs all observations and predictions to a CSV file
    - Triggers an audible alert and console warning on anomaly detection

    The loop runs indefinitely until interrupted by the user
    (Ctrl+C).
    """
    print("System monitoring started. Press Ctrl+C to stop.")

    try:
        while True:
            # Time metadata
            ts = int(time.time() * 1000)
            dt = datetime.utcnow().isoformat()

            # System metrics
            cpu = psutil.cpu_percent(interval=None) / 100.0
            ram = psutil.virtual_memory().used / psutil.virtual_memory().total
            disk_ratio = psutil.disk_usage("/").used / psutil.disk_usage("/").total

            # Model input
            X_raw = pd.DataFrame(
                [[cpu, ram, disk_ratio]],
                columns=FEATURES
            )

            X_processed = preprocessor.transform(X_raw)
            predicted_stress = int(model.predict(X_processed)[0])
            predicted_label = 'anomaly' if predicted_stress == 1 else 'normal'

            # Log to CSV
            row = {
                "timestamp_ms": ts,
                "datetime_utc": dt,
                "cpu_ratio": round(cpu, 4),
                "ram_ratio": round(ram, 4),
                "disk_ratio": round(disk_ratio, 4),
                "predicted_stress": predicted_label
            }

            pd.DataFrame([row]).to_csv(
                INFERENCE_CSV,
                mode="a",
                index=False,
                header=False
            )

            # Trigger beep on anomaly
            if predicted_stress == 1:
                print(
                    f"[{dt}] ⚠ Anomaly Detected | "
                    f"CPU={cpu:.4f}, RAM={ram:.4f}, Disk={disk_ratio:.4f}, "
                    f"Prediction={predicted_label}"
                )
                beep()

            time.sleep(LOG_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    """
    Entry point for real-time system monitoring.

    Loads the trained inference pipeline and starts the
    continuous monitoring loop. Intended to be run as a
    standalone process for live anomaly detection.
    """
    monitor_system()
