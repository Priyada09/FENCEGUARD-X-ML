# FENCEGUARD-X Experimental Data & Hardware Evidence

## Overview
This directory contains the original, uncorrupted experimental evidence collected directly from the **FENCEGUARD-X Safe Low-Voltage 3-Zone Hardware Prototype**.

The primary purpose of these experiments is to collect empirical multi-sensor telemetry—combining 3-zone electrical integrity monitoring (ADC voltage sensing), DC power parameters (INA219 bus voltage/current/power), and physical fence motion dynamics (MPU6050 6-DOF accelerometer and gyroscope)—to validate fault detection algorithms and train ML classification models.

---

## Safety Constraint & Lab Setup

> [!IMPORTANT]
> **SAFE LOW-VOLTAGE PROTOTYPE CONSTRAINT**:
> All experiments were conducted on a safe low-voltage benchtop prototype (3.3V DC logic / safe DC power supply). The system uses end-of-line (EOL) resistor voltage dividers connected to ESP32 ADC pins.
> **DO NOT** attempt to connect the ESP32 or INA219 sensor inputs directly to a high-voltage electric fence energizer without isolated high-voltage transducer circuitry.

---

## Directory Structure

```
hardware/experiments/
├── README.md                                 # This experimental documentation
├── physical_tamper/                          # MPU6050 + Electrical physical disturbance logs
│   ├── EXP_01_NORMAL_STATIONARY.csv          # 30-sample baseline normal stationary telemetry
│   └── EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv # Multi-state physical tamper telemetry log
└── electrical_faults/                        # Pure electrical fault condition logs
    └── sih_fence_raw_dataset.csv             # 35-sample raw 3-zone electrical dataset
```

---

## Hardware Configuration & Specifications

- **Microcontroller**: ESP32 DevKit V1
- **Zone ADC Pins**:
  - Zone 1: GPIO 34
  - Zone 2: GPIO 35
  - Zone 3: GPIO 32
- **I2C Bus**:
  - SDA: GPIO 21
  - SCL: GPIO 22
- **I2C Modules**:
  - INA219 Current/Power Monitor (`0x40`)
  - MPU6050 6-Axis IMU (`0x68`)
- **Fence Simulator**: 3-Zone low-voltage mesh with EOL resistor sensing

---

## Experiment Categories & Conditions

1. **Normal Stationary**: Fence at rest with stable DC voltage (~1.3–1.6V across zones).
2. **Light Vibration**: Environmental disturbances (wind, light contact) causing minor IMU noise without breach.
3. **Single Push**: Isolated physical push event on fence structure.
4. **Repeated Pushes**: Sustained physical activity representing climbing or forced access attempt.
5. **Strong Fence Shaking**: High-energy violent shaking of fence structure.
6. **Open/Cut Fault**: Physical wire cut or broken loop (~3.30V on affected zone).
7. **Short Circuit**: Direct short to ground or line-to-line contact (~0.00V on affected zone).
8. **Combined Breach**: Simultaneous physical movement and electrical fault.

---

## Telemetry Fields & Data Dictionary

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `timestamp_ms` / `sample_id` | Int | Sample timestamp (ms) or sequential sample ID |
| `zone1_v`, `zone2_v`, `zone3_v` | Float | Zone analog voltage readings (0.00 V – 3.30 V) |
| `bus_voltage_v` | Float | INA219 measured DC bus voltage |
| `current_ma` | Float | INA219 measured current draw (mA) |
| `power_mw` | Float | INA219 measured power draw (mW) |
| `ax`, `ay`, `az` | Int | MPU6050 raw 16-bit accelerometer outputs (X, Y, Z axes) |
| `gx`, `gy`, `gz` | Int | MPU6050 raw 16-bit gyroscope outputs (X, Y, Z axes) |
| `physical_event` / `condition` | String | Physical action or fault state observed |
| `electrical_state` / `fault_zone` | String | Zone electrical integrity state (`NORMAL`, `OPEN_CUT`, `SHORT`) |
| `label` | String | Target ground truth classification |
| `data_quality` | String | Data integrity tag (`MEASURED`, `LOOSE_CONNECTION_ANOMALY`, `IMPUTED_BUS_VOLTAGE`) |

---

## Data Integrity & Strict Traceability Rules

Per project data engineering standards:

1. **Raw Traceability**: Files in `hardware/experiments/` represent original empirical evidence. No raw measurements are artificially modified, smoothed, or deleted.
2. **Experimental Anomalies**: Known hardware artifacts (such as INA219 `bus_voltage_v = 0.000 V` due to a temporary loose breadboard jumper) remain intact and are explicitly tagged with `LOOSE_CONNECTION_ANOMALY` or `IMPUTED_BUS_VOLTAGE`. Any cleaning/imputation rules are performed strictly in the ML preprocessing pipeline and saved under `ml/dataset/processed/`.
3. **Multi-Modal Distinctions**: Physical motion combined with electrical fault (e.g. `STRONG_SHAKING` during `OPEN_CUT`) maintains `electrical_state = OPEN_CUT` and `label = ELECTRICAL_FAULT`. Physical events are not re-labeled purely to boost baseline classifier scores.

---

## Data Pipeline Hand-Off to ML Lead (Priyada)

Priyada (ML Lead) utilizes this data via the following reproducible pipeline:

$$\text{RAW EXPERIMENT} \longrightarrow \text{CLEANED DATA} \longrightarrow \text{FEATURE ENGINEERING} \longrightarrow \text{ML DATASET} \longrightarrow \text{MODEL}$$

1. **Raw Data Ingestion**: Load CSVs from `ml/dataset/raw/` (mirrored from `hardware/experiments/`).
2. **Feature Extraction**: Compute temporal rolling statistics (mean, std, min, max, peak-to-peak amplitude) for accelerometer/gyroscope channels and zone voltage deviations.
3. **Model Evaluation**: Train and evaluate multi-class classifiers (`NORMAL`, `PHYSICAL_TAMPER`, `OPEN_CUT`, `SHORT`).
4. **Validation**: Generate confusion matrices and evaluate precision, recall, and F1-score without fabricating performance metrics.
