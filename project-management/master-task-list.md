# Master Task List — FENCEGUARD-X

**Last Updated**: 19 August 2026  
**Current Active Team**: Anup, Priyada, Alok, Sakshi, Ananya  
**Current Ownership Model**: Hardware + Firmware → Anup; ML → Priyada; Backend + DB → Alok; Frontend + Deployment → Sakshi; Presentation → Ananya

---

## Task Format

```
TASK_ID | Task Name | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes
```

---

## 🔧 HARDWARE + FIRMWARE TASKS (ANUP)

### P0 — Critical

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| HW-01 | Finalize hardware architecture | Anup | P0 | DONE | 14-AUG 23:59 | None | Circuit diagram reviewed by team, BOM complete | Safe low-voltage design only |
| HW-02 | ESP32 + INA219 integration | Anup | P0 | DONE | 15-AUG 18:00 | HW-01 | INA219 produces stable readings ±1% | I2C protocol working |
| HW-03 | Safe low-voltage prototype build | Anup | P0 | DONE | 16-AUG 12:00 | HW-02 | Prototype built, electrically safe, isolated | No mains voltage exposure |
| HW-04 | Tamper detection setup | Anup | P0 | DONE | 15-AUG 20:00 | HW-01 | Motion sensor integrated and validated | Real raw data captured |
| HW-05 | Safety isolation mechanism | Anup | P0 | TODO | 16-AUG 15:00 | HW-02 | Relay responds to safety signal, cuts power | Fail-safe design verified |
| HW-06 | Local alarm (buzzer + LEDs) | Anup | P0 | TODO | 16-AUG 20:00 | HW-05 | Buzzer sounds, LEDs light on abnormal condition | Audio-visual feedback working |
| HW-07 | Hardware testing & validation | Anup | P0 | TODO | 18-AUG 12:00 | HW-06 | All sensors functioning, relay response <5ms, safety verified | Stress testing complete |
| HW-08 | Hardware/firmware integration | Anup | P0 | TODO | 18-AUG 18:00 | HW-07 | Firmware commands relay successfully, reads all sensors | Full integration verified |
| FW-01 | ESP32 firmware skeleton | Anup | P0 | TODO | 14-AUG 23:59 | None | Microcontroller tasks created and code compiles | GPIO and sensor initialization |
| FW-02 | Sensor data acquisition | Anup | P0 | TODO | 15-AUG 18:00 | FW-01, HW-02 | INA219 reads current, ADC reads voltage at 100Hz | Raw data stable |
| FW-03 | Voltage/current data processing | Anup | P0 | TODO | 15-AUG 20:00 | FW-02 | RMS, peak, variance calculated from raw samples | Feature extraction working |
| FW-04 | Tamper input handling | Anup | P0 | TODO | 16-AUG 12:00 | FW-01, HW-04 | GPIO interrupt fires on tamper, debounced | <10ms latency |
| FW-05 | Relay/safety controller logic | Anup | P0 | TODO | 16-AUG 15:00 | FW-03, HW-05 | Relay responds to safety signal, isolation verified | Fail-safe tested |
| FW-06 | Structured sensor output | Anup | P0 | TODO | 16-AUG 20:00 | FW-03, FW-04, FW-05 | Firmware outputs timestamp + sensor data structure | Ready for ML + backend |
| FW-07 | Communication interface (MQTT/REST) | Anup | P0 | TODO | 17-AUG 10:00 | FW-06 | Can publish events to backend endpoint | Configurable backend URL |
| FW-08 | Firmware testing & stability | Anup | P0 | TODO | 18-AUG 14:00 | FW-07 | Firmware runs without crash, memory stable | Watchdog tested |

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| HW-09 | Sensor filtering/calibration | Anup | P1 | TODO | 17-AUG 10:00 | HW-02 | Filter reduces noise to <2% false alarm rate | Calibration procedure documented |
| HW-10 | Status indicators documentation | Anup | P1 | TODO | 17-AUG 18:00 | HW-06 | LED/buzzer behavior documented in spec | User can interpret system status |
| HW-11 | Hardware documentation | Anup | P1 | TODO | 18-AUG 12:00 | HW-08 | Circuit schematics, wiring, assembly guide complete | Anyone can replicate setup |
| HW-12 | Integration testing (HW + FW) | Anup | P1 | TODO | 18-AUG 20:00 | HW-08 | Hardware responds to firmware commands reliably | Test matrix complete |
| FW-09 | Error handling | Anup | P1 | TODO | 17-AUG 18:00 | FW-08 | Graceful degradation on sensor failure, fallback logic | No hard crashes |
| FW-10 | Reconnection handling (WiFi) | Anup | P1 | TODO | 17-AUG 18:00 | FW-07 | WiFi reconnects automatically, maintains local operation | Offline mode verified |
| FW-11 | Firmware documentation | Anup | P1 | TODO | 18-AUG 18:00 | FW-08 | Code comments, README, architecture explained | Maintainable |

