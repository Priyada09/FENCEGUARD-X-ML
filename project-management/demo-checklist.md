# Demo Checklist — FENCEGUARD-X

**Date**: 20 August 2026  
**Time**: TBD (provided by SIH)  
**Duration**: 10-15 minutes (estimated)  
**Location**: SIH Venue / Virtual  

---

## Pre-Demo (19 August Evening)

### Hardware Readiness

- [ ] ESP32 powers on successfully
- [ ] All sensors connected and reporting data
- [ ] INA219 current sensor calibrated
- [ ] Tamper detection working (reed switch)
- [ ] Relay responds to signal (isolation confirmed)
- [ ] Buzzer sounds on abnormal condition
- [ ] LEDs light appropriately
- [ ] No loose connections or short circuits
- [ ] Battery/power supply stable (if wireless)
- [ ] Backup power supply ready
- [ ] Safe low-voltage configuration verified (no high-voltage exposure)

### Firmware Check

- [ ] Latest firmware compiled and uploaded to ESP32
- [ ] Serial monitor shows expected output
- [ ] Sensor data logging at 100Hz
- [ ] MQTT/HTTP connectivity established
- [ ] WiFi reconnects on network loss
- [ ] Local safety logic works offline
- [ ] Relay responds to firmware commands
- [ ] No compilation errors or warnings

### ML Model Ready

- [ ] Model saved in deployable format (TFLite)
- [ ] Inference latency verified <50ms
- [ ] Model accuracy documented (test set results)
- [ ] Confusion matrix available
- [ ] Feature importance explained

### Backend Verified

- [ ] Server running on stable port
- [ ] MongoDB connection verified
- [ ] Event API tested with curl/Postman
- [ ] Events persisting to database
- [ ] Dashboard API endpoints responding
- [ ] No database corruption
- [ ] Backup database created

### Dashboard Tested

- [ ] All components rendering correctly
- [ ] Real-time updates working
- [ ] Event history displays correctly
- [ ] Responsive on demo device (laptop/tablet)
- [ ] No console errors (browser dev tools)
- [ ] Loads quickly (<3 seconds)
- [ ] Gracefully handles offline state

### Presentation Ready

- [ ] Final PPT exported and backed up (USB, cloud, laptop)
- [ ] Slides reviewed by entire team
- [ ] No typos, grammatical errors, or consistency issues
- [ ] Technical claims verified (accuracy, latency, etc.)
- [ ] Demo flow documented step-by-step
- [ ] Backup presentation (images only, if technology fails)
- [ ] Team members assigned to present each section

### Documentation Complete

- [ ] README updated with latest info
- [ ] API documentation final
- [ ] Architecture document locked
- [ ] BOM complete with actual costs
- [ ] GitHub repository clean and organized
- [ ] All code commits have meaningful messages

### Team Prepared

- [ ] Each member rehearsed their section
- [ ] Q&A responses documented (see judge-qa.md)
- [ ] Demo script memorized (not reading)
- [ ] Time-boxed: full demo in <10 min
- [ ] Contingency plan documented (if demo fails)
- [ ] Confidence high across team

---

## Demo Day (20 August Morning)

### 1 Hour Before Demo

- [ ] Arrive 30+ minutes early
- [ ] Test WiFi connectivity in venue
- [ ] Power up all equipment
- [ ] Serial monitor connected to ESP32 (troubleshooting only)
- [ ] Backend server running (local or cloud)
- [ ] Dashboard loading correctly
- [ ] PPT advanced to first slide
- [ ] Backup demo video loaded (just in case)
- [ ] Phone for pictures/video documentation

### Equipment Checklist

- [ ] Laptop (primary presentation device)
- [ ] Backup laptop (if primary fails)
- [ ] ESP32 + all sensors + relay + power
- [ ] USB cables (multiple)
- [ ] Portable WiFi hotspot (backup internet)
- [ ] HDMI cable (for projector)
- [ ] Power adapter (fully charged)
- [ ] USB drive (with all code, docs, presentation)
- [ ] Printed materials (brief handout with team names/contacts)
- [ ] Pen + notebook (for notes from judges)

---

## Demo Script (10 minutes)

### [0:00–1:00] Introduction & Problem

**Speaker**: Ananya  
**Visual**: PPT Slide 1-3  

