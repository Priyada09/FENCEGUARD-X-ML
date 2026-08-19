# FENCEGUARD-X GitHub Project Setup

## GitHub Project Board: "FENCEGUARD-X — SIH Internal 20 AUG"

### Column Structure

```
[BACKLOG] ↓ [TODO] ↓ [IN PROGRESS] ↓ [REVIEW] ↓ [DONE] ↓ [BLOCKED]
```

---

## Workflow Rules

### Task Lifecycle

1. **BACKLOG**: New task, not yet assigned
2. **TODO**: Assigned to someone, ready to start
3. **IN PROGRESS**: Currently being worked on
4. **REVIEW**: Completed, awaiting approval/testing
5. **DONE**: Verified and merged
6. **BLOCKED**: Waiting on dependency or external input

### Every Task Must Have

- **Owner**: Assigned team member
- **Deadline**: Specific date/time
- **Priority**: P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
- **Status**: One of the columns above
- **Labels**: Module tags (hardware, firmware, ml, backend, dashboard)

---

## GitHub Issues Template

### Format
```markdown
## Task Title
**Issue**: MODULE-XX
**Owner**: @person
**Deadline**: YYYY-MM-DD HH:MM
**Priority**: P0/P1/P2/P3
**Module**: hardware/firmware/ml/backend/dashboard/integration/presentation

## Description
[Clear description of what needs to be done]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blockers
None / [Link to blocking issue]

## Subtasks
- [ ] Subtask 1
- [ ] Subtask 2
```

---

## All Issues to Create (TODAY - 14 AUG)

### 🔧 IoT & Hardware — ANUP

**IOT-01: Finalize hardware architecture**
- Owner: Anup
- Deadline: 14-AUG 23:59
- Priority: P0 (Critical)
- Description: Finalize ESP32 circuit design, sensor connections, relay logic
- Acceptance: Circuit diagram reviewed and approved

**IOT-02: ESP32 + INA219 integration**
- Owner: Anup
- Deadline: 15-AUG 18:00
- Priority: P0
- Description: Set up I2C communication, calibrate current sensor
- Acceptance: Can read accurate current values ±1%

**IOT-03: Tamper detection**
- Owner: Anup
- Deadline: 15-AUG 20:00
- Priority: P0
- Description: Integrate reed switch, interrupt handling
- Acceptance: Detects tamper within 10ms

**IOT-04: Relay/isolation mechanism**
- Owner: Anup
- Deadline: 16-AUG 12:00
- Priority: P0
- Description: Wire relay coil, test isolation logic, debouncing
- Acceptance: Relay cuts power reliably, 5ms response time

**IOT-05: Buzzer + status indicators**
- Owner: Anup
- Deadline: 16-AUG 15:00
- Priority: P1
- Description: Configure buzzer PWM, LED status indicators (red/yellow/green)
- Acceptance: All indicators working, correct states

**IOT-06: Safe low-voltage fence prototype**
- Owner: Anup
- Deadline: 17-AUG 10:00
- Priority: P0
- Description: Build working prototype with safety testing
- Acceptance: No electrical hazards, properly isolated

**IOT-07: Hardware testing**
- Owner: Anup
- Deadline: 18-AUG 14:00
- Priority: P1
- Description: Full hardware testing, stress testing, edge cases
- Acceptance: All tests pass, performance within spec

**IOT-08: Final hardware integration**
- Owner: Anup
- Deadline: 18-AUG 20:00
- Priority: P0
- Description: Package in enclosure, weatherproofing, final checks
- Acceptance: Ready for field deployment

---

### ⚙️ Firmware — ANUP

**FW-01: ESP32 firmware skeleton**
- Owner: Anup
- Deadline: 14-AUG 23:59
- Priority: P0
- Description: Set up FreeRTOS tasks, GPIO init, main loop
- Acceptance: Firmware compiles, ESP32 boots

**FW-02: Sensor data acquisition**
- Owner: Anup
- Deadline: 15-AUG 18:00
- Priority: P0
- Description: INA219 I2C driver, ADC sampling, 100Hz rate
- Acceptance: Sensor readings accurate and consistent