---

## 🧠 ML TASKS (PRIYADA)

### P0 — Critical

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| ML-01 | Define classification problem | Priyada | P0 | TODO | 14-AUG 23:59 | None | Classes defined: NORMAL, ELECTRICAL_FAULT, PHYSICAL_TAMPER, BREACH | Clear decision boundaries |
| ML-02 | Prepare dataset | Priyada | P0 | TODO | 15-AUG 14:00 | ML-01 | Real datasets ingested and validated | Data source documented |
| ML-03 | Feature engineering | Priyada | P0 | TODO | 15-AUG 18:00 | ML-02 | Motion and electrical features extracted | Feature correlation analyzed |
| ML-04 | Train baseline model | Priyada | P0 | TODO | 16-AUG 12:00 | ML-03 | Model trained on split data and evaluated | Scikit-learn baseline |
| ML-05 | Model evaluation & metrics | Priyada | P0 | TODO | 16-AUG 15:00 | ML-04 | Accuracy, precision, recall, F1-score documented | Confusion matrix created |
| ML-06 | Anomaly score implementation | Priyada | P0 | TODO | 17-AUG 10:00 | ML-05 | Model outputs confidence values | Threshold tuned for false-negative analysis |
| ML-07 | Export model for inference | Priyada | P0 | TODO | 17-AUG 14:00 | ML-06 | Model saved in portable format | Inference compatibility reviewed |
| ML-08 | Live inference testing | Priyada | P0 | TODO | 17-AUG 18:00 | ML-07, FW-06 | Model runs on live or recorded sensor data | End-to-end inference verified |

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| ML-09 | Explainability/feature importance | Priyada | P1 | TODO | 18-AUG 12:00 | ML-05 | Which features matter most documented | Judges can understand model |
| ML-10 | Model limitations documented | Priyada | P1 | TODO | 18-AUG 18:00 | ML-09 | What model CANNOT do clearly stated | No false claims |

---

## 💻 BACKEND TASKS (ALOK KUMAR)

### P0 — Critical

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| BE-01 | Backend setup | Alok Kumar | P0 | TODO | 14-AUG 23:59 | None | Node.js server running on localhost | Express + database ready |
| BE-02 | Event schema design | Alok Kumar | P0 | TODO | 15-AUG 12:00 | BE-01 | Event schema defined | Supports all event types |
| BE-03 | POST event API | Alok Kumar | P0 | TODO | 15-AUG 18:00 | BE-02 | /api/v1/events accepts events | Event persists to DB |
| BE-04 | GET status API | Alok Kumar | P0 | TODO | 15-AUG 20:00 | BE-02 | /api/v1/fence/status returns current state | Timestamp accurate |
| BE-05 | Database integration | Alok Kumar | P0 | TODO | 16-AUG 12:00 | BE-03, BE-04 | CRUD operations working | Queries optimized |
| BE-06 | ESP32 to backend integration | Alok Kumar | P0 | TODO | 17-AUG 10:00 | BE-05, FW-07 | Events flow to API and database | No data loss |
| BE-07 | Frontend API endpoints | Alok Kumar | P0 | TODO | 17-AUG 14:00 | BE-06 | API supports dashboard queries | Latency acceptable |
| BE-08 | Backend testing | Alok Kumar | P0 | TODO | 18-AUG 14:00 | BE-07 | API tests pass | Stability tested |

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| BE-09 | Incident/alert endpoints | Alok Kumar | P1 | TODO | 18-AUG 12:00 | BE-07 | Dashboard can retrieve critical events | Can filter by severity |
| BE-10 | Backend documentation | Alok Kumar | P1 | TODO | 18-AUG 18:00 | BE-08 | API documentation complete | Anyone can use API |

