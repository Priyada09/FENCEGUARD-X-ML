# Decision Log — FENCEGUARD-X

**Purpose**: Record all major technical and project decisions.  
**Last Updated**: 14 August 2026  

---

## Decision Format

```
DECISION-ID:
Date:
Decision:
Reason:
Alternatives Considered:
Chosen Approach:
Owner:
Impact:
Reversible:
Status:
```

---

## Core Architecture Decisions

### DECISION-001: Edge AI vs Cloud AI

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-001 |
| **Date** | 14 August 2026 |
| **Decision** | Process AI/ML inference on ESP32 edge controller, not cloud |
| **Reason** | Safety requires <100ms latency. WiFi roundtrip too slow. Offline capability needed. |
| **Alternatives** | 1) Cloud AI — cloud-based model inference; 2) Hybrid — local + cloud |
| **Chosen** | Edge AI on ESP32 using TensorFlow Lite Micro |
| **Owner** | Priyada + Anup |
| **Impact** | Model must be <200KB, inference <50ms, framework constrained to TFLite |
| **Reversible** | Partially — model training is TFLite-specific |
| **Status** | LOCKED (architecture-critical) |

**Notes**:
- Ensures autonomous operation without internet
- Adds complexity: model optimization for microcontroller
- Justifiable for safety system

---

### DECISION-002: Deterministic Safety Logic + ML Classification

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-002 |
| **Date** | 14 August 2026 |
| **Decision** | AI failure must NOT cause safety failure. Use deterministic rule-based thresholds + ML as enhancer. |
| **Reason** | Safety systems require fail-safe guarantees. ML inherently uncertain. Need independent protection path. |
| **Alternatives** | 1) ML-only decision; 2) Only thresholds (no ML) |
| **Chosen** | Layered: Hard thresholds (always active) + ML score (optional refinement) |
| **Owner** | Anup + Priyada |
| **Impact** | Requires dual logic: deterministic + probabilistic. More code, more testing. |
| **Reversible** | Yes — can revert to threshold-only if ML fails |
| **Status** | LOCKED |

**Logic**:
```
IF voltage_drop > THRESHOLD_CRITICAL
   OR current_spike > THRESHOLD_CRITICAL
   → ISOLATE (automatic, no ML)

IF ML_score(TAMPER) > 0.8
   AND voltage_change moderate
   → ISOLATE (with ML confirmation)

IF no_critical_event
   → Monitor locally
```

---

### DECISION-003: Safe Low-Voltage Prototype Only

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-003 |
| **Date** | 14 August 2026 |
| **Decision** | Prototype uses only safe low-voltage (<50V). No high-voltage/mains exposure during development/testing. |
| **Reason** | Team safety, SIH regulations, liability concerns. High-voltage remains conceptual/system-level discussion. |
| **Alternatives** | 1) Real high-voltage setup (dangerous); 2) Simulation only (no hardware) |
| **Chosen** | Safe demo hardware with scaled sensors that can be adapted to high-voltage conceptually |
| **Owner** | Anup |
| **Impact** | Hardware is proof-of-concept. Real-world would require certified protection gear & hardware. |
| **Reversible** | Yes — concept scales but requires re-certification |
| **Status** | LOCKED |

**Notes**:
- Judges understand this is prototype/demo
- Real deployment would involve licensed electricians + certified equipment
- Sufficient to demonstrate concept

---

## Hardware Component Decisions

### DECISION-004: ESP32 as Main Controller

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-004 |
| **Date** | 14 August 2026 |
| **Decision** | Use ESP32 (not STM32) as primary microcontroller |
| **Reason** | WiFi built-in, lower cost, better Arduino support, sufficient performance for ML inference |
| **Alternatives** | STM32H7 (more powerful but more expensive) |
| **Chosen** | ESP32 |
| **Owner** | Anup |
| **Impact** | Constrains to ~240 MHz, 520KB RAM. Model size <200KB. Latency target <50ms. |
| **Reversible** | Partially — C code portable but WiFi library ESP32-specific |
| **Status** | LOCKED |

**Performance Targets**:
- Sensor sampling: 100 Hz
- Feature extraction: <500ms
- ML inference: <50ms
- Safety isolation: <100ms total

---

