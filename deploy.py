import os
import time
from datetime import datetime
import pandas as pd
import psutil
import joblib

# =========================
# CONFIG
# =========================
CSV_FILE = "D:/Client_Projects/dcml2526/notebooks/Data/system_metrics_binary.csv"    # raw metrics + threshold label
PIPELINE_LOG = "D:/Client_Projects/dcml2526/test_results/pipeline_predictions.csv" # pipeline prediction log
LOG_INTERVAL_SEC = 1

# CPU_STRESS = 0.516
# RAM_STRESS = 0.76
# DISK_STRESS = 0.60

FEATURES = ["cpu_ratio", "ram_ratio", "disk_ratio"]
mode = 'SUPERVISED'
PIPELINE_FILE = "D:/Client_Projects/dcml2526/models/supervised_pipeline_simple.joblib" 

print(mode)

# =========================
# LOAD PIPELINE
# =========================
if not os.path.exists(PIPELINE_FILE):
    raise FileNotFoundError(f"Pipeline file not found: {PIPELINE_FILE}")
pipeline = joblib.load(PIPELINE_FILE)

# Extract preprocessing and model from pipeline
preprocessor = pipeline.named_steps['preprocess']
model = pipeline.named_steps['clf']

# =========================
# INIT PIPELINE LOG
# =========================
if not os.path.exists(PIPELINE_LOG):
    pd.DataFrame(columns=[
        "timestamp_ms",
        "datetime_utc",
        "cpu_ratio",
        "ram_ratio",
        "disk_ratio",
        "predicted_stress"
    ]).to_csv(PIPELINE_LOG, index=False)

# =========================
# DECIDE LABEL
# # =========================
# def decide_label(cpu, ram, disk):
#     return int(cpu > CPU_STRESS or ram > RAM_STRESS or disk > DISK_STRESS)

# =========================
# BEEP FUNCTION
# =========================
def beep():
    try:
        import winsound
        winsound.Beep(1000, 500)  # 1000Hz, 500ms
    except ImportError:
        print("\a")  # fallback for Linux/macOS

# =========================
# REAL-TIME MONITORING LOOP
# =========================
def monitor_system():
    print("Starting real-time monitoring. Press Ctrl+C to stop.")
    try:
        while True:
            ts = int(time.time() * 1000)
            dt = datetime.utcnow().isoformat()

            # -------------------
            # Read system metrics
            # -------------------
            cpu = psutil.cpu_percent(interval=None) / 100.0
            ram = psutil.virtual_memory().used / psutil.virtual_memory().total
            disk_ratio = psutil.disk_usage("/").used / psutil.disk_usage("/").total

            # -------------------
            # Threshold-based label
            # -------------------
            # label = decide_label(cpu, ram, disk_ratio)

            # log raw metrics
            row = pd.DataFrame([{
                "timestamp_ms": ts,
                "datetime_utc": dt,
                "cpu_ratio": round(cpu, 4),
                "ram_ratio": round(ram, 4),
                "disk_ratio": round(disk_ratio, 4),
                # "label": label
            }])
            row.to_csv(CSV_FILE, mode="a", index=False, header=False)

            # -------------------
            # Pipeline preprocessing
            # -------------------
            X_raw = pd.DataFrame([[cpu, ram, disk_ratio]], columns=FEATURES)
            X_processed = preprocessor.transform(X_raw)

            # -------------------
            # Model prediction
            # -------------------
            predicted_stress = int(model.predict(X_processed)[0])

            # beep if stressed
            if predicted_stress == 1:
                print(f"[{dt}] ⚠️ Stress Detected by Pipeline!")
                beep()

            # log pipeline prediction
            pipe_row = pd.DataFrame([{
                "timestamp_ms": ts,
                "datetime_utc": dt,
                "cpu_ratio": round(cpu, 4),
                "ram_ratio": round(ram, 4),
                "disk_ratio": round(disk_ratio, 4),
                "predicted_stress": predicted_stress
            }])
            pipe_row.to_csv(PIPELINE_LOG, mode="a", index=False, header=False)

            time.sleep(LOG_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    monitor_system()
