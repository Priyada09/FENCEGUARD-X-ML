"""Adapter: raw MQTT payload (nested JSON) -> flat raw motion sample.

Maps only the 6 IMU fields the physical-tamper feature pipeline needs
(ml/preprocessing/feature_pipeline.py). Everything else on the payload
(temperature, current, voltage, power, busVoltage, eventType, ...) is
intentionally ignored here - none of it is a physical-tamper model input.

Per Task 2 decision #6: this adapter does NOT invent a timestamp. The
representative ESP32 MQTT payload does not contain a timestamp field, and
it has not been confirmed that the live ESP32-published payload ever
carries one (only a "backend sample event payload" was mentioned, which
may not be the same object). Session boundaries for physical inference
are keyed explicitly by sensorId (see session_manager.py) instead of by
timestamp, so no timestamp is required for correct behavior here.
"""

from __future__ import annotations

from typing import Any, Mapping

# metadata.<key> -> raw feature-pipeline field name (feature_pipeline.py's
# LiveMotionFeatureExtractor.update() reads sample["ax"], sample["ay"], etc.
# directly).
METADATA_TO_RAW = {
    "accelX": "ax",
    "accelY": "ay",
    "accelZ": "az",
    "gyroX": "gx",
    "gyroY": "gy",
    "gyroZ": "gz",
}


class PayloadAdapterError(ValueError):
    """Raised when an incoming MQTT payload cannot be mapped to a raw
    physical-tamper motion sample: missing sensorId, missing 'metadata'
    object, or a missing/non-numeric IMU field. Nothing is ever fabricated
    to work around a problem like this - the caller should surface/log it.
    """


def extract_sensor_id(payload: Mapping[str, Any]) -> str:
    """Return payload["sensorId"], validated as a non-empty string."""
    sensor_id = payload.get("sensorId")
    if not isinstance(sensor_id, str) or not sensor_id:
        raise PayloadAdapterError(
            f"MQTT payload is missing a valid 'sensorId' field: {payload!r}"
        )
    return sensor_id


def to_physical_raw_sample(payload: Mapping[str, Any]) -> dict:
    """Map one MQTT payload to {"ax", "ay", "az", "gx", "gy", "gz"} - the
    raw sample shape consumed by LiveMotionFeatureExtractor.update().

    Raises PayloadAdapterError if 'metadata' is missing/not an object, or
    if any of the 6 required IMU fields is missing or not numeric.
    """
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        raise PayloadAdapterError(
            f"MQTT payload is missing a 'metadata' object: {payload!r}"
        )

    raw_sample: dict = {}
    missing = []
    invalid = []

    for metadata_key, raw_key in METADATA_TO_RAW.items():
        if metadata_key not in metadata:
            missing.append(metadata_key)
            continue
        value = metadata[metadata_key]
        # bool is a subclass of int in Python - explicitly excluded so a
        # stray `true`/`false` in the payload isn't silently treated as 1/0.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            invalid.append(metadata_key)
            continue
        raw_sample[raw_key] = float(value)

    if missing or invalid:
        problems = []
        if missing:
            problems.append(f"missing: {missing}")
        if invalid:
            problems.append(f"non-numeric: {invalid}")
        raise PayloadAdapterError(
            "MQTT payload has invalid IMU field(s) under 'metadata' ("
            + "; ".join(problems)
            + f"): {payload!r}"
        )

    return raw_sample
