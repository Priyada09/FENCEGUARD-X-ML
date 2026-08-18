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
    """Load a raw experiment CSV and validate the actual exported schema.

    Some real hardware exports include the label as a trailing field on each row
    instead of a separate header column. This loader preserves the raw values and
    reconstructs a `label` column without altering the source CSV.
    """
    with open(path, newline="", encoding="utf-8") as csvfile:
        rows = list(csv.reader(csvfile))

    if not rows:
        raise ValueError(f"CSV file is empty: {path}")

    header = rows[0]
    parsed_rows = []

    for row in rows[1:]:
        if len(row) == len(header) + 1:
            payload = row[:-1]
            label = row[-1]
        elif len(row) == len(header):
            payload = row
            label = None
        else:
            raise ValueError(
                f"Unexpected row width in {path}: expected {len(header)} or {len(header)+1}, got {len(row)}"
            )
        parsed_rows.append(payload + [label])

    reconstructed_header = header + ["label"]
    df = pd.DataFrame(parsed_rows, columns=reconstructed_header)

    missing = [col for col in RAW_SCHEMA if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def detect_session_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    """Mark timestamp resets or session boundaries.

    This is a placeholder implementation for future session-aware processing.
    """
    result = df.copy()
    if "timestamp_ms" in result.columns:
        timestamps = result["timestamp_ms"].astype(float)
        reset_mask = timestamps.diff().fillna(0).lt(0)
        result["session_boundary"] = reset_mask.astype(int)
    else:
        result["session_boundary"] = 0
    return result


def compute_motion_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute motion features from raw MPU6050 values."""
    result = df.copy()

    accel_x = result["ax"].astype(float)
    accel_y = result["ay"].astype(float)
    accel_z = result["az"].astype(float)
    gyro_x = result["gx"].astype(float)
    gyro_y = result["gy"].astype(float)
    gyro_z = result["gz"].astype(float)

    result["accel_magnitude"] = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
    result["gyro_magnitude"] = np.sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2)
    result["accel_delta"] = result["accel_magnitude"].diff().fillna(0.0)
    result["gyro_delta"] = result["gyro_magnitude"].diff().fillna(0.0)
    result["accel_variance"] = result["accel_magnitude"].rolling(window=5, min_periods=1).var().fillna(0.0)
    result["gyro_variance"] = result["gyro_magnitude"].rolling(window=5, min_periods=1).var().fillna(0.0)
    result["peak_acceleration"] = result["accel_magnitude"].rolling(window=5, min_periods=1).max().fillna(0.0)
    result["peak_gyro"] = result["gyro_magnitude"].rolling(window=5, min_periods=1).max().fillna(0.0)

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
    """Create the fused feature table from multiple raw CSV files."""
    frames: List[pd.DataFrame] = []
    for file_path in data_files:
        df = load_experiment_csv(file_path)
        df = detect_session_boundaries(df)
        df = compute_motion_features(df)
        df = compute_electrical_features(df)
        frames.append(df)

    if not frames:
        raise ValueError("No data files supplied to build_feature_table.")

    combined = pd.concat(frames, ignore_index=True)
    return combined


def summarize_dataset(df: pd.DataFrame) -> dict:
    """Return a lightweight summary for EDA and early model planning."""
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "labels": df["label"].value_counts().to_dict() if "label" in df.columns else {},
        "missing_values": df.isna().sum().to_dict(),
    }