---

## 🎨 FRONTEND + DEPLOYMENT TASKS (SAKSHI)

### P0 — Critical

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| DB-01 | Dashboard setup | Sakshi | P0 | TODO | 14-AUG 23:59 | None | App environment ready, basic page structure | Compiles without errors |
| DB-02 | Fence status component | Sakshi | P0 | TODO | 15-AUG 18:00 | DB-01, BE-04 | Displays current status and last event | Updates when API called |
| DB-03 | Event history view | Sakshi | P0 | TODO | 16-AUG 12:00 | DB-02, BE-05 | Events displayed in table/list | Can scroll through history |
| DB-04 | Dashboard/backend integration | Sakshi | P0 | TODO | 17-AUG 10:00 | DB-03, BE-07 | Dashboard fetches data from API | Live status works |
| DB-05 | Real-time updates (WebSocket/polling) | Sakshi | P0 | TODO | 17-AUG 14:00 | DB-04 | Dashboard updates without refresh | Live-ish experience |
| DB-06 | Visual alerts | Sakshi | P0 | TODO | 17-AUG 18:00 | DB-05 | Critical events highlighted | Color-coded |
| DB-07 | Dashboard testing | Sakshi | P0 | TODO | 18-AUG 14:00 | DB-06 | Dashboard loads, displays data, handles errors | Mobile responsive |
| DEP-01 | Demo hosting / deployment | Sakshi | P0 | TODO | 18-AUG 18:00 | DB-07 | App is available for demo and review | Demo-hosting path validated |

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| DB-08 | Dashboard documentation | Sakshi | P1 | TODO | 18-AUG 18:00 | DB-07 | How to use dashboard documented | User guide created |

---

## 🔗 INTEGRATION TASKS (ALL TEAM)

### P0 — Critical

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| INT-01 | ESP32 sensor → firmware processing | Anup | P0 | TODO | 16-AUG 12:00 | HW-02, FW-03 | Sensor data read and processed, no crashes | Demonstrated in hardware test |
| INT-02 | Firmware → ML inference | Anup + Priyada | P0 | TODO | 16-AUG 18:00 | FW-06, ML-07 | Real sensor data classified by ML model | Classification output verified |
| INT-03 | Firmware → Backend API | Anup + Alok | P0 | TODO | 16-AUG 20:00 | FW-07, BE-03 | ESP32 publishes event, API receives and stores it | End-to-end event flow |
| INT-04 | ML decision → Safety isolation | Priyada + Anup | P0 | TODO | 17-AUG 10:00 | ML-08, HW-05, FW-05 | When ML predicts FAULT/TAMPER, relay cuts | Safety mechanism verified |
| INT-05 | Backend → Dashboard | Alok + Sakshi | P0 | TODO | 17-AUG 14:00 | BE-07, DB-04 | Events appear on dashboard, status updates live | Real-time view working |
| INT-06 | Complete end-to-end demo | ALL | P0 | TODO | 18-AUG 18:00 | INT-01 through INT-05 | Trigger event → ESP32 detects → ML classifies → Relay isolates → Alert → Dashboard shows | Full pipeline working |
| INT-07 | Offline operation verification | ALL | P0 | TODO | 19-AUG 10:00 | INT-06 | System operates locally without WiFi, safety still functions | WiFi disconnected test passed |

---

## 📊 PRESENTATION TASKS (ANANYA)