### DECISION-005: INA219 for Current Sensing

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-005 |
| **Date** | 14 August 2026 |
| **Decision** | Use INA219 (±3.2A, I2C) for current measurement |
| **Reason** | Accurate, low cost, I2C digital interface, built-in shunt resistor |
| **Alternatives** | 1) ACS712 (analog out); 2) Custom shunt + ADC |
| **Chosen** | INA219 |
| **Owner** | Anup |
| **Impact** | Limited to low-current measurements (±3.2A). Real 300A+ fence would need larger sensor. |
| **Reversible** | Yes — same I2C interface works with other sensors |
| **Status** | LOCKED |

---

### DECISION-006: Relay-Based Isolation

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-006 |
| **Date** | 14 August 2026 |
| **Decision** | Use normally-closed relay for fail-safe isolation |
| **Reason** | Fails safe (cuts power on relay failure), no external power needed to cut power |
| **Alternatives** | MOSFET (faster but not fail-safe), SCR (latching, requires controlled turn-off) |
| **Chosen** | Normally-closed relay |
| **Owner** | Anup |
| **Impact** | Relay response ~50-100ms. Slower than solid-state but safer. |
| **Reversible** | Yes |
| **Status** | LOCKED |

---

## ML/AI Decisions

### DECISION-007: Classification Problem Definition

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-007 |
| **Date** | 14 August 2026 |
| **Decision** | Define 3 classes: NORMAL, TAMPERING, ELECTRICAL_FAULT |
| **Reason** | Captures main scenarios. Simpler than 5+ classes. Data collection feasible in 7 days. |
| **Alternatives** | 1) Binary (normal vs abnormal); 2) 5+ classes (too granular) |
| **Chosen** | 3-class (NORMAL, TAMPERING, FAULT) |
| **Owner** | Priyada |
| **Impact** | Requires 300-500 balanced training samples (50-50-50 split). Feasible. |
| **Reversible** | Partially — can merge classes late if needed |
| **Status** | LOCKED |

---

### DECISION-008: Random Forest Model (Baseline)

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-008 |
| **Date** | 14 August 2026 |
| **Decision** | Start with Random Forest. If insufficient, evaluate neural network. |
| **Reason** | Fast to train, interpretable (feature importance), works well with small datasets, TFLite-compatible |
| **Alternatives** | 1) Neural Network (more powerful, less interpretable); 2) SVM (slow inference on embedded) |
| **Chosen** | Random Forest → Neural Network (if needed) |
| **Owner** | Priyada |
| **Impact** | Random Forest is baseline. Can be replaced. TFLite conversion straightforward. |
| **Reversible** | Yes — can switch models |
| **Status** | Locked for now, flexible |

---

## Backend Decisions

### DECISION-009: MongoDB for Event Storage

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-009 |
| **Date** | 14 August 2026 |
| **Decision** | Use MongoDB (not SQL) for event persistence |
| **Reason** | Schema-flexible (events may have varying fields), JSON-native (matches API), easy scaling |
| **Alternatives** | PostgreSQL (structured, mature) |
| **Chosen** | MongoDB Atlas (managed service) |
| **Owner** | Alok Kumar |
| **Impact** | Queries simpler with JSON. Indexing on timestamp + event_type for performance. |
| **Reversible** | Partially — would require schema migration |
| **Status** | LOCKED |

---

### DECISION-010: REST API (not gRPC/GraphQL)

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-010 |
| **Date** | 14 August 2026 |
| **Decision** | Use REST API (JSON over HTTP) for ESP32 ↔ Backend communication |
| **Reason** | Simple, widely understood, ESP32 libraries readily available, adequate for this scale |
| **Alternatives** | 1) MQTT (pub/sub, better for IoT); 2) GraphQL (overkill for demo) |
| **Chosen** | REST API with HTTP POST for events |
| **Owner** | Alok Kumar + Anup |
| **Impact** | Can't be production-scale (would need MQTT later). Sufficient for demo. |
| **Reversible** | Yes — can migrate to MQTT |
| **Status** | LOCKED for 7-day hackathon |

---

## Frontend Decisions

### DECISION-011: React + Vite Dashboard

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-011 |
| **Date** | 14 August 2026 |
| **Decision** | Use React 18 + Vite for dashboard frontend |
| **Reason** | Modern, fast build, good for real-time updates with hooks/state management |
| **Alternatives** | Vue (lighter), vanilla HTML (too basic) |
| **Chosen** | React + Vite |
| **Owner** | Ananya |
| **Impact** | Requires npm environment. Learning curve if unfamiliar. But powerful. |
| **Reversible** | Yes |
| **Status** | LOCKED |

