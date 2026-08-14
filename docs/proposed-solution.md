# Proposed Solution

## Overview
**FENCEGUARD-X** is an intelligent, autonomous fence monitoring and protection system that uses IoT sensors, edge computing, and machine learning to provide real-time threat detection and automated response.

## Core Architecture

### Three-Layer System

#### **Layer 1: Sensing (Edge Hardware)**
- **Current Sensors (INA219)**: Real-time current flow measurement
- **Voltage Sensors**: Fence voltage monitoring
- **Tamper Sensors**: Physical breach detection
- **Temperature Sensors**: Thermal anomaly detection

#### **Layer 2: Intelligence (ESP32 + ML)**
- **ESP32 Microcontroller**: Data acquisition and preprocessing
- **ML Model**: Runs locally for low-latency anomaly detection
- **Safety Controller**: Autonomous relay logic
- **Communication Module**: Sends events to backend

#### **Layer 3: Management (Cloud Backend)**
- **Event Logging API**: Stores all fence events
- **Dashboard**: Real-time visualization
- **Historical Analysis**: Trend detection and reporting

---

## Key Features

### 1. Real-Time Monitoring
- **High-frequency sampling** of current, voltage, and tamper signals
- **Noise filtering** to eliminate false alarms
- **Edge processing** for <100ms response time

### 2. ML-Based Anomaly Detection
- **Classification Classes**: Normal → Tamper → Breakdown → Theft Attempt
- **Threshold-Based Rules** + **ML Model** combination
- **Adaptive Learning**: Model retrains with new patterns
- **>85% detection accuracy** target

### 3. Automatic Isolation
- **Relay Control**: Cuts power to compromised section
- **Latching Logic**: Prevents rapid cycling
- **Status Indicators**: LED/buzzer for local feedback

### 4. Event Logging & Analytics
- **Timestamped Events**: All anomalies recorded
- **Event Severity**: Critical, High, Medium, Low
- **Historical Trends**: Predict maintenance needs

### 5. Remote Management (Dashboard)
- **Live Fence Status**: Green (OK) → Yellow (Alert) → Red (Danger)
- **Event History**: Searchable log of all incidents
- **Alert Notifications**: Email/SMS on critical events
- **Statistics**: Uptime, incident count, response times

---

## Technology Stack

### Hardware
- **ESP32 Microcontroller** (dual-core, WiFi/BLE)
- **INA219 Current Sensor** (±3.2A, 16-bit)
- **Relay Module** (isolation control)
- **Buzzer + LEDs** (local alerts)

### Firmware
- **Arduino/ESP-IDF** (C/C++)
- **Sensor drivers** (I2C, ADC)
- **MQTT** (publish events)

### ML
- **Python** (model training)
- **TensorFlow/Scikit-learn** (model building)
- **TensorFlow Lite** (edge inference on ESP32)

### Backend
- **Node.js + Express** (REST API)
- **MongoDB** (event storage)
- **WebSocket** (real-time updates)

### Dashboard
- **React.js** (frontend)
- **Chart.js** (real-time graphs)
- **Socket.io** (live updates)

---

## System Workflow

```
[Sensor Data] 
    ↓
[ESP32: Preprocess & Filter]
    ↓
[ML Model: Classify Threat]
    ↓
[Decision Logic]
    ├─→ Normal: Log & Continue
    ├─→ Alert: Notify via API
    └─→ Critical: Isolate + Alert
    ↓
[Backend: Log Event]
    ↓
[Dashboard: Display Status]
```

---

## Advantages Over Existing Solutions

| Aspect | Traditional | FENCEGUARD-X |
|--------|-----------|--------------|
| **Response Time** | Minutes | <100ms |
| **Threat Classification** | No | Yes (ML-based) |
| **Automatic Isolation** | No | Yes |
| **Event Logging** | None | Complete audit trail |
| **False Alarms** | High | Low (<5%) |
| **Cloud Dependency** | Required | Optional |
| **Cost** | High (infrastructure) | Low (edge-based) |

---

## Success Metrics

- ✅ Detects tampering within 100ms
- ✅ Isolates compromised sections automatically
- ✅ <5% false alarm rate
- ✅ Logs 100% of events
- ✅ Dashboard updates in real-time
- ✅ Works offline (local decision-making)
- ✅ Operates continuously for >30 days