### P0 — Critical

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| PPT-01 | Problem statement slide | Ananya | P0 | TODO | 15-AUG 18:00 | None | Clear problem defined, impacts shown | Judges understand the issue |
| PPT-02 | Existing gap slide | Ananya | P0 | TODO | 15-AUG 20:00 | PPT-01 | Current solutions analyzed, gaps identified | Competitive analysis clear |
| PPT-03 | Proposed solution slide | Ananya | P0 | TODO | 16-AUG 12:00 | PPT-02 | FENCEGUARD-X approach explained | Value proposition clear |
| PPT-04 | System architecture slide | Ananya | P0 | TODO | 16-AUG 15:00 | PPT-03 | Block diagram, data flow shown | Judges understand design |
| PPT-05 | Working flow slide | Ananya | P0 | TODO | 16-AUG 20:00 | PPT-04 | How system operates step-by-step | Normal + edge cases shown |
| PPT-06 | AI/ML slide | Ananya | P0 | TODO | 17-AUG 12:00 | ML-05, PPT-05 | Model accuracy, features, decision logic shown | No false claims |
| PPT-07 | Innovation slide | Ananya | P0 | TODO | 17-AUG 14:00 | PPT-06 | What's unique/novel about FENCEGUARD-X | Competitive edge clear |
| PPT-08 | Impact & use cases slide | Ananya | P0 | TODO | 17-AUG 16:00 | PPT-07 | Real-world applications, market potential | Scalability discussed |
| PPT-09 | Live demo flow | Ananya | P0 | TODO | 18-AUG 12:00 | INT-06 | Demo narrated step-by-step in slides | Judges know what to expect |
| PPT-10 | Final PPT review & polish | Ananya | P0 | TODO | 18-AUG 18:00 | PPT-01 through PPT-09 | All slides reviewed by team, consistent branding, no typos | Presentation-ready |

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| PPT-11 | Q&A preparation | Ananya | P1 | TODO | 19-AUG 14:00 | PPT-10 | FAQ document created, team trained on answers | 20+ questions answered |

---

## 📝 TESTING & VALIDATION TASKS (ALL TEAM)

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| TEST-01 | Hardware stress test | Anup | P1 | TODO | 19-AUG 10:00 | HW-08 | System runs 4+ hours without failure | Reliability demonstrated |
| TEST-02 | Firmware crash testing | Anup | P1 | TODO | 19-AUG 12:00 | FW-08 | System recovers from sensor errors, connection loss | Resilience verified |
| TEST-03 | ML model robustness | Priyada | P1 | TODO | 19-AUG 14:00 | ML-10 | Model tested on edge cases | Limitations understood |
| TEST-04 | Backend API load test | Alok Kumar | P1 | TODO | 19-AUG 16:00 | BE-08 | API handles 10+ events/sec, no data loss | Performance acceptable |
| TEST-05 | Dashboard UX test | Sakshi | P1 | TODO | 19-AUG 18:00 | DB-07 | Dashboard usable by non-technical judge | No confusion |
| TEST-06 | Full system integration test | ALL | P1 | TODO | 19-AUG 20:00 | TEST-01 through TEST-05 | End-to-end system tested under real conditions | All scenarios pass |

---

## 📚 DOCUMENTATION TASKS (ALL)

### P1 — High

| ID | Task | Owner | Priority | Status | Deadline | Dependency | Definition of Done | Notes |
|----|------|-------|----------|--------|----------|------------|-------------------|-------|
| DOC-01 | GitHub README finalization | Ananya | P1 | TODO | 18-AUG 18:00 | All modules | Complete project overview in GitHub | Anyone can clone and understand |
| DOC-02 | Module READMEs | Each Owner | P1 | TODO | 18-AUG 18:00 | Each module | How to set up each module documented | Reproducible |
| DOC-03 | Architecture document finalization | Anup + Alok | P1 | TODO | 18-AUG 18:00 | INT-06 | Final architecture locked in docs | No more changes post-deadline |
| DOC-04 | Demo checklist & script | Ananya | P1 | TODO | 19-AUG 10:00 | PPT-09 | Step-by-step demo walkthrough documented | Team rehearsed |

---

## Summary by Status

```
BACKLOG (5):      Not yet prioritized
TODO (35):        Ready to start
IN PROGRESS (0):  Currently being worked on
REVIEW (0):       Awaiting approval
DONE (7):         Documentation files from setup
BLOCKED (0):      Waiting on dependency
```

---

## Summary by Priority

- **P0 (Critical)**: 27 tasks — MUST complete by 18 August
- **P1 (High)**: 15 tasks — Complete if time permits
- **P2-P3 (Lower)**: 5 tasks — Nice to have

---

## Critical Path (Must Not Slip)

1. **14 AUG**: HW-01, FW-01, ML-01 → Architecture frozen
2. **15 AUG**: HW-02, FW-02, ML-02 → Basic modules exist
3. **16 AUG**: INT-01, INT-02, INT-03 → First integration
4. **17 AUG**: INT-04, INT-05, INT-06 → End-to-end working
5. **18 AUG**: Feature freeze, all P0 DONE
6. **19 AUG**: Testing, rehearsal
7. **20 AUG**: Present to judges

---

**If any P0 task is delayed past its deadline, escalate immediately.**

