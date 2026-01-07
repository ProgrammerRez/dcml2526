import os
import time
from datetime import datetime
import pandas as pd
import psutil
import joblib
from from_root import from_root  # Make sure this is correctly implemented


# =========================
# CONFIGURATION
# =========================
OUTPUT_DIR = os.path.join(from_root(), "output")               # Top-level output directory
TEST_RESULTS_DIR = os.path.join(OUTPUT_DIR, "test_results")   # Folder for anomaly logs
ANOMALY_LOG = os.path.join(TEST_RESULTS_DIR, "anomalies.txt") # Anomaly log file

LOG_INTERVAL_SEC = 1
FEATURES = ["cpu_ratio", "ram_ratio", "disk_ratio"]
MODE = 'SUPERVISED'
PIPELINE_FILE = os.path.join(from_root(), "models", "supervised_pipeline_simple.joblib")

print(f"Monitoring Mode: {MODE}")


# =========================
# ENSURE OUTPUT DIRECTORIES AND LOG FILE
# =========================
os.makedirs(TEST_RESULTS_DIR, exist_ok=True)

if not os.path.exists(ANOMALY_LOG):
    with open(ANOMALY_LOG, "w", encoding='utf-8') as f:
        f.write(f"Anomaly Log Created at {datetime.utcnow().isoformat()} UTC\n")
print(f"Output directory and anomaly log ready: {ANOMALY_LOG}")


# =========================
# LOAD PIPELINE
# =========================
if not os.path.exists(PIPELINE_FILE):
    raise FileNotFoundError(f"Pipeline file not found: {PIPELINE_FILE}")

pipeline = joblib.load(PIPELINE_FILE)
preprocessor = pipeline.named_steps['preprocess']
model = pipeline.named_steps['clf']


# =========================
# FUNCTION DEFINITIONS
# =========================
def log_anomaly(dt: str, cpu: float, ram: float, disk: float, predicted_stress: int, log_file: str = ANOMALY_LOG):
    """
    Append an anomaly record to the anomaly log file.
    
    Args:
        dt (str): Timestamp in ISO format when the anomaly was detected.
        cpu (float): CPU usage ratio (0.0 - 1.0).
        ram (float): RAM usage ratio (0.0 - 1.0).
        disk (float): Disk usage ratio (0.0 - 1.0).
        predicted_stress (int): Predicted label from the model (1 = anomaly).
        log_file (str, optional): Path to the anomaly log file. Defaults to ANOMALY_LOG.
    """
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(
            f"[{dt}] ⚠️ Anomaly Detected | CPU: {cpu:.4f}, RAM: {ram:.4f}, Disk: {disk:.4f}, Prediction: {predicted_stress}\n"
        )


def beep():
    """
    Produce an audible beep to alert the user of an anomaly.
    
    Uses `winsound` on Windows; falls back to terminal bell on other platforms.
    """
    try:
        import winsound
        winsound.Beep(1000, 500)  # frequency=1000Hz, duration=500ms
    except ImportError:
        print("\a")  # fallback terminal bell


def monitor_system():
    """
    Start a real-time system monitoring loop.
    
    Continuously reads CPU, RAM, and Disk usage every `LOG_INTERVAL_SEC` seconds,
    preprocesses the features, predicts stress using the loaded pipeline, and
    logs any detected anomalies. Alerts the user with a beep when anomalies are detected.
    
    Press Ctrl+C to stop monitoring.
    """
    print("Starting real-time monitoring. Press Ctrl+C to stop.")
    try:
        while True:
            dt = datetime.utcnow().isoformat()

            # Read system metrics
            cpu = psutil.cpu_percent(interval=None) / 100.0
            ram = psutil.virtual_memory().used / psutil.virtual_memory().total
            disk_ratio = psutil.disk_usage("/").used / psutil.disk_usage("/").total

            # Pipeline preprocessing
            X_raw = pd.DataFrame([[cpu, ram, disk_ratio]], columns=FEATURES)
            X_processed = preprocessor.transform(X_raw)

            # Model prediction
            predicted_stress = int(model.predict(X_processed)[0])

            # Only log anomalies
            if predicted_stress == 1:
                log_anomaly(dt, cpu, ram, disk_ratio, predicted_stress)
                print(f"[{dt}] ⚠️ Stress Detected by Pipeline!")
                beep()

            time.sleep(LOG_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    monitor_system()
