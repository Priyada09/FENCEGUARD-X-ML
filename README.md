# FENCEGUARD-X
## AI + IoT Based Electric Fence Safety & Unauthorized-Use Prevention System

**SIH 2026 — Internal Round: 20 August 2026**  
**Current Status**: Hardware Electrical Layer COMPLETE & VALIDATED | Next: Physical Tamper Detection

---

## 👥 TEAM (5 Members)

| Member | Role | Primary Responsibility |
|--------|------|----------------------|
| **Anup** | IoT & Automation Lead | Hardware (3-zone electrical + physical tamper), sensors, safety isolation, integration |
| **Jayesh** | Firmware Lead | ESP32 firmware, sensor acquisition, zone classification, sensor fusion, communication |
| **Priyada** | ML Lead | Dataset analysis, EDA, baseline modeling, fault classification, feature importance |
| **Alok Kumar** | Backend Lead | REST API, MongoDB schema, event logging, telemetry ingestion, integration |
| **Ananya** | Presentation Lead | Architecture diagrams, innovation story, demo flow, PPT, judging preparation |

**Collaboration Principle**: Everyone contributes to integration & testing. No silos.

---

## 🔍 PROBLEM STATEMENT

Electric fences provide critical perimeter security, but face challenges:
- **Unauthorized access & tampering** go undetected until post-incident review
- **Electrical faults** (cuts, shorts) disable security without operator awareness
- **Manual inspection** is time-consuming and reactive
- **Physical tampering** (climbing, pushing, vibrating) is hard to distinguish from environmental disturbance
- **Automatic response** requires real-time fault detection and localization

**Impact**: Delayed response to intrusions can result in livestock loss, property damage, or security breaches.

---

## 💡 OUR SOLUTION

**FENCEGUARD-X** is a real-time, AI-powered monitoring system deployed on a safe low-voltage **3-zone prototype** that demonstrates:

### Phase 1 ✅ **ELECTRICAL FAULT DETECTION** (COMPLETE)
- Three independent electrical zones with EOL (End-of-Line) integrity sensing
- Real-time detection and **localization** of:
  - **NORMAL**: All zones operating at nominal voltage
  - **OPEN/CUT**: Zone voltage rises to ~3.30V (loss of load)
  - **SHORT**: Zone voltage falls to ~0.00V (short to ground)
  - **MULTI_FAULT**: Multiple simultaneous zone faults detected per-zone
- Experimental validation with 26-sample dataset
- INA219 provides bus voltage, current, and power measurements

### Phase 2 🔄 **PHYSICAL TAMPER DETECTION** (IN PROGRESS)
- Movement/vibration sensor integration to detect physical contact
- Distinguish between intentional tampering and environmental disturbance
- Sensor fusion with electrical data for multi-modal threat classification

### Integration Layers
- **Detection**: Zone voltage + INA219 + future tamper sensor
- **Validation**: Sensor quality checks and consistency
- **Localization**: Per-zone fault identification
- **Fusion**: Combine electrical + physical evidence
- **Classification**: NORMAL / ALERT / CRITICAL severity
- **Isolation**: Safe relay logic for prototype
- **Alerting**: Backend event logging + dashboard
- **Logging**: Historical event database

---

## ⚙️ SYSTEM PIPELINE

```
SENSE (Zone voltages, INA219, tamper sensor)
  ↓
VALIDATE (Check sensor validity)
  ↓
LOCALIZE (Determine affected zone(s))
  ↓
FUSE (Combine electrical + physical evidence)
  ↓
CLASSIFY (NORMAL / ALERT / CRITICAL)
  ↓
ISOLATE (Trigger safe isolation logic)
  ↓
ALERT (Operator notification)
  ↓
LOG (Backend database + dashboard)
```

---

## 🏗️ 3-ZONE ARCHITECTURE

```
                    3-ZONE SAFE FENCE PROTOTYPE
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
      ELECTRICAL LAYER                  PHYSICAL LAYER
             |                                 |
      Zone 1 EOL sensing              Movement/vibration/
      Zone 2 EOL sensing              tamper sensing
      Zone 3 EOL sensing                       |
             |                                 |
             +----------------+----------------+
                              |
                              v
                            ESP32
                              |
              +---------------+---------------+
              |                               |
              v                               v
          INA219                        Zone States
      Voltage/Current/Power        Z1 / Z2 / Z3 Status
              |                               |
              +---------------+---------------+
                              |
                              v
                       SENSOR FUSION
                              |
                    +---------+---------+
                    |         |         |
                    v         v         v
                 NORMAL     ALERT    CRITICAL
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
           Backend          Event         Safety/
           API              System        Isolation
```

