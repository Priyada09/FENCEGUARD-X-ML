"""End-to-end: representative MQTT payload -> adapter -> session_manager
-> predictor, for a single sensorId across two samples."""

import copy
import math

from ml.inference.payload_adapter import extract_sensor_id, to_physical_raw_sample
from ml.inference.session_manager import PhysicalSessionManager
from ml.inference.physical_predictor import PhysicalTamperPredictor

REPRESENTATIVE_PAYLOAD = {
    "sensorId": "ZONE_1",
    "eventType": "normal",
    "current": 0.12,
    "voltage": 3.30,
    "temperature": 28.5,
    "metadata": {
        "power": 0.396,
        "busVoltage": 3.30,
        "accelX": 0.02,
        "accelY": 0.01,
        "accelZ": 0.98,
        "gyroX": 0.12,
        "gyroY": 0.08,
        "gyroZ": 0.05,
    },
}


def _second_payload():
    payload = copy.deepcopy(REPRESENTATIVE_PAYLOAD)
    payload["metadata"]["accelX"] = 0.9
    payload["metadata"]["accelY"] = 0.6
    payload["metadata"]["accelZ"] = 0.4
    payload["metadata"]["gyroX"] = 1.1
    payload["metadata"]["gyroY"] = 0.9
    payload["metadata"]["gyroZ"] = 0.7
    return payload


def test_first_live_payload_yields_no_prediction():
    manager = PhysicalSessionManager()
    predictor = PhysicalTamperPredictor()

    sensor_id = extract_sensor_id(REPRESENTATIVE_PAYLOAD)
    raw_sample = to_physical_raw_sample(REPRESENTATIVE_PAYLOAD)
    features = manager.update(sensor_id, raw_sample)
    result = predictor.predict(sensor_id, features)

    assert result.ready is False


def test_second_live_payload_for_same_sensor_yields_prediction():
    manager = PhysicalSessionManager()
    predictor = PhysicalTamperPredictor()

    sensor_id = extract_sensor_id(REPRESENTATIVE_PAYLOAD)

    # Sample 1: first sample of ZONE_1's session -> not ready.
    raw_1 = to_physical_raw_sample(REPRESENTATIVE_PAYLOAD)
    features_1 = manager.update(sensor_id, raw_1)
    result_1 = predictor.predict(sensor_id, features_1)
    assert result_1.ready is False

    # Sample 2: same sensorId -> deltas/rolling_std now finite -> predicts.
    raw_2 = to_physical_raw_sample(_second_payload())
    features_2 = manager.update(sensor_id, raw_2)
    result_2 = predictor.predict(sensor_id, features_2)

    assert result_2.ready is True
    assert result_2.label in {"NORMAL", "PHYSICAL_TAMPER"}
    assert list(result_2.features.keys()) == predictor.feature_order
    for value in result_2.features.values():
        assert math.isfinite(value)


def test_two_zones_interleaved_do_not_cross_contaminate():
    manager = PhysicalSessionManager()
    predictor = PhysicalTamperPredictor()

    zone1_payload = REPRESENTATIVE_PAYLOAD
    zone2_payload = copy.deepcopy(REPRESENTATIVE_PAYLOAD)
    zone2_payload["sensorId"] = "ZONE_2"

    # ZONE_1 first sample.
    f1 = manager.update("ZONE_1", to_physical_raw_sample(zone1_payload))
    r1 = predictor.predict("ZONE_1", f1)
    assert r1.ready is False

    # ZONE_1 second sample -> ready.
    f1b = manager.update("ZONE_1", to_physical_raw_sample(_second_payload()))
    r1b = predictor.predict("ZONE_1", f1b)
    assert r1b.ready is True

    # ZONE_2's first-ever sample, arriving after ZONE_1 is already
    # "warmed up" - must still be treated as ZONE_2's first sample.
    f2 = manager.update("ZONE_2", to_physical_raw_sample(zone2_payload))
    r2 = predictor.predict("ZONE_2", f2)
    assert r2.ready is False
