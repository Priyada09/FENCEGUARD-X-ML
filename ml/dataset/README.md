# ML Dataset Documentation

## Overview

This directory contains the experimental dataset collected from FENCEGUARD-X hardware prototype testing.

**Dataset File**: `raw/sih_fence_raw_dataset.csv`

---

## Data Source

**Collection Method**: Experimental testing on safe low-voltage prototype  
**Hardware Platform**: ESP32 + INA219 current sensor  
**Collection Date**: August 2026  
**Number of Samples**: 26 records  
**Zones**: 3 independent electrical zones  

---

## Experimental Setup

### Hardware Configuration

- **Microcontroller**: ESP32
- **Current/Power Sensor**: INA219 (I2C, ±3.2A range)
- **Voltage Measurement**: ADC input with voltage divider
- **Fence Simulation**: Low-voltage load (safe demonstration only)
- **Zone Integrity Sensing**: EOL (End-of-Line) resistor method per zone

### Test Conditions

- **Bus Voltage Range**: 3.0–3.4 V (prototype safe operating range)
- **Current Range**: 80–125 mA (typical load)
- **Power Range**: 250–420 mW (calculated)
- **Sampling Frequency**: 10 ms intervals
- **Environmental**: Indoor lab, controlled conditions

### Important Safety Note

⚠️ **This is a SAFE LOW-VOLTAGE PROTOTYPE** — NOT a real high-voltage electric fence.
- All voltages < 4V
- All currents < 200 mA
- Safe to touch, no electrical hazard
- Designed for proof-of-concept validation only

---

## Dataset Columns

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| `sample_id` | Integer | — | Unique sample identifier (1–26) |
| `zone1_voltage_v` | Float | Volts | Measured voltage on Zone 1 |
| `zone2_voltage_v` | Float | Volts | Measured voltage on Zone 2 |
| `zone3_voltage_v` | Float | Volts | Measured voltage on Zone 3 |
| `bus_voltage_v` | Float | Volts | Main bus voltage (from INA219) |
| `current_ma` | Float | Milliamps | Total system current |
| `power_mw` | Float | Milliwatts | Calculated power (V × I) |
| `condition` | String | — | Fault condition state |
| `fault_zone` | String | — | Zone(s) affected, or "NONE" for normal |
| `data_quality` | String | — | Measurement type (MEASURED or IMPUTED) |

---

## Condition Classes

### NORMAL
- All zones operating at nominal voltage (~1.3–1.6 V each)
- Electrical circuit intact
- No anomalies detected
- **Samples**: 1, 2

### OPEN_CUT
- One or more zones show elevated voltage (~3.30 V)
- Indicates open circuit / wire cut in affected zone
- Other zones remain normal
- **Samples**: 3–6, 15–22, 25–26

### SHORT
- One or more zones show near-zero voltage (~0.00 V)
- Indicates short circuit in affected zone
- **Samples**: 7–14, 23

### MULTI_FAULT
- Multiple zones affected simultaneously
- Example: Zone 1 OPEN_CUT + Zone 2 SHORT
- **Samples**: 24

---

## Fault Zone Localization

The system successfully localizes which zone(s) contain the fault:

| Condition | Zone 1 | Zone 2 | Zone 3 | Fault Zone |
|-----------|--------|--------|--------|-----------|
| NORMAL | ~1.5V | ~1.5V | ~1.5V | NONE |
| OPEN_CUT | ~3.30V | ~1.5V | ~1.5V | ZONE1 |
| OPEN_CUT | ~1.5V | ~3.30V | ~1.5V | ZONE2 |
| OPEN_CUT | ~1.5V | ~1.5V | ~3.30V | ZONE3 |
| SHORT | ~0.00V | ~1.5V | ~1.5V | ZONE1 |
| SHORT | ~1.5V | ~0.00V | ~1.5V | ZONE2 |
| SHORT | ~1.5V | ~1.5V | ~0.00V | ZONE3 |
| MULTI_FAULT | ~3.30V | ~0.00V | ~1.5V | ZONE1_OPEN_ZONE2_SHORT |

---

## Data Quality & Imputation

### MEASURED Rows
- Directly acquired from sensors
- No preprocessing applied
- Full confidence in accuracy

### IMPUTED_BUS_VOLTAGE Rows
- **Reason**: Some original readings showed `bus_voltage = 0.000 V`
- **Root Cause**: Identified as loose connections in prototype wiring, NOT sensor failure
- **Action Taken**: Bus voltage values imputed using regression or contextual average
- **Impact**: Zone voltage readings are valid; bus voltage should be treated with caution
- **Rows Affected**: 6, 16, 17, 22, 24, 26

