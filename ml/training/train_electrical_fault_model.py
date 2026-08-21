"""Persist the EXISTING electrical fault DecisionTree baseline as a reusable artifact.

This script does NOT define a new model. It reproduces, exactly, the baseline
already implemented and validated in:
    ml/notebooks/01_electrical_fault_baseline.ipynb

Specifically it reproduces:
- DecisionTreeClassifier(max_depth=4, random_state=42)
- Trained only on the 20 MEASURED rows of ml/dataset/raw/sih_fence_raw_dataset.csv
- Features (exact order): zone1_voltage_v, zone2_voltage_v, zone3_voltage_v,
  bus_voltage_v, current_ma, power_mw
- Target: condition (used as-is, no relabeling/merging)
- The 6 IMPUTED_BUS_VOLTAGE rows are excluded from training, exactly as in
  the notebook.

No train/test split, no cross-validation, and no performance metrics are
introduced here — none exist in the source notebook, so none are computed
here either. This script's only job is to make the already-existing baseline
loadable outside of the notebook.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import sklearn


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
ML_DIR = THIS_FILE.parents[1]  # ml/

DATA_PATH = ML_DIR / "dataset" / "raw" / "sih_fence_raw_dataset.csv"
MODEL_OUT_PATH = ML_DIR / "models" / "electrical_fault_model.joblib"
METADATA_OUT_PATH = ML_DIR / "models" / "electrical_fault_model_metadata.json"

# ---------------------------------------------------------------------------
# Exact spec from the existing notebook (01_electrical_fault_baseline.ipynb)
# ---------------------------------------------------------------------------
FEATURE_COLUMNS = [
    "zone1_voltage_v",
    "zone2_voltage_v",
    "zone3_voltage_v",
    "bus_voltage_v",
    "current_ma",
    "power_mw",
]
TARGET_COLUMN = "condition"
MAX_DEPTH = 4
RANDOM_STATE = 42


def load_measured_rows(data_path: Path) -> pd.DataFrame:
    """Load the raw dataset and return only the MEASURED rows.

    The 6 IMPUTED_BUS_VOLTAGE rows are excluded, exactly as in the existing
    notebook (Cell 5 / Cell 12: df_measured = df_raw[df_raw["data_quality"]
    == "MEASURED"]).
    """
    df_raw = pd.read_csv(data_path)
    df_measured = df_raw[df_raw["data_quality"] == "MEASURED"].copy()
    return df_measured


def train_electrical_baseline(df_measured: pd.DataFrame) -> DecisionTreeClassifier:
    """Train the existing baseline DecisionTreeClassifier, unchanged.

    Identical to train_baseline_tree() in the source notebook.
    """
    X_train = df_measured[FEATURE_COLUMNS]
    y_train = df_measured[TARGET_COLUMN]

    model = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


def build_metadata(df_measured: pd.DataFrame, model: DecisionTreeClassifier) -> dict:
    class_distribution = (
        df_measured[TARGET_COLUMN].value_counts().to_dict()
    )
    # Ensure plain python ints for JSON serialization
    class_distribution = {str(k): int(v) for k, v in class_distribution.items()}

    metadata = {
        "model_type": "DecisionTreeClassifier",
        "sklearn_version": sklearn.__version__,
        "hyperparameters": {
            "max_depth": MAX_DEPTH,
            "random_state": RANDOM_STATE,
        },
        "feature_columns_exact_order": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "model_classes": list(model.classes_),
        "training_row_count": int(len(df_measured)),
        "training_class_distribution_measured_only": class_distribution,
        "source_dataset": "ml/dataset/raw/sih_fence_raw_dataset.csv",
        "rows_excluded": "6 IMPUTED_BUS_VOLTAGE rows excluded from training (bus_voltage_v reconstructed, not measured)",
        "train_test_split": False,
        "cross_validation": False,
        "performance_metrics": "NOT COMPUTED - none exist in the source notebook (01_electrical_fault_baseline.ipynb); "
                                 "dataset is too small/imbalanced for meaningful metrics",
        "validation_status": "NOT INDEPENDENTLY VALIDATED. This is a proof-of-concept baseline "
                              "persisted exactly as implemented in the existing notebook. "
                              "No accuracy, precision, recall, F1, or confusion matrix has been "
                              "computed for this model, in this script or the source notebook.",
    }
    return metadata


def main() -> None:
    df_measured = load_measured_rows(DATA_PATH)

    print(f"Loaded {len(df_measured)} MEASURED rows from {DATA_PATH}")
    print("Training class distribution (MEASURED only):")
    print(df_measured[TARGET_COLUMN].value_counts())

    model = train_electrical_baseline(df_measured)
    print(f"\nTrained DecisionTreeClassifier(max_depth={MAX_DEPTH}, random_state={RANDOM_STATE})")
    print(f"model.classes_ = {list(model.classes_)}")

    MODEL_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT_PATH)
    print(f"\nSaved model artifact -> {MODEL_OUT_PATH}")

    metadata = build_metadata(df_measured, model)
    with open(METADATA_OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata -> {METADATA_OUT_PATH}")


if __name__ == "__main__":
    main()