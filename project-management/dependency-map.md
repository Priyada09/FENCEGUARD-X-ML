# Dependency Map — FENCEGUARD-X

**Purpose**: Visualize task dependencies to prevent bottlenecks  
**Last Updated**: 19 August 2026  

---

## Dependency Graph (Critical Path)

```
START (14-AUG)
    ↓
HW-01: Architecture Freeze
    ↓
HW-02: ESP32 + INA219        FW-01: Firmware Skeleton      ML-01: Problem Definition      BE-01: Backend Setup
    ↓                         ↓                              ↓                              ↓
HW-03: Prototype Build        FW-02: Sensor Acquisition    ML-02: Prepare Dataset        BE-02: Event Schema
    ↓                         ↓                              ↓                              ↓
HW-04: Tamper Detection       FW-03: Data Processing        ML-03: Feature Engineering    BE-03: POST API
    ↓                         ↓                              ↓                              ↓
HW-05: Safety Isolation       FW-04: Tamper Input          ML-04: Train Model            BE-04: GET Status
    ↓                         ↓                              ↓                              ↓
HW-06: Local Alarm            FW-05: Relay Control         ML-05: Evaluate               BE-05: Database
    ↓                         ↓                              ↓                              ↓
HW-07: Testing                FW-06: Structured Output      ML-06: Anomaly Score          BE-06: Integration
    ↓                         ↓                              ↓                              ↓
HW-08: HW/FW Integration      FW-07: Communication         ML-07: Model Export          BE-07: Dashboard API
    ╲                         ╱                              ╱                              ╱
     ╲                       ╱                              ╱                              ╱
      ╰─────────────────────┴──────────────────────────────┴──────────────────────────────╯
                                    ↓
                        INT-01: Sensor → Firmware (16-AUG 12:00)
                                    ↓
                        INT-02: Firmware → ML (16-AUG 18:00)
                                    ↓
                        INT-03: Firmware → Backend (16-AUG 20:00)
                                    ↓
                        INT-04: ML → Isolation (17-AUG 10:00)
                                    ↓
                        INT-05: Backend → Dashboard (17-AUG 14:00)
                                    ↓
                        INT-06: End-to-End Demo (18-AUG 18:00)
                                    ↓
                        M5: Feature Freeze (18-AUG 00:00)
                                    ↓
                        M6: Final Testing (19-AUG 18:00)
                                    ↓
                        M7: SIH Demo (20-AUG 10:00)
```

---

## Dependency Matrix (Who Blocks Whom)

| Dependent Task | Blocked By | Blocker Owner | Blocker Due | Days Buffer |
|---|---|---|---|---|
| FW-02 | HW-02 (INA219 working) | Anup | 15-AUG 12:00 | -2 |
| FW-03 | FW-02 (sensor data) | Anup | 15-AUG 18:00 | 1 |
| FW-05 | HW-05 (relay ready) | Anup | 16-AUG 15:00 | -1 |
| FW-06 | FW-03, FW-04, FW-05 | Anup | 16-AUG 20:00 | 1 |
| FW-07 | FW-06 (data structure) | Anup | 17-AUG 10:00 | 2 |
| ML-04 | ML-03 (features) + ML-02 (dataset) | Priyada | 16-AUG 12:00 | 0 |
| ML-07 | ML-06 (score) + TFLite tools | Priyada | 17-AUG 14:00 | 2 |
| ML-08 | ML-07 (model) + FW-06 (output format) | Priyada + Anup | 17-AUG 18:00 | 2 |
| BE-03 | BE-02 (schema) | Alok Kumar | 15-AUG 18:00 | 1 |
| BE-05 | BE-03 (POST) + BE-04 (GET) | Alok Kumar | 16-AUG 12:00 | 0 |
| BE-06 | BE-05 (DB) + FW-07 (communication) | Alok Kumar + Anup | 17-AUG 10:00 | 2 |
| BE-07 | BE-06 (integration) + DB-04 (dashboard) | Alok Kumar + Sakshi | 17-AUG 14:00 | 2 |
| DB-02 | BE-04 (API status) | Alok Kumar | 15-AUG 20:00 | 2 |
| DB-04 | DB-02 (component) + BE-07 (API) | Ananya + Alok Kumar | 17-AUG 10:00 | 2 |
| DB-05 | DB-04 (integration) | Ananya | 17-AUG 14:00 | 2 |
| INT-01 | HW-02, FW-03 | Anup | 16-AUG 12:00 | ⚠️ CRITICAL |
| INT-02 | FW-06, ML-07 | Anup + Priyada | 16-AUG 18:00 | ⚠️ CRITICAL |
| INT-03 | FW-07, BE-03 | Anup + Alok Kumar | 16-AUG 20:00 | ⚠️ CRITICAL |

