# Contributing to FENCEGUARD-X

This guide explains how to contribute to the FENCEGUARD-X project during the SIH 2026 7-day sprint (14-20 August).

---

## Core Principles

1. **Respect the schedule**: Deadlines are not suggestions
2. **Communicate early**: Don't silently struggle. Flag blockers immediately
3. **Test before committing**: Untested code is broken code
4. **Document as you code**: Comments and READMEs for future you
5. **No hallucination**: Only report verified, tested results

---

## Workflow

### 1. Get Your Task

1. Go to GitHub Issues
2. Find task assigned to you (or self-assign if unassigned)
3. Move it to "IN PROGRESS"
4. Note the **deadline** and **definition of done**

### 2. Create a Branch

```bash
git checkout -b feature/[task-id]-[brief-name]
```

**Examples**:
```bash
git checkout -b feature/HW-02-ina219-sensor
git checkout -b feature/FW-06-structured-output
git checkout -b feature/ML-04-train-model
git checkout -b feature/BE-03-post-api
git checkout -b feature/DB-04-integration
```

### 3. Implement

- Write code with comments
- Test as you go (unit tests if possible)
- Update relevant README or documentation
- Keep commits focused and logical

### 4. Verify (Definition of Done)

Before committing, check every item in the **Definition of Done**:

```
- [ ] Code written
- [ ] Code compiles/runs
- [ ] Unit tests pass (if applicable)
- [ ] Tested on actual hardware/environment
- [ ] Documentation updated
- [ ] No known bugs
- [ ] Commit message is clear
```

**Example "Definition of Done" for FW-02**:

```
- [ ] INA219 reads current at 100Hz
- [ ] Readings stable (±1%)
- [ ] No crashes
- [ ] Serial output shows raw data
- [ ] Code commented
- [ ] firmware/README.md updated
```

### 5. Commit

```bash
git commit -m "feat: add INA219 sensor acquisition at 100Hz

- Implemented I2C protocol for INA219
- Sample rate: 100Hz with Kalman filtering
- Stability: ±1% measurement error
- Verified on hardware

Closes #HW-02"
```

**Commit message format**:
```
type: short description

Longer explanation if needed.
- Point 1
- Point 2

Closes #[issue-number]
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`

### 6. Push & Create Pull Request

```bash
git push origin feature/HW-02-ina219-sensor
```

Then on GitHub:
- Create Pull Request
- Fill in PR template (What changed? Why? Testing?)
- Assign reviewer (your module lead or Anup)
- Link the issue

### 7. Code Review

