# Experiment Plan

## Scope and safety

This project uses a safe low-voltage prototype for SIH demonstration only. The system is not a real high-voltage electric fence and no hazardous electrical experiments are planned or allowed. All experiments remain within safe laboratory conditions for the ESP32, INA219, MPU6050, and 3-zone prototype wiring.

## Current evidence status

- Real experimental data already exists for: `EXP_01_NORMAL_STATIONARY.csv`
- The raw file is stored at: `data/raw/tamper_experiments/EXP_01_NORMAL_STATIONARY.csv`
- The dataset is treated as real collected hardware data and has not been modified.
- The raw CSV currently exports a trailing label value on each observation row, rather than a separate `label` header column. This is preserved as a real export quirk and is not rewritten.
- The future experiments below are documented as templates only and not generated as CSV files in this repository.

## Experiment catalog

| Experiment ID | Experiment name | Status | Purpose |
|---|---|---|---|
| EXP_01 | NORMAL_STATIONARY | DONE / VERIFIED | Establish baseline with fence untouched |
| EXP_02 | LIGHT_VIBRATION | PENDING | Capture natural movement / low-level vibration |
| EXP_03 | PHYSICAL_TAMPER | PENDING | Realistic physical pushing or manipulation |
| EXP_04 | REPEATED_TAMPER | PENDING | Repeated movement to assess persistence |
| EXP_05 | STRONG_TAMPER | PENDING | Stronger motion within safe prototype limits |
| EXP_06 | ZONE1_OPEN | PENDING | Zone 1 open/cut electrical behavior |
| EXP_07 | ZONE2_OPEN | PENDING | Zone 2 open/cut electrical behavior |
| EXP_08 | ZONE3_OPEN | PENDING | Zone 3 open/cut electrical behavior |
| EXP_09 | ZONE1_SHORT | PENDING | Zone 1 short electrical behavior |
| EXP_10 | ZONE2_SHORT | PENDING | Zone 2 short electrical behavior |
| EXP_11 | ZONE3_SHORT | PENDING | Zone 3 short electrical behavior |
| EXP_12 | COMBINED_BREACH | PENDING | Physical tamper + electrical fault combined scenario |

## EXP_01_NORMAL_STATIONARY

Status: DONE / VERIFIED

Description:
- Fence untouched
- Establishes baseline for stationary operation
- Confirms sensor behavior under zero-motion conditions

Evidence:
- Raw file exists in `data/raw/tamper_experiments/EXP_01_NORMAL_STATIONARY.csv`
- Schema includes `timestamp_ms`, zone voltages, bus voltage, current, power, `ax`, `ay`, `az`, `gx`, `gy`, `gz`, and `label`

## EXP_02_LIGHT_VIBRATION

Status: PENDING

Objective:
- Record approximately 10 seconds of untouched baseline
- Apply controlled light vibration for approximately 5 seconds
- Stop the disturbance
- Record another approximately 10 seconds of quiet behavior

Required capture:
- Save as `EXP_02_LIGHT_VIBRATION.csv`
- Use same schema as the raw tamper experimental data
- Keep original raw values without synthetic modification

Procedure:
1. Start logging.
2. Record approximately 10 seconds untouched.
3. Apply controlled light vibration to the fence/post for about 5 seconds.
4. Stop the vibration.
5. Record approximately 10 more seconds.
6. Save the final CSV.

## EXP_03_PHYSICAL_TAMPER

Status: PENDING

Objective:
- Capture realistic physical manipulation of the prototype fence
- Observe motion and electrical context together
- Build examples of physical tamper for later fusion analysis

Procedure:
- Use low-force, controlled motion within prototype limits.
- Ensure the event is safe and repeatable.
- Record the full sensor stream before, during, and after the event.

## EXP_04_REPEATED_TAMPER

Status: PENDING

Objective:
- Capture repeated physical disturbance events
- Determine if repeated movement creates a distinct temporal pattern

## EXP_05_STRONG_TAMPER

Status: PENDING

Objective:
- Apply stronger motion within safe prototype limits
- Measure the dynamic range of the MPU6050 during clear physical disturbance

## EXP_06 to EXP_11: electrical fault experiments

Status: PENDING

Purpose:
- Confirm per-zone electrical signatures for open and short faults
- Preserve the current proven electrical detection behavior
- Use the same 3-zone architecture and safe low-voltage conditions

Files to create when performed:
- `EXP_06_ZONE1_OPEN.csv`
- `EXP_07_ZONE2_OPEN.csv`
- `EXP_08_ZONE3_OPEN.csv`
- `EXP_09_ZONE1_SHORT.csv`
- `EXP_10_ZONE2_SHORT.csv`
- `EXP_11_ZONE3_SHORT.csv`

## EXP_12_COMBINED_BREACH

Status: PENDING

Objective:
- Capture a combined event where physical disturbance and electrical fault overlap
- Provide examples for breach classification in the sensor-fusion pipeline

## Template for future experiment records

Each new experiment should include:

- experiment_id
- timestamp_ms
- zone1_v
- zone2_v
- zone3_v
- bus_voltage_v
- current_ma
- power_mw
- ax
- ay
- az
- gx
- gy
- gz
- label
- notes

Important rule:
- Do not create synthetic experimental datasets.
- Only add the documentation template until the real hardware experiment has been performed.

## TODO

- [TODO] Collect EXP_02_LIGHT_VIBRATION raw data.
- [TODO] Collect EXP_03_PHYSICAL_TAMPER raw data.
- [TODO] Collect EXP_04_REPEATED_TAMPER raw data.
- [TODO] Collect EXP_05_STRONG_TAMPER raw data.
- [TODO] Collect EXP_06-11 electrical fault datasets.
- [TODO] Collect EXP_12_COMBINED_BREACH raw data.
- [TODO] Train and validate the sensor-fusion baseline model once enough real data exists.
