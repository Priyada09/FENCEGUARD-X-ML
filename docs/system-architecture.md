# System Architecture

## Overview

FENCEGUARD-X uses a **multi-layer architecture** combining electrical fault detection with physical tamper sensing. The current prototype implements **3-zone electrical integrity monitoring** with INA219 power measurement. Future phases will add physical movement/vibration sensors for comprehensive threat detection.

**Current Status**: 3-zone electrical detection VALIDATED on safe low-voltage prototype

---

## High-Level System Architecture

```
                    3-ZONE SAFE FENCE PROTOTYPE
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
      ELECTRICAL LAYER                  PHYSICAL LAYER
             |                                 |
      Zone 1 EOL sensing              Movement/vibration/
      Zone 2 EOL sensing              tamper sensing
      Zone 3 EOL sensing              (TBD: Phase 2)
             |                                 |
             +----------------+----------------+
                              |
                        ┌─────────────┐
                        │   ESP32     │
                        │ Microcontroller
                        └──────┬──────┘
                              |
        ┌─────────────────────┼─────────────────────┐
        |                     |                     |
        v                     v                     v
    INA219                Zone States          Sensor
    (I2C Bus)          (GPIO ADC Reads)      Fusion
    ├─ Bus Voltage     ├─ Zone 1 Voltage    ├─ Electrical
    ├─ Current         ├─ Zone 2 Voltage    ├─ Physical (Future)
    └─ Power           └─ Zone 3 Voltage    └─ Classification

                        ↓
                  DECISION LOGIC
                  ├─ Per-Zone State
                  ├─ System Severity
                  └─ Isolation Action

                        ↓
        ┌───────────────────────────────────┐
        │    SAFETY & COMMUNICATION         │
        ├─ Relay Control (Isolation)        │
        ├─ LED/Buzzer (Local Feedback)      │
        ├─ WiFi/MQTT (Remote Alert)         │
        └───────────────────────────────────┘

                        ↓
        ┌───────────────────────────────────┐
        │  BACKEND (Node.js + MongoDB)      │
        ├─ Telemetry API                    │
        ├─ Event Logging                    │
        ├─ WebSocket (Real-time)            │
        └───────────────────────────────────┘

                        ↓
        ┌───────────────────────────────────┐
        │   DASHBOARD (React.js)            │
        ├─ Live Zone Status (3 zones)       │
        ├─ Bus Voltage/Current/Power        │
        ├─ Event History                    │
        └─ Severity Indicators              │
        └───────────────────────────────────┘
```

---

## Processing Pipeline

```
SENSE
  ↓ Read all zone voltages + INA219
  ├─ Zone 1 voltage (0-3.5V range)
  ├─ Zone 2 voltage (0-3.5V range)
  ├─ Zone 3 voltage (0-3.5V range)
  ├─ Bus voltage (3.0-3.4V typical)
  ├─ Current (80-125 mA typical)
  └─ Power (calculated: V × I)

VALIDATE
  ↓ Check sensor validity
  ├─ Zone voltage in valid range?
  ├─ Bus voltage reasonable?
  ├─ Current within limits?
  └─ Flag imputed values vs measured

LOCALIZE
  ↓ Identify which zone(s) affected
  ├─ Zone voltage ~3.30V → OPEN_CUT
  ├─ Zone voltage ~0.00V → SHORT
  ├─ Zone voltage 1.3-1.6V → NORMAL
  └─ Multiple zones may be faulty

FUSE
  ↓ Combine electrical + physical evidence
  ├─ Electrical fault detected?
  ├─ Physical tamper detected? (Future)
  ├─ Multiple simultaneous faults?
  └─ Confidence scoring

CLASSIFY
  ↓ Determine severity
  ├─ NORMAL: All zones healthy
  ├─ ALERT: Electrical fault OR tamper detected
  ├─ CRITICAL: Multiple faults OR manual override
  └─ Assign severity level

ISOLATE
  ↓ Trigger safety actions
  ├─ NORMAL: No action
  ├─ ALERT: Log event, notify backend
  ├─ CRITICAL: Cut relay, sound buzzer, send alert
  └─ Prevent false-positive cycling

ALERT
  ↓ Notify operator
  ├─ LED status (GREEN/YELLOW/RED)
  ├─ Buzzer tone (for CRITICAL)
  ├─ MQTT/HTTP to backend
  └─ Post to dashboard

LOG
  ↓ Persistent storage
  ├─ Timestamp, zone states, fault type
  ├─ Bus voltage, current, power at time of event
  ├─ Sensor quality flags
  └─ Backend database archive
```

