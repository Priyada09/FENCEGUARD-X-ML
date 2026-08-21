"""Per-sensorId session state for physical-tamper live inference.

Each sensorId gets its own LiveMotionFeatureExtractor instance, imported
unmodified from ml.preprocessing.feature_pipeline, so concurrent zones
(ZONE_1, ZONE_2, ZONE_3, ...) never share rolling windows or delta state
(Task 2 decision #5). session_id is always pinned explicitly to sensorId
when calling .update() - no timestamp-based session-boundary detection is
used, per decision #6 (no confirmed timestamp on the live payload).

feature_pipeline.py itself is not modified in any way.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

# Make the repo root importable regardless of the caller's cwd/PYTHONPATH,
# mirroring the existing repo's own convention (train_physical_tamper_model.py)
# of resolving paths from Path(__file__) rather than assuming cwd.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ml.preprocessing.feature_pipeline import (  # noqa: E402
    DEFAULT_WINDOW,
    LiveMotionFeatureExtractor,
)


class PhysicalSessionManager:
    """Owns one LiveMotionFeatureExtractor per sensorId.

    Usage:
        manager = PhysicalSessionManager()
        features = manager.update("ZONE_1", {"ax": .., "ay": .., "az": ..,
                                               "gx": .., "gy": .., "gz": ..})
    """

    def __init__(self, window: int = DEFAULT_WINDOW):
        self._window = window
        self._extractors: Dict[str, LiveMotionFeatureExtractor] = {}

    def _get_extractor(self, sensor_id: str) -> LiveMotionFeatureExtractor:
        extractor = self._extractors.get(sensor_id)
        if extractor is None:
            extractor = LiveMotionFeatureExtractor(window=self._window)
            self._extractors[sensor_id] = extractor
        return extractor

    def update(self, sensor_id: str, raw_sample: dict) -> dict:
        """Feed one raw sample ({"ax","ay","az","gx","gy","gz"}) for
        sensor_id into that sensor's own extractor and return the 8
        motion features. Unmodified LiveMotionFeatureExtractor.update()
        semantics apply: NaN delta_accel/delta_gyro/rolling_std on the
        first sample of a (re)started session, exactly as the offline
        batch path behaves.
        """
        extractor = self._get_extractor(sensor_id)
        return extractor.update(raw_sample, session_id=sensor_id)

    def reset(self, sensor_id: str) -> None:
        """Drop all state for a given sensorId (e.g. on device reconnect
        or an explicit re-arm), so its next sample is treated as the
        first sample of a new session."""
        self._extractors.pop(sensor_id, None)

    def known_sensor_ids(self) -> List[str]:
        return list(self._extractors.keys())
