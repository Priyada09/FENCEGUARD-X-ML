# Firmware README

## Overview

FENCEGUARD-X firmware runs on ESP32, handling:
- **Phase 1 ✅ COMPLETE**: 3-zone electrical fault detection (zone voltage sensing + INA219)
- **Phase 2 🔄 IN PROGRESS**: Physical tamper sensor integration (future: accelerometer/vibration)
- **Ongoing**: Sensor fusion, telemetry, MQTT/HTTP communication, relay control

**Current Status**: Electrical zone acquisition validated with 26-sample experimental dataset. Physical tamper integration pending.

---

## Quick Start

### Prerequisites
- Arduino IDE (v2.0+) or PlatformIO
- ESP32 board support installed (v2.0.0+)
- Python 3.9+ (for ML model conversion, future)
- Git for version control

### Setup
```bash
# Clone firmware repository
git clone <repo> firmware
cd firmware/esp32

# Option 1: Arduino IDE
#   1. File → Preferences → Additional Boards Manager URLs
#   2. Add: https://dl.espressif.com/dl/package_esp32_index.json
#   3. Tools → Board Manager → Search "esp32" → Install
#   4. Tools → Board → ESP32 Dev Module
#   5. Sketch → Upload

# Option 2: PlatformIO (Recommended)
pip install platformio
platformio run --target upload
```

### First Flash Test
```bash
# Monitor serial output
platformio device monitor --speed 115200

# Expected output:
# [ESP32] Starting FENCEGUARD-X Firmware v1.0
# [SENSOR] Initializing INA219... OK
# [ADC] Reading zone voltages... OK
# [SYSTEM] Ready for telemetry
```

---

## Firmware Structure

```
esp32/
├─ main/
│  ├─ main.cpp                      # Entry point, FreeRTOS task scheduler
│  ├─ config.h                      # Configuration constants, I2C addresses, GPIO pins
│  │
│  ├─ ELECTRICAL LAYER (Phase 1)
│  ├─ sensor_driver.cpp              # ADC init, zone voltage acquisition (all 3 zones)
│  ├─ ina219_driver.cpp              # I2C communication, bus voltage/current/power
│  ├─ zone_classifier.cpp            # Per-zone state determination (NORMAL/OPEN/SHORT)
│  │
│  ├─ PHYSICAL LAYER (Phase 2 - TBD)
│  ├─ tamper_sensor_driver.cpp       # Future: accelerometer/vibration sensor I/O
│  │
│  ├─ PROCESSING LAYER
│  ├─ data_filter.cpp                # Moving average, validation, outlier removal
│  ├─ sensor_fusion.cpp              # Combine electrical + physical (future) evidence
│  ├─ telemetry.cpp                  # Payload assembly (zone states + INA219 + metadata)
│  │
│  ├─ DECISION LAYER
│  ├─ safety_logic.cpp               # Isolation decision: NORMAL / ALERT / CRITICAL
│  ├─ relay_controller.cpp           # GPIO relay actuation + debouncing
│  │
│  ├─ COMMUNICATION LAYER
│  ├─ mqtt_handler.cpp               # MQTT event publishing (future, optional)
│  ├─ http_handler.cpp               # HTTP/REST telemetry posting
│  ├─ storage.cpp                    # EEPROM circular buffer for offline logging
│  │
│  └─ utils.cpp                      # Timing, string utilities, debugging
│
├─ models/
│  └─ model.tflite                   # TensorFlow Lite model (future, Phase 3)
│
├─ platformio.ini                    # Build configuration, board settings, libraries
├─ .gitignore
└─ README.md                         # This file
```

---

## Key Modules

### 1. Sensor Driver — Zone Voltage Acquisition (COMPLETE ✅)

**File**: `sensor_driver.cpp`

**Functionality**:
- Initializes ESP32 ADC channels (3 channels for Zone 1, 2, 3)
- Reads analog voltage from each zone (0–3.5V range)
- Sampling at 100 Hz (every 10 ms)
- Applies 12-bit resolution

**Key Functions**:
```cpp
void adc_init();
  // Configure ADC GPIO pins, setup channels
  
float read_zone_voltage(int zone_num);
  // Read single zone voltage
  // Returns: voltage in volts (0.0 – 3.5V)

void read_all_zones(float *zone_voltages[3]);
  // Read all 3 zone voltages in one call
  // Populates array: [zone1_v, zone2_v, zone3_v]
```

