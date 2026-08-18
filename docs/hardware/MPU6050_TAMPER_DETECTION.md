# MPU6050 Tamper Detection Notes

## Current status

The MPU6050 is communicating and returning six raw measurements:
- `ax`
- `ay`
- `az`
- `gx`
- `gy`
- `gz`

This is confirmed by the real experimental data in `data/raw/tamper_experiments/EXP_01_NORMAL_STATIONARY.csv`.

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

## TODO

- [TODO] Capture EXP_02_LIGHT_VIBRATION data to model normal disturbance.
- [TODO] Capture EXP_03_PHYSICAL_TAMPER data to model real tamper signatures.
- [TODO] Build a fused feature pipeline combining electrical and motion data.
- [TODO] Train a baseline classifier after enough real data exists.