**FW-03: Data filtering**
- Owner: Anup
- Deadline: 15-AUG 20:00
- Priority: P1
- Description: Moving average filter, outlier rejection
- Acceptance: False alarm rate <5%

**FW-04: Tamper event handling**
- Owner: Anup
- Deadline: 16-AUG 12:00
- Priority: P0
- Description: Interrupt handler for reed switch
- Acceptance: <10ms detection latency

**FW-05: Relay control**
- Owner: Anup
- Deadline: 16-AUG 15:00
- Priority: P0
- Description: GPIO relay driver, safety logic, cooldown
- Acceptance: Relay responds reliably

**FW-06: Communication protocol**
- Owner: Anup
- Deadline: 17-AUG 10:00
- Priority: P1
- Description: MQTT client, JSON event publishing
- Acceptance: Events published reliably to backend

**FW-07: Firmware testing**
- Owner: Anup
- Deadline: 18-AUG 14:00
- Priority: P1
- Description: Unit tests, integration tests, serial output validation
- Acceptance: All tests pass, no crashes

---

### 🧠 Machine Learning — PRIYADA

**ML-01: Define detection classes**
- Owner: Priyada
- Deadline: 14-AUG 23:59
- Priority: P0
- Description: Define what "normal", "alert", "critical" mean
- Acceptance: Class definitions documented

**ML-02: Prepare dataset**
- Owner: Priyada
- Deadline: 15-AUG 14:00
- Priority: P0
- Description: Collect/simulate 10,000+ sensor samples
- Acceptance: Balanced dataset (80% normal, 10% alert, 10% critical)

**ML-03: Feature engineering**
- Owner: Priyada
- Deadline: 15-AUG 18:00
- Priority: P1
- Description: Extract RMS, peak, variance, dI/dt features
- Acceptance: Feature correlation analysis done

**ML-04: Train baseline model**
- Owner: Priyada
- Deadline: 16-AUG 12:00
- Priority: P0
- Description: Random Forest or NN training, cross-validation
- Acceptance: >85% accuracy achieved

**ML-05: Evaluate model**
- Owner: Priyada
- Deadline: 16-AUG 15:00
- Priority: P1
- Description: Confusion matrix, ROC curve, threshold tuning
- Acceptance: False positive rate <5%, F1-score >0.85

**ML-06: Anomaly score implementation**
- Owner: Priyada
- Deadline: 17-AUG 10:00
- Priority: P1
- Description: Convert model output to 0-1 score
- Acceptance: Score correlates with anomaly severity

**ML-07: Integrate inference in firmware**
- Owner: Priyada
- Deadline: 17-AUG 18:00
- Priority: P0
- Description: Convert to TFLite, embed in ESP32
- Acceptance: Inference runs <50ms on device

**ML-08: Prepare ML results for presentation**
- Owner: Priyada
- Deadline: 18-AUG 20:00
- Priority: P1
- Description: Accuracy plots, use case examples, future work
- Acceptance: Presentation slides ready

---

### 💻 Backend — ALOK KUMAR

**BE-01: Backend setup**
- Owner: Alok Kumar
- Deadline: 14-AUG 23:59
- Priority: P0
- Description: Node.js + Express + MongoDB Atlas setup
- Acceptance: Server runs on localhost:5000

**BE-02: Define event schema**
- Owner: Alok Kumar
- Deadline: 15-AUG 12:00
- Priority: P0
- Description: MongoDB event collection schema, indexes
- Acceptance: Schema documented, sample data inserted

**BE-03: POST event API**
- Owner: Alok Kumar
- Deadline: 15-AUG 18:00
- Priority: P0
- Description: /api/v1/events POST endpoint for ESP32
- Acceptance: Can log events from firmware

**BE-04: GET status API**
- Owner: Alok Kumar
- Deadline: 15-AUG 20:00
- Priority: P1
- Description: /api/v1/fence/status endpoint
- Acceptance: Returns current fence state

**BE-05: Event database integration**
- Owner: Alok Kumar
- Deadline: 16-AUG 12:00
- Priority: P0
- Description: Full CRUD operations, query API
- Acceptance: Can retrieve events with filters