**Important**: Do NOT use IMPUTED_BUS_VOLTAGE rows for direct sensor validation during baseline ML training. Separate them for preprocessing pipeline testing instead.

---

## Observed Signature Thresholds

**CAUTION**: These are EXPERIMENTALLY OBSERVED values on a low-voltage prototype. They are NOT universal thresholds applicable to real commercial electric fences.

### Zone Voltage Signatures (Prototype-Specific)

| Condition | Zone Voltage | Notes |
|-----------|--------------|-------|
| **NORMAL** | 1.3–1.6 V | Varies by zone wiring resistance |
| **OPEN_CUT** | ~3.30 V (elevated) | Near bus voltage, indicates loss of load |
| **SHORT** | ~0.00 V (near ground) | Indicates direct short to ground |

### Bus Voltage

- **Normal Operation**: 3.2–3.4 V (safe lab supply)
- **Never**: 0–1 V under normal load conditions

### Current & Power

- **Normal Load**: 80–125 mA, 250–420 mW
- **Varies by**: Zone count, wiring length, load resistance

---

## Dataset Limitations

1. **Small Size**: Only 26 samples (lab conditions)
   - Insufficient for production ML model
   - Suitable for proof-of-concept baseline

2. **Single Environment**: 
   - Indoor, controlled lab setup
   - No environmental variation (temperature, humidity, noise)
   - No real-world interference

3. **Single Prototype Instance**:
   - One ESP32, one INA219 unit
   - No validation across hardware variations

4. **Synthetic Faults**:
   - Faults manually introduced for testing
   - Not observing naturally occurring degradation

5. **No Physical Tamper Data**:
   - This dataset is ELECTRICAL FAULT ONLY
   - Physical tamper/movement sensor data to be added in Phase 2

---

## Data Processing Pipeline

### Phase 1 (Current): Raw Exploration
```
raw/sih_fence_raw_dataset.csv
    ↓
[Load & Inspect]
    ↓
[Separate MEASURED vs IMPUTED]
    ↓
[EDA & Visualization]
    ↓
[Baseline ML Training]
```

### Phase 2 (Planned): Feature Engineering
```
[Feature extraction: RMS, peak, variance]
    ↓
[Normalization / Standardization]
    ↓
processed/sih_fence_processed.csv
```

### Phase 3 (Planned): Model Training
```
[Train-test split]
    ↓
[Baseline models: Decision Tree, Random Forest, Logistic Regression]
    ↓
[Evaluate: Accuracy, Precision, Recall, F1, Confusion Matrix]
    ↓
models/baseline_model.pkl
models/model_v1.tflite
```

---

## How to Use This Dataset

### For EDA (Exploratory Data Analysis)
```python
import pandas as pd

df = pd.read_csv('raw/sih_fence_raw_dataset.csv')
print(df.head())
print(df.describe())
print(df['condition'].value_counts())

# Separate measured vs imputed
measured = df[df['data_quality'] == 'MEASURED']
imputed = df[df['data_quality'] == 'IMPUTED_BUS_VOLTAGE']
```

### For Baseline Model Training
```python
# Features
X = df[['zone1_voltage_v', 'zone2_voltage_v', 'zone3_voltage_v', 
         'bus_voltage_v', 'current_ma', 'power_mw']]

# Label
y = df['condition']  # NORMAL, OPEN_CUT, SHORT, MULTI_FAULT

# Train
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)
```

### For Fault Zone Localization
```python
# Predict which zone is faulty
y_zone = df['fault_zone']  # NONE, ZONE1, ZONE2, ZONE3, ZONE1_OPEN_ZONE2_SHORT, etc.
```

---

## Future Phases

### Phase 2: Physical Tamper Dataset
- Accelerometer / vibration sensor data
- Fence movement patterns
- Environmental disturbance patterns
- ML integration for multimodal detection

### Phase 3: Extended Collection
- Longer time periods
- Environmental variation
- Hardware degradation patterns
- Real-world deployment data (if applicable)

---

## Reproducibility & Citation

To reference this dataset in reports:

```
FENCEGUARD-X Electrical Fault Dataset v1.0
Smart India Hackathon 2026, Internal Round
Collected: August 2026
Hardware: ESP32 + INA219 Prototype
Safe Low-Voltage Lab Demonstration
```

---

## Contact & Questions

**Dataset Owner**: Priyada (ML Lead)  
**Hardware Owner**: Anup (IoT & Automation Lead)  
**Firmware Owner**: Jayesh (Firmware Lead)  

For dataset questions, corrections, or additional samples, please contact the team via GitHub issues.

---

**Last Updated**: August 17, 2026  
**Repository**: patilanup421-pixel/SIH-2026
