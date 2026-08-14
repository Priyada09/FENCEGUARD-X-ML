# Risk Register — FENCEGUARD-X

**Last Updated**: 14 August 2026  
**Next Review**: 15 August 2026, 6:00 PM  

---

## Risk Matrix

```
        PROBABILITY
         Low | Med | High
       ──────┼─────┼──────
    H   │ 5  │ 10 │ 15
  I   ───┼─────┼──────
  M   M  │ 3  │ 6  │ 12
  P   ───┼─────┼──────
  A   L  │ 1  │ 2  │ 4
  C   ───┴─────┴──────
  T

  Higher number = Higher overall risk
```

---

## Critical Risks (≥12)

### RISK-001: Integration Delayed Past 16-AUG

| Property | Value |
|----------|-------|
| **ID** | RISK-001 |
| **Risk** | Integration cannot complete by 16-AUG deadline, cascades to feature freeze |
| **Probability** | HIGH (60%) |
| **Impact** | HIGH (Project cannot show full MVP) |
| **Risk Score** | 15 |
| **Status** | ACTIVE |

**Why it matters**:
- If INT-01 through INT-03 don't work by 16-AUG, team enters panic mode
- Feature freeze on 18-AUG leaves only 2 days for integration
- Judges expect working MVP, not separate modules

**Mitigation**:
- ✅ Start integration on 16-AUG without fail (not 17-18 AUG)
- ✅ Daily sync during integration phase
- ✅ Parallel work during 15-AUG so modules ready
- ✅ Pre-test each module independently

**Contingency**:
- If integration fails 16-AUG evening:
  1. Continue bugfixing 17-AUG all day
  2. Prepare backup: Show working individual modules + diagram
  3. Demonstrate concept manually if needed

**Owner**: Anup (Integration Coordinator)

---

### RISK-002: Hardware Prototype Failure

| Property | Value |
|----------|-------|
| **ID** | RISK-002 |
| **Risk** | INA219, sensors, or relay fails or doesn't arrive |
| **Probability** | MEDIUM-HIGH (40%) |
| **Impact** | HIGH (No hardware demo) |
| **Risk Score** | 12 |
| **Status** | ACTIVE |

**Why it matters**:
- No hardware = Judges see only software simulation
- Loss of credibility
- Assumes prototype works, but may not

**Mitigation**:
- ✅ Order components now (14-AUG) with same-day shipping if possible
- ✅ Have spare sensors/relays on hand
- ✅ Use breadboard (not PCB) for faster iteration
- ✅ Emulate hardware in firmware if sensor unavailable

**Contingency**:
- If hardware fails day-of-demo:
  1. Run backend API simulator
  2. Show recorded demo video
  3. Explain what would happen with real hardware

**Owner**: Anup

---

## High Risks (6-10)

### RISK-003: ML Model Underperformance

| Property | Value |
|----------|-------|
| **ID** | RISK-003 |
| **Risk** | ML model accuracy <85%, fails to classify tampering |
| **Probability** | MEDIUM (50%) |
| **Impact** | MEDIUM (Safety logic fails, system unreliable) |
| **Risk Score** | 10 |
| **Status** | ACTIVE |

**Why it matters**:
- Model is key differentiator
- If ML doesn't work, project relies only on threshold logic (boring)
- Judges expect AI to add value

**Mitigation**:
- ✅ Start with simple baseline (Random Forest) — don't overcomplicate
- ✅ Collect balanced dataset early (by 15-AUG)
- ✅ If accuracy insufficient, use deterministic fallback
- ✅ Document limitations honestly

**Contingency**:
- If accuracy <85%:
  1. Keep deterministic rule-based logic as primary safety
  2. Use ML as secondary classifier
  3. Explain: "AI enhances but doesn't replace safety logic"

**Owner**: Priyada

---

### RISK-004: WiFi/Backend Connectivity Failure

| Property | Value |
|----------|-------|
| **ID** | RISK-004 |
| **Risk** | WiFi unavailable during demo, backend unreachable |
| **Probability** | MEDIUM (30%) |
| **Impact** | MEDIUM (Dashboard goes dark, but safety still works locally) |
| **Risk Score** | 6 |
| **Status** | ACTIVE |

**Why it matters**:
- Judges may test by disconnecting WiFi
- System MUST work offline
- Otherwise looks fragile

**Mitigation**:
- ✅ Test offline mode thoroughly (19-AUG)
- ✅ Local storage of events when offline
- ✅ Safety isolation must work without WiFi
- ✅ Resume transmission when WiFi returns

**Contingency**:
- If WiFi fails during demo:
  1. Show local operation (LEDs, buzzer still work)
  2. Show event log stored on device
  3. Explain: "Backend is for monitoring, not safety"

**Owner**: Jayesh + Alok Kumar

---

### RISK-005: Relay Failure / Safety Mechanism Doesn't Isolate

| Property | Value |
|----------|-------|
| **ID** | RISK-005 |
| **Risk** | Relay doesn't cut power, safety mechanism unreliable |
| **Probability** | MEDIUM (25%) |
| **Impact** | HIGH (Safety compromise) |
| **Risk Score** | 8 |
| **Status** | ACTIVE |