- Your reviewer checks your code
- Respond to feedback
- Make requested changes in new commits (don't rewrite history)
- Get approval ✅

### 8. Merge

Once approved:
```bash
# On GitHub, click "Squash and merge" or "Merge"
```

Then:
```bash
git checkout develop
git pull origin develop
```

### 9. Move Issue to Done

- On GitHub, move issue card to "DONE"
- Add comment: "✅ Merged to develop, demo ready"

---

## Communication

### Asking for Help

**Use GitHub Issues** (public, everyone sees it):

```
@Anup I'm blocked on HW-02. The INA219 won't initialize over I2C. 
Can you help debug the wiring? Error: timeout on address 0x40.

[Screenshot of serial output]

Blocking: INT-01 (scheduled 16-AUG)
```

**Use Slack** (if urgent, <1 hour response needed):

```
@team INA219 not working. We need to debug before 15-AUG 18:00. 
Call in 15 min?
```

**Do NOT**:
- Email (gets lost)
- Direct messages only (information disappears)
- Assume someone knows you're stuck (always mention publicly)

### Daily Standup

Every day at **10:00 AM**:

```
DONE TODAY:
- Initialized I2C on ESP32
- INA219 responds to address scan

WORKING ON:
- Reading actual current values
- Filtering noise

BLOCKED:
- INA219 breakout board not arriving (still checking supplier)

NEEDS FROM OTHERS:
- Jayesh: Can firmware test with simulated current data if hardware delayed?

CONFIDENCE: 🟡 (slight concern about sensor arrival, but workaround ready)
```

---

## Code Standards

### Firmware (C/C++)

```cpp
// Good: Clear variable names, comments
float read_current_ina219() {
  // Read raw ADC value from INA219 over I2C
  uint16_t raw = ina219.readBusVoltage_raw();
  
  // Convert to amps (current_lsb = 0.1mA per bit)
  float current_amps = raw * 0.0001;
  
  return current_amps;
}

// Bad: Cryptic
float rci() {
  int x = ina219.rBV_r();
  return x * 0.0001;
}
```

### Python (ML, Backend)

```python
# Good: Type hints, docstrings
def extract_features(voltage_samples: List[float], 
                     current_samples: List[float]) -> np.ndarray:
  """
  Extract 6 features from sensor samples.
  
  Args:
    voltage_samples: Raw voltage readings (V)
    current_samples: Raw current readings (A)
    
  Returns:
    Feature vector [v_rms, i_rms, dv_dt, di_dt, power, anomaly_score]
  """
  v_rms = np.sqrt(np.mean(voltage_samples**2))
  i_rms = np.sqrt(np.mean(current_samples**2))
  # ... more features
  return np.array([v_rms, i_rms, ...])

# Bad: No documentation
def exf(vs, cs):
  v = np.sqrt(np.mean(vs**2))
  i = np.sqrt(np.mean(cs**2))
  return np.array([v, i, ...])
```

### JavaScript (Dashboard)

```javascript
// Good: Clear names, comments
const fetchFenceStatus = async () => {
  try {
    const response = await fetch('/api/v1/fence/status');
    if (!response.ok) throw new Error('API error');
    
    const data = await response.json();
    setFenceStatus(data);
  } catch (error) {
    console.error('Failed to fetch status:', error);
    setError(error.message);
  }
};

// Bad: Cryptic, no error handling
const fs = async () => {
  const r = await fetch('/api/v1/fence/status');
  const d = await r.json();
  setStatus(d);
};
```

---

## Testing

### Minimum Requirements

Every P0 task must be tested before marking DONE.

**Hardware**:
- [ ] Physical sensor responds as expected
- [ ] Readings are stable (not floating/jittery)
- [ ] Error cases handled (sensor disconnected, etc.)

**Firmware**:
- [ ] Code compiles without errors/warnings
- [ ] Runs without crashes for 10+ minutes
- [ ] Serial output shows expected values
- [ ] Integrates with dependent module (e.g., HW + FW together)

**ML**:
- [ ] Model trains without errors
- [ ] Evaluation metrics calculated
- [ ] Confusion matrix generated
- [ ] Inference latency measured

**Backend**:
- [ ] API responds to requests
- [ ] Data persists to database
- [ ] Can retrieve data (queries work)
- [ ] No SQL/logic errors in production code

**Dashboard**:
- [ ] Page renders without errors
- [ ] Data fetches and displays
- [ ] Responsive on laptop + mobile
- [ ] No console errors (open DevTools)

---

## Documentation

### Code Comments

Add comments for **why**, not **what**:

```python
# Bad: Just describes what the code does
current = ina219.read()  # read current

# Good: Explains reasoning
# We use the INA219 instead of a shunt resistor because it provides 
# higher accuracy (±0.4%) and I2C interface for easy ESP32 integration
current = ina219.read()  # Read in milliamps
```

### README Updates

When you finish a task, update the relevant README with:

1. **How to set up** (if needed)
2. **How to use** (if a library/API)
3. **Expected output** (example)
4. **Known issues** (if any)

**Example**:

```markdown
## INA219 Current Sensing (HW-02)

### Setup

1. Connect INA219 to ESP32 via I2C (SDA=21, SCL=22)
2. Solder 0.1Ω shunt resistor (included in breakout)
3. Power on

### Code

```cpp
ina219.begin(0x40);  // Default address
float current = ina219.readCurrent_mA();  // Get current in mA
```

### Example Output

```
[10:30:45.123] Current: 0.85A, Voltage: 48.2V, Power: 40.97W
[10:30:45.223] Current: 0.87A, Voltage: 48.1V, Power: 41.83W
```

### Known Issues

- First 5 readings may be unstable. Discard during startup.
- ADS1115 samples only 128 times per second (slower than expected).
```
```

---

## Common Mistakes (Avoid These)

### ❌ Marking DONE Without Testing

```
"I wrote the code and it compiles. DONE!"

❌ NOT DONE until tested on actual hardware/data
```

### ❌ Committing Broken Code

```
"I'll fix it tomorrow"

❌ Commit only working code to main branch
```

### ❌ Silent Failure

```
"I'm struggling, but I'll figure it out"

❌ Ask for help immediately. Time is precious.
```

### ❌ Unclear Commit Messages

```
"bug fix" or "update" or "stuff"

❌ Be specific: "fix: timeout issue in INA219 init (increase delay to 100ms)"
```

### ❌ Feature Creep

```
"While I'm here, let me add a nice UI feature"

❌ Stick to your task. Nice-to-haves after deadline.
```

---

## Tools & Setup

### Git

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/FENCEGUARD-X.git
cd FENCEGUARD-X

# Set up branches
git checkout -b feature/your-task

# Check status
git status

# Add changes
git add .

# Commit
git commit -m "feat: your change"

# Push
git push origin feature/your-task
```

---

### For Firmware (Anup)

Install Arduino IDE or PlatformIO:
- Arduino IDE: https://www.arduino.cc/en/software
- PlatformIO: https://platformio.org/

### For ML (Priyada)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r ml/requirements.txt

# Launch Jupyter
jupyter notebook ml/notebooks/
```

### For Backend (Alok Kumar)

```bash
# Install Node
# https://nodejs.org/

# Set up project
cd backend
npm install

# Run server
npm start
```

### For Dashboard (Sakshi)

```bash
# Create React app
cd dashboard
npm install

# Start dev server
npm run dev
```

---

## Escalation Path

**If you're stuck**:

1. **First**: Try to solve yourself (15-30 min max)
2. **Then**: Ask in GitHub Issue with @mention
3. **No response in 30 min?**: Ping in Slack
4. **Still stuck?**: Call Anup (integration lead) for quick call
5. **More than 1 hour stuck?**: This is a blocker — escalate to team

**Example escalation**:

```
1. GitHub Issue: @Anup Can you help with I2C timeout?
   [Wait 30 min]
   
2. Slack: @team Quick call? I2C not working. Need help in 15 min.
   [Wait 15 min, no response]
   
3. Call: Anup, I'm stuck on I2C and it's blocking FW-02. 
   Can we pair-debug for 15 min?
```

---

## Success Criteria for a Good Contribution

- ✅ Code solves the stated problem
- ✅ Code is tested (not just compiled)
- ✅ Code is documented (comments + README)
- ✅ Commit messages are clear
- ✅ PR explains what changed and why
- ✅ Definition of Done is 100% checked
- ✅ Reviewer approved
- ✅ No blockers left unmentioned

---

## Final Reminders

- **Deadline is non-negotiable**: 20 August at 10:00 AM
- **Feature freeze is real**: 18 August, no new features
- **Communicate early**: Silence = problem
- **Test everything**: Untested = broken
- **Help teammates**: You're a team, not individuals
- **Be proud**: You're building something real

---

**Thank you for contributing to FENCEGUARD-X.** 

Together, we're going to build a safety system that actually works. 🚀