---

## 📊 CURRENT STATUS (Updated: 17 August 2026)

| Component | Status | Details | Owner |
|-----------|--------|---------|-------|
| **Hardware** | 🟢 **COMPLETE** | 3-zone electrical detection validated with real prototype data | Anup |
| **Firmware** | 🟡 IN PROGRESS | Electrical acquisition validated; physical tamper integration pending | Jayesh |
| **ML** | 🟡 IN PROGRESS | Real experimental dataset ready; baseline model pending | Priyada |
| **Backend** | 🟡 IN PROGRESS | Schema updated; API integration pending | Alok Kumar |
| **Dashboard** | 🟡 IN PROGRESS | Real-time display framework pending | Ananya |
| **Integration** | 🔴 PENDING | Schedule: 16–18 AUG critical path | All |
| **Demo** | 🔴 PENDING | Rehearsal: 19 AUG | All |

---

## 📈 KEY METRICS

**Hardware Validation**:
- ✅ 3 zones × 3 conditions = 9-state electrical fault matrix
- ✅ Fault localization accuracy: 100% (on prototype)
- ✅ Bus voltage range: 3.0–3.4V (safe lab operation)
- ✅ Current range: 80–125 mA (typical load)
- ✅ Dataset: 26 samples, real experimental data

**ML Readiness**:
- ✅ Dataset available: `ml/dataset/raw/sih_fence_raw_dataset.csv`
- ✅ Data quality: 85% MEASURED, 15% IMPUTED (documented)
- ⏳ Baseline model accuracy: TBD (Phase 1 evaluation)
- ⏳ Feature importance: TBD (Phase 1 analysis)

---

## 🗓️ TIMELINE (6 DAYS TO LAUNCH)

| Date | Milestone | Status |
|------|-----------|--------|
| **17 AUG** | Hardware validation complete; dataset available | ✅ DONE |
| **18 AUG** | Physical tamper hardware integration | 🔄 IN PROGRESS |
| **18 AUG** | Firmware sensor fusion + ML baseline | 🔄 IN PROGRESS |
| **18 AUG** | Backend integration + database | 🔄 IN PROGRESS |
| **18 AUG 18:00** | **FEATURE FREEZE** | ⏳ PENDING |
| **19 AUG** | End-to-end testing + demo rehearsal | ⏳ PENDING |
| **20 AUG 10:00** | 🏆 **INTERNAL ROUND** | 🎯 TARGET |

---

## 📚 DOCUMENTATION

**Quick Start**: [QUICK_START.md](QUICK_START.md)  
**Team Workflow**: [TEAM_COLLABORATION.md](TEAM_COLLABORATION.md)  
**Status Tracking**: [PROJECT_STATUS.md](PROJECT_STATUS.md)  
**Architecture**: [docs/system-architecture.md](docs/system-architecture.md)  
**Innovation**: [docs/innovation.md](docs/innovation.md)  
**Dataset**: [ml/dataset/README.md](ml/dataset/README.md)  

---

## ⚠️ IMPORTANT DISCLAIMERS

1. **SAFE LOW-VOLTAGE PROTOTYPE**
   - All voltages < 4V, all currents < 200 mA
   - NOT a real high-voltage electric fence
   - Indoor lab demonstration only

2. **EXPERIMENTAL DATA**
   - 26 samples collected in controlled conditions
   - NOT production-scale dataset
   - Represents proof-of-concept validation only

3. **NO HIGH-VOLTAGE CLAIMS**
   - Prototype cannot safely operate on real electric fences
   - Do NOT adapt this design for high-voltage commercial use without professional electrical engineering review
   - Safety certification required for actual deployment

---

## 🚀 QUICK LINKS

