"""Physical-tamper prediction using the EXISTING trained Decision Tree.

Loads ml/models/physical_tamper_model.joblib and
ml/models/physical_tamper_model_metadata.json exactly as already committed
- no retraining, no formula changes, no edits to either file. The 8
features are always passed to the model in metadata["feature_order"]
(the exact order the model was trained on).

Per Task 2 decision #9: if any of the 8 features is missing or non-finite
(NaN/inf) - which happens for delta_accel/delta_gyro/rolling_std on the
first live sample of a sensorId's session - no prediction is made and
nothing is fabricated. The caller gets a `ready=False` result and should
wait for the next sample.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Optional

import joblib
import pandas as pd

THIS_DIR = Path(__file__).resolve().parent
ML_DIR = THIS_DIR.parent

DEFAULT_MODEL_PATH = ML_DIR / "models" / "physical_tamper_model.joblib"
DEFAULT_METADATA_PATH = ML_DIR / "models" / "physical_tamper_model_metadata.json"


class PhysicalPredictionResult:
    """Outcome of one attempted physical-tamper prediction for a sensorId."""

    __slots__ = ("sensor_id", "ready", "reason", "label", "probabilities", "features")

    def __init__(
        self,
        sensor_id: str,
        ready: bool,
        reason: Optional[str] = None,
        label: Optional[str] = None,
        probabilities: Optional[Dict[str, float]] = None,
        features: Optional[dict] = None,
    ):
        self.sensor_id = sensor_id
        self.ready = ready
        self.reason = reason
        self.label = label
        self.probabilities = probabilities
        self.features = features

    def __repr__(self) -> str:
        if self.ready:
            return (
                f"PhysicalPredictionResult(sensor_id={self.sensor_id!r}, "
                f"ready=True, label={self.label!r})"
            )
        return (
            f"PhysicalPredictionResult(sensor_id={self.sensor_id!r}, "
            f"ready=False, reason={self.reason!r})"
        )


class PhysicalTamperPredictor:
    """Thin wrapper around the existing joblib DecisionTreeClassifier."""

    def __init__(
        self,
        model_path: Path = DEFAULT_MODEL_PATH,
        metadata_path: Path = DEFAULT_METADATA_PATH,
    ):
        with open(metadata_path) as f:
            self.metadata = json.load(f)

        # Source of truth for feature order - read from the existing
        # metadata file, never hardcoded/re-derived here.
        self.feature_order = list(self.metadata["feature_order"])
        self.label_order = self.metadata.get("label_order")

        self.model = joblib.load(model_path)

    def predict(self, sensor_id: str, features: dict) -> PhysicalPredictionResult:
        """features: the 8-feature dict returned by
        PhysicalSessionManager.update() (i.e. LiveMotionFeatureExtractor
        .update()'s output) for this sensor_id.
        """
        missing = [name for name in self.feature_order if name not in features]
        if missing:
            return PhysicalPredictionResult(
                sensor_id=sensor_id,
                ready=False,
                reason=f"missing feature(s): {missing}",
                features=features,
            )

        non_finite = [
            name
            for name in self.feature_order
            if not math.isfinite(features[name])
        ]
        if non_finite:
            return PhysicalPredictionResult(
                sensor_id=sensor_id,
                ready=False,
                reason=(
                    "not enough samples yet for this sensor - "
                    f"non-finite feature(s): {non_finite}"
                ),
                features=features,
            )

        ordered_row = {name: features[name] for name in self.feature_order}
        X = pd.DataFrame([ordered_row], columns=self.feature_order)

        label = self.model.predict(X)[0]

        probabilities = None
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X)[0]
            probabilities = {
                str(cls): float(p) for cls, p in zip(self.model.classes_, proba)
            }

        return PhysicalPredictionResult(
            sensor_id=sensor_id,
            ready=True,
            label=str(label),
            probabilities=probabilities,
            features=ordered_row,
        )
