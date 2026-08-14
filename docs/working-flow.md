# Working Flow

## System Workflow Overview

### Phase 1: Initialization (Power On)

```
1. ESP32 boots
   ├─ Load configuration from EEPROM
   ├─ Initialize sensors (I2C, ADC, GPIO)
   ├─ Load ML model (TensorFlow Lite)
   ├─ Connect to WiFi
   └─ Subscribe to MQTT broker

2. System Status
   ├─ LED blinks BLUE (initializing)
   └─ Ready for operation (LED turns GREEN)
```

---

### Phase 2: Normal Operation (Continuous Monitoring)

#### **Every 10 milliseconds:**
```
┌─ Sensor Sampling ─────────────────────────────┐
│ 1. Read INA219 (current)                      │
│ 2. Read ADC (voltage)                         │
│ 3. Read GPIO (tamper sensor)                  │
│ 4. Store in circular buffer                   │
└───────────────────────────────────────────────┘
```

#### **Every 500 milliseconds:**
```
┌─ Feature Extraction ──────────────────────────┐
│ 1. Calculate RMS current: √(Σ(I²)/N)         │
│ 2. Calculate peak current: max(I)             │
│ 3. Calculate variance: Σ((I - mean(I))²)/N   │
│ 4. Voltage status: HIGH/NORMAL/LOW            │
│ 5. Rate of change: dI/dt                      │
└───────────────────────────────────────────────┘
        ↓
┌─ ML Model Classification ─────────────────────┐
│ TensorFlow Lite inference (<50ms)            │
│                                               │
│ Input: [I_rms, I_peak, I_var, V, dI/dt]     │
│ ↓                                             │
│ Model decision: What is the threat?          │
│ ↓                                             │
│ Output: anomaly_score (0.0 - 1.0)            │
│         class: [NORMAL | ALERT | CRITICAL]   │
└───────────────────────────────────────────────┘
        ↓
┌─ Threshold Evaluation ────────────────────────┐
│ IF anomaly_score >= 0.8                      │
│     → State = CRITICAL (cut power)            │
│ ELSE IF anomaly_score >= 0.5                 │
│     → State = ALERT (notify)                  │
│ ELSE                                          │
│     → State = NORMAL (continue)               │
└───────────────────────────────────────────────┘
        ↓
┌─ Action Execution ────────────────────────────┐
│ NORMAL:                                       │
│   ├─ Keep relay ON                            │
│   ├─ LED = GREEN                              │
│   ├─ No event posted                          │
│                                               │
│ ALERT:                                        │
│   ├─ Keep relay ON (monitored closely)       │
│   ├─ LED = YELLOW                             │
│   ├─ POST to backend (event logging)          │
│   ├─ Log to EEPROM                            │
│                                               │
│ CRITICAL:                                     │
│   ├─ Cut relay (power OFF) ⚡                │
│   ├─ Sound buzzer (500ms pulse)              │
│   ├─ LED = RED (blink)                        │
│   ├─ POST to backend (alert)                  │
│   ├─ Log to EEPROM                            │
│   └─ Cooldown: wait 5 seconds                 │
└───────────────────────────────────────────────┘
```

#### **Outcome:**
```
┌─ Backend Event Logging ────────────────────────┐
│ MQTT publish to "fence/events"                │
│                                               │
│ {                                             │
│   "timestamp": 1723634400000,                 │
│   "sensorId": "ESP32-001",                    │
│   "current": 2.45,                            │
│   "voltage": 380,                             │
│   "anomalyScore": 0.87,                       │
│   "eventType": "critical",                    │
│   "action": "relay_cut"                       │
│ }                                             │
└───────────────────────────────────────────────┘
        ↓
┌─ Dashboard Update (Real-Time) ────────────────┐
│ WebSocket broadcast to all connected clients │
│ Dashboard displays: 🔴 RED CRITICAL          │
│ User receives notification (email/SMS)       │
└───────────────────────────────────────────────┘
```

---

### Phase 3: Tamper Detection (Edge Case)

#### **Scenario: Fence wire cut or tamper detected**

```
STEP 1: Physical Breach
        ↓
STEP 2: Reed Switch Triggered
        ├─ GPIO interrupt fires immediately
        └─ Interrupt handler called
        ↓
STEP 3: Emergency Isolation (<1ms)
        ├─ Relay contact opens (power cut)
        ├─ Buzzer starts
        └─ LED turns RED
        ↓
STEP 4: Event Logging
        ├─ Create event: {type: "tamper", action: "relay_cut"}
        ├─ Publish via MQTT
        └─ Store in EEPROM (if offline)
        ↓
STEP 5: User Notification
        ├─ Dashboard alerts
        ├─ Email/SMS sent
        └─ Operator takes action
```

---

### Phase 4: Recovery (After Isolation)

#### **Manual Reset Process:**

