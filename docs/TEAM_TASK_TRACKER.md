# Team Task Tracker

## Current active team (August 2026)

| Team member | Ownership |
|---|---|
| Anup Patil | Hardware + firmware, ESP32 integration, sensor integration, experimental data collection, sensor-fusion integration |
| Priyada | ML, data preprocessing, feature engineering, model training, evaluation |
| Alok Kumar | Backend, API, database, event processing |
| Sakshi | Frontend, dashboard, frontend API integration, deployment, demo hosting |
| Ananya | Presentation, documentation, pitch, demo narrative |

> Current ownership is assigned by role; no future tasks are assigned to Jayesh.

## Status legend
- DONE = evidence exists in repo or from team work
- DONE/VERIFY = component is implemented but should be rechecked before claiming completion
- IN PROGRESS = active work
- PENDING = not yet completed
- NEXT = immediate next action

## Team status table

| Team member | Task | Status | Notes |
|---|---|---|---|
| Anup | 3-zone hardware | DONE | Prototype architecture and 3-zone electrical detection are part of the project status and validated hardware work. |
| Anup | electrical fault testing | DONE | Open and short scenarios are documented as demonstrated. |
| Anup | MPU6050 integration | DONE | Sensor communication verified and raw 6-DOF telemetry captured across experiments. |
| Anup | normal baseline collection | DONE | `EXP_01_NORMAL_STATIONARY.csv` exists as real baseline telemetry. |
| Anup | physical tamper datasets | DONE | `EXP_02_PHYSICAL_EXPERIMENTS_LABELED.csv` collected and preserved under `hardware/experiments/physical_tamper/`. |
| Anup | firmware integration | IN PROGRESS | Hardware and firmware ownership consolidated under Anup. |
| Anup | sensor fusion integration | PENDING | Sensor-fusion algorithm and real-time classification pending ML pipeline completion. |
| Priyada | ML pipeline design | NEXT | Start with raw ingestion, validation, and feature engineering. |
| Priyada | raw dataset ingestion | NEXT | Ingest the experimental CSVs and validate schema. |
| Priyada | feature engineering | NEXT | Compute motion and electrical derived features. |
| Priyada | EDA | PENDING | Planned after ingestion and validation. |
| Priyada | baseline Random Forest | PENDING | To be trained after enough representative data exists. |
| Priyada | evaluation | PENDING | Must include accuracy, precision, recall, F1, and confusion matrix. |
| Priyada | sensor-fusion classifier | PENDING | This is a future model after baseline validation. |
| Alok | backend architecture | IN PROGRESS | Design should align with future sensor-fusion outputs. |
| Alok | API contract | PENDING/VERIFY | Event schema must reflect `event_type` and status outputs. |
| Alok | event schema | PENDING | Must eventually include fusion outputs and confidence. |
| Alok | database integration | PENDING | Integrate after event design is finalized. |
| Alok | live sensor integration | PENDING | Only after validated stream is available. |
| Sakshi | frontend dashboard | IN PROGRESS | Frontend and deployment tasks now belong to Sakshi. |
| Sakshi | API integration | PENDING | Dashboard should consume backend event API once available. |
| Sakshi | deployment | PENDING | Demo hosting and deployment are part of current ownership. |
| Ananya | architecture slides | IN PROGRESS | Narrative must emphasize sensor fusion and actual project constraints. |
| Ananya | problem statement | DONE/VERIFY | Documentation exists and matches the project objective. |
| Ananya | innovation explanation | IN PROGRESS | Must distinguish electrical detection + sensor fusion story. |
| Ananya | ML/sensor-fusion explanation | PENDING | Depends on validated ML pipeline and experimental data. |
| Ananya | demo flow | PENDING | Requires integrated prototype or scenario walkthrough. |
| Ananya | final pitch | PENDING | Final pitch after technical validation. |

## High-priority next actions

1. Collect `EXP_02_LIGHT_VIBRATION.csv`.
2. Collect `EXP_03_PHYSICAL_TAMPER.csv`.
3. Validate session/timestamp handling for raw sensor logs.
4. Build the ML preprocessing skeleton and feature extraction pipeline.
5. Keep all raw data and labels unmodified.
6. Finalize frontend dashboard contract with backend data model.

## TODO markers

- [TODO] Complete EXP_02_LIGHT_VIBRATION collection.
- [TODO] Complete EXP_03_PHYSICAL_TAMPER collection.
- [TODO] Complete EXP_04_REPEATED_TAMPER collection.
- [TODO] Complete EXP_05_STRONG_TAMPER collection.
- [TODO] Complete EXP_06-11 electrical experiments.
- [TODO] Complete EXP_12_COMBINED_BREACH collection.
- [TODO] Validate model metrics after training.
- [TODO] Build and connect frontend dashboard with backend API.