**BE-06: ESP32/backend integration**
- Owner: Alok Kumar
- Deadline: 17-AUG 10:00
- Priority: P0
- Description: MQTT broker setup, event subscription
- Acceptance: Events flowing from ESP32 to database

**BE-07: Dashboard integration**
- Owner: Alok Kumar
- Deadline: 17-AUG 18:00
- Priority: P1
- Description: WebSocket setup, real-time event push
- Acceptance: Dashboard updates in real-time

---

### 🎤 Presentation — ANANYA

**PPT-01: Problem**
- Owner: Ananya
- Deadline: 15-AUG 18:00
- Priority: P1
- Description: Slide 1-2: Problem statement, current gaps
- Acceptance: Compelling problem statement done

**PPT-02: Existing gap**
- Owner: Ananya
- Deadline: 15-AUG 20:00
- Priority: P1
- Description: What's missing in existing solutions
- Acceptance: Competitor analysis complete

**PPT-03: Proposed solution**
- Owner: Ananya
- Deadline: 16-AUG 12:00
- Priority: P1
- Description: How FENCEGUARD-X solves the problem
- Acceptance: Solution clearly explained

**PPT-04: Architecture**
- Owner: Ananya
- Deadline: 16-AUG 15:00
- Priority: P1
- Description: System architecture diagram + explanation
- Acceptance: Clear, well-labeled diagram

**PPT-05: Working**
- Owner: Ananya
- Deadline: 17-AUG 10:00
- Priority: P1
- Description: How it works (workflow, pipeline)
- Acceptance: Animation or demo video included

**PPT-06: AI/ML**
- Owner: Ananya
- Deadline: 17-AUG 12:00
- Priority: P1
- Description: ML model, accuracy, detection capability
- Acceptance: Performance metrics shown

**PPT-07: Innovation**
- Owner: Ananya
- Deadline: 17-AUG 14:00
- Priority: P1
- Description: What's unique about FENCEGUARD-X
- Acceptance: 3-4 key innovations highlighted

**PPT-08: Impact/use cases**
- Owner: Ananya
- Deadline: 17-AUG 16:00
- Priority: P1
- Description: Real-world applications, market potential
- Acceptance: 5+ use cases presented

**PPT-09: Future scope**
- Owner: Ananya
- Deadline: 17-AUG 18:00
- Priority: P2
- Description: What comes next, scaling plans
- Acceptance: Roadmap for next 12 months

**PPT-10: Final presentation**
- Owner: Ananya
- Deadline: 18-AUG 12:00
- Priority: P0
- Description: All slides polished, rehearsed, ready
- Acceptance: Presentation reviewed by all members

**PPT-11: Q&A preparation**
- Owner: Ananya
- Deadline: 19-AUG 14:00
- Priority: P1
- Description: Prepare answers to likely judge questions
- Acceptance: FAQ document created, team trained

---

### 🚨 INTEGRATION Issues

**INT-01: ESP32 → ML data pipeline**
- Owner: ALL (Anup + Priyada primarily)
- Deadline: 16-AUG 18:00
- Priority: P0 (CRITICAL)
- Description: Sensor data → ML model → classification working end-to-end
- Acceptance: Real sensor data classified correctly by model

**INT-02: ESP32 → Backend API**
- Owner: ALL (Anup + Alok Kumar primarily)
- Deadline: 16-AUG 20:00
- Priority: P0 (CRITICAL)
- Description: Events flowing from firmware to MongoDB
- Acceptance: Can query database for ESP32 events

**INT-03: ML decision → Safety controller**
- Owner: ALL (Priyada + Anup primarily)
- Deadline: 17-AUG 10:00
- Priority: P0 (CRITICAL)
- Description: When ML says "critical", relay cuts automatically
- Acceptance: End-to-end critical event triggers isolation

**INT-04: Backend → Dashboard**
- Owner: ALL (Alok Kumar + Ananya primarily)
- Deadline: 17-AUG 14:00
- Priority: P0 (CRITICAL)
- Description: Real-time events visible on dashboard
- Acceptance: New events appear on dashboard <1 second