**Why it matters**:
- Safety isolation is core feature
- If relay fails, entire system is unsafe
- Must be fail-safe (cuts power on failure)

**Mitigation**:
- ✅ Use fail-safe relay (defaults to open/disconnected)
- ✅ Test relay response <5ms
- ✅ Manual override provided
- ✅ Stress test relay (HW-07)

**Contingency**:
- If relay unreliable:
  1. Use manual switch + circuit breaker
  2. Add watchdog timer for automatic cutoff
  3. Document workaround, explain to judges

**Owner**: Anup + Jayesh

---

## Medium Risks (3-5)

### RISK-006: Sensor Noise / False Alarms

| Property | Value |
|----------|-------|
| **ID** | RISK-006 |
| **Risk** | Noisy sensor data causes frequent false positives |
| **Probability** | MEDIUM (40%) |
| **Impact** | MEDIUM (User loses trust in system) |
| **Risk Score** | 5 |
| **Status** | ACTIVE |

**Mitigation**:
- ✅ Implement Kalman filter + moving average
- ✅ Calibrate during startup
- ✅ Tune detection thresholds for <5% false alarm rate

**Owner**: Jayesh + Anup

---

### RISK-007: Dataset Weak / Unbalanced

| Property | Value |
|----------|-------|
| **ID** | RISK-007 |
| **Risk** | Training data insufficient or biased toward one class |
| **Probability** | MEDIUM (35%) |
| **Impact** | MEDIUM (Model trained on bad data) |
| **Risk Score** | 4 |
| **Status** | ACTIVE |

**Mitigation**:
- ✅ Collect balanced samples (equal count per class)
- ✅ Synthetic data augmentation if necessary
- ✅ Cross-validation with stratified k-fold

**Owner**: Priyada

---

### RISK-008: Feature Freeze Not Enforced

| Property | Value |
|----------|-------|
| **ID** | RISK-008 |
| **Risk** | Team keeps adding features after 18-AUG, misses deadline |
| **Probability** | MEDIUM (30%) |
| **Impact** | MEDIUM (Unfinished polishing, bugs) |
| **Risk Score** | 4 |
| **Status** | ACTIVE |

**Mitigation**:
- ✅ 18-AUG = Hard deadline, no new features
- ✅ Only bugfixes + docs after
- ✅ Anup enforces freeze

**Owner**: Anup + Ananya

---

## Low Risks (<3)

### RISK-009: Presentation Panic / Poor Communication

| Property | Value |
|----------|-------|
| **ID** | RISK-009 |
| **Risk** | Presentation unclear, judges confused by technical jargon |
| **Probability** | LOW (20%) |
| **Impact** | MEDIUM (Judges undervalue project) |
| **Risk Score** | 2 |
| **Status** | ACTIVE |

**Mitigation**:
- ✅ Mock judging 19-AUG
- ✅ Clear slides, simple language
- ✅ Practice delivery

**Owner**: Ananya

---

### RISK-010: Last-Minute Changes Break System

| Property | Value |
|----------|-------|
| **ID** | RISK-010 |
| **Risk** | Unexpected change on 20-AUG breaks something |
| **Probability** | LOW (10%) |
| **Impact** | MEDIUM (Demo fails) |
| **Risk Score** | 1 |
| **Status** | ACTIVE |

**Mitigation**:
- ✅ Lock code 19-AUG evening
- ✅ Final system test pass before 20-AUG 9:00 AM
- ✅ No commits after 19-AUG 18:00

**Owner**: Anup

---

## Risk Monitoring Schedule

- **Daily**: Check for new blockers (in standup)
- **15-AUG 6:00 PM**: Review risks, update scores
- **16-AUG 6:00 PM**: Critical review (integration phase)
- **17-AUG 6:00 PM**: Impact assessment
- **18-AUG 6:00 PM**: Feature freeze checkpoint
- **19-AUG 6:00 PM**: Final review before demo

---

## Risk Escalation

**If risk probability increases**:
1. Update this register
2. Mention in standup
3. Create GitHub issue if needed
4. Activate contingency if impact HIGH

**If new risk discovered**:
1. Add to register with score
2. Alert team immediately
3. Create mitigation plan
4. Reassess daily

---

## Decision: Accept, Mitigate, or Avoid?

| Risk | Decision | Reasoning |
|------|----------|-----------|
| Integration delay | **MITIGATE** | Start 16-AUG, daily sync |
| Hardware failure | **MITIGATE** | Spare parts, recorded demo backup |
| ML underperformance | **MITIGATE** | Fallback to deterministic logic |
| WiFi failure | **ACCEPT** | Local operation is feature, not bug |
| Relay failure | **MITIGATE** | Fail-safe design, stress test |
| Sensor noise | **MITIGATE** | Filtering + calibration |
| Dataset weak | **MITIGATE** | Balanced collection, augmentation |
| Feature creep | **ACCEPT** | Hard freeze enforced |
| Presentation panic | **MITIGATE** | Mock judging |
| Last-minute changes | **ACCEPT** | Code freeze on 19-AUG 18:00 |

---

**Risk ownership**: Anup monitors overall, each owner monitors their domain.  
**Next escalation**: 15 August 6:00 PM

