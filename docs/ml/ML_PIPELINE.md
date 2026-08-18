# ML Pipeline Plan

## Current status

This repository contains a real experimental CSV for stationary baseline data, but no final ML model has been trained or validated yet. The current focus is on structuring a reliable sensor-fusion pipeline before claiming performance.

Important constraints:
- Do not use synthetic data to replace real experiments.
- Do not claim production-level performance from a small prototype dataset.
- Keep raw data intact and use derived features in a separate processing pipeline.

## Data sources

Planned ingestion sources:
- `data/raw/tamper_experiments/EXP_01_NORMAL_STATIONARY.csv`
- future raw experiment CSV files for vibration, tamper, and electrical fault cases

## Raw schema

The raw dataset schema is:

- `timestamp_ms`
- `zone1_v`
- `zone2_v`
- `zone3_v`
- `bus_voltage_v`
- `current_ma`
- `power_mw`
- `ax`
- `ay`
- `az`
- `gx`
- `gy`
- `gz`
- `label`

## ML workflow

### 1. Load raw CSV files

- Read all raw sensor logs from `data/raw/tamper_experiments/`
- Keep session-level metadata separate from sensor streams
- Preserve timestamp ordering when possible
- Treat timestamp reset between sessions as a real hardware condition, not as an error to fabricate away

### 2. Validate data

Validation checks:
- required columns exist
- numeric values parse cleanly
- impossible values are flagged
- duplicate or missing rows are reviewed
- session boundaries are separated where needed

### 3. Handle session/timestamp boundaries

We need to account for:
- ESP32 reset conditions
- timestamp resets or non-monotonic ordering
- per-session event windows

Recommended approach:
- sort by timestamp when available
- detect resets by large drops or repeated values
- assign session IDs and event window IDs before feature engineering

### 4. Calculate motion features

Recommended derived motion features:
- `accel_magnitude`
- `gyro_magnitude`
- `accel_delta`
- `gyro_delta`
- `accel_variance`
- `gyro_variance`
- `peak_acceleration`
- `peak_gyro`
- `event_duration`

These features should be computed from the raw `ax`, `ay`, `az`, `gx`, `gy`, and `gz` values over a defined window.

### 5. Calculate electrical features

Electrical signals should be retained and used directly as features:
- `zone1_v`
- `zone2_v`
- `zone3_v`
- `bus_voltage_v`
- `current_ma`
- `power_mw`

Optional derived electrical features:
- per-zone deviation from baseline
- voltage delta across adjacent samples
- current spike magnitude
- power change over time

### 6. Combine features

A sensor-fusion dataset should merge:
- motion features
- electrical features
- event context
- optional label metadata

The implementation should clearly separate: raw data, derived features, and final classification target.

### 7. Visualize distributions

Before modeling:
- plot distributions of each feature by class
- inspect class separation for the motion channel
- inspect zone voltage distributions for fault scenarios
- check whether classes are balanced or skewed

### 8. Check class balance

Expected target classes:
- `NORMAL`
- `ELECTRICAL_FAULT`
- `PHYSICAL_TAMPER`
- `BREACH`

We must check whether the dataset is balanced enough for a representative baseline model. Small prototype datasets often show imbalance.

### 9. Detect noise and outliers

- inspect extreme motion spikes
- compare with known baseline conditions
- check whether obvious instrumentation errors should be excluded
- avoid deleting valid raw data without a documented reason

### 10. Prepare train/test split without leakage

Recommended practice:
- group by session or event before split
- avoid leakage across the same physical event window
- keep a held-out validation or test set for final metrics

## Baseline model

Recommended initial model:
- Random Forest classifier

Reason:
- works well on structured tabular sensor features
- robust to small and noisy datasets
- easier to interpret than deep learning for early prototyping

## Target labels

The long-term classification target is expected to be one of:
- `NORMAL`
- `ELECTRICAL_FAULT`
- `PHYSICAL_TAMPER`
- `BREACH`

These categories should be validated once enough real experimental data exists.

## Required evaluation metrics

The model should record:
- accuracy
- precision
- recall
- F1-score
- confusion matrix

Special attention:
- false negatives are critical for security monitoring
- recall for tamper and breach classes must be reviewed seriously
- a high overall accuracy alone is not enough for a safety/security system

## Current project status

The project is in the early experimental ML phase. The repository currently has:
- real baseline data present
- no trained model file in a verified production location
- no final evaluation report yet
- no claim of sensor-fusion model performance yet

## TODO

- [TODO] Build data ingestion utilities for raw CSV files.
- [TODO] Add validation for missing values and session boundaries.
- [TODO] Implement feature extraction for motion and electrical channels.
- [TODO] Create exploratory plots and class-balance checks.
- [TODO] Train a baseline Random Forest model.
- [TODO] Publish accuracy, precision, recall, F1-score, and confusion matrix.
- [TODO] Review tamper and breach recall before considering deployment.
- [TODO] Upgrade to richer models only if the collected data supports it.