---

## Component Details

### 1. **Sensing Layer (ELECTRICAL)**

#### Zone Voltage Sensors
- **Method**: EOL (End-of-Line) resistor network
- **Type**: Each zone has independent voltage measurement
- **Interface**: ADC (analog-to-digital converter on ESP32)
- **Range**: 0–3.5V
- **Resolution**: 12-bit (ESP32 native)

#### Zone Voltage Signatures (Prototype-Specific)
| Condition | Zone Voltage | Bus Voltage | Current | Status |
|-----------|--------------|-------------|---------|--------|
| NORMAL | 1.3–1.6V | 3.2–3.4V | 80–125 mA | ✅ All Zones OK |
| OPEN_CUT | ~3.30V (affected zone) | 3.0–3.3V | 60–90 mA | ⚠️ Loss of load |
| SHORT | ~0.00V (affected zone) | 2.8–3.2V | 100–130 mA | 🔴 Short circuit |
| MULTI_FAULT | Mixed (see below) | Variable | Variable | 🔴 Multiple faults |

**Example Multi-Fault**:
- Zone 1: ~3.30V (OPEN_CUT)
- Zone 2: ~0.00V (SHORT)
- Zone 3: 1.5V (NORMAL)
- **Classification**: MULTI_FAULT, affects Z1+Z2

#### INA219 Power Sensor
- **Manufacturer**: Texas Instruments
- **Interface**: I2C (0x40 default address)
- **Measurements**:
  - Bus voltage: 0–26V (26V max)
  - Shunt voltage: ±81mV
  - Current: ±3.2A (with appropriate shunt resistor)
  - Power: Calculated (P = V × I)
- **Sample Rate**: 10 Hz default, configurable up to 860 Hz
- **Accuracy**: ±1% voltage, ±0.5% current

#### Sensing Layer Summary (Phase 1)
```
Zone 1 ──┐
Zone 2 ──┼─→ ADC Multiplexer ──→ ESP32 GPIO/ADC
Zone 3 ──┤
         └─→ Bus Voltage

INA219 (I2C) ──→ ESP32 I2C Bus
           ├─ Bus Voltage
           ├─ Current
           └─ Power
```

### 2. **Sensing Layer (PHYSICAL) — Phase 2**

**Not yet implemented. TBD candidates**:
- Accelerometer (ADXL345): Detects fence movement, climbing
- Vibration sensor: Distinguishes physical tampering from wind
- Strain gauge: Detects climbing or pushing force
- Thermal camera: Detects body heat near fence

**Selection Criteria**:
- Low cost (< $10 per unit)
- Low power consumption
- Compatible with ESP32 GPIO/I2C
- Environmental robustness (rain, heat, dust)

---

### 3. **Edge Processing (ESP32)**

**Microcontroller Specs:**
- Dual-core Xtensa 32-bit @ 240 MHz
- 520 KB SRAM, 4 MB Flash
- Built-in WiFi 802.11 b/g/n
- Bluetooth 4.2 (BLE)
- 12 ADC channels (12-bit, ~100 ksps)
- 2 I2C buses (100/400 kHz)
- 16 GPIO pins

**Firmware Modules:**
```
esp32/main/
├── sensor_driver.cpp       # ADC init, zone voltage reading
├── ina219_driver.cpp       # I2C, INA219 communication
├── data_filter.cpp         # Moving average, validation
├── zone_classifier.cpp     # Per-zone state determination
├── sensor_fusion.cpp       # Electrical + physical fusion
├── ml_inference.cpp        # TensorFlow Lite (future)
├── relay_controller.cpp    # GPIO relay actuation
├── mqtt_handler.cpp        # MQTT event publishing
├── telemetry.cpp           # Payload assembly
├── safety_logic.cpp        # Isolation decision logic
└── main.cpp                # FreeRTOS task scheduler
```