```
STEP 1: Physical Inspection
        ├─ Operator checks fence
        └─ Identifies cause (tampering, wire fault, etc.)
        ↓
STEP 2: Reset Signal
        ├─ Press manual reset button on ESP32, OR
        ├─ Send "reset" command via MQTT, OR
        └─ Use Dashboard "Restore Power" button
        ↓
STEP 3: Relay Re-engagement
        ├─ Cooldown timer expires (5 seconds)
        ├─ ESP32 verifies current is normal
        └─ Relay contact closes (power restored)
        ↓
STEP 4: Verification
        ├─ Current sampling resumes
        ├─ LED transitions YELLOW → GREEN (if normal)
        ├─ Event posted: {action: "relay_restored"}
        └─ System returns to continuous monitoring
```

---

## Critical Scenarios

### Scenario A: High Current Spike (Accidental Short)

```
Timeline:
T=0ms:     Current jumps to 3.5A (short detected)
T=50ms:    ML model classifies as ANOMALY
T=60ms:    Threshold exceeded → relay cuts
T=100ms:   Event logged and sent to backend
T=500ms:   Dashboard shows RED alert
T=1000ms:  Operator reviews issue

Action: Manual inspection → If safe → Reset relay
```

### Scenario B: Gradual Voltage Drop (Aging Wire)

```
Timeline:
T=0:       Voltage steady at 380V
T=1min:    Voltage drops to 350V (slow degradation)
T=10min:   Voltage at 300V, anomaly_score rises gradually
T=20min:   anomaly_score > 0.5 → ALERT triggered
T=30min:   Backend receives multiple alerts
T=60min:   Dashboard shows YELLOW warning

Action: Predictive maintenance scheduled
```

### Scenario C: False Alarm (Power Fluctuation)

```
Timeline:
T=0:       Voltage spike to 420V (utility fluctuation)
T=50ms:    Raw sensor detects anomaly
T=100ms:   Filter smooths data → ML model says NORMAL
T=500ms:   No event posted (filter prevents false alarm)

Action: No operator action needed (system suppressed false alarm)
```

### Scenario D: Offline Operation (WiFi Lost)

```
Timeline:
T=0:       Connection lost to WiFi
T=10ms:    ESP32 detects offline condition
T=20ms:    Events still logged to local EEPROM
T=100ms:   Relay logic continues normally (independent)
T=5min:    WiFi reconnects
T=10min:   Buffered events synced to backend

Action: System operates autonomously, eventually catches up
```

---

## Data Pipeline (Complete Cycle)

```
SENSOR → FILTER → ML MODEL → DECISION → RELAY → LOG → DASHBOARD
  ↓        ↓         ↓          ↓        ↓      ↓      ↓
 INA219   RMS      TF-Lite   Score    GPIO   MQTT  Browser
 10ms    Average   <50ms     Check    1ms    Async  Real-time
  ↓        ↓         ↓          ↓        ↓      ↓      ↓
[Raw Data] [Clean]  [Classes] [Action] [Power] [Event] [View]
```

**Total Latency from Anomaly to Relay Cut: <100ms**

---

## State Machine

```
┌──────────────┐
│ INITIALIZING │
└──────┬───────┘
       │ (sensors ready, model loaded)
       ↓
┌──────────────────┐
│   MONITORING     │◄──────┐
│ (LED: GREEN)     │       │
└──────┬───────────┘       │
       │                   │
   (anomaly_score < 0.5)   │
       │                   │
       ↓                   │
┌──────────────────┐       │
│    ALERTING      │       │
│ (LED: YELLOW)    │       │
└──────┬───────────┘       │
       │                   │
   (anomaly_score >= 0.8)  │
       │                   │
       ↓                   │
┌──────────────────┐       │
│  CRITICAL        │       │
│ (LED: RED)       │       │
│ Relay: CUT       │       │
└──────┬───────────┘       │
       │                   │
   (manual reset)          │
       │                   │
       └───────────────────┘
```

---

## Event Types and Severity

| Event Type | Description | Severity | Action |
|------------|-------------|----------|--------|
| NORMAL | All sensors OK | Green | Continue |
| HIGH_CURRENT | Current exceeds threshold | Yellow | Alert |
| LOW_VOLTAGE | Voltage drops below threshold | Yellow | Alert |
| TAMPER_DETECTED | Reed switch triggered | Red | Isolate |
| BREAKDOWN | Sustained high current | Red | Isolate |
| RECOVERY | System restored after isolation | Green | Monitor |
| OFFLINE | Backend connection lost | Gray | Continue locally |

---

## Performance Metrics (Expected)

| Metric | Value |
|--------|-------|
| Sensor Sampling Rate | 100 Hz (10ms) |
| Feature Extraction Rate | 2 Hz (500ms) |
| ML Inference Latency | <50ms |
| Relay Isolation Time | 1-5ms |
| Total Detection-to-Action | <100ms |
| Dashboard Update Rate | 1-2 Hz (real-time) |
| Event Logging Latency | <500ms |
| False Positive Rate | <5% |
| System Uptime | >99.5% |

