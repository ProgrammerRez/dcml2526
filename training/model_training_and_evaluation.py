from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from from_root import from_root
import joblib
import os
import pandas as pd
from typing import Tuple, Dict, Any
from imblearn.pipeline import Pipeline

# =========================
# PATHS
# =========================
MODEL_PATH = os.path.join(from_root(), 'models', 'supervised_pipeline_simple.joblib')
PARAMS_PATH = os.path.join(from_root(), 'models', 'supervised_best_params_simple.joblib')


# =========================
# FUNCTION DEFINITIONS
# =========================
def model_training_and_eval(
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Tuple[Pipeline, Dict[str, Any]]:
    """
    Perform multi-model grid search, train the best model, and evaluate it on the test set.

    Steps:
        - Defines parameter grids for Logistic Regression, Random Forest, and Gradient Boosting.
        - Performs 5-fold GridSearchCV using F1-score.
        - Prints best model and parameters.
        - Evaluates on the test set with confusion matrix and classification report.

    Args:
        pipeline (Pipeline): Preprocessing + classifier pipeline.
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training labels.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): Test labels.

    Returns:
        Tuple[Pipeline, Dict[str, Any]]:
            - best_model: Trained pipeline with best hyperparameters.
            - best_params: Dictionary of best parameters from grid search.
    """
    # =========================
    # PARAMETER GRID (MULTI-MODEL)
    # =========================
    param_grid = [
        # ---- Logistic Regression ----
        {
            "clf": [LogisticRegression(max_iter=1000, solver="liblinear")],
            "clf__C": [0.1, 1.0, 10.0],
        },
        # ---- Random Forest ----
        {
            "clf": [RandomForestClassifier(random_state=42, n_jobs=-1)],
            "clf__n_estimators": [100, 200],
            "clf__max_depth": [None, 10, 20],
            "clf__min_samples_split": [2, 5],
        },
        # ---- Gradient Boosting ----
        {
            "clf": [GradientBoostingClassifier(random_state=42)],
            "clf__n_estimators": [100, 200],
            "clf__learning_rate": [0.05, 0.1],
            "clf__max_depth": [3, 5],
        }
    ]

    # =========================
    # GRID SEARCH CV
    # =========================
    grid = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="f1",
        cv=5,
        n_jobs=-1,
        verbose=2
    )

    # =========================
    # TRAIN (CV RUNS HERE)
    # =========================
    grid.fit(X_train, y_train)

    # =========================
    # BEST MODEL
    # =========================
    best_model = grid.best_estimator_
    best_params = grid.best_params_

    print("\nBest model:")
    print(best_model.named_steps["clf"])
    print("\nBest parameters:")
    print(best_params)

    # =========================
    # FINAL EVALUATION
    # =========================
    y_pred = best_model.predict(X_test)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return best_model, best_params


def save_model_and_params(best_model: Pipeline, best_params: Dict[str, Any]):
    """
    Save the trained pipeline and best hyperparameters to disk.

    Args:
        best_model (Pipeline): Trained ML pipeline.
        best_params (dict): Best parameters from grid search.
    """
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(best_params, PARAMS_PATH)
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Best parameters saved to: {PARAMS_PATH}")


# =========================
# MAIN (OPTIONAL TEST)
# =========================
if __name__ == "__main__":
    from data_preprocessing import preprocess_data  # your preprocessing script
    from data_ingestion import load_data  # your .env loader script

    # Load data and preprocess
    df = load_data()
    pipeline, X_train, y_train, X_test, y_test = preprocess_data(df)

    # Train and evaluate
    best_model, best_params = model_training_and_eval(pipeline, X_train, y_train, X_test, y_test)

    # Save results
    save_model_and_params(best_model, best_params)
