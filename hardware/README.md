# Hardware Documentation

## Overview

FENCEGUARD-X hardware prototype demonstrates **safe low-voltage, 3-zone electrical fault detection** using ESP32 and INA219 power sensor. This is a **proof-of-concept lab demonstration**, not a real high-voltage electric fence.

**Current Status** ✅ **PHASE 1 COMPLETE**:
- 3-zone electrical integrity sensing validated
- INA219 bus voltage/current/power measurement working
- 26-sample experimental dataset collected
- 100% fault detection accuracy across 9-state electrical matrix
- Prototype ready for Phase 2 (physical tamper sensor integration)

---

## ⚠️ SAFETY DISCLAIMER

**This is a SAFE LOW-VOLTAGE DEMONSTRATION**
- All voltages: < 4V
- All currents: < 200 mA  
- Safe to touch, no electrical hazard
- Indoor lab testing only
- NOT suitable for real electric fence deployment without professional electrical engineering review

---

## Hardware Components

### 1. Microcontroller

| Component | Specification | Purpose |
|-----------|----------------|---------|
| **ESP32 DevKit** | Dual-core 240MHz, 520KB RAM, 4MB Flash | Main controller, sensor acquisition, decision logic |
| **USB-Serial** | CH340 or FTDI | Programming and serial monitoring |

**Pinout Configuration**:
```
ESP32 Pin  | Function           | External Connection
-----------|-------------------|--------------------
GPIO32     | Zone 1 ADC        | Voltage sensor 1
GPIO33     | Zone 2 ADC        | Voltage sensor 2
GPIO34     | Zone 3 ADC        | Voltage sensor 3
GPIO21     | I2C SDA           | INA219 data line
GPIO22     | I2C SCL           | INA219 clock line
GPIO25     | LED Green         | Status (normal)
GPIO26     | LED Yellow        | Status (alert)
GPIO27     | LED Red           | Status (critical)
GPIO14     | Buzzer            | Audible alert
GPIO22     | Relay Control     | Power isolation

GND        | Common Ground     | All sensors
3V3        | Power Supply      | All sensors
```

### 2. Electrical Fault Detection

#### Zone Voltage Sensors (3 independent)

Each zone has **End-of-Line (EOL) resistor-based integrity sensing**:

**Circuit per Zone**:
```
    +3.3V (from ESP32 supply)
      |
      R1 (1kΩ)
      |
    +----- ADC GPIO (to ESP32)
      |
      R2 (EOL resistor, zone-dependent)
      |
    [ZONE LOAD]
      |
     GND

Expected voltages (with typical load):
- Normal operation: 1.3–1.6V at ADC
- Open/cut (R2 open): ~3.3V at ADC
- Short (R2 short): ~0.0V at ADC
```

**Zone Components**:
| Zone | R1 (Ω) | R2 EOL (Ω) | Load | Expected Normal Voltage |
|------|--------|------------|------|------------------------|
| Zone 1 | 1k | 470Ω | Load 1 | ~1.5V |
| Zone 2 | 1k | 470Ω | Load 2 | ~1.5V |
| Zone 3 | 1k | 470Ω | Load 3 | ~1.5V |

**Fault Signatures** (Experimentally Observed):
| Condition | Voltage | Reason |
|-----------|---------|--------|
| NORMAL | 1.3–1.6V | Voltage divider working, load drawing current |
| OPEN/CUT | ~3.30V | EOL resistor open, ADC reads full supply (through R1) |
| SHORT | ~0.00V | Zone shorted to ground, ADC reads near 0V |

### 3. INA219 Power Sensor

**Sensor**: Texas Instruments INA219 (16-bit, I2C)

**Connections**:
```
INA219 Pin  | ESP32 Connection
------------|------------------
VCC (3V3)   | 3V3 (through decoupling cap 100nF)
GND         | GND
SDA         | GPIO21
SCL         | GPIO22
A0, A1      | GND (Address: 0x40)

IN+ / IN-   | Shunt resistor (10mΩ or 100mΩ)
Shunt       | Between power and load
```

**Measurements**:
- **Bus Voltage**: Measures main supply voltage (0–26V range, prototype: 3.0–3.4V)
- **Current**: Through integrated shunt amplifier (±3.2A range with appropriate shunt)
- **Power**: Calculated (P = V × I)
- **Accuracy**: ±1% voltage, ±0.5% current

**I2C Communication**:
```
Device Address: 0x40 (when A0, A1 tied to GND)
Bus Speed: 400 kHz (standard I2C fast mode)
Registers: Standard INA219 register map
```

### 4. Relay Control (Safety Isolation)