**Electrical Thresholds** (Prototype-Specific):
```
NORMAL:     1.3–1.6V per zone
OPEN_CUT:   ~3.30V (elevated, loss of load)
SHORT:      ~0.00V (near ground, short circuit)
```

**Validation**:
- ✅ All 3 zones reading correctly
- ✅ Signatures match experimentally observed values
- ✅ No false positives in lab testing

---

### 2. INA219 Power Sensor Driver (COMPLETE ✅)

**File**: `ina219_driver.cpp`

**Functionality**:
- I2C communication with INA219 (address: 0x40 default)
- Reads bus voltage (0–26V, accurate to ±1%)
- Reads current through shunt resistor (±3.2A)
- Calculates power (P = V × I)
- Sampling at 10 Hz (every 100 ms)

**Key Functions**:
```cpp
void ina219_init();
  // Configure I2C, set calibration registers
  
float get_bus_voltage();
  // Returns: bus voltage in volts
  
float get_current_ma();
  // Returns: current in milliamps
  
float get_power_mw();
  // Returns: power in milliwatts
```

**Data Ranges** (Prototype):
| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Bus Voltage | 3.0 | 3.3 | 3.4 | V |
| Current | 60 | 100 | 130 | mA |
| Power | 200 | 330 | 440 | mW |

**Known Issues & Fixes**:
- **Issue**: Some early readings showed bus_voltage = 0.000V
- **Root Cause**: Loose I2C/power connections in prototype
- **Fix**: Implemented connection validation; flagged imputed values in dataset
- **Status**: ✅ Resolved during Phase 1 testing

---

### 3. Zone Classifier (COMPLETE ✅)

**File**: `zone_classifier.cpp`

**Functionality**:
- Analyzes each zone's voltage independently
- Classifies zone state: NORMAL / OPEN_CUT / SHORT / ANOMALY
- Detects multi-fault conditions (multiple zones faulty simultaneously)
- Outputs per-zone state + overall system severity

**Zone State Machine**:
```cpp
typedef enum {
    ZONE_NORMAL = 0,      // Zone voltage 1.0–1.8V
    ZONE_OPEN_CUT = 1,    // Zone voltage ≥ 2.5V (elevated)
    ZONE_SHORT = 2,       // Zone voltage ≤ 0.5V (near ground)
    ZONE_ANOMALY = 3      // Unexpected range
} ZoneState;

typedef struct {
    ZoneState state;
    float voltage;
    uint32_t stable_since_ms;  // How long in current state
    uint8_t confidence;         // 0–100%
} ZoneStatus;

ZoneStatus classifyZone(float zone_voltage, ZoneState previous_state);
  // Input: raw zone voltage
  // Output: classified state + confidence
  
void detectMultiFault();
  // Check if multiple zones are faulty simultaneously
  // Sets overall_condition to MULTI_FAULT if so
```

**Example Classification**:
```
Zone Voltages: [1.48V, 3.30V, 1.29V]
Zone States:   [NORMAL, OPEN_CUT, NORMAL]
Fault Zone:    ZONE2
Severity:      ALERT
```

**Validation Results** (from 26-sample dataset):
- ✅ Correct state classification: 100% accuracy
- ✅ Fault localization: Correctly identified affected zone(s) every time
- ✅ Multi-fault detection: Successfully detected Zone1+Zone2 simultaneous fault
- ✅ False positives: 0 (in lab conditions)

---

### 4. Data Filter (Signal Processing)

**File**: `data_filter.cpp`

**Functionality**:
- Noise reduction (moving average over 5–10 samples)
- Outlier detection (spike suppression)
- Data validation (range checking)
- Quality flagging (MEASURED vs IMPUTED)

**Key Functions**:
```cpp
float moving_average(float new_sample, float* buffer, int size);
  // Returns smoothed value
  
bool validate_zone_voltage(float voltage);
  // Returns true if voltage in valid range
  
bool validate_bus_voltage(float voltage);
  // Returns true if voltage reasonable
```

**Filtering Strategy**:
```
Raw Sample → Moving Average (5 samples)
           → Range Validation
           → Outlier Check
           → Quality Flag
           → Feature Extraction
           → Zone Classification
```

---

### 5. Sensor Fusion (Phase 1: Electrical Only)

**File**: `sensor_fusion.cpp`

**Functionality** (Current):
- Combines all zone voltages + INA219 measurements
- Checks consistency (e.g., if zone is OPEN, current should be LOW)
- Confidence scoring based on data agreement
- Outputs: overall_state, affected_zones, severity