```
"Good morning/afternoon, I'm Ananya, PM of FENCEGUARD-X team.

[Problem Slide]
"Electric fences are critical for agricultural and perimeter security, 
but existing systems are reactive. When a breach or tampering happens, 
it's detected only after damage is done. We're introducing FENCEGUARD-X: 
AI-powered automatic safety isolation for electric fences."

[Gap Slide]
"Current solutions lack:
- Real-time anomaly detection
- Automatic response
- Intelligent classification
- Cloud accountability"
```

**Time Check**: 1 minute elapsed. Proceed if on track.

---

### [1:00–3:00] System Architecture & Components

**Speaker**: Anup  
**Visual**: PPT Slide 4 (Architecture), Hardware on table  

```
"Let me show you how FENCEGUARD-X works.

[Architecture Slide]
We have three layers:

1. SENSING: Voltage and current sensors continuously monitor the fence
2. INTELLIGENCE: Edge AI on an ESP32 processes data locally
3. SAFETY: If tampering is detected, automatic relay isolation

Here's the actual hardware."
```

**Live Demo Part 1: Sensors Reading**

```
"Let's see it in action. Right now, the fence is in NORMAL state."

[Show Dashboard: Voltage 48V, Current 0.5A, Status: NORMAL]

"The sensors are taking readings at 100Hz. The firmware is filtering 
the noisy data and computing features. Let me trigger a tamper event."
```

**Action**: Disconnects tamper reed switch or simulates by hand  
**Expected**: Buzzer sounds, LEDs flash, console shows TAMPER detection  

**Time Check**: 3 minutes elapsed

---

### [3:00–5:30] AI/ML Classification

**Speaker**: Priyada  
**Visual**: PPT Slide 6 (ML), Console output  

```
"The AI is trained on three scenarios:

1. NORMAL operation (no alerts)
2. TAMPERING (physical breach detected)
3. ELECTRICAL FAULT (voltage/current anomaly)

[Show model metrics]
Our Random Forest model achieves 94% accuracy on test data.

[Show Feature Importance]
The top features the model uses are:
- Current spike magnitude
- Voltage drop rate
- Sensor change velocity"
```

**Live Demo Part 2: ML Classification**

```
"As the event occurs, the model classifies it in real-time."

[Console shows]: 
```
timestamp: 2026-08-20 10:05:30
features: [voltage: 47.2, current: 0.8, rate: 0.05, ...]
ml_score: 0.92
classification: TAMPERING
confidence: 92%
```

**Action**: Safety relay cuts power  
**Visual**: Relay clicks audibly, LEDs go red, dashboard updates  

**Time Check**: 5.5 minutes elapsed

---

### [5:30–7:30] Backend & Logging

**Speaker**: Alok Kumar  
**Visual**: PPT Slide 7-8, Dashboard event log  

```
"The event is automatically logged to our backend for accountability.

[Show Dashboard Event Log]
This event was recorded with:
- Precise timestamp
- All sensor readings
- ML classification + confidence score
- Isolated timestamp
- User/location info

The API is running on [URL], and we're storing everything in MongoDB 
for real-time analytics and historical review."
```

**Live Demo Part 3: Backend Response**

```
"In this scenario, a manager can review the incident:
- What triggered the alarm
- When it happened
- What action was taken
- Was it legitimate or false alarm"
```

[Navigate Dashboard to show]:
- Event history
- Incident details (timestamps, classification, confidence)
- Graph of voltage/current over time around event

**Time Check**: 7.5 minutes elapsed

---

### [7:30–9:00] Safety & Offline Capability

**Speaker**: Anup  
**Visual**: PPT Slide 9 (Safety Architecture)  

```
"A key feature: AI failure is NOT safety failure.

[Show Safety Architecture Slide]
Even if the ML model were to crash or give wrong predictions, 
our deterministic safety logic ALWAYS monitors:

- Voltage threshold: If drop > 40V, isolate immediately
- Current spike: If increase > 300%, isolate immediately
- Watchdog timer: If processor hangs, relay defaults to safe

And critically, this works OFFLINE:
[Disconnect WiFi on laptop]

The system continues to monitor and protect. The dashboard goes dark, 
but the fence is still protected locally. When WiFi returns, 
[reconnect WiFi] events sync automatically."
```

**Time Check**: 9 minutes elapsed

---

### [9:00–9:45] Innovation & Scale

**Speaker**: Ananya  
**Visual**: PPT Slide 10-11  

```
"Innovation highlights:

1. Edge AI: Sub-100ms response, works offline
2. Fail-safe design: Thresholds + ML, not ML-only
3. Automatic isolation: No human intervention needed
4. Tamper-resistant: Comprehensive sensor fusion
5. Autonomous + verifiable: Every action logged