**INT-05: Complete end-to-end demonstration**
- Owner: ALL
- Deadline: 18-AUG 18:00
- Priority: P0 (CRITICAL)
- Description: Full system demo: sensor→firmware→backend→dashboard
- Acceptance: Complete flow works without manual intervention

---

## Labels to Create

```
hardware     - Hardware design & testing
firmware     - ESP32 firmware development
ml           - Machine learning & training
backend      - Backend API & database
dashboard    - Frontend UI & visualization
integration  - Multi-module integration
presentation - PPT & demo materials
bug          - Issues / fixes needed
enhancement  - Feature requests
documentation - Docs & wikis
P0-critical  - Must be done
P1-high      - Important
P2-medium    - Nice to have
P3-low       - Can wait
blocked      - Waiting on dependency
```

---

## Daily Standup Checklist (10 min sync)

**Template for team sync every morning 10:00 AM:**

```
Team Standup - 14 AUG 2026

✅ Anup (Hardware):
   - What did you do yesterday?
   - What will you do today?
   - Any blockers?

✅ Sakshi (Frontend/Deployment):
   - What did you do yesterday?
   - What will you do today?
   - Any blockers?

✅ Priyada (ML):
   - What did you do yesterday?
   - What will you do today?
   - Any blockers?

✅ Alok Kumar (Backend):
   - What did you do yesterday?
   - What will you do today?
   - Any blockers?

✅ Ananya (Presentation):
   - What did you do yesterday?
   - What will you do today?
   - Any blockers?

🚨 Blockers to resolve:
   - [List any cross-team dependencies]
   - [Assign owner to unblock]
```

---

## Milestone Timeline

| Date | Milestone | Status Check |
|------|-----------|--------------|
| 14-AUG | Planning + setup | Issues created, assigned |
| 15-AUG | Basic modules | Hardware + FW + ML/BE basics working |
| 16-AUG | 🔥 First Integration | At least INT-01 or INT-02 working |
| 17-AUG | End-to-end system | Complete pipeline working |
| 18-AUG | 🔒 FEATURE FREEZE | No new features, only bugfixes |
| 19-AUG | Testing + polish | PPT final, demo rehearsed |
| 20-AUG | 🏆 INTERNAL ROUND | SHOWTIME |

---

## GitHub Board Best Practices

### Moving Cards
- **TO TODO**: Task assigned + prerequisites met
- **TO IN PROGRESS**: You're actively working, started code
- **TO REVIEW**: Code written, tested locally, ready for review
- **TO DONE**: Reviewed, merged, deployed, working in production
- **TO BLOCKED**: Waiting on other task/person, can't proceed

### Never Leave a Card In Progress Overnight
- If stuck: mark BLOCKED with comment why
- If done: move to REVIEW/DONE
- If paused: move back to TODO with note

### Update Title As You Go
- GOOD: "ESP32 + INA219 integration - calibration done"
- BAD: "esp32 ina219"

### Use Labels Consistently
- Every card must have at least 1 module label
- Add priority labels (P0/P1/P2/P3)
- Add status labels if appropriate

---

## GitHub Collaboration Rules

1. **Each card = 1 person's responsibility**
   - Assign to ONE person (or tag co-owner with @mention)

2. **Update daily**
   - Move cards to reflect actual status
   - Add comments with progress

3. **Link dependencies**
   - Use "Depends on" or "Blocks" in comments
   - Ref other issues: `depends on #15`

4. **No silent failures**
   - If blocked: mark BLOCKED immediately
   - If going wrong: comment and ask for help
   - If going great: celebrate in comments!

5. **Before merging anything**
   - Move to REVIEW first
   - Get approval from team lead
   - Then move to DONE

---

## How to Get Started

1. Go to GitHub Repo: FENCEGUARD-X
2. Click "Projects" tab
3. Create new project: "FENCEGUARD-X — SIH Internal 20 AUG"
4. Set columns: BACKLOG → TODO → IN PROGRESS → REVIEW → DONE → BLOCKED
5. Create issues from templates above
6. Assign each issue to respective team member
7. Set deadlines
8. Pin critical issues (P0)
9. Have first standup at 10 AM

---

**Remember**: GitHub Project Board is your single source of truth. If it's not in GitHub, it doesn't exist.

Let's make this project legendary! 🚀
