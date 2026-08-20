"""Feature engineering skeleton for the FENCEGUARD-X sensor-fusion pipeline.

This module intentionally focuses on validation, feature extraction, and dataset
preparation for real experimental CSVs. It does not fabricate data or make
final model claims.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

import numpy as np
import pandas as pd


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
    window: int = 5,
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

    result["accel_mag"] = np.sqrt(
        accel_x**2 + accel_y**2 + accel_z**2
    )

    result["gyro_mag"] = np.sqrt(
        gyro_x**2 + gyro_y**2 + gyro_z**2
    )

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
        window=5,
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
