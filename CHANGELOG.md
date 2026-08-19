# CHANGELOG — FENCEGUARD-X

All notable changes to the FENCEGUARD-X project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2026-08-19] — 3-Zone Prototype Alignment & Dataset Standardization

### Updated

- **Team Ownership Alignment**:
  - **Anup**: IoT & Automation + Firmware/Hardware Lead
  - **Priyada**: ML Lead
  - **Alok Kumar**: Backend Lead
  - **Sakshi**: Frontend & Deployment Lead
  - **Ananya**: Presentation Lead
  - *Jayesh*: Removed from active team roster; firmware responsibilities covered by Anup.

- **Dataset Organization & Integrity**:
  - Standardized original experimental evidence into `hardware/experiments/physical_tamper/` (`EXP_01_NORMAL_STATIONARY.csv`, `EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv`) and `hardware/experiments/electrical_faults/` (`sih_fence_raw_dataset.csv`).
  - Mirrored raw experimental datasets under `ml/dataset/raw/` for Priyada's ML pipeline.
  - Preserved exact empirical measurements and tagged loose connection anomalies (`LOOSE_CONNECTION_ANOMALY`, `IMPUTED_BUS_VOLTAGE`).

- **Hardware & Sensor Fusion Alignment**:
  - Documented 3-zone low-voltage prototype GPIO allocations (Zone 1: GPIO 34, Zone 2: GPIO 35, Zone 3: GPIO 32; I2C 21/22 for INA219 @ 0x40 and MPU6050 @ 0x68).
  - Outlined multi-axis temporal motion feature extraction ($||a||, ||\omega||, \Delta a, \Delta \omega$, rolling std/mean) fused with electrical zone states.

---

## [2026-08-14] — Initial Project Setup

### Added

- **Documentation**: 22 markdown files (5600+ lines)
  - Problem statement
  - Proposed solution
  - System architecture
  - Working flow & scenarios
  - Innovation & competitive analysis
  - 10+ use cases
  - Technology stack
  - Bill of Materials
  - References & learning resources

- **Project Management Structure**:
  - Master task list template
  - Daily standup format
  - Risk register
  - Decision log
  - Milestone tracker
  - Project status dashboard

- **Repository Structure**:
  - Hardware folder (circuit, schematics, testing)
  - Firmware folder (ESP32 code skeleton)
  - ML folder (notebooks, dataset, training)
  - Backend folder (API structure)
  - Dashboard folder (React structure)
  - Presentation folder (PPT, diagrams, demo)
  - Media folder (assets)

- **Team Documentation**:
  - Complete role definitions
  - Ownership matrix
  - 7-day execution timeline
  - Daily communication plan
  - Collaboration guidelines

- **GitHub Infrastructure** (Ready to deploy):
  - Issue templates (task, bug, integration, feature)
  - PR template
  - GitHub workflows structure
  - .gitignore

### Team Responsibilities Assigned

- **Anup** (IoT & Automation): Hardware architecture, sensors, safety isolation
- **Jayesh** (Firmware): ESP32 firmware, sensor acquisition, communication
- **Priyada** (ML): Dataset, features, anomaly detection, classification
- **Alok Kumar** (Backend): APIs, database, event logging, integration
- **Ananya** (Presentation): PPT, diagrams, documentation, pitch, demo story

### Timeline Established

- **14 August**: Planning + Architecture Freeze
- **15 August**: Basic Modules Working
- **16 August**: 🔥 First Integration (CRITICAL)
- **17 August**: Integrated MVP
- **18 August**: Feature Freeze
- **19 August**: Testing + Rehearsal
- **20 August**: SIH Internal Round

### Defined Priorities

- **P0 (Critical)**: 27 tasks
  - Core MVP must work
  - Safety mechanisms must function
  - Integration must happen on schedule

- **P1 (High)**: 15 tasks
  - Quality improvements
  - Documentation
  - Testing

- **P2-P3 (Medium/Low)**: 5 tasks
  - Polish, optimization
  - Can be deferred if time pressured

### Important Engineering Principles

- ✅ **Safety First**: AI failure must NOT equal safety failure
- ✅ **Deterministic Local Protection**: Edge controller must work offline
- ✅ **No Hallucination**: Only report tested, verified results
- ✅ **Evidence-Based**: Every metric backed by evaluation
- ✅ **Early Integration**: Start 16-AUG, not 19-AUG

### Current Blockers

**None** — Project at initialization phase

### Known Risks

| Risk | Mitigation |
|------|-----------|
| Integration delayed | Daily sync, start on 16-AUG without fail |
| Hardware failure | Backup components, simulated demo ready |
| ML insufficient | Deterministic fallback + edge logic |
| Feature creep | Feature freeze on 18-AUG strictly enforced |

### Next Actions

1. Create GitHub repository
2. Push all documentation
3. Create GitHub Project Board
4. Generate 47 GitHub Issues
5. First team standup @ 10 AM
6. Begin task execution

---

## Status Legend

- 🟢 **Complete** — Task finished and tested
- 🟡 **In Progress** — Currently being worked on
- 🔴 **Blocked/Not Started** — Either blocked or not yet begun
- 🔵 **On Hold** — Deliberately paused

---

**Project Initialization Complete**  
**Ready for team execution**  
**Next Checkpoint: 15 August 2026, 6:00 PM**