**Sampling Strategy:**
```
Every 10ms (100 Hz):
  - Read all 3 zone voltages
  - Read INA219 (bus, current, power)

Every 500ms:
  - Extract features (RMS, peak, variance)
  - Run zone classifier
  - Detect faults
  - Publish telemetry if changed

Every 5 seconds:
  - Publish full telemetry to backend
  - Log to EEPROM (circular buffer)
```

---

### 4. **Zone Classification Logic**

**Per-Zone State Machine:**
```
For each zone (Zone1, Zone2, Zone3):

IF zone_voltage >= 2.5V (elevated):
    State = OPEN_CUT
    Reason = "Zone voltage near bus voltage → loss of load"
    Severity = HIGH

ELSE IF zone_voltage <= 0.5V (near ground):
    State = SHORT
    Reason = "Zone voltage near ground → short to ground"
    Severity = CRITICAL

ELSE IF 1.0V <= zone_voltage <= 1.8V (nominal):
    State = NORMAL
    Reason = "Zone voltage in expected range"
    Severity = NONE

ELSE:
    State = ANOMALY
    Reason = "Unexpected voltage level"
    Severity = MEDIUM
```

**Multi-Fault Detection:**
```
Count faulted zones:
  faulted_count = count(zone with fault)
  
IF faulted_count == 0:
    system_state = NORMAL
    
ELSE IF faulted_count == 1:
    system_state = ALERT
    fault_zone = [ZONE1 | ZONE2 | ZONE3]
    
ELSE IF faulted_count >= 2:
    system_state = CRITICAL
    fault_zone = [ZONE1_ZONE2_ZONE3 combinations]
    additional_severity = EXTREME
```

---

### 5. **Sensor Fusion (Phase 1: Electrical Only)**

```
Input:
  ├─ Zone 1 voltage + state (NORMAL/OPEN/SHORT)
  ├─ Zone 2 voltage + state (NORMAL/OPEN/SHORT)
  ├─ Zone 3 voltage + state (NORMAL/OPEN/SHORT)
  ├─ Bus voltage (INA219)
  ├─ Current (INA219)
  └─ Power (INA219)

Processing:
  ├─ Check consistency:
  │   IF open_zone_count > 0 AND current is LOW
  │       → Likely real OPEN_CUT (not sensor noise)
  │
  │   IF short_zone_count > 0 AND current is HIGH
  │       → Likely real SHORT (not sensor noise)
  │
  ├─ Confidence scoring:
  │   confidence = 0.0 to 1.0
  │   ├─ Data quality (measured vs imputed)
  │   ├─ Consistency check results
  │   ├─ Repeated detection (debouncing)
  │   └─ Physical plausibility
  │

Output:
  ├─ Overall system state: NORMAL / ALERT / CRITICAL
  ├─ Fault type: NONE / OPEN_CUT / SHORT / MULTI_FAULT
  ├─ Affected zone(s): NONE / ZONE1 / ZONE2 / ZONE3 / (combinations)
  ├─ Severity: NONE / LOW / MEDIUM / HIGH / CRITICAL
  └─ Confidence: 0–100%
```

**Future Addition (Phase 2: Physical Tamper)**:
```
Input:
  ├─ Accelerometer data (if available)
  ├─ Vibration frequency analysis
  ├─ Force/strain gauge (if available)
  └─ Electrical state (from Phase 1)

Processing:
  ├─ Pattern matching:
  │   IF vibration_freq in [1–5 Hz] AND acceleration > 2G
  │       → Likely human climbing/pushing
  │
  │   IF vibration_freq in [0.1–1 Hz] AND low acceleration
  │       → Likely wind or animal
  │
  ├─ Temporal analysis:
  │   IF sustained vibration > 10 seconds
  │       → Likely intentional tampering
  │

Output:
  ├─ Tamper detected: YES / NO
  ├─ Confidence: 0–100%
  ├─ Environmental vs intentional: classification
  └─ Additional severity modifier (if tamper + electrical fault)
```