---

## Project Management Decisions

### DECISION-012: GitHub as Single Source of Truth

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-012 |
| **Date** | 14 August 2026 |
| **Decision** | Use GitHub Issues + Project Board as primary task tracking (not Jira, Trello, etc.) |
| **Reason** | Already have GitHub repo. Integrated with code. Free. Real-time updates. |
| **Alternatives** | Jira (enterprise), Trello (simple but disconnected) |
| **Chosen** | GitHub |
| **Owner** | Ananya (PM) |
| **Impact** | All communication goes to GitHub. Team discipline required. |
| **Reversible** | Yes |
| **Status** | LOCKED |

---

### DECISION-013: Feature Freeze on 18-AUG 00:00

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-013 |
| **Date** | 14 August 2026 |
| **Decision** | Hard feature freeze on 18 August at midnight. Only bugfixes after. |
| **Reason** | 7-day timeline extremely tight. 18-AUG freeze allows 1.5 days for testing + 0.5 day rehearsal. |
| **Alternatives** | Soft freeze (allow exceptions), no freeze (chaos) |
| **Chosen** | Hard freeze |
| **Owner** | Anup + Ananya |
| **Impact** | Any feature not DONE by 18-AUG midnight does NOT ship. Period. |
| **Reversible** | No — cannot be extended |
| **Status** | LOCKED |

---

### DECISION-014: Daily 10 AM Standup

| Property | Value |
|----------|-------|
| **Decision ID** | DECISION-014 |
| **Date** | 14 August 2026 |
| **Decision** | Mandatory daily standup at 10:00 AM (14-20 AUG) |
| **Reason** | 7 days is short. Daily sync prevents silent failures. Quick escalation of blockers. |
| **Alternatives** | Twice-daily (overkill), weekly (too rare) |
| **Chosen** | Daily 10 AM |
| **Owner** | Ananya (scheduling) |
| **Impact** | 10-minute time commitment daily. Non-negotiable. |
| **Reversible** | Yes, but not recommended |
| **Status** | LOCKED |

---

## Decision Review Process

Every decision should be reviewed if:
- New blocker discovered contradicts the decision
- Original assumption proves false
- Better alternative emerges

**Review process**:
1. Notify team in standup
2. Document reason for review
3. Vote if consensus unclear
4. Update decision with new date/status

---

## Locked vs. Flexible Decisions

| Decision | Lock Status | Can Override If | |
|----------|------------|-----------------|-----|
| DECISION-001 (Edge AI) | 🔴 LOCKED | Impossible to meet latency requirement | Architecture-critical |
| DECISION-002 (Deterministic + ML) | 🔴 LOCKED | Safety compromise not acceptable | Safety-critical |
| DECISION-003 (Safe low-voltage) | 🔴 LOCKED | Team safety non-negotiable | Liability |
| DECISION-004 (ESP32) | 🟡 FLEXIBLE | Major performance issue discovered | Can pivot to STM32 if needed |
| DECISION-005 (INA219) | 🟡 FLEXIBLE | Sensor doesn't arrive (use alternative) | Similar I2C sensors interchangeable |
| DECISION-006 (Relay isolation) | 🟡 FLEXIBLE | Relay fails (use MOSFET + watchdog) | Can adapt |
| DECISION-007 (3-class) | 🟡 FLEXIBLE | Dataset allows 4+ classes | Can expand classes |
| DECISION-008 (Random Forest) | 🟡 FLEXIBLE | Model underperforms (switch to NN) | Can pivot |
| DECISION-009 (MongoDB) | 🟡 FLEXIBLE | Can't get Atlas (use local) | Schema portable |
| DECISION-010 (REST API) | 🟡 FLEXIBLE | Can add MQTT later | Not production-critical |
| DECISION-011 (React) | 🟡 FLEXIBLE | Team struggles (pivot to Vue) | UI is secondary |
| DECISION-012 (GitHub tracking) | 🟡 FLEXIBLE | GitHub down (use Jira temporarily) | Process not tool-dependent |
| DECISION-013 (Feature freeze) | 🔴 LOCKED | Deadline non-negotiable | SIH is 20-AUG hard date |
| DECISION-014 (Daily standup) | 🔴 LOCKED | Communication critical | Accountability |

---

**Next Decision Review**: 15 August 2026, 6:00 PM  
**Process**: Any new decisions must be logged here within 24 hours

