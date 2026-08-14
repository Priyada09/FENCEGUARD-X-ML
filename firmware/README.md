# Firmware README

## Overview
FENCEGUARD-X firmware runs on ESP32, handling sensor acquisition, data filtering, ML inference, relay control, and MQTT communication.

## Quick Start

### Prerequisites
- Arduino IDE or PlatformIO
- ESP32 board support installed
- Python 3.9+ (for ML model conversion)
- Git for version control

### Setup
```bash
# Clone firmware
git clone <repo> firmware
cd firmware/esp32

# Install dependencies
# Option 1: Arduino IDE
#   - Install board: Boards Manager → esp32
#   - Install libraries: Library Manager (search each)

# Option 2: PlatformIO
platformio project init --board esp32dev

# Flash firmware
platformio run --target upload
```

## Firmware Structure

```
esp32/
├─ main/
│  ├─ main.cpp                 # Entry point
│  ├─ config.h                 # Configuration constants
│  ├─ sensor_driver.cpp        # I2C, ADC, GPIO init
│  ├─ data_filter.cpp          # Signal processing
│  ├─ ml_model.cpp             # TensorFlow Lite inference
│  ├─ relay_controller.cpp     # Isolation logic
│  ├─ mqtt_handler.cpp         # Event publishing
│  ├─ storage.cpp              # EEPROM management
│  └─ utils.cpp                # Utilities
│
├─ models/
│  └─ model.tflite             # Quantized ML model
│
├─ platformio.ini              # PlatformIO config
└─ README.md                   # This file
```

## Key Modules

### 1. Sensor Driver (sensor_driver.cpp)
- I2C initialization for INA219
- ADC setup for voltage measurement
- GPIO interrupt for tamper detection
- Sampling at 100Hz (10ms intervals)

### 2. Data Filter (data_filter.cpp)
- Moving average filter (noise reduction)
- Kalman filter (optional, adaptive)
- Outlier removal (spike suppression)
- Feature extraction: RMS, peak, variance

### 3. ML Inference (ml_model.cpp)
- TensorFlow Lite model loading
- Input preprocessing
- Classification: NORMAL | ALERT | CRITICAL
- Latency: <50ms per inference

### 4. Relay Controller (relay_controller.cpp)
- Threshold-based decision making
- Relay actuation (GPIO control)
- Debouncing logic (prevent rapid cycling)
- Manual reset handling

### 5. MQTT Handler (mqtt_handler.cpp)
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
