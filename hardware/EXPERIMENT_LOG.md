# Hardware Experiment Log
## FENCEGUARD-X Electrical & Tamper Detection Validation

---

## PHASE 1 — 3-Zone Electrical Detection

### Objective
Validate electrical integrity monitoring for three independent fence zones. Test all combinations of zone conditions (NORMAL, OPEN/CUT, SHORT) to achieve 100% fault detection and localization.

### Date Conducted
17 August 2026

### Tested Conditions

| Zone | NORMAL | OPEN/CUT | SHORT |
|------|--------|----------|-------|
| Zone 1 | ✅ PASS | ✅ PASS | ✅ PASS |
| Zone 2 | ✅ PASS | ✅ PASS | ✅ PASS |
| Zone 3 | ✅ PASS | ✅ PASS | ✅ PASS |

**Total Test Cases**: 9  
**Passed**: 9  
**Failed**: 0  
**Success Rate**: 100%

### Sensors & Components

| Component | Model | Purpose | Status |
|-----------|-------|---------|--------|
| Microcontroller | ESP32 DevKit | Main processing, ADC, I2C | ✅ Working |
| Voltage Sensing | GPIO 34, 35, 32 | Zone voltage acquisition (ADC) | ✅ Working |
| Zone Detection | End-of-line resistors (1kΩ + 470Ω) | Electrical integrity via voltage divider | ✅ Working |
| Power Monitor | INA219 I2C Sensor | Bus voltage, current, power | ✅ Working |
| Communication | UART Serial (115200 baud) | Data output & debugging | ✅ Working |

### Observed Voltage Signatures

**NORMAL STATE** (Load connected, circuit intact):
- Zone voltage: 1.3–1.6 V
- Cause: Voltage divider (R1 1kΩ, R2 470Ω zone load)
- Detection method: Threshold 1.0–1.8V
- Status: ✅ Reliable, consistent across all 26 measurements

**OPEN/CUT STATE** (Load disconnected, circuit broken):
- Zone voltage: ~3.30 V (approaches bus voltage)
- Cause: Load resistance infinite, all current flows through R1
- Detection method: Threshold > 2.5V
- Status: ✅ Reliable, high signal-to-noise ratio

**SHORT STATE** (Load short-circuited to ground):
- Zone voltage: ~0.00 V (near ground)
- Cause: Load resistance near 0Ω, voltage divider shows R2 shorted
- Detection method: Threshold < 0.5V
- Status: ✅ Reliable, clear distinction from other states

**These are experimental prototype observations and are NOT universal thresholds.**
**Voltage signatures may vary based on:**
- R1 and R2 resistor values
- ADC calibration
- Load impedance characteristics
- Environmental conditions (temperature, humidity)

### INA219 Power Sensor

**Sensor Specifications**:
- Address: 0x40 (I2C)
- Bus Voltage Range: 0–26V (±1% accuracy)
- Current Shunt: ±3.2A (±0.5% accuracy)
- Power Calculation: P = V × I

**Typical Prototype Measurements**:

| Metric | Min | Typical | Max | Unit |
|--------|-----|---------|-----|------|
| Bus Voltage | 2.8 | 3.3 | 3.4 | V |
| Current | 60 | 105 | 130 | mA |
| Power | 200 | 330 | 440 | mW |

**Data Quality Notes**:
- 22 out of 26 samples (85%) show valid measurements → labeled **MEASURED**
- 4 out of 26 samples (15%) show bus_voltage = 0.000V → labeled **IMPUTED_BUS_VOLTAGE**
  - Cause: Loose I2C/power connections (hardware issue, not sensor failure)
  - Action: Connection tightened, subsequent measurements normal
  - Handling: These 4 samples included in dataset with data_quality flag for ML transparency

### Detection Accuracy

**False Positive Rate**: 0%  
- No NORMAL zones incorrectly classified as OPEN/SHORT
- No false alarms reported in any of 26 samples

**False Negative Rate**: 0%  
- No faulty zones missed (all 11 OPEN/CUT detected)
- No SHORT states missed (all 12 SHORT detected)
- No multi-fault missed (MULTI_FAULT sample detected)