---

### 6. **Safety Controller Logic**

```
Input:
  ├─ System state: NORMAL / ALERT / CRITICAL
  ├─ Confidence: 0–100%
  ├─ Recent event history (last 5 seconds)
  └─ Current relay status: ON / OFF

Processing:

IF state == NORMAL:
    relay_command = ON (no isolation)
    led = GREEN
    buzzer = OFF
    
ELSE IF state == ALERT:
    relay_command = ON (preserve power, alert operator)
    led = YELLOW (warning)
    buzzer = SHORT_BEEP (0.5 sec, once per minute)
    post_event_to_backend()
    
ELSE IF state == CRITICAL:
    relay_command = OFF (cut power immediately)
    led = RED (danger)
    buzzer = CONTINUOUS (3 sec on, 1 sec off cycle)
    post_critical_event_to_backend()
    send_sms_alert() [if configured]
    
    # Debounce: prevent rapid cycling
    IF time_since_last_isolation < 5 seconds:
        relay_cooldown()  # Wait 5 sec before re-engaging
    ELSE:
        allow_manual_reset()  # Operator must manually reset
```

---

### 7. **Backend API (Node.js + MongoDB)**

**REST Endpoints:**
```
POST   /api/telemetry
       └─ Receive sensor data from ESP32
       └─ Fields: timestamp, zone1_v, zone2_v, zone3_v, bus_v, current, power

GET    /api/events
       └─ Retrieve historical events with filters
       └─ Query: ?startDate=2026-08-17&zone=ZONE1&type=OPEN_CUT

POST   /api/events
       └─ Log a critical event from ESP32

GET    /api/status
       └─ Current system state
       └─ Returns: zones[], latest_event, bus_voltage, current, severity

WebSocket /ws
       └─ Real-time updates (live dashboard)
       └─ Emits: system_state, new_events, zone_updates
```

**Database Schema:**
```
Telemetry Collection:
{
  _id: ObjectId,
  timestamp: ISODate,
  device_id: String,
  zone1_voltage_v: Number,
  zone2_voltage_v: Number,
  zone3_voltage_v: Number,
  bus_voltage_v: Number,
  current_ma: Number,
  power_mw: Number,
  data_quality: String  // "MEASURED" | "IMPUTED_BUS_VOLTAGE"
}

Event Collection:
{
  _id: ObjectId,
  timestamp: ISODate,
  device_id: String,
  condition: String,      // "NORMAL" | "OPEN_CUT" | "SHORT" | "MULTI_FAULT"
  fault_zone: String,     // "NONE" | "ZONE1" | "ZONE2" | "ZONE3" | "ZONE1_OPEN_ZONE2_SHORT"
  severity: String,       // "NORMAL" | "ALERT" | "CRITICAL"
  confidence: Number,     // 0.0–1.0
  action_taken: String,   // "NONE" | "RELAY_CUT" | "ALERT_SENT"
  zone1_status: String,
  zone2_status: String,
  zone3_status: String
}
```

---

### 8. **Dashboard (React.js + WebSocket)**

**Real-Time Display:**
```
┌─────────────────────────────────────────────────────┐
│          FENCEGUARD-X LIVE DASHBOARD                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  System Status:  🟢 NORMAL    Severity: LOW         │
│                                                     │
├─────────────────────────────────────────────────────┤
│  ZONE 1              ZONE 2              ZONE 3     │
│  Voltage: 1.49V      Voltage: 1.47V      Voltage: 1.42V
│  Status: 🟢 NORMAL   Status: 🟢 NORMAL   Status: 🟢 NORMAL
│                                                     │
├─────────────────────────────────────────────────────┤
│  Bus Voltage: 3.328V  │  Current: 121.40mA         │
│  Power: 406.00mW      │                             │
├─────────────────────────────────────────────────────┤
│  LAST 10 EVENTS                                     │
│  17-AUG 14:23:45  ZONE2 SHORT      → CRITICAL      │
│  17-AUG 14:22:10  NORMAL            → OK            │
│  17-AUG 14:15:32  ZONE1 OPEN_CUT    → ALERT        │
│  ...                                                 │
└─────────────────────────────────────────────────────┘
```

