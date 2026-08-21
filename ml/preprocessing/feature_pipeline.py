"""Feature engineering skeleton for the FENCEGUARD-X sensor-fusion pipeline.

This module intentionally focuses on validation, feature extraction, and dataset
preparation for real experimental CSVs. It does not fabricate data or make
final model claims.
"""

from __future__ import annotations

import csv
from collections import deque
from pathlib import Path
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Shared constants / formulas
#
# These are the single source of truth for the motion-feature window size
# and the 8 feature names/order, used by BOTH the existing offline/batch
# path (compute_motion_features / build_feature_table) and the live
# streaming path (LiveMotionFeatureExtractor) added for Task 2. Nothing
# below changes any existing formula or default value.
# ---------------------------------------------------------------------------

DEFAULT_WINDOW = 5

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

# Raw fields expected from a single live sample (subset of RAW_SCHEMA that
# the motion-feature calculations actually depend on).
LIVE_RAW_FIELDS = ["timestamp_ms", "ax", "ay", "az", "gx", "gy", "gz"]


def _vector_magnitude(x, y, z):
    """sqrt(x^2 + y^2 + z^2).

    This is the exact formula already used inline in compute_motion_features
    for both accel_mag and gyro_mag, extracted here so the batch path and
    the live-inference path (LiveMotionFeatureExtractor) call the same
    implementation instead of maintaining it twice.
    """
    return np.sqrt(np.asarray(x, dtype=float) ** 2 + np.asarray(y, dtype=float) ** 2 + np.asarray(z, dtype=float) ** 2)


RAW_SCHEMA = [
    "timestamp_ms",
    "zone1_v",
    "zone2_v",
    "zone3_v",
    "bus_voltage_v",
    "current_ma",
    "power_mw",
    "ax",
    "ay",
    "az",
    "gx",
    "gy",
    "gz",
    "label",
]


