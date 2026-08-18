# Daily Standup Template — FENCEGUARD-X

Use this format every day at 10:00 AM (or async updates in Slack/GitHub).

---

## Standing Meeting Details

- **Time**: 10:00 AM daily (14-20 AUG)
- **Duration**: 10 minutes
- **Format**: Each person answers 3 questions
- **Recording**: Notes in `daily-standup.md`
- **Escalation**: Flag BLOCKED immediately

---

## Template (Copy for each day)

```
═════════════════════════════════════════
  DAILY STANDUP — FENCEGUARD-X
  Date: [DATE]
  Duration: [START] – [END]
  Attendees: [NAMES]
═════════════════════════════════════════

─────────────────────────────────────────
ANUP — Hardware + Firmware
─────────────────────────────────────────

DONE TODAY:
- 

CURRENTLY WORKING ON:
- 

PENDING / BLOCKED:
- 

DEPENDENCIES NEEDED:
- 

CONFIDENCE LEVEL: 🟢 / 🟡 / 🔴
(Green = on track, Yellow = slight concern, Red = critical issue)

EVIDENCE:
(commit hash, screenshot, test result, or link)

─────────────────────────────────────────
PRIYADA — ML
─────────────────────────────────────────

DONE TODAY:
- 

CURRENTLY WORKING ON:
- 

PENDING / BLOCKED:
- 

DEPENDENCIES NEEDED:
- 

CONFIDENCE LEVEL: 🟢 / 🟡 / 🔴

EVIDENCE:
(commit hash, screenshot, test result, or link)

─────────────────────────────────────────
ALOK KUMAR — Backend
─────────────────────────────────────────

DONE TODAY:
- 

CURRENTLY WORKING ON:
- 

PENDING / BLOCKED:
- 

DEPENDENCIES NEEDED:
- 

CONFIDENCE LEVEL: 🟢 / 🟡 / 🔴

EVIDENCE:
(commit hash, screenshot, test result, or link)

─────────────────────────────────────────
ANANYA — Presentation & PM
─────────────────────────────────────────

DONE TODAY:
- 

CURRENTLY WORKING ON:
- 

PENDING / BLOCKED:
- 

DEPENDENCIES NEEDED:
- 

CONFIDENCE LEVEL: 🟢 / 🟡 / 🔴

EVIDENCE:
(commit hash, screenshot, test result, or link)

─────────────────────────────────────────
TEAM DECISIONS MADE:
─────────────────────────────────────────

- 

─────────────────────────────────────────
BLOCKERS TO RESOLVE:
─────────────────────────────────────────

- 

─────────────────────────────────────────
NEXT STANDUP PRIORITIES:
─────────────────────────────────────────

- 

─────────────────────────────────────────
OVERALL TEAM CONFIDENCE: 🟢 / 🟡 / 🔴
─────────────────────────────────────────
```

---

## Standing Meeting Rules

### Do's

✅ Be honest. If blocked, say so.  
✅ Be specific. "Working on ML model" is vague. "Debugging Random Forest feature importance" is clear.  
✅ Provide evidence. Commit hash, test result, screenshot.  
✅ Ask for help. "Can I get someone to pair-debug?" is encouraged.  
✅ Keep it to 2 minutes per person.  

### Don'ts

❌ Don't discuss implementation details (save for later).  
❌ Don't minimize problems. Escalate blockers immediately.  
❌ Don't update later. Update in real-time as you work.  
❌ Don't claim DONE unless tested.  

---

## Escalation Rules

If your confidence is 🔴 (Red):

1. **Immediately**: Flag in Slack/GitHub with @mention
2. **Within 15 min**: Talk to Anup (integration coordinator)
3. **Within 30 min**: Team discusses solution
4. **Within 1 hour**: Action plan created to unblock

**Example Red situations**:
- Hardware doesn't arrive
- Sensor not working
- Firmware won't compile
- Model accuracy below threshold
- Backend API failing
- Integration can't complete

Do NOT proceed silently with workarounds.

---

## Daily Commitment

Everyone commits to:
- ✅ Update standup by end-of-day (or async in GitHub Issues)
- ✅ Respond to blockers within 1 hour
- ✅ Support teammates in difficulty
- ✅ Evidence for every DONE task

---

## Example Standup Entry

```
PRIYADA — ML

DONE TODAY:
- Collected 200 training samples for NORMAL class
- Feature extraction pipeline working (voltage, current, rate-of-change)

CURRENTLY WORKING ON:
- Training Random Forest model
- Tuning hyperparameters for precision >95%

PENDING / BLOCKED:
- Need 300 TAMPER-class samples from Anup's hardware
- Waiting for Anup's firmware output and the sensor-fusion feature stream

DEPENDENCIES NEEDED:
- Anup: Please provide tampered-sensor data by 16-AUG 10:00 AM
- Anup: Firmware feature output by 15-AUG 20:00

CONFIDENCE LEVEL: 🟡
(Slight concern: not enough tamper data yet, but can train on synthetic perturbations)

EVIDENCE:
- Commit: abc1234 (feature extraction code)
- Screenshot: notebooks/02-Feature_Engineering.ipynb
- Training log: models/train_log_2026-08-15.txt
```

---

## Historical Standups

This file will be updated daily. Previous standups are archived below for reference.

**[14 AUG] — Project Initialization**
- Architecture finalized
- All documentation created
- Team structure confirmed
- GitHub setup in progress

---

**[Standups will be recorded here starting 15 AUG]**

