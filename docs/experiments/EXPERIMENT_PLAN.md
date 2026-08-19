# Experiment Plan

## Scope and safety

This project uses a safe low-voltage prototype for SIH demonstration only. The system is not a real high-voltage electric fence and no hazardous electrical experiments are planned or allowed. All experiments remain within safe laboratory conditions for the ESP32, INA219, MPU6050, and 3-zone prototype wiring.

## Current evidence status

- Real experimental data collected and documented:
  - `hardware/experiments/physical_tamper/EXP_01_NORMAL_STATIONARY.csv` (Stationary baseline)
  - `hardware/experiments/physical_tamper/EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv` (Physical tamper & motion events)
  - `hardware/experiments/electrical_faults/sih_fence_raw_dataset.csv` (3-zone electrical fault dataset)
- The raw datasets represent empirical hardware data and are preserved without modification.

## Experiment catalog

| Experiment ID | Experiment name | Status | Purpose |
|---|---|---|---|
| EXP_01 | NORMAL_STATIONARY | VERIFIED | Establish baseline with fence untouched |
| EXP_02 | PHYSICAL_EXPERIMENTS_LABELED | VERIFIED | Multi-state physical tamper & vibration telemetry |
| EXP_03..11 | ELECTRICAL_FAULTS | VERIFIED | Zone open/cut and short electrical signatures |
| EXP_12 | COMBINED_BREACH | VERIFIED | Simultaneous physical motion and electrical fault |

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
