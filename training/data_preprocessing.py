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


def preprocess_data(
    df: pd.DataFrame
) -> Tuple[Pipeline, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Prepare a supervised learning pipeline and split data into train/test sets.

    This function:
    - Extracts predefined system ratio features
    - Performs a stratified train/test split on the target label
    - Scales numeric features using StandardScaler
    - Applies SMOTE with a safe, data-dependent neighbor configuration
    - Constructs an imbalanced-learn Pipeline with Logistic Regression

    Args:
        df (pd.DataFrame): Input dataset containing feature columns and
            a binary target column named `pred_label`.

    Returns:
        Tuple containing:
            pipeline (Pipeline): Preprocessing + SMOTE + classifier pipeline.
            X_train (pd.DataFrame): Training feature matrix.
            y_train (pd.Series): Training labels.
            X_test (pd.DataFrame): Test feature matrix.
            y_test (pd.Series): Test labels.
    """

    X = df[FEATURES]
    y = df["pred_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), FEATURES)
        ]
    )

    minority_count = y_train.value_counts().min()
    k_neighbors = max(1, min(2, minority_count - 1))

    smote = SMOTE(
        k_neighbors=k_neighbors,
        random_state=42
    )

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("smote", smote),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    return pipeline, X_train, y_train, X_test, y_test


def main():
    """
    Execute a local preprocessing sanity check.

    Loads raw data, constructs the preprocessing pipeline,
    performs a train/test split, and prints the training
    class distribution to verify imbalance handling.

    Intended for development-time validation only.
    """
    from data_ingestion import load_data

    df = load_data()
    pipeline, X_train, y_train, X_test, y_test = preprocess_data(df)

    print("Pipeline ready")
    print("Training class distribution:")
    print(y_train.value_counts())


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
