# FENCEGUARD-X
## AI + IoT Based Electric Fence Safety & Unauthorized-Use Prevention System

**SIH 2026 — Internal Round: 20 August**

---

## 👥 TEAM

| Member | Role | Main Responsibility |
|--------|------|-------------------|
| **Anup** | IoT & Automation Lead | Hardware, sensors, isolation, integration |
| **Jayesh** | Firmware Lead | ESP32 firmware, sensor acquisition, communication |
| **Priyada** | ML Lead | Dataset, anomaly detection, classification |
| **Alok Kumar** | Backend Lead | API, database, event logging |
| **Ananya** | Presentation Lead | PPT, documentation, pitch, demo story |

### **All 5 → Integration & Testing**
Nobody should say: *"That's not my part."*

On **16–18 Aug**, everyone needs to help integrate. We succeed or fail as one team.

---

## 🔍 PROBLEM

Electric fences are critical safety infrastructure, but:
- **Unauthorized access** remains a major challenge
- **Tampering detection** is reactive, not predictive
- **System isolation** isn't automatic enough
- **Response time** is crucial in emergency scenarios

---

## 💡 OUR SOLUTION

A real-time, AI-powered monitoring system that:
1. **Continuously monitors** fence health and current flow
2. **Detects anomalies** using machine learning
3. **Classifies threats** (tampering, breakdown, theft attempt)
4. **Automatically isolates** unsafe sections
5. **Alerts operators** in real-time
6. **Logs all events** for post-incident analysis

---

## ⚙️ CORE PIPELINE

```
Monitor → Detect → Classify → Isolate → Alert → Log
```

**Real-time** | **Autonomous** | **Intelligent** | **Safe**

---

## 🏗️ SYSTEM ARCHITECTURE

```
[Fence Sensors (INA219, Current Sensors)]
          ↓
[ESP32 Data Acquisition]
          ↓
[ML Model (Anomaly Detection)]
          ↓
[Safety Controller (Relay Logic)]
          ↓
[Backend API (Event Logging)]
          ↓
[Dashboard (Real-time Visualization)]
```

---

## 📊 CURRENT STATUS

| Component | Status | Owner |
|-----------|--------|-------|
| Hardware | 🟡 In Progress | Anup |
| Firmware | 🟡 In Progress | Jayesh |
| ML | 🟡 In Progress | Priyada |
| Backend | 🟡 In Progress | Alok Kumar |
| Dashboard | 🟡 In Progress | Ananya |
| Integration | 🔴 Pending | All |
| Demo | 🔴 Pending | All |

---

## 🗓️ MILESTONES

| Date | Milestone | Owner |
|------|-----------|-------|
| **14 AUG** | Planning + individual module setup | All |
| **15 AUG** | Hardware + firmware + ML/backend basic modules | All |
| **16 AUG** | 🔥 First integration | All |
| **17 AUG** | End-to-end system | All |
| **18 AUG** | 🔒 FEATURE FREEZE | All |
| **19 AUG** | Testing + PPT + mock judging + backup demo | All |
| **20 AUG** | 🏆 **INTERNAL ROUND** | All |

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