---

## Critical Path Analysis

### Forward Dependency Chain (Longest)

```
HW-01 (0h)
  → HW-02 (12h)
    → HW-03 (36h)
      → HW-05 (60h)
        → HW-08 (86h) [Hardware done]
              ↓
        (Parallel with FW-01-07)
              ↓
        FW-01 (0h)
          → FW-02 (24h)
            → FW-03 (36h)
              → FW-06 (72h)
                → FW-07 (90h) [Firmware communication ready]
                      ↓
        (Parallel with ML-01-07, BE-01-07)
                      ↓
        ML-01 (0h)
          → ML-02 (24h)
            → ML-03 (36h)
              → ML-04 (60h)
                → ML-07 (84h)
                  → ML-08 (102h) [ML inference ready]
                        ↓
        BE-01 (0h)
          → BE-02 (12h)
            → BE-03 (24h)
              → BE-05 (48h)
                → BE-06 (72h)
                  → BE-07 (90h) [Backend integration ready]
                        ↓
                INT-01, INT-02, INT-03 (96h) ⚠️ INTEGRATION STARTS
                        ↓
                INT-04, INT-05, INT-06 (144h)
                        ↓
                DEMO (168h)
```

**Total critical path duration**: 168 hours (7 days exactly)  
**Slack time**: 0 hours  
**Schedule is razor-thin** — every day must execute perfectly

---

## Blocking Risk Analysis

### High-Risk Dependencies (If Slip, Everything Slips)

| Dependency | Risk | Owner | Mitigation |
|---|---|---|---|
| HW-02 (Sensors) | Hardware doesn't arrive | Anup | Order TODAY, same-day shipping if possible. Have spare. |
| FW-02 (Sensor reading) | Code won't compile | Anup | Set up Arduino IDE/PlatformIO NOW, test on demo ESP32 board. |
| ML-02 (Dataset) | Data collection too slow | Priyada | Start collecting TODAY. Use simulated data if real not available. |
| BE-02 (Database schema) | Schema too rigid | Alok Kumar | Design schema flexibly. Avoid strict validation early. |
| INT-03 (API integration) | Network unreliable | Alok Kumar + Anup | Test HTTP over WiFi, have USB fallback for testing. |

### Medium-Risk Dependencies (Can Be Worked Around)

| Dependency | Risk | Owner | Mitigation |
|---|---|---|---|
| HW-05 (Relay) | Relay damaged | Anup | Have spare relay. Use software simulation if needed. |
| ML-07 (Model export) | TFLite conversion fails | Priyada | Test conversion early, have ONNX fallback. |
| DB-04 (Dashboard integration) | API format mismatch | Ananya + Alok Kumar | Agree on API contract by 15-AUG, lock it. |
| INT-06 (End-to-end) | Latency too high | ALL | Profile early, optimize late. Know target <500ms total. |

---

## Parallel Work Opportunities (Reduce Dependency Risk)

### Days 1-2 (14-15 AUG)

These can happen in parallel, independently:

```
Anup (Hardware+Firmware)  Priyada (ML)           Alok Kumar (Backend)    Sakshi (Frontend)     Ananya (Presentation)
├─ HW-01                 ├─ FW-01                    ├─ ML-01                      ├─ BE-01                    ├─ PPT-01
├─ HW-02                 ├─ FW-02                    ├─ ML-02                      ├─ BE-02                    ├─ PPT-02
├─ HW-03                 └─ FW-03                    ├─ ML-03                      └─ BE-03                    └─ Task management
└─ HW-04                                            └─ (Start ML-04)

→ No blocking between modules yet
→ Each owner can work independently
→ Synchronize at INT phase (16-AUG)
```

### Day 3 (16 AUG)

Blocking starts. Modules must be ready to integrate:

```
FW-06 waiting for: HW-02 (input ready)
ML-07 waiting for: ML-03 (features complete) + FW-06 (output format)
BE-06 waiting for: FW-07 (communication) + BE-05 (API ready)
DB-04 waiting for: BE-07 (API endpoints)
```

**Critical**: If any prerequisite slips, escalate **immediately**.