**Inputs**:
```cpp
struct SensorData {
    float zone1_voltage;    // Zone 1 voltage
    float zone2_voltage;    // Zone 2 voltage
    float zone3_voltage;    // Zone 3 voltage
    float bus_voltage;      // INA219 bus voltage
    float current_ma;       // INA219 current
    float power_mw;         // INA219 power
    uint8_t data_quality;   // MEASURED or IMPUTED_BUS_VOLTAGE
};
```

**Outputs**:
```cpp
typedef enum {
    SYSTEM_NORMAL = 0,
    SYSTEM_ALERT = 1,
    SYSTEM_CRITICAL = 2
} SystemState;

typedef enum {
    FAULT_NONE = 0,
    FAULT_OPEN_CUT = 1,
    FAULT_SHORT = 2,
    FAULT_MULTI = 3
} FaultType;

struct FusedState {
    SystemState state;         // NORMAL / ALERT / CRITICAL
    FaultType fault_type;      // NONE / OPEN_CUT / SHORT / MULTI
    char fault_zones[32];      // "ZONE2" or "ZONE1_ZONE3" etc.
    uint8_t severity;          // 0–100
    uint8_t confidence;        // 0–100%
};

FusedState fuseSensorData(SensorData sensors);
```

**Consistency Checks**:
```
IF zone_open AND current is LOW:
    confidence += 20%  // Consistent
ELSE IF zone_open AND current is HIGH:
    confidence -= 10%  // Unexpected (possible noise)

IF zone_short AND current is HIGH:
    confidence += 20%  // Consistent
ELSE IF zone_short AND current is LOW:
    confidence -= 10%  // Unexpected
```

---

### 6. Telemetry Payload Assembly

**File**: `telemetry.cpp`

**Functionality**:
- Assembles complete sensor data snapshot
- Timestamps all measurements
- Includes zone states + INA219 readings
- Flags data quality (measured vs imputed)
- Formats for HTTP/MQTT transmission

**Telemetry Payload** (JSON):
```json
{
  "timestamp": "2026-08-17T14:23:45Z",
  "device_id": "ESP32_001",
  "zone1_voltage_v": 1.48,
  "zone2_voltage_v": 3.30,
  "zone3_voltage_v": 1.29,
  "zone1_status": "NORMAL",
  "zone2_status": "OPEN_CUT",
  "zone3_status": "NORMAL",
  "bus_voltage_v": 3.276,
  "current_ma": 88.20,
  "power_mw": 294.00,
  "condition": "OPEN_CUT",
  "fault_zone": "ZONE2",
  "severity": "ALERT",
  "confidence": 0.98,
  "data_quality": "MEASURED"
}
```

---

### 7. Safety Logic & Relay Control

**File**: `safety_logic.cpp` + `relay_controller.cpp`

**Functionality**:
- Decision logic: should we isolate?
- Relay GPIO actuation (low-level control)
- Debouncing (prevent rapid relay cycling)
- Manual reset handling
- LED/buzzer status feedback

**Decision Tree**:
```
SYSTEM_NORMAL:
  relay_state = ON
  led = GREEN
  buzzer = OFF

SYSTEM_ALERT:
  relay_state = ON (preserve power, alert only)
  led = YELLOW
  buzzer = SHORT_BEEP (0.5 sec once/minute)
  post_event_to_backend()

SYSTEM_CRITICAL:
  relay_state = OFF (cut power immediately)
  led = RED
  buzzer = CONTINUOUS (3s on, 1s off)
  post_critical_event_to_backend()
  
  # Debounce: prevent rapid cycling
  IF time_since_last_isolation < 5 seconds:
    wait(5 seconds)  // Cooldown
  ELSE:
    allow_manual_reset()  // Operator override
```

**Relay Actuation** (GPIO Control):
```cpp
#define RELAY_PIN GPIO_NUM_22  // Configuration in config.h

void relay_set(bool state) {
    digitalWrite(RELAY_PIN, state ? HIGH : LOW);
}

void isolation_cut() {
    relay_set(false);  // Cut power
    digitalWrite(LED_RED, HIGH);
    sound_buzzer(3000);  // 3000 ms continuous
}

void isolation_restore() {
    relay_set(true);   // Restore power
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_RED, LOW);
}
```

---

### 8. Telemetry Communication

**File**: `http_handler.cpp` (Primary) + `mqtt_handler.cpp` (Future)

