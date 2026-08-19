# FENCEGUARD-X

Smart IoT + Edge AI based electric fence monitoring, tamper detection and zone-wise fault identification.

## Project objective

FENCEGUARD-X is a safe low-voltage prototype for perimeter monitoring that combines:
- zone-wise electrical fault detection
- current and power monitoring
- 6-axis physical motion sensing
- temporal event analysis
- sensor fusion for classification
- future edge/ML-based decision support

The goal is not to build a dangerous high-voltage system. The goal is to demonstrate a safe lab prototype for SIH with realistic sensor-fusion logic and real experimental data.

## Current active team (August 2026)

| Member | Role and ownership |
|---|---|
| Anup Patil | Hardware + Firmware, ESP32 integration, sensor integration, experimental data collection, sensor-fusion integration |
| Priyada | Machine learning, preprocessing, feature engineering, model training, evaluation |
| Alok Kumar | Backend, API, database, event processing |
| Sakshi | Frontend, dashboard, API integration on frontend, deployment, demo hosting |
| Ananya | Presentation, documentation, pitch, demo narrative |

> Jayesh is not an active team member for this current SIH 2026 phase. Hardware and firmware ownership is currently handled by Anup.

## Problem being solved

Traditional fence monitoring is often reactive. It may detect a failure only after the problem has already caused operational damage or security risk. In this project, the system is designed to distinguish between:
- normal operation
- electrical faults such as open/cut and short conditions
- physical tampering and vibration
- combined breach events where motion and electrical events occur together

## 3-zone architecture

The prototype uses a 3-zone fence model:
- Zone 1
- Zone 2
- Zone 3

Each zone is monitored independently for electrical integrity and physical disturbance context.

## Hardware

Current prototype hardware includes:
- ESP32
- 3 fence zones
- INA219 current/voltage/power sensor
- MPU6050 6-axis IMU
  - AX, AY, AZ
  - GX, GY, GZ
- safe low-voltage DC fence simulator
- zone voltage sensing

This is a safe low-voltage experimental representation. It is not a real high-voltage electric fence.

## Electrical detection

The electrical sensing layer already demonstrates the expected zone states:
- NORMAL
- OPEN/CUT
- SHORT

The system logs the following fields:
- `zone1_v`
- `zone2_v`
- `zone3_v`
- `bus_voltage_v`
- `current_ma`
- `power_mw`

The current logic already demonstrates:
- Zone 1 open/cut
- Zone 2 open/cut
- Zone 3 open/cut
- Zone 1 short
- Zone 2 short
- Zone 3 short

This functionality is preserved and not removed.

## Physical tamper detection

The earlier idea of using one arbitrary MPU6050 threshold is not used.

The approved approach is a sensor-fusion strategy that considers:
1. accelerometer change
2. gyroscope change
3. event duration
4. electrical condition
5. zone information

The architecture is:

MPU6050
  -> AX AY AZ
  -> GX GY GZ
  -> motion feature extraction
    -> acceleration magnitude
    -> gyro magnitude
    -> acceleration delta
    -> gyro delta
    -> variance
    -> peak values
    -> event duration

Electrical sensors
  -> zone voltage values
  -> INA219 voltage/current/power

Both streams
  -> feature fusion
  -> rule-based baseline + ML classifier
    -> NORMAL
    -> ELECTRICAL_FAULT
    -> PHYSICAL_TAMPER
    -> BREACH

## MPU6050 status

MPU6050 communication is working. The raw dataset includes six motion values:
- AX
- AY
- AZ
- GX
- GY
- GZ

The dataset shows values such as:
- AX ≈ -11779
- AY ≈ 809
- AZ ≈ 9786

This is expected because the sensor is mounted at an angle and gravity is distributed across axes. The raw values are not assumed to be zero in stationary conditions.

## Experimental data

The project contains real experimental data collected from prototype testing:
- [hardware/experiments/physical_tamper/EXP_01_NORMAL_STATIONARY.csv](hardware/experiments/physical_tamper/EXP_01_NORMAL_STATIONARY.csv)
- [hardware/experiments/physical_tamper/EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv](hardware/experiments/physical_tamper/EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv)
- [hardware/experiments/electrical_faults/sih_fence_raw_dataset.csv](hardware/experiments/electrical_faults/sih_fence_raw_dataset.csv)
- [ml/dataset/raw/sih_fence_raw_dataset.csv](ml/dataset/raw/sih_fence_raw_dataset.csv)

This is real hardware data, preserving original readings and loose connection annotations. Schema includes:
- `timestamp_ms` / `sample_id`
- `zone1_v`, `zone2_v`, `zone3_v`
- `bus_voltage_v`, `current_ma`, `power_mw`
- `ax`, `ay`, `az`, `gx`, `gy`, `gz`
- `physical_event`, `electrical_state`, `label`, `data_quality`

## ML plan

