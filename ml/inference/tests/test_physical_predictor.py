import json
import math

from sklearn.tree import DecisionTreeClassifier

from ml.inference.physical_predictor import (
    DEFAULT_METADATA_PATH,
    PhysicalTamperPredictor,
)

FINITE_FEATURES = {
    "accel_mag": 0.99,
    "gyro_mag": 0.16,
    "delta_accel": 0.05,
    "delta_gyro": 0.02,
    "rolling_mean": 0.97,
    "rolling_std": 0.01,
    "peak_accel": 1.01,
    "peak_gyro": 0.18,
}

FIRST_SAMPLE_FEATURES = {
    **FINITE_FEATURES,
    "delta_accel": float("nan"),
    "delta_gyro": float("nan"),
    "rolling_std": float("nan"),
}


def test_loads_existing_joblib_model_unmodified():
    predictor = PhysicalTamperPredictor()
    assert isinstance(predictor.model, DecisionTreeClassifier)
    assert set(predictor.model.classes_) == {"NORMAL", "PHYSICAL_TAMPER"}


def test_feature_order_matches_committed_metadata_exactly():
    with open(DEFAULT_METADATA_PATH) as f:
        metadata = json.load(f)

    predictor = PhysicalTamperPredictor()
    assert predictor.feature_order == metadata["feature_order"]
    assert predictor.feature_order == [
        "accel_mag",
        "gyro_mag",
        "delta_accel",
        "delta_gyro",
        "rolling_mean",
        "rolling_std",
        "peak_accel",
        "peak_gyro",
    ]


def test_feature_order_matches_model_feature_names_in():
    predictor = PhysicalTamperPredictor()
    # sklearn records the column order/names the model was actually fit
    # on; this must match metadata["feature_order"] exactly, or the model
    # would silently receive columns in the wrong order.
    assert list(predictor.model.feature_names_in_) == predictor.feature_order


def test_first_sample_with_nan_features_returns_not_ready():
    predictor = PhysicalTamperPredictor()
    result = predictor.predict("ZONE_1", FIRST_SAMPLE_FEATURES)

    assert result.ready is False
    assert result.label is None
    assert "delta_accel" in result.reason
    assert "delta_gyro" in result.reason
    assert "rolling_std" in result.reason


def test_second_sample_with_finite_features_returns_prediction():
    predictor = PhysicalTamperPredictor()
    result = predictor.predict("ZONE_1", FINITE_FEATURES)

    assert result.ready is True
    assert result.label in {"NORMAL", "PHYSICAL_TAMPER"}
    assert result.probabilities is not None
    assert math.isclose(sum(result.probabilities.values()), 1.0, abs_tol=1e-6)


def test_missing_feature_key_returns_not_ready():
    predictor = PhysicalTamperPredictor()
    incomplete = {k: v for k, v in FINITE_FEATURES.items() if k != "peak_gyro"}
    result = predictor.predict("ZONE_1", incomplete)

    assert result.ready is False
    assert "peak_gyro" in result.reason


def test_ordered_features_sent_to_model_preserve_exact_order():
    predictor = PhysicalTamperPredictor()
    # Feed features in a deliberately shuffled dict order - Python dicts
    # preserve insertion order, so this checks the predictor re-orders by
    # feature_order rather than relying on caller-supplied ordering.
    shuffled = dict(reversed(list(FINITE_FEATURES.items())))
    result = predictor.predict("ZONE_1", shuffled)

    assert result.ready is True
    assert list(result.features.keys()) == predictor.feature_order