**HTTP (Primary)**:
```cpp
void send_telemetry_http(FusedState state, SensorData sensors) {
    // POST to backend API
    // Endpoint: http://backend:5000/api/telemetry
    // Method: POST
    // Body: JSON payload (see Telemetry section above)
    // Retry: 3x on failure
}
```

**MQTT (Optional, Future)**:
```cpp
void send_event_mqtt(FusedState state) {
    // Publish to MQTT broker
    // Topic: fenceguard/events
    // Payload: JSON event
    // QoS: 1 (at-least-once delivery)
}
```

**Offline Fallback**:
- If backend unreachable: log to EEPROM (circular buffer, 100 events)
- Attempt retry every 30 seconds
- On backend reconnect: flush buffered events

---

### 9. Main Task Scheduler (FreeRTOS)

**File**: `main.cpp`

**FreeRTOS Tasks**:
```cpp
// Task 1: Sensor Acquisition (Core 0, Priority 3)
void task_read_sensors(void *arg) {
    while(1) {
        read_all_zones(zone_voltages);
        read_ina219();
        vTaskDelay(10 / portTICK_PERIOD_MS);  // 10 ms (100 Hz)
    }
}

// Task 2: Filtering & Classification (Core 1, Priority 2)
void task_process_data(void *arg) {
    while(1) {
        filter_sensor_data();
        classify_zones();
        fuse_sensor_data();
        vTaskDelay(500 / portTICK_PERIOD_MS);  // 500 ms
    }
}

// Task 3: Safety Logic & Relay Control (Core 1, Priority 3)
void task_safety_control(void *arg) {
    while(1) {
        if (system_state == CRITICAL) {
            isolation_cut();
        } else if (system_state == NORMAL) {
            isolation_restore();
        }
        vTaskDelay(100 / portTICK_PERIOD_MS);  // 100 ms
    }
}

// Task 4: Telemetry Communication (Core 1, Priority 1)
void task_send_telemetry(void *arg) {
    while(1) {
        if (time_to_send_telemetry()) {
            send_telemetry_http(fused_state, sensor_data);
        }
        vTaskDelay(5000 / portTICK_PERIOD_MS);  // Every 5 seconds
    }
}

void setup() {
    Serial.begin(115200);
    adc_init();
    ina219_init();
    relay_init();
    wifi_connect();
    
    xTaskCreatePinnedToCore(task_read_sensors, "ReadSensors", 2048, NULL, 3, NULL, 0);
    xTaskCreatePinnedToCore(task_process_data, "ProcessData", 2048, NULL, 2, NULL, 1);
    xTaskCreatePinnedToCore(task_safety_control, "SafetyControl", 2048, NULL, 3, NULL, 1);
    xTaskCreatePinnedToCore(task_send_telemetry, "Telemetry", 4096, NULL, 1, NULL, 1);
}

void loop() {
    // All work handled by FreeRTOS tasks
    delay(1000);
}
```

---

## Phase 2: Physical Tamper Integration (PLANNED)

**Timeline**: After electrical layer validated (17–18 AUG)

**Sensor Options**:
1. **Accelerometer (ADXL345)**: Detects movement/vibration
2. **Vibration Sensor**: Resonance analysis
3. **Strain Gauge**: Force/weight sensing (for climbing)

**Integration Plan**:
```
New File: tamper_sensor_driver.cpp
  ├─ Read accelerometer (I2C)
  ├─ FFT analysis (frequency detection)
  ├─ Pattern matching (climbing vs. wind)
  └─ Output: tamper_confidence (0–100%)

Update: sensor_fusion.cpp
  ├─ Combine electrical + physical data
  ├─ Rule: electrical fault + sustained vibration → HIGH confidence
  ├─ Rule: vibration only, no electrical fault → check patterns
  └─ Output: updated system_state, multimodal_confidence
```

---

## Phase 3: ML Model Inference (FUTURE)

**Timeline**: After baseline model trained (19–20 AUG, if time permits)

**Model Details**:
- Model type: Random Forest or Neural Network (TensorFlow Lite)
- Input features: [zone1_v, zone2_v, zone3_v, bus_v, current_ma, power_mw]
- Output: Probability distribution across [NORMAL, OPEN_CUT, SHORT, MULTI_FAULT]
- Latency requirement: <50ms on ESP32
- Model size: <1MB (to fit in ESP32 SPIFFS)

