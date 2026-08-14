---
name: Integration
about: Track integration work between modules
title: "[INT] "
labels: integration
assignees: ''

---

## Integration Objective

[What two or more modules need to work together?]

Example: "Firmware → Backend API: ESP32 publishes events to backend"

## Modules Involved

- [ ] Hardware
- [ ] Firmware
- [ ] ML
- [ ] Backend
- [ ] Dashboard
- [ ] Presentation

## Dependencies

[What must be DONE before this integration can start?]
- #issue-number (e.g., FW-06 "Structured sensor output")
- #issue-number (e.g., BE-03 "POST event API")

## Expected Interface

### Data Flow

```
Module A
    ↓
[Describe format, protocol, latency requirement]
    ↓
Module B
```

### Example

```json
{
  "timestamp": "2026-08-15T10:30:45.123Z",
  "voltage": 48.5,
  "current": 0.75,
  "features": [48.5, 0.75, 0.02, 0.001],
  "ml_score": 0.85,
  "classification": "NORMAL"
}
```

## Test Procedure

[How will we know this integration works?]

- [ ] Step 1: [Set up module A in state X]
- [ ] Step 2: [Trigger action in module A]
- [ ] Step 3: [Verify module B responds correctly]
- [ ] Expected result: [Specific observable outcome]

## Success Criteria

- [ ] Data flows from Module A to Module B without error
- [ ] Latency measured: [target <XX ms]
- [ ] No data loss or corruption
- [ ] Handles error gracefully (e.g., WiFi disconnect)
- [ ] Evidence: [commit hash, test log, screenshot]

## Blockers

[What could prevent this from working?]

- [ ] Blocker 1: [description]
- [ ] Blocker 2: [description]

## Owners

- **Module A Owner**: @[person]
- **Module B Owner**: @[person]
- **Integration Lead**: @[person]

## Notes

[Any additional context]
