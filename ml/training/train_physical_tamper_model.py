"""
train_physical_tamper_model.py

Persists the EXISTING physical-tamper Decision Tree that was already trained
in ml/notebooks/02_physical_motion_eda_and_baseline.ipynb.

This script does NOT introduce any new modeling decisions. It reproduces,
exactly, the training logic already present in the notebook (see the cell
that defines MOTION_FEATURES / TARGET_COLUMN and the cell that fits
`tree_model = DecisionTreeClassifier(max_depth=4, random_state=42)`), and
saves the resulting model + metadata as reusable artifacts.

Source of truth:
    - Model-ready dataset: ml/dataset/processed/physical_tamper_model_ready.csv
      (already produced by the notebook's binary target preparation /
      model-ready dataset preparation steps; 39 rows, 8 features,
      target = physical_target with classes NORMAL / PHYSICAL_TAMPER)

Explicitly NOT done here (by design, matching the notebook prototype):
    - No train/test split
    - No cross-validation
    - No hyperparameter tuning
    - No oversampling / undersampling
    - No change to the 8 features, their formulas, or the target definition

The resulting training accuracy is a TRAINING-set fit metric only, not a
validated generalization result (all 7 PHYSICAL_TAMPER rows come from a
single session, as noted in the notebook).
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# ---------------------------------------------------------------------------
# Paths (relative to this file, so the script works regardless of cwd)
# ---------------------------------------------------------------------------
THIS_DIR = Path(__file__).resolve().parent
ML_DIR = THIS_DIR.parent

MODEL_READY_CSV = ML_DIR / "dataset" / "processed" / "physical_tamper_model_ready.csv"
MODEL_OUTPUT_DIR = ML_DIR / "models"
MODEL_OUTPUT_PATH = MODEL_OUTPUT_DIR / "physical_tamper_model.joblib"
METADATA_OUTPUT_PATH = MODEL_OUTPUT_DIR / "physical_tamper_model_metadata.json"

# ---------------------------------------------------------------------------
# EXACT same feature order / target / labels as the notebook
# (ml/notebooks/02_physical_motion_eda_and_baseline.ipynb, cell defining
# MOTION_FEATURES / TARGET_COLUMN / LABEL_ORDER)
# ---------------------------------------------------------------------------
MOTION_FEATURES = [
    "accel_mag",
    "gyro_mag",
    "delta_accel",
    "delta_gyro",
    "rolling_mean",
    "rolling_std",
    "peak_accel",
    "peak_gyro",
]
TARGET_COLUMN = "physical_target"
LABEL_ORDER = ["NORMAL", "PHYSICAL_TAMPER"]


def load_model_ready_dataset() -> pd.DataFrame:
    """Load the existing model-ready dataset (already produced by the
    notebook's session-aware feature extraction -> physical-tamper EDA ->
    binary target preparation -> model-ready dataset preparation steps).
    This script does not recompute features; it reuses the existing,
    already-processed CSV as the source of truth.
    """
    if not MODEL_READY_CSV.exists():
        raise FileNotFoundError(
            f"Expected model-ready dataset at {MODEL_READY_CSV}, but it was not found."
        )

    df = pd.read_csv(MODEL_READY_CSV)

    if list(df.columns[2:]) != MOTION_FEATURES:
        # The CSV column order should already match MOTION_FEATURES; this is
        # just a safety check, not a transformation.
        raise ValueError(
            "Model-ready dataset columns do not match the expected 8 features "
            f"in the expected order. Found: {list(df.columns[2:])}"
        )

    return df


def train_model(df: pd.DataFrame) -> DecisionTreeClassifier:
    """Reproduce the EXACT training already performed in the notebook."""
    X = df[MOTION_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()

    tree_model = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree_model.fit(X, y)

    train_accuracy = accuracy_score(y, tree_model.predict(X))
    print(f"Decision Tree fit on {len(df)} model-ready rows (prototype demonstration).")
    print(f"Training accuracy: {train_accuracy:.4f} (NOT a validated generalization result)")

    return tree_model


def save_artifacts(model: DecisionTreeClassifier, n_rows: int) -> None:
    MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"Saved model to: {MODEL_OUTPUT_PATH}")

    metadata = {
        "model_type": type(model).__name__,
        "max_depth": model.max_depth,
        "random_state": model.random_state,
        "feature_order": MOTION_FEATURES,
        "target_column": TARGET_COLUMN,
        "label_order": LABEL_ORDER,
        "training_rows": n_rows,
        "source_dataset": str(MODEL_READY_CSV.relative_to(ML_DIR.parent)),
        "notes": (
            "Training-set fit metric only, not a validated generalization result. "
            "All 7 PHYSICAL_TAMPER rows come from a single session."
        ),
    }
    with open(METADATA_OUTPUT_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata to: {METADATA_OUTPUT_PATH}")


def main():
    df = load_model_ready_dataset()
    model = train_model(df)
    save_artifacts(model, n_rows=len(df))


if __name__ == "__main__":
    main()