**Pages:**
1. **Live Monitor**: Real-time zone status + bus metrics
2. **Event Log**: Searchable history, filters by zone/type/date
3. **Analytics**: Graphs (current, voltage, power over time)
4. **Configuration**: Thresholds, alert rules, device settings
5. **Notifications**: Active alerts + email/SMS settings

---

## Experimental Validation (Phase 1 Complete)

**Test Matrix** (All 9 combinations validated):
```
                 Zone 1        Zone 2        Zone 3
Scenario 1:      NORMAL        NORMAL        NORMAL        ✅ Detected
Scenario 2:      OPEN_CUT      NORMAL        NORMAL        ✅ Detected
Scenario 3:      NORMAL        OPEN_CUT      NORMAL        ✅ Detected
Scenario 4:      NORMAL        NORMAL        OPEN_CUT      ✅ Detected
Scenario 5:      SHORT         NORMAL        NORMAL        ✅ Detected
Scenario 6:      NORMAL        SHORT         NORMAL        ✅ Detected
Scenario 7:      NORMAL        NORMAL        SHORT         ✅ Detected
Scenario 8:      OPEN_CUT      SHORT         NORMAL        ✅ Multi-Fault Detected
Scenario 9+:     [Other combinations]                      ✅ All working
```

**Results**:
- Fault localization accuracy: 100% on prototype
- False-positive rate: 0% (in lab conditions)
- Response time: <100ms from sensor to relay
- Data quality: 26 samples collected (85% measured, 15% imputed)

---

## Future Enhancements

### Phase 2: Physical Tamper Detection
- Accelerometer integration
- Vibration pattern analysis
- Environmental vs. intentional tampering classification

### Phase 3: ML Model Optimization
- Larger dataset collection
- Baseline model training (Decision Tree, Random Forest)
- TensorFlow Lite export for ESP32 inference

### Phase 4: Commercial Deployment
- High-voltage fence compatibility (with professional electrical review)
- Cloud backend scaling
- Mobile app for remote monitoring
- SMS/email alerts
- Predictive maintenance (trend analysis)

---

**Last Updated**: 17 August 2026  
**Architecture Version**: 1.1 (3-zone electrical + future physical tamper)

## Communication Protocols

### ESP32 ↔ Sensors
- **I2C**: INA219 (100 kHz)
- **ADC**: Voltage input (10-bit, 1MHz)
- **GPIO**: Interrupt-driven for tamper
- **1-Wire**: DS18B20 temperature

### ESP32 ↔ Backend
- **MQTT** (preferred): Low bandwidth, subscribe/publish
- **HTTP REST** (fallback): Direct API posting
- **TLS/SSL**: Encrypted communication

### Backend ↔ Dashboard
- **WebSocket**: Real-time event push
- **REST API**: Historical data fetch
- **JSON**: Standardized data format

---

## Fallback & Reliability

### Offline Mode
- ESP32 operates independently
- Relay cuts power on local detection
- Events stored in EEPROM (limited)
- Syncs with backend when connectivity restored

### Redundancy
- Dual threshold system (rule-based + ML)
- Manual override via physical button
- Battery backup for ESP32 (optional UPS)
- Watchdog timer to prevent freezing

---

## Power Consumption

| Component | Power (mW) | Uptime |
|-----------|-----------|--------|
| ESP32 (active) | 80 | >1 month |
| INA219 | 1 | - |
| Relay (on) | 100 | 5V source |
| Buzzer | 50 | alerts only |
| **Total (average)** | **~100mW** | **30 days** |

---

## Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Detection Latency | <100ms | Real-time response |
| ML Accuracy | >85% | Minimize false positives |
| Event Logging | 100% | Compliance/audit |
| Dashboard Update | <500ms | User experience |
| System Uptime | >99.5% | Critical safety |
| False Alarm Rate | <5% | User trust |