Priyada’s pipeline follows:
1. Load raw CSV files from `ml/dataset/raw/`
2. Validate data and preserve data quality annotations (`MEASURED`, `LOOSE_CONNECTION_ANOMALY`, `IMPUTED_BUS_VOLTAGE`)
3. Handle session and timestamp boundaries
4. Calculate multi-axis motion features
5. Calculate zone electrical features
6. Combine features for sensor fusion
7. Visualize feature distributions & correlations
8. Check class balance
9. Detect noise and outliers
10. Prepare stratified train/test split without leakage

Recommended derived features:
- `accel_magnitude`
- `gyro_magnitude`
- `accel_delta`
- `gyro_delta`
- `accel_variance`
- `gyro_variance`
- `peak_acceleration`
- `peak_gyro`
- `event_duration`

Electrical features:
- `zone1_v`
- `zone2_v`
- `zone3_v`
- `bus_voltage_v`
- `current_ma`
- `power_mw`

Target classes:
- `NORMAL`
- `ELECTRICAL_FAULT`
- `PHYSICAL_TAMPER`
- `BREACH`

The baseline model will evaluate Random Forest / Decision Tree algorithms.

The evaluation will report:
- accuracy
- precision
- recall
- F1-score
- confusion matrix

False negatives for tamper and breach classes will be analyzed carefully.

## Repository structure

```text
FENCEGUARD-X/
├── README.md
├── PROJECT_STATUS.md
├── PROJECT_IMPLEMENTATION_REPORT.md
├── AUDIT_REPORT_17AUG2026.md
├── TEAM_COLLABORATION.md
├── EXECUTION_CHECKLIST.md
├── QUICK_START.md
├── hardware/
│   ├── README.md
│   ├── components.md
│   ├── EXPERIMENT_LOG.md
│   ├── integration/
│   ├── sensors/
│   ├── zone-testing/
│   └── experiments/
│       ├── README.md
│       ├── physical_tamper/
│       │   ├── EXP_01_NORMAL_STATIONARY.csv
│       │   └── EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv
│       └── electrical_faults/
│           └── sih_fence_raw_dataset.csv
├── firmware/
│   ├── README.md
│   └── esp32/
├── backend/
│   ├── README.md
│   ├── api/
│   └── database/
├── dashboard/
│   └── README.md
├── frontend/
├── ml/
│   ├── README.md
│   ├── dataset/
│   │   ├── README.md
│   │   ├── raw/
│   │   └── processed/
│   ├── preprocessing/
│   ├── notebooks/
│   ├── models/
│   └── training/
├── docs/
└── project-management/
```

## Current implementation status

| Area | Status | Notes |
|---|---|---|
| 3-zone hardware | DONE | Prototype is present and documented |
| electrical fault testing | DONE | Open and short cases are part of the project baseline |
| MPU6050 integration | DONE | Communication is working and raw values are captured |
| normal baseline collection | DONE | Real dataset is present |
| light vibration dataset | PENDING | Next hardware experiment |
| physical tamper dataset | PENDING | Pending real collection |
| combined breach dataset | PENDING | Pending real collection |
| sensor fusion integration | PENDING | Future stage |
| ML pipeline design | NEXT | Initial data ingestion and feature engineering |
| backend event schema | PENDING/VERIFY | Design is future-facing |
| dashboard contract | PENDING | Real-time claims require live backend |

## Pending work

- collect `EXP_02_LIGHT_VIBRATION.csv`
- collect `EXP_03_PHYSICAL_TAMPER.csv`
- collect repeated and strong tamper datasets
- collect zone open/short electrical datasets
- collect combined breach dataset
- process raw sensor data with session-aware feature pipeline
- train baseline Random Forest classification model
- validate recall on tamper and breach classes
- integrate backend and frontend around fused events

## Safety note

This prototype uses safe low-voltage DC only.
Do not connect ESP32, INA219, MPU6050, or breadboard electronics directly to a real high-voltage electric fence.
This project remains a low-voltage SIH demonstration and must not be modified into a dangerous high-voltage implementation.

## Key documentation

- [docs/experiments/EXPERIMENT_PLAN.md](docs/experiments/EXPERIMENT_PLAN.md)
- [docs/ml/ML_PIPELINE.md](docs/ml/ML_PIPELINE.md)
- [docs/hardware/SENSOR_FUSION_ARCHITECTURE.md](docs/hardware/SENSOR_FUSION_ARCHITECTURE.md)
- [docs/hardware/MPU6050_TAMPER_DETECTION.md](docs/hardware/MPU6050_TAMPER_DETECTION.md)
- [docs/architecture/SYSTEM_ARCHITECTURE.md](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [docs/TEAM_TASK_TRACKER.md](docs/TEAM_TASK_TRACKER.md)

## Last updated

18 August 2026

## Status summary

This repository currently contains:
- a validated low-voltage prototype design and electrical sensing workflow
- real experimental baseline data for normal stationary conditions
- missing next-stage documentation and ML pipeline scaffolding
- pending physical-disturbance and sensor-fusion data collection

No ML performance claims are made before a valid model is trained and evaluated on real experimental data.

