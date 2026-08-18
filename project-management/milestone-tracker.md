# Milestone Tracker — FENCEGUARD-X

**Purpose**: Track progress toward major milestones  
**Last Updated**: 14 August 2026  
**Next Review**: Daily at 6:00 PM  

---

## Milestones Overview

| Milestone | Target Date | Status | Progress | Description |
|-----------|-------------|--------|----------|-------------|
| **M1: Architecture Freeze** | 14-AUG 23:59 | 🟡 In Progress | 90% | Finalize design, all docs done |
| **M2: Module Baselines** | 15-AUG 18:00 | 🔴 TODO | 0% | Each module has basic working code |
| **M3: First Integration** | 16-AUG 18:00 | 🔴 TODO | 0% | ≥1 end-to-end flow working |
| **M4: Integrated MVP** | 17-AUG 18:00 | 🔴 TODO | 0% | Complete pipeline functional |
| **M5: Feature Freeze** | 18-AUG 00:00 | 🔴 TODO | 0% | No new features after this |
| **M6: Final Testing** | 19-AUG 18:00 | 🔴 TODO | 0% | System validated, team rehearsed |
| **M7: SIH Internal** | 20-AUG 10:00 | 🔴 TODO | 0% | Delivery to judges |

---

## M1: Architecture Freeze ✅

**Target**: 14 August 2026, 11:59 PM  
**Status**: 🟡 In Progress  
**Progress**: 90%  

### Criteria

- [ ] System architecture diagram finalized
- [ ] Technology stack confirmed (no changes after this)
- [ ] API contracts defined
- [ ] Database schema locked
- [ ] Hardware bill of materials complete
- [ ] All documentation written (22 files, 5600+ lines)
- [ ] Team roles & responsibilities clear
- [ ] 7-day schedule published
- [ ] Risk register completed
- [ ] GitHub project board structure ready

### Tasks Due

| Task | Owner | Status |
|------|-------|--------|
| Finalize architecture doc | Anup + Alok | ✅ DONE |
| Confirm technology stack | ALL | ✅ DONE |
| Create task list (47 issues) | Ananya | ✅ DONE |
| Publish master timeline | Ananya | ✅ DONE |

### Blockers

**None** — This milestone is complete pending GitHub setup

### Notes

- Documentation is locked. Future changes require decision log entry.
- Architecture is NOT locked (can pivot if needed, but document why).
- Once GitHub repo live, rest of milestones proceed in parallel.

---

## M2: Module Baselines Working ✅

**Target**: 15 August 2026, 6:00 PM  
**Status**: 🔴 TODO (depends on M1 completion + GitHub setup)  
**Progress**: 0%  

### Hardware Criteria

- [ ] ESP32 boots successfully
- [ ] INA219 reads current (±1% stable)
- [ ] ADC reads voltage (calibrated)
- [ ] Tamper sensor responds to trigger
- [ ] Relay moves on command
- [ ] Buzzer and LEDs functional

### Firmware Criteria

- [ ] FreeRTOS tasks initialized
- [ ] Main loop running at 100Hz
- [ ] Sensor data flowing to UART/storage
- [ ] No crashes for 30+ minutes

### ML Criteria

- [ ] Dataset collected (200+ normal samples)
- [ ] Features extracted (6 features per sample)
- [ ] Random Forest model training started
- [ ] First accuracy estimate available

### Backend Criteria

- [ ] Node.js server running on localhost:5000
- [ ] MongoDB connection verified
- [ ] POST /api/v1/events endpoint responding
- [ ] Sample event saved to DB

### Dashboard Criteria

- [ ] React app compiles without errors
- [ ] Basic page structure in place
- [ ] Can fetch data from API (async working)

### Blockers Allowed

At this stage, ok to have:
- Modules not talking to each other yet
- ML model not accurate yet
- Dashboard UI not polished yet

### Notes

- Focus: Get each module working independently
- Evidence: Commit + screenshot for each module
- Next milestone starts INT-01 integration

---

## M3: First Integration 🔥

**Target**: 16 August 2026, 6:00 PM  
**Status**: 🔴 TODO  
**Progress**: 0%  

### Critical Path (Must All Happen)

| Integration | Description | Modules | Owner |
|-------------|-------------|---------|-------|
| INT-01 | Sensors → Firmware processing | HW + FW | Anup |
| INT-02 | Firmware → ML inference | FW + ML | Priyada |
| INT-03 | Firmware → Backend API | FW + BE | Alok Kumar |

### Success Criteria

- ✅ **INT-01**: Firmware reads sensor, outputs feature vector (DONE by 16-AUG 12:00)
- ✅ **INT-02**: ML model classifies firmware output (DONE by 16-AUG 18:00)
- ✅ **INT-03**: Firmware POSTs event to backend, API stores in DB (DONE by 16-AUG 20:00)

### Escalation

If any INT task slips:
1. **Immediate**: Flag in standup with reason
2. **Within 30 min**: Anup assembles quick fix task force
3. **Within 2 hours**: Workaround or plan created
4. **Do not proceed to 17 AUG without INT-01, INT-02, INT-03 complete**

### Backup Plan (If INT fails)

- Keep modules running independently
- Show data flow as slides/simulations
- Prepare manual integration demo (hand-run data through each component)

### Notes

- This is the make-or-break milestone
- If we hit this, we know MVP is achievable
- All hands required

---

## M4: Integrated MVP

**Target**: 17 August 2026, 6:00 PM  
**Status**: 🔴 TODO  
**Progress**: 0%  

