# ML Dataset Documentation

## Overview

This directory contains the experimental datasets used by **Priyada (ML Lead)** for feature engineering, baseline classification, and ML model development for the **FENCEGUARD-X** system.

All raw datasets mirror the original experimental evidence in `hardware/experiments/`.

---

## Directory Structure

```
ml/dataset/
├── README.md                                 # This dataset guide
├── raw/                                      # Raw experimental data files
│   ├── sih_fence_raw_dataset.csv             # 35-sample raw 3-zone electrical dataset
│   ├── EXP_01_NORMAL_STATIONARY.csv          # 30-sample raw stationary baseline telemetry
│   └── EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv # Raw physical tamper experiment logs
└── processed/                                # Cleaned & feature-engineered outputs
```

---

## Complete ML Data Pipeline

$$\text{RAW EXPERIMENT} \longrightarrow \text{CLEANED DATA} \longrightarrow \text{FEATURE ENGINEERING} \longrightarrow \text{TRAIN/TEST SPLIT} \longrightarrow \text{MODEL EVALUATION}$$

### 1. RAW
Direct empirical measurements captured by ESP32 ADC, INA219, and MPU6050 during low-voltage lab experiments. Includes raw hardware artifacts such as INA219 `bus_voltage_v = 0.000 V` loose jumper events explicitly tagged in `data_quality`.

### 2. CLEANING
Data preprocessing pipeline handles missing values, imputes known sensor dropouts where documented (`IMPUTED_BUS_VOLTAGE`), and validates physical bounds without altering raw empirical source files.

### 3. VALIDATION
Sanity checks on zone voltage ranges (0–3.3V), INA219 power logic ($P = V \times I$), and MPU6050 16-bit signed integer accelerometer/gyroscope bounds.

### 4. FEATURE ENGINEERING
Temporal windowing (e.g. 500ms / 1000ms rolling windows) computes derived multi-modal features:
- **Motion Features**: Acceleration magnitude ($||a||$), gyro magnitude ($||\omega||$), $\Delta a$, $\Delta \omega$, rolling mean, rolling standard deviation, peak acceleration, peak gyro, event duration/persistence.
- **Electrical Features**: Per-zone voltage deviation from normal baseline ($\Delta V_z$), bus voltage variance, current delta.

### 5. TRAIN / TEST SPLIT
Stratified train/test splitting preserving class proportions across `NORMAL`, `PHYSICAL_TAMPER`, `OPEN_CUT`, `SHORT`, and `MULTI_FAULT`.

### 6. MODEL EVALUATION
Priyada (ML Lead) evaluates baseline classifiers (RandomForest, DecisionTree, SVM, XGBoost) and produces:
- Confusion Matrix
- Precision, Recall, F1-Score per class
- Feature Importance ranking

---

## Safety & Data Integrity Constraints

> [!IMPORTANT]
> **LAB PROTOTYPE SCOPE**: All data was collected on a safe low-voltage prototype.
> **DATA INTEGRITY**: No raw rows are fabricated or artificially smoothed. Sensor anomalies remain identifiable in raw files. Final ML accuracy metrics are **TBD** pending Priyada's model execution.