**Relay Module**:
```
GPIO22 (ESP32)
  |
  └─── Relay Driver Transistor
         |
         └─── Relay Coil (5V logic)
                |
                ├─ Normally Open (NO) contacts
                └─ Normally Closed (NC) contacts
```

**Behavior**:
- **GPIO22 = HIGH**: Relay energized, contacts close → **Power ON**
- **GPIO22 = LOW**: Relay de-energized, contacts open → **Power CUT**

**Debouncing**:
```
When CRITICAL condition detected:
  1. Cut relay immediately
  2. Wait 5 seconds (cooldown)
  3. Re-enable only if system returns to NORMAL
  4. Prevent rapid cycling (relay wear prevention)
```

### 5. Status Indicators

#### LEDs
| LED | Color | GPIO | Meaning |
|-----|-------|------|---------|
| LED1 | Green | GPIO25 | System NORMAL, all zones OK |
| LED2 | Yellow | GPIO26 | ALERT, electrical fault detected, monitoring |
| LED3 | Red | GPIO27 | CRITICAL, relay cut, immediate action needed |

#### Buzzer
| Condition | Sound | GPIO |
|-----------|-------|------|
| NORMAL | OFF | GPIO14 |
| ALERT | Short beep (0.5s) every 60s | GPIO14 PWM |
| CRITICAL | Continuous (3s on, 1s off) | GPIO14 PWM |

---

## Prototype Assembly

### BOM (Bill of Materials)

| Component | Qty | Cost (Approx) | Supplier |
|-----------|-----|---------------|----------|
| ESP32 DevKit | 1 | $10 | Amazon, Aliexpress |
| INA219 I2C Module | 1 | $3 | Amazon, Aliexpress |
| Resistor 1kΩ (1/4W) | 6 | $0.10 | Any electronics distributor |
| Resistor 470Ω (1/4W) | 3 | $0.10 | Any electronics distributor |
| Relay Module (5V) | 1 | $3 | Amazon, Aliexpress |
| LED Green (3mm) | 1 | $0.20 | Any electronics distributor |
| LED Yellow (3mm) | 1 | $0.20 | Any electronics distributor |
| LED Red (3mm) | 1 | $0.20 | Any electronics distributor |
| Buzzer (5V, passive) | 1 | $1 | Amazon, Aliexpress |
| Breadboard (830 tie-points) | 1 | $5 | Amazon |
| Jumper wires (M-M, F-F) | Assorted | $3 | Amazon |
| USB Cable (Type-B micro) | 1 | $2 | Any electronics distributor |
| **TOTAL** | | **~$30** | |

### Breadboard Layout

```
[Breadboard schematic diagram to be added]

Key Connections:
1. ESP32 GPIO32/33/34 → Zone voltage dividers (R1 + R2)
2. ESP32 GPIO21/22 → INA219 (I2C SDA/SCL)
3. INA219 → Shunt resistor → Load → GND
4. ESP32 GPIO25/26/27 → LEDs (with 220Ω current limiting)
5. ESP32 GPIO14 → Buzzer (through transistor driver)
6. ESP32 GPIO22 → Relay coil (through TIP31 transistor)
7. Relay NO contacts → Fence load power path
8. All grounds connected to single point (star configuration)
```

### Testing Procedure

#### Phase 1: Power-On Self-Test
```
1. Connect USB cable to ESP32
2. Monitor serial output (115200 baud)
3. Verify startup messages:
   [SYSTEM] Starting FENCEGUARD-X
   [ADC] Initializing channels... OK
   [I2C] INA219 connected... OK
4. LED Green should illuminate
```

#### Phase 2: Zone Voltage Verification
```
For each zone (Zone 1, 2, 3):

NORMAL state:
  1. Connect zone load to zone circuit
  2. Power on
  3. Check serial: Zone voltage ~1.3–1.6V
  4. Expected: LED Green

OPEN state:
  1. Disconnect zone load (simulate cut)
  2. Check serial: Zone voltage ~3.3V
  3. Expected: LED Yellow, ALERT event

SHORT state:
  1. Short zone output to GND (simulate short)
  2. Check serial: Zone voltage ~0.0V
  3. Expected: LED Red, CRITICAL event, relay cuts
```

#### Phase 3: INA219 Verification
```
1. Connect power supply to load circuit
2. Read serial output:
   Bus Voltage: 3.2–3.4V
   Current: 80–130 mA
   Power: 250–420 mW
3. Verify values match multimeter readings (±2% tolerance)
```

#### Phase 4: Relay & Isolation
```
1. Set system to CRITICAL condition (short zone)
2. Verify relay clicks (audible/visual)
3. Verify:
   - LED Red illuminated
   - Buzzer continuous sound
   - Power path interrupted (load voltage drops to 0)
4. Manual reset button (if implemented)
```

