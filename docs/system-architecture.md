# System Architecture

## High-Level Block Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FENCEGUARD-X System                           │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ FENCE PERIMETER (INA219 Current Sensors, Voltage Sensors, Tamper)   │
└──────────────┬───────────────────────────────────────────────────────┘
               │ Analog/Digital Signals
               ↓
┌──────────────────────────────────────────────────────────────────────┐
│ ESP32 GATEWAY                                                        │
│  ├─ ADC: 12-bit analog sampling (multiple channels)                 │
│  ├─ I2C: INA219 current measurement                                 │
│  ├─ GPIO: Relay control, Tamper interrupt                           │
│  ├─ UART: Serial communication                                       │
│  └─ WiFi/BLE: Connectivity                                           │
└──────────────┬───────────────────────────────────────────────────────┘
               │ Preprocessed Data
               ↓
┌──────────────────────────────────────────────────────────────────────┐
│ DATA PROCESSING (On ESP32)                                           │
│  ├─ Noise filtering (moving average, Kalman)                        │
│  ├─ Feature extraction (RMS, peak, variance)                        │
│  ├─ Threshold-based alerts                                           │
│  └─ ML inference (TensorFlow Lite)                                   │
└──────────────┬───────────────────────────────────────────────────────┘
               │ Classification: [Normal | Alert | Critical]
               ↓
┌──────────────────────────────────────────────────────────────────────┐
│ SAFETY CONTROLLER (On ESP32)                                         │
│  ├─ Decision logic: Should we isolate?                              │
│  ├─ Relay actuation: Cut/restore power                              │
│  ├─ Debouncing: Prevent rapid cycling                               │
│  └─ Local feedback: LED, buzzer status                              │
└──────────────┬───────────────────────────────────────────────────────┘
               │ Event Notification
               ├─────────────────────────────────────────┐
               │                                         │
               ↓                                         ↓
    ┌─────────────────────┐              ┌──────────────────────┐
    │ MQTT Broker         │              │ REST API (Optional)  │
    │ (mosquitto)         │              │ (Direct posting)     │
    └──────────┬──────────┘              └──────────┬───────────┘
               │                                    │
               └────────────────┬───────────────────┘
                                │
                                ↓
              ┌──────────────────────────────────┐
              │ BACKEND (Node.js + MongoDB)     │
              │  ├─ Event API                    │
              │  ├─ Event Storage                │
              │  ├─ Authentication               │
              │  └─ WebSocket (real-time)        │
              └──────────────┬───────────────────┘
                             │
                ┌────────────┴───────────┐
                │                        │
                ↓                        ↓
         ┌────────────┐            ┌──────────────┐
         │ Dashboard  │            │ Mobile App   │
         │ (React)    │            │ (React Native)
         └────────────┘            └──────────────┘
```

---

## Component Description

### 1. **Sensing Layer**

| Sensor | Parameter | Range | Interface |
|--------|-----------|-------|-----------|
| INA219 | Current | ±3.2A | I2C |
| Voltage Divider | Voltage | 0-400V | ADC |
| Reed Switch | Tamper | On/Off | GPIO Interrupt |
| DS18B20 | Temperature | -55 to +125°C | 1-Wire |

### 2. **Edge Processing (ESP32)**

**Microcontroller Specs:**
- Dual-core @ 240 MHz
- 520 KB SRAM, 4 MB Flash
- WiFi 802.11 b/g/n
- Bluetooth 4.2 (BLE)
- 12 ADC channels (12-bit)

**Key Modules:**
```
esp32/
├── sensor_driver.c       # ADC, I2C initialization
├── filter.c              # Signal processing
├── ml_inference.c        # TensorFlow Lite inference
├── relay_controller.c    # Isolation logic
├── mqtt_client.c         # Event publishing
└── main.c                # Task scheduling (FreeRTOS)
```

### 3. **ML Model (Inference)**

**Model Type:** Random Forest / Neural Network (TensorFlow Lite)

**Input Features:**
- Current RMS
- Current Peak
- Current Variance
- Voltage level
- Rate of change (dI/dt)
- Tamper state

**Output Classes:**
- 0: Normal
- 1: Anomaly (High current spike)
- 2: Tamper (Reed switch triggered)
- 3: Breakdown (Low voltage, high current)

**Latency:** <50ms inference on ESP32

### 4. **Safety Controller Logic**

```
IF anomaly_score > HIGH_THRESHOLD:
    SET relay = OFF (cut power)
    SET buzzer = ON (alert)
    SET led = RED (danger)
    POST event to backend
    WAIT 5 seconds (cooldown)
ELIF anomaly_score > MED_THRESHOLD:
    POST alert to backend
    SET led = YELLOW (warning)
ELSE:
    SET led = GREEN (ok)
```

### 5. **Backend (API)**

**REST Endpoints:**
```
POST   /api/events          # Log fence event
GET    /api/events          # Retrieve events
GET    /api/fence/status    # Current fence state
GET    /api/analytics       # Historical analysis
```

**Database Schema:**
```
events {
  _id: ObjectId
  timestamp: Date
  sensorId: String
  eventType: String      # "normal", "alert", "critical"
  current: Number        # in Amperes
  voltage: Number        # in Volts
  anomalyScore: Number   # 0-1
  action: String         # "none", "relay_cut", "alert_sent"
}
```

### 6. **Dashboard (Real-Time UI)**

**Pages:**
- **Live Monitor**: Current fence status (green/yellow/red)
- **Event Log**: Searchable history of all events
- **Analytics**: Graphs of current/voltage over time
- **Alerts**: Active notifications
- **Settings**: Configure thresholds, alert rules

---

## Data Flow Sequence

### Normal Operation
```
1. Sensor samples current (INA219)
2. ESP32 reads ADC every 10ms
3. Filter applies moving average
4. Every 500ms: Features extracted
5. ML model classifies state
6. If alert: Send MQTT message
7. Backend logs event
8. Dashboard updates in real-time
```

### Critical Event (Tampering Detected)
```
1. Reed switch triggered → GPIO interrupt
2. ESP32 immediately cuts relay (0.1ms)
3. Buzzer sounds (100Hz for 500ms)
4. LED turns RED
5. Event posted to backend
6. Dashboard shows RED alert
7. Operator receives notification
8. Manual inspection initiated
```

---

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