---

## Risk Mitigation Parallel Work

For each task, identify what can happen in parallel:

### Example: FW-06 (Structured Output)

```
Primary Path (FW-06 depends on FW-03, FW-04, FW-05):
  Anup: FW-06 (start at 15-AUG 22:00, after FW-05 done)

Parallel Preparation:
  Alok Kumar: Design JSON format for firmware output
  Priyada: Design feature vector format for ML input
  Anup: Prepare test harness to simulate sensor data
  
Result: FW-06 completed faster because groundwork was laid
```

### Example: INT-03 (Firmware → Backend)

```
Primary Path (INT-03 depends on FW-07, BE-03):
  Anup + Alok: Integrate (start at 16-AUG 18:00)

Parallel Preparation:
  Anup: Set up WiFi hotspot for testing
  Ananya: Document the API contract in writing
  Priyada: Prepare test data to send to API
  
Result: INT-03 goes smoothly because all prep done
```

---

## Contingency Chains (If A Slips, Do B Instead)

### If HW-02 (Sensors) Slip Past 15-AUG 18:00

```
Plan A (Preferred): Get sensors working
Plan B (Backup): Use software simulation
  → FW-02 reads from random number generator (realistic range)
  → ML trains on simulated data
  → INT-03 uses simulated data in API
  
Cost: Loss of real hardware demo, but system still works
Timeline Impact: 0 hours (covered by parallel simulation)
```

### If ML-04 (Training) Gives Bad Accuracy (<80%)

```
Plan A (Preferred): Improve training
  → Get more/better data
  → Use Neural Network instead of Random Forest
  → Tune hyperparameters

Plan B (Backup): Fall back to deterministic thresholds
  → Disable ML predictions
  → Use ONLY voltage/current thresholds
  → Document limitation: "AI would enhance, but deterministic logic sufficient"
  
Cost: Loss of AI differentiation, but system still safer
Timeline Impact: 0 hours (thresholds already in FW-05)
```

### If INT-03 (Backend API) Fails Due to WiFi

```
Plan A (Preferred): Get WiFi working
  → Use personal hotspot
  → Hardwire backend to same network

Plan B (Backup): Use USB-based communication
  → Firmware writes events to UART
  → Python script on laptop reads UART → writes to API
  
Cost: Awkward demo, but integration proven
Timeline Impact: 4 hours (write USB bridge)
```

### If Dashboard Frontend Lags

```
Plan A (Preferred): Get React dashboard working
  → Build fast version with minimal styling
  → Use template components

Plan B (Backup): Use terminal/browser API explorer
  → Open Postman/curl in terminal
  → Show API responses directly
  → Explain: "API is core. UI is secondary."
  
Cost: Less impressive visually, but integration proven
Timeline Impact: 0 hours (API is what matters)
```

---

## Dependency Violation Detection

**If any of these happen, escalate immediately**:

- ❌ Task X marked DONE but Dependent Task Y says "still blocked"
- ❌ Owner of Task X and Owner of Dependent Y don't communicate
- ❌ Blocker owner doesn't update status daily
- ❌ Dependent task starts before blocker is actually DONE (not just "60% done")
- ❌ More than 1 task is blocked at same time (indicates root cause issue)

---

## Daily Dependency Check

**Every standup (10:00 AM), ask**:

1. Are all my blockers on track?
2. Is anyone waiting on me? Do I need to accelerate?
3. Do I have a contingency if my blocker slips?

**If answer to (1) or (2) is NO**:

→ Escalate to Anup (integration lead) immediately  
→ Do not wait until end of day

---

## Dependency Status (Updated 14-AUG)

```
14-AUG 09:30: All tasks are at "READY TO START" state
              No blockers yet (all prerequisites are setup/architecture)

15-AUG 18:00: CHECKPOINT 1
              Check that Module Baselines (M2) are all DONE
              If any P0 task is BLOCKED, escalate

16-AUG 12:00: CHECKPOINT 2
              Check that INT-01 is working
              If not, assembly task force immediately

16-AUG 18:00: CHECKPOINT 3
              Check that INT-02 is working

16-AUG 20:00: CHECKPOINT 4
              Check that INT-03 is working
              
17-AUG 18:00: CHECKPOINT 5
              Check that all integrations (INT-01 through INT-06) are DONE
              If not, emergency meeting to replan remaining 3 days
```

---

**Dependency ownership**: Anup monitors overall + each owner monitors dependencies in their domain