#### Phase 5: Multi-Fault Detection
```
1. Simultaneously fault two zones:
   - Zone 1: OPEN (3.3V)
   - Zone 2: SHORT (0.0V)
   - Zone 3: NORMAL (1.5V)
2. Verify serial output: "MULTI_FAULT detected"
3. Verify critical relay action triggered
```

---

## Experimental Validation Results

### Test Matrix (All 9 Combinations)

| # | Zone 1 | Zone 2 | Zone 3 | Expected State | Observed | Confidence |
|---|--------|--------|--------|----------------|----------|------------|
| 1 | NORMAL | NORMAL | NORMAL | NORMAL | ✅ PASS | 100% |
| 2 | OPEN | NORMAL | NORMAL | ALERT (Z1) | ✅ PASS | 100% |
| 3 | SHORT | NORMAL | NORMAL | CRITICAL (Z1) | ✅ PASS | 100% |
| 4 | NORMAL | OPEN | NORMAL | ALERT (Z2) | ✅ PASS | 100% |
| 5 | NORMAL | SHORT | NORMAL | CRITICAL (Z2) | ✅ PASS | 100% |
| 6 | NORMAL | NORMAL | OPEN | ALERT (Z3) | ✅ PASS | 100% |
| 7 | NORMAL | NORMAL | SHORT | CRITICAL (Z3) | ✅ PASS | 100% |
| 8 | OPEN | SHORT | NORMAL | CRITICAL (Z1+Z2) | ✅ PASS | 100% |
| 9 | NORMAL | NORMAL | NORMAL | NORMAL (Repeat) | ✅ PASS | 100% |

**Overall Accuracy**: 100% (9/9 correct)  
**False Positives**: 0  
**False Negatives**: 0

### Dataset Collected

**File**: `ml/dataset/raw/sih_fence_raw_dataset.csv`

**Statistics**:
- Total samples: 26
- Measured: 22 (85%)
- Imputed (bus voltage): 4 (15%)
- Normal state: 2 samples
- Open faults: 11 samples (44%)
- Short faults: 12 samples (46%)
- Multi-fault: 1 sample (4%)

---

## Phase 2: Physical Tamper Detection (PLANNED)

**Timeline**: 17–18 AUG 2026

**Objective**: Add hardware to detect physical fence manipulation (climbing, pushing, vibration)

**Sensor Candidates**:
1. **Accelerometer (ADXL345)**: I2C, detects acceleration (gravity + movement)
2. **Vibration Sensor**: Passive or analog, detects resonance
3. **Strain Gauge**: Detects bending force (for climbing)

**Selection Criteria**:
- Cost: < $10
- Power: < 50 mA
- Interface: I2C or analog input
- Weather resistance: Sealed enclosure compatible

**Planned Integration**:
```
Accelerometer (I2C)
  |
  └─→ FFT analysis (frequency domain)
       ├─ 1–5 Hz: Likely human climbing/pushing
       ├─ 0.1–1 Hz: Likely wind or animal
       ├─ >10 Hz: Unlikely natural source
       └─ Confidence scoring

Combined with electrical state:
  - Electrical fault + vibration → HIGH confidence tamper
  - Vibration only → CHECK patterns
  - Electrical fault only → Electrical issue only
```

---

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Zone voltage = 0V always | Loose connections | Check GPIO pins, resolder breadboard |
| Zone voltage = 3.3V always | Open circuit in voltage divider | Check R1, R2, connections |
| INA219 not responding | I2C address conflict, loose wires | Verify address (0x40), check SDA/SCL |
| Relay doesn't click | GPIO22 not reaching coil driver | Check transistor, relay wiring |
| LEDs not lighting | GPIO output issue or polarity | Verify GPIO configuration, LED polarity |
| Fuzzy zone readings | Noise on ADC lines | Add 100nF cap to each ADC input |

---

## Next Steps

1. ✅ **PHASE 1 COMPLETE**: Electrical detection validated
2. 🔄 **PHASE 2**: Physical tamper sensor procurement + firmware integration (17–18 AUG)
3. 📊 **PHASE 3**: ML baseline model training (18–19 AUG)
4. 🔌 **PHASE 4**: Backend API + Dashboard integration (18–19 AUG)
5. 🎬 **PHASE 5**: End-to-end demo rehearsal (19 AUG)
6. 🏆 **PHASE 6**: SIH Internal Round presentation (20 AUG)

---

## Contact & Support

**Hardware Lead**: Anup (IoT & Automation)  
**Questions/Issues**: Open GitHub issue with label `hardware`

---

**Last Updated**: 17 August 2026  
**Prototype Status**: ✅ Electrical Detection COMPLETE | Phase 2 Pending  
**Safety Status**: Safe low-voltage lab demonstration only