- **GitHub Repository**: [patilanup421-pixel/SIH-2026](https://github.com/patilanup421-pixel/SIH-2026)
- **Hardware Setup**: [hardware/README.md](hardware/README.md)
- **Firmware Guide**: [firmware/README.md](firmware/README.md)
- **ML Pipeline**: [ml/README.md](ml/README.md)
- **Backend API**: [backend/README.md](backend/README.md)
- **Dashboard**: [dashboard/README.md](dashboard/README.md)

**Last Updated**: 17 August 2026

---

## 📚 DOCUMENTATION

- [Problem Statement](docs/problem-statement.md)
- [Proposed Solution](docs/proposed-solution.md)
- [System Architecture](docs/system-architecture.md)
- [Working Flow](docs/working-flow.md)
- [Innovation](docs/innovation.md)
- [Use Cases](docs/use-cases.md)
- [Technology Stack](docs/technology-stack.md)
- [Bill of Materials](docs/BOM.md)
- [References](docs/references.md)

---

## 📁 PROJECT STRUCTURE

```
FENCEGUARD-X/
├── README.md                      (this file)
├── docs/                          (documentation)
│   ├── problem-statement.md
│   ├── proposed-solution.md
│   ├── system-architecture.md
│   ├── working-flow.md
│   ├── innovation.md
│   ├── use-cases.md
│   ├── technology-stack.md
│   ├── BOM.md
│   └── references.md
├── hardware/                      (IoT & sensors)
│   ├── circuit/
│   ├── schematics/
│   ├── components.md
│   └── testing/
├── firmware/                      (ESP32 code)
│   ├── esp32/
│   └── README.md
├── ml/                            (Machine learning)
│   ├── dataset/
│   ├── notebooks/
│   ├── models/
│   ├── training/
│   └── README.md
├── backend/                       (API & database)
│   ├── api/
│   ├── database/
│   └── README.md
├── dashboard/                     (UI visualization)
│   └── README.md
├── presentation/                  (SIH deliverables)
│   ├── PPT/
│   ├── diagrams/
│   └── demo/
├── media/                         (Assets)
│   ├── photos/
│   ├── videos/
│   └── screenshots/
└── .gitignore
```

---

## 🚀 GETTING STARTED

### Setup

1. Clone this repository
2. Read [System Architecture](docs/system-architecture.md)
3. Check your team's README in respective folders:
   - [Hardware Setup](hardware/README.md)
   - [Firmware Setup](firmware/README.md)
   - [ML Setup](ml/README.md)
   - [Backend Setup](backend/README.md)
   - [Dashboard Setup](dashboard/README.md)

### Daily Workflow

1. **Start of day**: Check GitHub Project board for assigned tasks
2. **During work**: Move tasks to IN PROGRESS
3. **When done**: Move to REVIEW and tag reviewers
4. **Daily sync**: 10-minute standup on task blockers

---

## 📌 GITHUB COLLABORATION RULE

> **"From today, GitHub will be our single source of truth."**
>
> Every task will be added to the project board with an **owner** and **deadline**.
> - If you're working on something → move it to **IN PROGRESS**
> - Once completed and tested → move it to **REVIEW/DONE**
> - Any blocker → mark it **BLOCKED** instead of waiting
> - We'll have a **10-minute daily sync** to check progress

---

## 🎯 SUCCESS CRITERIA

- ✅ Hardware prototype passes safety tests
- ✅ ESP32 acquires and transmits sensor data reliably
- ✅ ML model detects anomalies with >85% accuracy
- ✅ Backend API logs all events with sub-second latency
- ✅ Dashboard visualizes fence status in real-time
- ✅ Complete end-to-end demonstration working
- ✅ All team members can explain their module in 2 minutes

---

## 🔗 USEFUL LINKS

- **GitHub Project**: [FENCEGUARD-X — SIH Internal 20 AUG](#) (link to project board)
- **Issues Tracker**: Check GitHub Issues for daily tasks
- **Communication**: Use GitHub Discussions for technical questions

---

## 📞 SUPPORT & ESCALATION

| Issue Type | Owner | Response Time |
|-----------|-------|----------------|
| Hardware blocker | Anup | 30 min |
| Firmware issue | Jayesh | 30 min |
| ML question | Priyada | 1 hour |
| Backend bug | Alok Kumar | 30 min |
| Presentation delay | Ananya | 2 hours |
| Integration blocker | **All** | **15 min** |

---

## 📄 LICENSE

This project is part of **Smart India Hackathon 2026 (SIH)**.
All rights reserved during the competition.

---

**Last Updated**: 14 August 2026
**Status**: 🟡 Active Development
