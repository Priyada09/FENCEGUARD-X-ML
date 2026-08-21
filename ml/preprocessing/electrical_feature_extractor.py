"""Reusable feature-extraction interface for the EXISTING electrical fault baseline.

Scope (E3 only): this module does ONE thing — take the six raw electrical
values the model already expects, validate them, and return them as an
ordered vector suitable for ``electrical_fault_model.joblib.predict(...)``.

It intentionally does NOT:
- introduce new/derived features
- apply scaling, normalization, or any other preprocessing
- connect to MQTT
- expose a /predict endpoint
- touch the physical-tamper pipeline, backend, frontend, or firmware

Source of truth for the feature list and order (verified in E1 against
``ml/notebooks/01_electrical_fault_baseline.ipynb`` and
``ml/training/train_electrical_fault_model.py``):

    FEATURE_COLUMNS = [
        "zone1_voltage_v",
        "zone2_voltage_v",
        "zone3_voltage_v",
        "bus_voltage_v",
        "current_ma",
        "power_mw",
    ]

The existing baseline performs no feature engineering or scaling, so this
module is a validating pass-through only.
"""

from __future__ import annotations

import numbers
from dataclasses import dataclass
from typing import Iterable, List, Mapping, Sequence


# ---------------------------------------------------------------------------
# Exact feature contract of ml/models/electrical_fault_model.joblib
# (must stay identical to FEATURE_COLUMNS in
#  ml/training/train_electrical_fault_model.py — do not reorder/rename)
# ---------------------------------------------------------------------------
ELECTRICAL_FEATURE_ORDER: List[str] = [
    "zone1_voltage_v",
    "zone2_voltage_v",
    "zone3_voltage_v",
    "bus_voltage_v",
    "current_ma",
    "power_mw",
]


class ElectricalFeatureValidationError(ValueError):
    """Raised when raw electrical input fields are missing or non-numeric."""


@dataclass(frozen=True)
class ElectricalFeatureVector:
    """An ordered, validated electrical feature vector.

    ``values`` is guaranteed to:
    - contain exactly the 6 features in ELECTRICAL_FEATURE_ORDER
    - be in that exact order
    - contain only numeric (int/float) values

    No scaling or transformation has been applied to these values — they are
    the raw values as provided, matching the existing notebook baseline.
    """

    values: List[float]

    def as_list(self) -> List[float]:
        """Return the plain ordered list, e.g. for model.predict([vector])."""
        return list(self.values)

    def as_dict(self) -> dict:
        """Return the ordered values keyed by feature name (for logging/debugging)."""
        return dict(zip(ELECTRICAL_FEATURE_ORDER, self.values))


def extract_electrical_features(
    raw_fields: Mapping[str, object],
) -> ElectricalFeatureVector:
    """Validate and order raw electrical fields into the model's expected input.

    Parameters
    ----------
    raw_fields:
        A mapping (e.g. dict) containing at least the six required keys in
        ELECTRICAL_FEATURE_ORDER. Extra keys are ignored. No transformation
        is applied to the values found — this function performs validation
        and ordering only, matching the "no feature engineering / no
        scaling" behavior confirmed in the existing notebook (E1).

    Returns
    -------
    ElectricalFeatureVector
        The six required values, validated and in the exact order the saved
        model (``electrical_fault_model.joblib``) expects.

    Raises
    ------
    ElectricalFeatureValidationError
        If any required field is missing, ``None``, or not numeric (bool is
        rejected too, since it is not a genuine sensor reading even though
        Python treats bool as a subclass of int).
    """
    if raw_fields is None:
        raise ElectricalFeatureValidationError("raw_fields must not be None")

    missing_fields: List[str] = []
    non_numeric_fields: List[str] = []
    ordered_values: List[float] = []

    for feature_name in ELECTRICAL_FEATURE_ORDER:
        if feature_name not in raw_fields or raw_fields[feature_name] is None:
            missing_fields.append(feature_name)
            continue

        value = raw_fields[feature_name]

        # Reject bool explicitly: isinstance(True, int) is True in Python,
        # but a boolean is not a valid sensor reading.
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            non_numeric_fields.append(feature_name)
            continue

        ordered_values.append(float(value))

    if missing_fields or non_numeric_fields:
        error_parts = []
        if missing_fields:
            error_parts.append(f"missing required field(s): {missing_fields}")
        if non_numeric_fields:
            error_parts.append(f"non-numeric value(s) for field(s): {non_numeric_fields}")
        raise ElectricalFeatureValidationError(
            "Invalid electrical input — " + "; ".join(error_parts)
        )

    return ElectricalFeatureVector(values=ordered_values)


def extract_electrical_features_batch(
    raw_fields_list: Iterable[Mapping[str, object]],
) -> List[ElectricalFeatureVector]:
    """Convenience wrapper: validate/order a batch of raw field mappings.

    Each item is validated independently via extract_electrical_features().
    A ValueError from any single row propagates immediately (fail-fast);
    this module does not silently drop invalid rows.
    """
    return [extract_electrical_features(row) for row in raw_fields_list]


def feature_order() -> Sequence[str]:
    """Return the exact feature order expected by the saved electrical model."""
    return tuple(ELECTRICAL_FEATURE_ORDER)