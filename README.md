# 🛡️ DCML Custom Anomaly Detector

A high-performance, standalone system monitor and anomaly detector designed for workstations. This project uses machine learning (Random Forest) to identify unusual system behavior in real-time.

---

## �️ Environment Setup

It is recommended to use a Python virtual environment to keep dependencies isolated:

1. **Create the Environment**:
   ```powershell
   python -m venv venv
   ```
2. **Activate the Environment**:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

## �🚀 Getting Started (New Device Workflow)

When deploying this project to a new system, you must "train" the detector to understand that specific device's baseline behavior. Follow these steps:

1. **Collect Baseline Data**: 
   Run the logger in the background while performing "normal" activities.
   ```powershell
   python metric_logger.py
   ```
2. **Inject Anomalies (Optional but Recommended)**: 
   While the logger is running, use the stress test tool to generate "known" anomaly peaks.
   ```powershell
   python run_tests.py
   ```
3. **Train the Model**: 
   Once you have enough data in `system_metrics_binary.csv`, generate a new calibrated model.
   ```powershell
   python retrain.py
   ```
4. **Start Monitoring**: 
   Run the main detector to protect your system.
   ```powershell
   python main.py
   ```

---

## 📂 Project Components

| Script | Description |
| :--- | :--- |
| `main.py` | **The Core**. Runs the real-time monitoring loop, applies the ML model to current metrics, and triggers a beep alert/log when stress is detected. |
| `retrain.py` | **The Brain**. Loads the collected CSV data, applies threshold-based labeling, performs hyperparameter tuning, and saves a new `supervised_pipeline_simple.joblib` model. |
| `run_tests.py` | **The Injector**. A CLI menu tool to run controlled stress tests on CPU (max threads), RAM (allocations), or Disk (heavy I/O writing). |
| `metric_logger.py`| **The Collector**. Silently records CPU, RAM, and Disk usage at 1-second intervals and saves them to the dataset. |

---

## ⚙️ Configuration (`.env`)

You can fine-tune the labeling logic by editing the `.env` file. These values determine the "cutoff" for what is considered an anomaly during the retraining process:

- `CPU_QUANTILE`: The percentile threshold for CPU alerts (e.g., 0.95 = top 5% of usage).
- `RAM_QUANTILE`: The percentile threshold for Memory.
- `DISK_QUANTILE`: The percentile threshold for Disk I/O.
- `ERROR`: A safety margin added to thresholds to prevent false positives from minor spikes.

---

## 🛠️ Requirements

The project depends on the following libraries:
- `psutil`: System monitoring.
- `scikit-learn`: Machine learning algorithms.
- `pandas`: Data manipulation.
- `joblib`: Model persistence.
- `imbalanced-learn`: Handling class imbalance with SMOTE.
- `python-dotenv`: Environment variable management.
- `from-root`: Relative path management.
- `pypdf`: PDF text extraction (for reports).