[Slide: Use Cases]
This applies to:
- Agricultural fences (protect livestock, $$ loss reduction)
- Border security (detect breaches instantly)
- High-security facilities (evidence collection)
- Smart grids (equipment theft prevention)
- Wildlife sanctuaries (poacher deterrence)

Market opportunity is ~$2.5B+ globally."
```

**Time Check**: 9:45 minutes

---

### [9:45–10:00] Wrap-up & Q&A

**Speaker**: Ananya  

```
"FENCEGUARD-X is a production-ready prototype demonstrating 
AI-powered safety isolation. It's safe, autonomous, and scales.

Thank you. We're open for questions."
```

---

## Contingency Plan (If Hardware Fails)

### Scenario A: Hardware doesn't power up

1. **Immediate action**: Switch to Backup Demo (recorded video)
2. **Explain**: "We have a recorded demo since live tech can be unpredictable"
3. **Show**: Pre-recorded video (30 seconds) showing sensor data, classification, relay isolation
4. **Fallback**: Show PPT slides with architecture + explain without live hardware
5. **Confidence**: "The concept is proven via simulation. Production hardware is being tested independently."

### Scenario B: WiFi unavailable

1. **Immediate action**: Demonstrate offline operation
2. **Show**: Local console output proving system works without internet
3. **Explain**: "This is actually a feature. Safety doesn't depend on WiFi."
4. **Fallback**: Show database screenshot (events were logged when WiFi was available earlier)

### Scenario C: Dashboard won't load

1. **Immediate action**: Show backend database directly (MongoDB Atlas UI or terminal)
2. **Explain**: "The API and database are working. It's just the UI layer."
3. **Fallback**: Show raw API responses (curl commands in terminal)

### Scenario D: ML model gives wrong classification

1. **Immediate action**: Point to deterministic safety logic
2. **Explain**: "AI is a bonus classifier, not required. The hard thresholds always work."
3. **Fallback**: Trigger event again, show threshold-based isolation

### Scenario E: Relay doesn't respond

1. **Immediate action**: Explain fail-safe: "Relay defaults to OPEN, cutting power on any failure"
2. **Fallback**: Demonstrate manual switch or circuit breaker as backup
3. **Confidence**: "Safety is guaranteed by hardware design, not software."

---

## Judging Evaluation Criteria

**Judges typically score on**:

1. **Problem Understanding** (15%)
   - ✅ Clear statement of the problem
   - ✅ Why it matters
   - ✅ Real-world impact

2. **Solution Approach** (20%)
   - ✅ Technical innovation
   - ✅ Practical feasibility
   - ✅ Safety-first design

3. **Working Prototype** (25%)
   - ✅ Core MVP functional
   - ✅ Reliable demonstration
   - ✅ All modules integrated

4. **Technical Depth** (20%)
   - ✅ AI/ML component non-trivial
   - ✅ Hardware + software integration
   - ✅ Well-documented decisions

5. **Presentation** (10%)
   - ✅ Clear communication
   - ✅ Time management
   - ✅ Confidence

6. **Scalability & Impact** (10%)
   - ✅ Market potential
   - ✅ Real-world applicability
   - ✅ Competitive edge

**Your strategy**: Hit all 6 criteria in the 10-minute demo.

---

## Post-Demo (20 August Afternoon)

- [ ] Collect judge feedback (written if available)
- [ ] Photograph/video the working system
- [ ] Document any judge questions for future reference
- [ ] Celebrate! 🎉
- [ ] Debrief: What went well? What surprised you?
- [ ] Archive all evidence (photos, videos, screenshots)

---

## Final Confidence Check

Before entering the demo room, **every team member must answer YES to**:

- [ ] I can explain my module in 2 minutes
- [ ] I can answer 3 common objections
- [ ] I've practiced my part 5+ times
- [ ] I'm confident in the technical accuracy
- [ ] I understand the fallback if X breaks
- [ ] I know what "DONE" means for this project
- [ ] I'm proud of this work
- [ ] I can stay calm if things go wrong

---

**Demo Success Criteria**: 
✅ Problem clearly stated  
✅ Solution demonstrated (live OR recorded backup)  
✅ Safety mechanism shown  
✅ ML/AI component visible  
✅ Integration end-to-end  
✅ All team members spoke  
✅ Time kept within 10 minutes  
✅ No technical panic  

---

**Good luck. Go win! 🏆**