**Fault Localization Accuracy**: 100%  
- System correctly identified which zone(s) were faulty
- Multi-fault support validated (2+ zones faulty simultaneously, sample 24)

### Zone Voltage Distribution

```
NORMAL:       1.3–1.6V    [█████████░] Tight cluster, low variance
OPEN/CUT:     ~3.30V      [█░░░░░░░░] Single peak, near 3.3V
SHORT:        ~0.00V      [░░░░░░░░█] Single peak, near 0V

Clear separation between states → High classification confidence
```

### Sample Data from Experiment

| Sample | Z1 (V) | Z2 (V) | Z3 (V) | Bus (V) | Curr (mA) | Pow (mW) | Condition | Fault Zone | Status |
|--------|--------|--------|--------|---------|-----------|----------|-----------|-----------|--------|
| 1 | 1.45 | 1.50 | 1.48 | 3.3 | 105 | 347 | NORMAL | NONE | ✅ OK |
| 2 | 1.52 | 1.55 | 1.50 | 3.3 | 108 | 356 | NORMAL | NONE | ✅ OK |
| 3 | 1.48 | 3.30 | 1.52 | 3.2 | 85 | 272 | OPEN_CUT | ZONE2 | ✅ OK |
| 7 | 0.02 | 1.50 | 1.48 | 3.3 | 110 | 363 | SHORT | ZONE1 | ✅ OK |
| 24 | 3.30 | 0.00 | 1.50 | 3.0 | 109 | 314 | MULTI_FAULT | Z1_OPEN_Z2_SHORT | ✅ OK |

**See ml/dataset/raw/sih_fence_raw_dataset.csv for complete 26-sample dataset.**

### Multi-Fault Testing

**Objective**: Validate system behavior when 2+ zones are faulty simultaneously

**Test Case**: Zone 1 OPEN + Zone 2 SHORT + Zone 3 NORMAL

**Expected Behavior**:
- Detect Zone 1 open circuit (voltage ~3.3V)
- Detect Zone 2 short circuit (voltage ~0V)
- Confirm Zone 3 intact (voltage ~1.5V)
- System state → CRITICAL (2+ faults)
- Action → Isolate power (relay cut)

**Observed Behavior**: ✅ **EXACT MATCH** (Sample 24 in dataset)
- Zone 1 voltage: 3.30V → Correctly identified as OPEN
- Zone 2 voltage: 0.00V → Correctly identified as SHORT
- Zone 3 voltage: 1.50V → Correctly identified as NORMAL
- System classification: CRITICAL (correct)

**Confidence Score**: 100%

---

## PHASE 2 — Physical Tamper/Movement Detection

### Status
**🟡 IN PROGRESS**

### Objective
Detect physical fence movement, vibration, or deliberate manipulation attempts even when electrical integrity remains normal. Provides additional security layer beyond electrical sensing.

### Planned Approach

1. **Sensor Selection** (17-AUG, PENDING)
   - Candidates: ADXL345 accelerometer, vibration sensor, strain gauge
   - Decision required: Anup (IoT Lead)
   - Criteria: I2C compatibility, low power, accurate frequency response (0.1–5Hz)

2. **Hardware Integration** (18-AUG)
   - Mount physical sensor on fence structure
   - Connect to ESP32 via I2C or GPIO
   - Test sensor responsiveness

3. **Baseline Collection** (18-AUG)
   - Record sensor readings for normal fence conditions
   - Establish noise floor and sensitivity thresholds
   - Document baseline patterns

4. **Tamper Data Collection** (18-AUG)
   - Simulate common attack patterns:
     - Climbing (0.5–2 Hz movements)
     - Cutting/sawing (3–5 Hz vibrations)
     - Deliberate shaking (1–3 Hz)
   - Record sensor response to each attack type
   - Build tamper signature database

5. **Sensor Fusion Integration** (18-AUG)
   - Combine electrical evidence (zone states)
   - Add physical evidence (accelerometer/vibration)
   - Implement confidence scoring:
     - Electrical fault + physical tamper → CRITICAL
     - Electrical fault only → ALERT
     - Physical tamper only → ALERT
     - Neither → NORMAL

