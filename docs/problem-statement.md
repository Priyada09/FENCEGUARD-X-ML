# Problem Statement

## Background
Electric fences are widely used as protective barriers in agricultural, industrial, and perimeter security applications. However, current systems have significant vulnerabilities:

### Current Challenges
1. **Reactive Monitoring**: Fence breaches are detected after damage occurs
2. **Limited Awareness**: Operators cannot distinguish between accidental faults and intentional tampering
3. **Manual Response**: Safety isolation requires manual intervention
4. **No Intelligence**: Systems cannot predict failures or anomalies
5. **Poor Auditability**: Limited logging of tampering attempts or system faults

### Impact
- **Security Risk**: Unauthorized access not caught in time
- **Cost**: Replacement of damaged sections
- **Downtime**: Fence disabled until repairs complete
- **Safety**: Delayed isolation can endanger both humans and livestock

## Existing Solutions - Gaps

| Existing Solution | Capability | Gap |
|------------------|-----------|-----|
| **Dumb Relay System** | Cuts power on high current | No detection, no logging |
| **Basic Monitoring** | Voltage sensor on fence | No anomaly detection, no automation |
| **SCADA Systems** | Centralized monitoring | Expensive, requires infrastructure |
| **Motion Sensors** | Detect tampering | Many false positives, no system context |

## What's Missing
- **Real-time anomaly detection** using ML
- **Automatic isolation** based on threat classification
- **Event logging** for compliance and investigation
- **Predictive maintenance** using historical data
- **Autonomous decision-making** at the edge

---

## SIH 2026 Challenge

Design an **AI + IoT Based Electric Fence Safety & Unauthorized-Use Prevention System** that:
- Detects fence anomalies in real-time
- Classifies threats automatically
- Isolates unsafe sections autonomously
- Logs all events for auditing
- Operates without continuous cloud connectivity

