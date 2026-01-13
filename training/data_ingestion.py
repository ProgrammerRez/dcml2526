import pandas as pd
from from_root import from_root
from dotenv import load_dotenv
import os

# =========================
# LOAD ENV VARIABLES
# =========================
env_path = os.path.join(from_root(), '.env')
load_dotenv(env_path)

PATH = os.path.join(from_root(), 'notebooks', 'Data', 'system_metrics_binary.csv')

# Load thresholds from .env and convert to float
try:
    CPU_QUANTILE = float(os.getenv('CPU_QUANTILE'))
    RAM_QUANTILE = float(os.getenv('RAM_QUANTILE'))
    DISK_QUANTILE = float(os.getenv('DISK_QUANTILE'))
    ERROR = float(os.getenv('ERROR', 0.1))  # default error if not set
except TypeError:
    raise ValueError("One or more .env variables are missing or invalid. "
                    "Ensure CPU_QUANTILE, RAM_QUANTILE, DISK_QUANTILE, and ERROR are set.")


# =========================
# FUNCTION DEFINITIONS
# =========================
def load_data() -> pd.DataFrame:
    """
    Load system metrics dataset, compute dynamic thresholds from quantiles,
    and apply a rule-based anomaly detection.

    Returns:
        pd.DataFrame: Original dataset with an added 'pred_label' column,
                    where 1 = anomaly, 0 = normal.

    Behavior:
        - Thresholds are computed from quantiles specified in .env.
        - RAM and Disk thresholds are increased by ERROR to reduce false positives.
        - Records are flagged as anomalies if any metric exceeds its threshold.
        - Prints label counts, percentages, and computed thresholds.
    """
    # Load dataset
    df = pd.read_csv(PATH)

    # Compute thresholds
    thresholds = {
        "cpu": df["cpu_ratio"].quantile(CPU_QUANTILE),
        "ram": df["ram_ratio"].quantile(RAM_QUANTILE) + ERROR,
        "disk": df["disk_ratio"].quantile(DISK_QUANTILE) + ERROR
    }

    # Apply rule-based anomaly detection
    df["pred_label"] = (
        (df["cpu_ratio"] > thresholds["cpu"]) |
        (df["ram_ratio"] > thresholds["ram"]) |
        (df["disk_ratio"] > thresholds["disk"])
    ).astype(int)

    # Print statistics
    print("Label counts:")
    print(df["pred_label"].value_counts())

    print("\nLabel percentages:")
    print(df["pred_label"].value_counts(normalize=True) * 100)

    print("\nComputed thresholds:")
    for k, v in thresholds.items():
        print(f"{k}: {v:.4f}")

    return df


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    df = load_data()
    print("\nData loaded and thresholds applied successfully.")
