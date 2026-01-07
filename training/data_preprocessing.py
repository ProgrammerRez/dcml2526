from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
import pandas as pd
from typing import Tuple

# =========================
# CONFIGURATION
# =========================
FEATURES = ["cpu_ratio", "ram_ratio", "disk_ratio"]


# =========================
# FUNCTION DEFINITIONS
# =========================
def preprocess_data(df: pd.DataFrame) -> Tuple[Pipeline, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Prepare a machine learning pipeline for anomaly detection.
    
    Steps included:
        - Split dataset into train and test sets (stratified by 'pred_label').
        - Standardize numeric features using StandardScaler.
        - Apply SMOTE to oversample minority class in training set.
        - Build a pipeline combining preprocessing, SMOTE, and classifier.

    Args:
        df (pd.DataFrame): Dataset containing features and 'pred_label'.

    Returns:
        Tuple containing:
            - pipeline (Pipeline): Imbalanced-learn pipeline with preprocessing and LogisticRegression.
            - X_train (pd.DataFrame): Training features.
            - y_train (pd.Series): Training labels.
            - X_test (pd.DataFrame): Test features.
            - y_test (pd.Series): Test labels.
    """
    # Split features and target
    X = df[FEATURES]
    y = df['pred_label']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # Preprocessing: scale numeric features
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), FEATURES)
        ]
    )

    # Pipeline: preprocessing + SMOTE + Logistic Regression classifier
    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("smote", SMOTE(random_state=42)),
        ("clf", LogisticRegression())
    ])

    return pipeline, X_train, y_train, X_test, y_test


# =========================
# MAIN (OPTIONAL TEST)
# =========================
if __name__ == "__main__":
    # Example usage
    from data_ingestion import load_data  # assuming you saved the previous .env loader as load_data_env.py
    df = load_data()
    pipeline, X_train, y_train, X_test, y_test = preprocess_data(df)
    print("Pipeline and train-test split ready.")