**Implementation**:
```cpp
// Load model at startup
interpreter = tflite::GetMutableInterpreter(&error_reporter);
interpreter->AllocateTensors();

// In processing loop:
void task_ml_inference(void *arg) {
    while(1) {
        // Prepare input tensor
        float* input_data = interpreter->typed_input_tensor<float>(0);
        input_data[0] = zone1_voltage;
        input_data[1] = zone2_voltage;
        input_data[2] = zone3_voltage;
        input_data[3] = bus_voltage;
        input_data[4] = current_ma;
        input_data[5] = power_mw;
        
        // Run inference
        interpreter->Invoke();
        
        // Get output probabilities
        float* output = interpreter->typed_output_tensor<float>(0);
        // output[0] = P(NORMAL)
        // output[1] = P(OPEN_CUT)
        // output[2] = P(SHORT)
        // output[3] = P(MULTI_FAULT)
        
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}
```

---

## Testing Checklist

### Electrical Detection (PHASE 1)
- [x] Zone 1 NORMAL detection
- [x] Zone 2 NORMAL detection
- [x] Zone 3 NORMAL detection
- [x] Zone 1 OPEN_CUT detection
- [x] Zone 2 OPEN_CUT detection
- [x] Zone 3 OPEN_CUT detection
- [x] Zone 1 SHORT detection
- [x] Zone 2 SHORT detection
- [x] Zone 3 SHORT detection
- [x] Multi-fault (Z1+Z2) detection
- [ ] Relay isolation test
- [ ] LED/buzzer status test
- [ ] Telemetry transmission test

### Physical Tamper (PHASE 2)
- [ ] Accelerometer sensor reading
- [ ] Movement detection (fence shake)
- [ ] Climbing simulation detection
- [ ] Wind/environmental noise rejection
- [ ] Sensor fusion confidence scoring

---

## Debugging

### Serial Monitor Output
```bash
[SYSTEM] Starting FENCEGUARD-X Firmware v1.0
[ADC] Initializing channels... OK
[I2C] INA219 connected (0x40)... OK
[WIFI] Connected to network... OK
[SYSTEM] Ready

[SENSOR] Z1:1.48V Z2:3.30V Z3:1.29V
[SENSOR] BusV:3.276V Curr:88.2mA Pow:294mW
[PROCESS] Z1:NORMAL Z2:OPEN_CUT Z3:NORMAL
[SAFETY] State:ALERT Fault:ZONE2 Severity:HIGH
[HTTP] POST /api/telemetry... 200 OK
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Zone voltage = 0.000V | Loose ADC connection | Check GPIO pins, soldering |
| INA219 not responding | I2C address mismatch | Verify address (0x40), check pullups |
| Relay not switching | GPIO pin incorrect | Confirm GPIO_NUM in config.h |
| WiFi timeout | Network unavailable | Use local fallback mode |
| High CPU usage | Too many task priority conflicts | Reduce logging, increase delays |

---

## Configuration (config.h)

```cpp
// GPIO PINS
#define ZONE1_PIN GPIO_NUM_32
#define ZONE2_PIN GPIO_NUM_33
#define ZONE3_PIN GPIO_NUM_34
#define RELAY_PIN GPIO_NUM_22
#define LED_GREEN GPIO_NUM_25
#define LED_YELLOW GPIO_NUM_26
#define LED_RED GPIO_NUM_27
#define BUZZER_PIN GPIO_NUM_14

// I2C
#define I2C_SDA GPIO_NUM_21
#define I2C_SCL GPIO_NUM_22
#define INA219_ADDRESS 0x40

// THRESHOLDS
#define ZONE_OPEN_THRESHOLD 2.5  // Voltage above this = OPEN_CUT
#define ZONE_SHORT_THRESHOLD 0.5 // Voltage below this = SHORT
#define CONFIDENCE_MIN 0.70       // Minimum confidence to act

// NETWORK
#define WIFI_SSID "YourSSID"
#define WIFI_PASS "YourPassword"
#define BACKEND_URL "http://192.168.1.100:5000/api/telemetry"

// TELEMETRY
#define TELEMETRY_INTERVAL_MS 5000  // Send every 5 seconds
#define RELAY_COOLDOWN_MS 5000      // Prevent rapid cycling
```

---

**Last Updated**: 17 August 2026  
**Firmware Version**: 1.0 (Electrical Detection Complete, Physical Tamper Pending)  
**Next Milestone**: Physical tamper sensor integration by 18-AUG
- Connect to MQTT broker
- Publish events: fence/events topic
- Subscribe to commands: fence/commands topic
- Reconnection logic (auto-retry)

### 6. Storage (storage.cpp)
- EEPROM read/write for configuration
- Event buffering (offline operation)
- Firmware version tracking

## Configuration

Edit `config.h`:
```cpp
// Sensor Parameters
#define INA219_ADDRESS 0x40
#define SAMPLING_RATE_MS 10
#define FILTER_WINDOW_SIZE 50