6. **Testing & Validation** (19-AUG)
   - Test hybrid detection logic
   - Verify low false positive rate
   - Demo for judges (20-AUG)

### Next Steps

- [ ] **TODAY (17-AUG)**: Anup finalizes physical sensor selection
- [ ] **18-AUG**: Integrate selected sensor with firmware
- [ ] **18-AUG**: Collect baseline and tamper data
- [ ] **18-AUG**: Implement sensor fusion in firmware
- [ ] **19-AUG**: Full system testing and demo rehearsal

---

## PHASE 3 — ML Model Integration (Future)

### Objective
Train machine learning models to recognize electrical fault patterns and improve classification confidence beyond rule-based thresholds.

### Planned Approach

1. **Feature Engineering**
   - Zone voltage RMS values
   - Current/power patterns
   - Temporal changes (rate-of-change)
   - Multi-zone correlation

2. **Baseline Models** (Priyada, 18-AUG)
   - Decision Tree (simple, interpretable)
   - Random Forest (robust, better accuracy)
   - Logistic Regression (baseline)

3. **Model Evaluation**
   - Accuracy, precision, recall, F1-score
   - Confusion matrix analysis
   - Feature importance ranking

4. **Model Deployment**
   - Convert to TensorFlow Lite
   - Optimize for ESP32 inference (<50ms latency)
   - Store in SPIFFS (< 1MB)
   - Integrate with firmware inference pipeline

5. **Performance Target**
   - Model accuracy: >85% (on 26-sample validation set)
   - Inference time: <50ms per sample
   - Memory footprint: <1MB

---

## SAFETY & DISCLAIMER

### ⚠️ IMPORTANT

This is a **SAFE LOW-VOLTAGE PROTOTYPE** for demonstration and research purposes only.

**Voltage & Current Levels** (All Safe):
- Zone voltages: 0–3.3V (safe to touch)
- Bus voltage: ~3.3V (safe to touch)
- Current draw: <200mA (safe, no burn risk)
- Total power: <500mW (minimal heat generation)

**NOT Suitable For**:
- Real high-voltage electric fence deployment
- Production animal containment systems
- Any application with AC power or >50V
- Use without professional electrical engineering review

**Required Before Real-World Use**:
- Professional electrical certification
- High-voltage component selection and testing
- Fault isolation and protection circuits
- Proper grounding and earthing
- Safety interlocks and emergency procedures
- Regulatory compliance review

---

## DATASET

### Location
`ml/dataset/raw/sih_fence_raw_dataset.csv`

### Contents
26 real experimental samples collected during Phase 1 validation.

### Data Quality
- **MEASURED**: 22 samples (85%) — Valid sensor readings
- **IMPUTED**: 4 samples (15%) — Bus voltage imputed due to loose connections

### Usage
- ML training (Priyada, 18-AUG)
- Baseline model evaluation
- Feature importance analysis
- Confusion matrix generation

---

## EXPERIMENTAL VALIDATION SUMMARY

| Item | Target | Achieved | Status |
|------|--------|----------|--------|
| Zone 1 NORMAL detection | ✅ | ✅ | PASS |
| Zone 1 OPEN/CUT detection | ✅ | ✅ | PASS |
| Zone 1 SHORT detection | ✅ | ✅ | PASS |
| Zone 2 NORMAL detection | ✅ | ✅ | PASS |
| Zone 2 OPEN/CUT detection | ✅ | ✅ | PASS |
| Zone 2 SHORT detection | ✅ | ✅ | PASS |
| Zone 3 NORMAL detection | ✅ | ✅ | PASS |
| Zone 3 OPEN/CUT detection | ✅ | ✅ | PASS |
| Zone 3 SHORT detection | ✅ | ✅ | PASS |
| Multi-fault detection | ✅ | ✅ | PASS |
| **OVERALL ACCURACY** | **>90%** | **100%** | **🏆 EXCEEDS TARGET** |

---

**Experiment Log Last Updated**: 17 August 2026, Evening  
**Next Review**: 18 August 2026, 18:00 (Feature Freeze)  
**Status**: ✅ PHASE 1 COMPLETE, PHASE 2 IN PROGRESS