### Success Criteria

- [ ] Complete data flow: Sensors → Firmware → ML → Backend → Dashboard
- [ ] Trigger event manually on hardware
- [ ] Event appears on dashboard in real-time
- [ ] Safety isolation mechanism works
- [ ] Local alarm (buzzer + LEDs) sounds
- [ ] Backend logs event with full metadata
- [ ] All 7 integration tasks (INT-01 through INT-07) DONE
- [ ] System runs for 1+ hour without crashes

### Deliverables

- ✅ End-to-end working system (for real, not simulated)
- ✅ All P0 tasks moved to DONE
- ✅ Demo script finalized
- ✅ Backup recorded demo prepared

### Remaining Work

- [ ] Polish (UI, error messages, docs)
- [ ] Performance optimization
- [ ] Edge case testing

### Notes

- By end of 17-AUG, team should be confident system works
- 18-AUG is feature freeze: no new features, only bugfixes

---

## M5: Feature Freeze 🔒

**Target**: 18 August 2026, 12:00 AM (midnight)  
**Status**: 🔴 TODO  
**Progress**: 0%  

### What Happens

- 🔴 **NO NEW FEATURES** after this date
- ✅ Bugfixes allowed
- ✅ Documentation updates allowed
- ✅ Optimization allowed
- 🔴 Do not add "nice-to-haves"

### Checkpoint

- [ ] All P0 tasks DONE (27 tasks)
- [ ] System is stable
- [ ] Known bugs documented with severity
- [ ] PPT draft complete
- [ ] Team sleep schedule normalized (can rest 18-AUG afternoon)

### Enforcement

- Anup is empowered to BLOCK any PR that adds features
- Team agrees not to commit features after deadline
- Focus shifts to testing + presentation

### Notes

- This is **not** a soft deadline
- Exceptions require Anup + Ananya approval (rare)

---

## M6: Final Testing & Rehearsal

**Target**: 19 August 2026, 6:00 PM  
**Status**: 🔴 TODO  
**Progress**: 0%  

### Testing Checklist

- [ ] Hardware stress test (run 4+ hours, no crashes)
- [ ] Firmware firmware crash recovery test
- [ ] ML model robustness test (edge cases)
- [ ] Backend API load test (10+ events/sec)
- [ ] Dashboard responsive design test
- [ ] WiFi disconnect/reconnect test
- [ ] Offline operation test
- [ ] Full end-to-end demo run (3x)

### Presentation Rehearsal

- [ ] Full team runs demo + Q&A (3x timed, <10 min)
- [ ] Mock judging with external person
- [ ] PPT finalized and printed (backup)
- [ ] Each team member confident in their part
- [ ] Contingency plans documented

### Deliverables

- ✅ System tested and validated
- ✅ Demo script perfected
- ✅ Recorded backup demo (in case live fails)
- ✅ All team members ready & confident
- ✅ Judges Q&A prep complete

### Notes

- 19-AUG evening: Team should be 80%+ confident
- 20-AUG morning: Final verification only (no new fixes)

---

## M7: SIH Internal Round

**Target**: 20 August 2026, 10:00 AM  
**Status**: 🔴 TODO  
**Progress**: 0%  

### Pre-Demo (9:00 AM)

- [ ] All equipment powers up successfully
- [ ] WiFi connected (or hotspot ready)
- [ ] Backend server running
- [ ] Dashboard loads
- [ ] PPT ready on presentation device
- [ ] Team arrives 30+ min early
- [ ] Confidence level: 🟢 Green

### Demo Execution

- [ ] Follow demo script (10 min exactly)
- [ ] All 5 team members speak
- [ ] Live demo OR recorded backup plays
- [ ] Problem → Solution → Working proof
- [ ] No panicking, even if something breaks

### Post-Demo

- [ ] Q&A session (5-10 min)
- [ ] Team answers confidently
- [ ] Collect judge feedback
- [ ] Photo/video of working system
- [ ] Debrief: What went well? What surprised you?

### Success

- 🏆 Judges impressed
- 🏆 Project demonstrates understanding of problem
- 🏆 System actually works (or graceful fallback)
- 🏆 Team can articulate technical depth
- 🏆 Innovation is clear
- 🏆 Team won SIH Internal Round 🎉

### Notes

- Enjoy the moment
- You've worked hard
- Be proud regardless of outcome
- This is a portfolio piece

---

## Overall Progress

```
14-AUG [████░░░░░░░░░░░░░░░░░░░] 15%  — Architecture
15-AUG [████████░░░░░░░░░░░░░░░░] 33%  — Modules
16-AUG [██████████░░░░░░░░░░░░░░] 50%  — Integration
17-AUG [████████████░░░░░░░░░░░░] 66%  — MVP
18-AUG [██████████████░░░░░░░░░░] 80%  — Freeze
19-AUG [██████████████████░░░░░░] 90%  — Ready
20-AUG [████████████████████████] 100% — Done!
```

---

## Milestone Dependencies

```
M1: Architecture Freeze
        ↓
M2: Module Baselines (parallel work allowed)
        ↓
M3: First Integration ⚠️ CRITICAL
        ↓
M4: Integrated MVP ⚠️ CRITICAL
        ↓
M5: Feature Freeze
        ↓
M6: Final Testing
        ↓
M7: SIH Internal Round
```

**No milestone can be skipped.**

---

**Milestone Review**: Daily at 6:00 PM standup  
**Status Updates**: commit to master-task-list + PROJECT_STATUS.md