// Thresholds
#define CURRENT_ALERT_THRESHOLD 2.5    // Amperes
#define CURRENT_CRITICAL_THRESHOLD 3.0 // Amperes
#define VOLTAGE_MIN_THRESHOLD 200      // Volts

// MQTT
#define MQTT_BROKER "test.mosquitto.org"
#define MQTT_PORT 1883
#define MQTT_TOPIC "fence/events"

// Relay
#define RELAY_PIN 27
#define RELAY_COOLDOWN_MS 5000
```

## Uploading Firmware

### Using Arduino IDE
1. Tools → Board → ESP32 Dev Module
2. Tools → Port → COM# (your device)
3. Sketch → Upload
4. Monitor serial output (Ctrl+Shift+M)

### Using PlatformIO (Recommended)
```bash
platformio run --target upload        # Build and upload
platformio device monitor             # Serial monitor
platformio run --target clean         # Clean build
```

## Serial Monitor Output

```
[14:32:15.123] ESP32 starting...
[14:32:15.456] INA219 initialized at 0x40
[14:32:15.789] Connecting to WiFi: FENCEGUARD_NET
[14:32:18.012] WiFi connected (RSSI: -65 dBm)
[14:32:18.345] Connecting to MQTT broker...
[14:32:18.678] MQTT connected
[14:32:19.001] System ready - monitoring fence

[14:32:30.456] Current: 1.23A, Voltage: 380V, Status: NORMAL
[14:32:31.456] Current: 1.24A, Voltage: 379V, Status: NORMAL
[14:32:32.456] Current: 2.87A, Voltage: 375V, Status: ALERT
[14:32:32.789] Publishing event: anomaly_score=0.72, action=alert
[14:32:33.456] Current: 3.15A, Voltage: 350V, Status: CRITICAL
[14:32:33.678] ISOLATING! Relay cut at 14:32:33
```

## Testing Firmware

### Unit Tests (PlatformIO)
```bash
platformio test                 # Run all tests
platformio test --filter test_* # Filter by name
```

### Manual Testing
1. **Sensor Calibration**: Read raw INA219 values
2. **Filter Validation**: Apply known signals, check output
3. **Relay Test**: Toggle relay via GPIO command
4. **MQTT Test**: Publish test events, verify received

## Debugging

### Enable Debug Output
```cpp
#define DEBUG 1     // In config.h
```

### Serial Plotter (Arduino IDE)
Tools → Serial Plotter (visualize sensor data in real-time)

### Logic Analyzer
Use Saleae Logic Analyzer to inspect:
- I2C communication (INA219)
- GPIO state changes (relay, tamper)
- Interrupt timing

## OTA Updates (Optional)

Enable over-the-air firmware updates:
```cpp
#include <ArduinoOTA.h>

void setup() {
  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();
  // ... rest of code
}
```

Upload new firmware from Arduino IDE: Tools → Port → esp32 OTA

## Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Sensor Sampling | 100 Hz | 10ms intervals |
| Filter Update | 2 Hz | 500ms |
| ML Inference | 20 Hz | <50ms |
| Relay Response | <5ms | GPIO toggle |
| MQTT Publish | <500ms | Network dependent |
| WiFi Connection | 2-3s | First boot |

## Power Consumption

| State | Current | Notes |
|-------|---------|-------|
| Active (WiFi on) | 80mA | Normal operation |
| Active (WiFi off) | 40mA | Local processing only |
| Deep sleep | 10µA | Emergency backup |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| INA219 not found | Check I2C address, verify SDA/SCL pins |
| MQTT not connecting | Check WiFi connection, verify broker address |
| Relay not triggering | Test GPIO with LED first, check relay power |
| Model inference fails | Verify model.tflite loaded, check RAM |
| Serial not showing data | Check baud rate (115200), verify USB cable |

## Next Steps

1. [Review Hardware Setup](../hardware/README.md)
2. [Set up ML Model](../ml/README.md)
3. [Configure Backend](../backend/README.md)

---

**Contact**: Jayesh (Firmware Lead)
**Last Updated**: 14 August 2026
