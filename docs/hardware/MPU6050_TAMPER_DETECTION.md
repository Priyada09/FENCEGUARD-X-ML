# MPU6050 Tamper Detection Notes

## Current status

The MPU6050 is communicating and returning six raw measurements:
- `ax`
- `ay`
- `az`
- `gx`
- `gy`
- `gz`

This is confirmed by the real experimental data in `hardware/experiments/physical_tamper/EXP_01_NORMAL_STATIONARY.csv` and `EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv`.

## Important interpretation rule

The sensor is mounted at an angle. Therefore it has a static gravitational component distributed across the axes.

Example stationary values seen in the dataset:
- `ax ≈ -11779`
- `ay ≈ 809`
- `az ≈ 9786`

These values are expected and do not imply a fault. They indicate that the accelerometer is measuring gravity in a tilted orientation.

## Why a fixed threshold is not acceptable

A rule such as:
- `magnitude > threshold = TAMPER`

is not reliable for this prototype because:
- static gravity changes the baseline substantially
- the mounting angle shifts the axis values
- environmental vibration may naturally increase motion magnitude
- the same motion must be evaluated in electrical context and over time

## Preferred detection approach

Use a combination of:
1. accelerometer change
2. gyroscope change
3. event duration
4. electrical condition
5. zone information

A more realistic feature set includes:
- acceleration magnitude
- gyro magnitude
- acceleration delta
- gyro delta
- variance
- peak values
- duration of motion event

## Practical rule-based direction

The project should treat physical movement as suspicious when there is:
- a sustained increase in motion energy
- a coherent increase in both acceleration and gyro values
- a pattern that is not explained by normal stationary baseline
- a concurrent electrical or zone-context anomaly that suggests a breach

## Safety and data discipline

- Keep raw MPU6050 values intact.
- Do not smooth or fabricate values to fit a threshold.
- Preserve the stationary baseline dataset as the reference for drift and orientation.
- Do not claim final tamper detection accuracy until real experiments are collected and assessed.

## Status Summary

- [x] MPU6050 sensor hardware connection and I2C communication verified.
- [x] Raw motion telemetry captured across physical experiment scenarios.
- [ ] Sensor-fusion algorithm and temporal feature extraction pipeline implementation.
- [ ] Baseline ML classifier training and recall evaluation by ML Lead (Priyada).
