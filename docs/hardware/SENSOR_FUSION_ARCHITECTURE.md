# Sensor Fusion Architecture

## Overview

The project is designed around a multi-sensor perimeter-monitoring architecture:
- electrical integrity sensing for each fence zone
- current and power sensing through INA219
- physical motion sensing through MPU6050
- temporal analysis over event windows
- fusion of electrical and motion evidence for classification

This is intentionally a safe low-voltage prototype and not a live high-voltage electric fence.

## Sensor inputs

### Motion sensor stream

MPU6050 provides six raw values:
- `ax`, `ay`, `az`
- `gx`, `gy`, `gz`

These values are used to derive:
- acceleration magnitude
- gyro magnitude
- acceleration delta
- gyro delta
- variance
- peak values
- event duration

### Electrical sensor stream

The electrical layer provides:
- `zone1_v`
- `zone2_v`
- `zone3_v`
- `bus_voltage_v`
- `current_ma`
- `power_mw`

## Current implemented status

The repository already contains evidence of successful electrical detection and stationary baseline data:
- 3 fence zones are monitored independently
- open/cut and short conditions for each zone have been demonstrated in project documents
- `EXP_01_NORMAL_STATIONARY.csv` is present as real experimental data

The sensor-fusion classifier is not claimed to be complete or trained at this time.

## Architecture flow

```text
MPU6050
  ├── ax, ay, az
  ├── gx, gy, gz
  └──> motion feature extraction
        ├── acceleration magnitude
        ├── gyro magnitude
        ├── acceleration delta
        ├── gyro delta
        ├── variance
        ├── peak values
        └── event duration

Electrical sensors
  ├── zone1_v
  ├── zone2_v
  ├── zone3_v
  ├── bus_voltage_v
  ├── current_ma
  └── power_mw

Motion + Electrical streams
  └──> feature fusion
        └──> rule-based baseline + ML classifier
              ├── NORMAL
              ├── ELECTRICAL_FAULT
              ├── PHYSICAL_TAMPER
              └── BREACH
```

## Design principle

The system does not use a single arbitrary MPU6050 threshold such as:
- `magnitude > fixed arbitrary threshold = TAMPER`

That approach is rejected because the sensor is mounted at an angle and experiences a static gravity component. The raw accelerometer values are therefore not expected to be near zero in a stationary case.

## Fusion logic

The future classification logic should consider:
1. accelerometer change
2. gyroscope change
3. event duration
4. electrical condition
5. zone information

This means physical tampering is judged using a combination of motion dynamics and contextual electrical state, not a single raw magnitude value.

## Rule-based baseline

A valid early baseline can be built using rule logic such as:
- zone voltage outside normal operating range
- abnormal current/power patterns
- sustained motion energy above background noise
- coherent electrical + motion events in the same time window

This baseline is a stepping stone to the ML model; it is not a substitute for trained classification.

## ML direction

The ML plan is intentionally conservative:
- collect enough real experiments
- build derived motion and electrical features
- evaluate class balance and outliers
- train a Random Forest baseline
- measure recall for tamper and breach classes

## TODO

- [TODO] Add more real motion and fault experiment CSVs.
- [TODO] Build fused feature dataset.
- [TODO] Train the baseline Random Forest model.
- [TODO] Validate recall for tamper and breach events.
- [TODO] Integrate results into backend event schema.