def load_experiment_csv(path: str | Path) -> pd.DataFrame:
    """Load a raw experiment CSV and validate its exported schema.

    Supports both:
    1. CSVs where the label is already present in the header.
    2. CSVs where the label is an extra trailing field in each data row.

    The raw CSV is never modified.
    """
    with open(path, newline="", encoding="utf-8") as csvfile:
        rows = list(csv.reader(csvfile))

    if not rows:
        raise ValueError(f"CSV file is empty: {path}")

    header = rows[0]
    header_has_label = "label" in header
    parsed_rows = []

    for row in rows[1:]:
        if header_has_label:
            if len(row) != len(header):
                raise ValueError(
                    f"Unexpected row width in {path}: "
                    f"expected {len(header)}, got {len(row)}"
                )
            parsed_rows.append(row)

        else:
            if len(row) == len(header) + 1:
                parsed_rows.append(row)

            elif len(row) == len(header):
                parsed_rows.append(row + [None])

            else:
                raise ValueError(
                    f"Unexpected row width in {path}: "
                    f"expected {len(header)} or {len(header) + 1}, "
                    f"got {len(row)}"
                )

    if header_has_label:
        reconstructed_header = header
    else:
        reconstructed_header = header + ["label"]

    df = pd.DataFrame(parsed_rows, columns=reconstructed_header)

    missing = [col for col in RAW_SCHEMA if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if not df.columns.is_unique:
        duplicate_columns = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(
            f"Duplicate columns detected in {path}: {duplicate_columns}"
        )

    return df

def detect_session_boundaries(
    df: pd.DataFrame,
    group_col: str | None = None,
) -> pd.DataFrame:
    """Assign globally unique session IDs.

    A new session starts when:
    1. the experiment/group changes, or
    2. the timestamp resets or decreases.

    Session IDs are unique across experiments so that temporal features
    never mix unrelated recordings.
    """
    result = df.reset_index(drop=True).copy()

    if group_col is not None and group_col in result.columns:
        group = result[group_col].astype(str)
        group_changed = group.ne(group.shift())
    else:
        group = pd.Series("SESSION", index=result.index)
        group_changed = pd.Series(False, index=result.index)

    if "timestamp_ms" in result.columns:
        timestamps = pd.to_numeric(
            result["timestamp_ms"], errors="coerce"
        )
        timestamp_reset = timestamps.diff().le(0)
    else:
        timestamp_reset = pd.Series(False, index=result.index)

    session_start = group_changed | timestamp_reset
    session_start.iloc[0] = True

    session_number = session_start.groupby(group).cumsum()

    result["session_id"] = (
        group
        + "_S"
        + session_number.astype(str)
    )

    return result

def compute_motion_features(
    df: pd.DataFrame,
    window: int = DEFAULT_WINDOW,
) -> pd.DataFrame:
    """Compute session-aware motion features from MPU6050 values.

    Deltas and rolling statistics are calculated separately within each
    session so unrelated experiments never influence one another.
    """
    if "session_id" not in df.columns:
        raise ValueError(
            "df must contain 'session_id'. "
            "Call detect_session_boundaries() first."
        )

    result = df.copy()

    accel_x = pd.to_numeric(result["ax"], errors="coerce")
    accel_y = pd.to_numeric(result["ay"], errors="coerce")
    accel_z = pd.to_numeric(result["az"], errors="coerce")

    gyro_x = pd.to_numeric(result["gx"], errors="coerce")
    gyro_y = pd.to_numeric(result["gy"], errors="coerce")
    gyro_z = pd.to_numeric(result["gz"], errors="coerce")

    result["accel_mag"] = _vector_magnitude(accel_x, accel_y, accel_z)

    result["gyro_mag"] = _vector_magnitude(gyro_x, gyro_y, gyro_z)

    accel_by_session = result.groupby("session_id")["accel_mag"]
    gyro_by_session = result.groupby("session_id")["gyro_mag"]

    result["delta_accel"] = accel_by_session.diff().abs()
    result["delta_gyro"] = gyro_by_session.diff().abs()

    result["rolling_mean"] = accel_by_session.transform(
        lambda s: s.rolling(window=window, min_periods=1).mean()
    )

    result["rolling_std"] = accel_by_session.transform(
        lambda s: s.rolling(window=window, min_periods=1).std()
    )

    result["peak_accel"] = accel_by_session.transform(
        lambda s: s.rolling(window=window, min_periods=1).max()
    )

    result["peak_gyro"] = gyro_by_session.transform(
        lambda s: s.rolling(window=window, min_periods=1).max()
    )

    return result


class LiveMotionFeatureExtractor:
    """Session-aware, incremental motion-feature extractor.

    This is the SAME 8 motion features, computed with the SAME formulas and
    the SAME session-aware window=5 / min_periods=1 semantics as
    compute_motion_features(), but produced one raw sample at a time so the
    identical calculations can eventually be reused for live inference
    (streaming MPU6050 samples) instead of only offline batch processing.

    It does not fabricate delta/rolling values for the first sample of a
    session: exactly like the offline batch path (where
    groupby("session_id")["accel_mag"].diff() is NaN for a session's first
    row), delta_accel/delta_gyro are returned as float('nan') for the first
    sample seen after a (re)start or a detected session boundary.

    Session-boundary handling mirrors detect_session_boundaries(): a new
    session starts when an explicit session_id changes, or (if no
    session_id is supplied) when timestamp_ms resets/decreases relative to
    the previous sample. Either way, the underlying per-session buffers are
    cleared exactly as compute_motion_features() isolates each session_id
    group so unrelated recordings never influence one another.

    Usage:
        extractor = LiveMotionFeatureExtractor()
        features = extractor.update({
            "timestamp_ms": 1000, "ax": .., "ay": .., "az": ..,
            "gx": .., "gy": .., "gz": ..,
        })
        # features == {"accel_mag": ..., "gyro_mag": ..., "delta_accel": ...,
        #              "delta_gyro": ..., "rolling_mean": ...,
        #              "rolling_std": ..., "peak_accel": ..., "peak_gyro": ...}
    """

    def __init__(self, window: int = DEFAULT_WINDOW):
        self.window = window
        self._session_id: Optional[str] = None
        self._last_timestamp_ms: Optional[float] = None
        self._accel_window: deque = deque(maxlen=window)
        self._gyro_window: deque = deque(maxlen=window)
        self._prev_accel_mag: Optional[float] = None
        self._prev_gyro_mag: Optional[float] = None

    def reset(self) -> None:
        """Clear all session state (start fresh, as if newly constructed)."""
        self._session_id = None
        self._last_timestamp_ms = None
        self._accel_window.clear()
        self._gyro_window.clear()
        self._prev_accel_mag = None
        self._prev_gyro_mag = None

    def _start_new_session(self, session_id: str) -> None:
        self._session_id = session_id
        self._accel_window.clear()
        self._gyro_window.clear()
        self._prev_accel_mag = None
        self._prev_gyro_mag = None

    def update(self, sample: dict, session_id: str | None = None) -> dict:
        """Feed one raw sample and return its 8 motion features.

        sample must contain: ax, ay, az, gx, gy, gz, and (for automatic
        session-boundary detection) timestamp_ms.

        session_id: pass an explicit session/experiment identifier when the
        caller already knows session boundaries (mirrors the group_col
        behavior of detect_session_boundaries). If omitted, a boundary is
        inferred from timestamp_ms resetting or decreasing, matching
        detect_session_boundaries()'s timestamp-reset rule for a single,
        ungrouped stream.
        """
        raw_timestamp_ms = sample.get("timestamp_ms")
        # Coerce numerically for comparison purposes only (mirrors
        # detect_session_boundaries()'s pd.to_numeric(errors="coerce") on
        # timestamp_ms) so string-typed timestamps (e.g. straight from a
        # CSV row) don't get compared lexicographically.
        try:
            timestamp_ms = float(raw_timestamp_ms) if raw_timestamp_ms is not None else None
        except (TypeError, ValueError):
            timestamp_ms = None

        if session_id is not None:
            is_new_session = session_id != self._session_id
        else:
            session_id = self._session_id if self._session_id is not None else "LIVE_S1"
            is_new_session = self._session_id is None or (
                self._last_timestamp_ms is not None
                and timestamp_ms is not None
                and timestamp_ms <= self._last_timestamp_ms
            )

        if is_new_session:
            self._start_new_session(session_id)

        self._last_timestamp_ms = timestamp_ms

        accel_mag = float(_vector_magnitude(sample["ax"], sample["ay"], sample["az"]))
        gyro_mag = float(_vector_magnitude(sample["gx"], sample["gy"], sample["gz"]))

        # Do not fabricate a delta for the first sample of a session -
        # matches the offline .diff() -> NaN behavior exactly.
        delta_accel = (
            abs(accel_mag - self._prev_accel_mag)
            if self._prev_accel_mag is not None
            else float("nan")
        )
        delta_gyro = (
            abs(gyro_mag - self._prev_gyro_mag)
            if self._prev_gyro_mag is not None
            else float("nan")
        )

        self._accel_window.append(accel_mag)
        self._gyro_window.append(gyro_mag)

        accel_values = np.fromiter(self._accel_window, dtype=float)
        gyro_values = np.fromiter(self._gyro_window, dtype=float)

        rolling_mean = float(accel_values.mean())
        # pandas Series.std() default ddof=1; a single-sample window is NaN,
        # exactly like rolling(window=5, min_periods=1).std() on the first
        # row of a session.
        rolling_std = (
            float(np.std(accel_values, ddof=1)) if accel_values.size > 1 else float("nan")
        )
        peak_accel = float(accel_values.max())
        peak_gyro = float(gyro_values.max())

        self._prev_accel_mag = accel_mag
        self._prev_gyro_mag = gyro_mag

        return {
            "accel_mag": accel_mag,
            "gyro_mag": gyro_mag,
            "delta_accel": delta_accel,
            "delta_gyro": delta_gyro,
            "rolling_mean": rolling_mean,
            "rolling_std": rolling_std,
            "peak_accel": peak_accel,
            "peak_gyro": peak_gyro,
        }


def compute_electrical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Retain electrical measurements and create simple derived values."""
    result = df.copy()
    for col in ["zone1_v", "zone2_v", "zone3_v", "bus_voltage_v", "current_ma", "power_mw"]:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    result["zone_voltage_mean"] = result[["zone1_v", "zone2_v", "zone3_v"]].mean(axis=1)
    result["zone_voltage_std"] = result[["zone1_v", "zone2_v", "zone3_v"]].std(axis=1, ddof=0).fillna(0.0)
    return result


def build_feature_table(data_files: Iterable[str | Path]) -> pd.DataFrame:
    """Create a fused, session-aware feature table from raw CSV files."""
    frames: List[pd.DataFrame] = []

    for file_path in data_files:
        df = load_experiment_csv(file_path)

        # Use the source filename as the experiment identifier.
        experiment_id = Path(file_path).stem
        df["experiment_id"] = experiment_id

        frames.append(df)

    if not frames:
        raise ValueError("No data files supplied to build_feature_table.")

    combined = pd.concat(
        frames,
        ignore_index=True,
        sort=False,
    )

    combined = detect_session_boundaries(
        combined,
        group_col="experiment_id",
    )

    combined = compute_motion_features(
        combined,
        window=DEFAULT_WINDOW,
    )

    combined = compute_electrical_features(combined)

    return combined


def summarize_dataset(df: pd.DataFrame) -> dict:
    """Return a lightweight summary for EDA and early model planning."""
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "labels": df["label"].value_counts().to_dict() if "label" in df.columns else {},
        "missing_values": df.isna().sum().to_dict(),
    }
