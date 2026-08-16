# Backend README

## Overview

FENCEGUARD-X backend provides REST APIs for:
- **Telemetry Ingestion**: Real-time sensor data from ESP32
- **Event Logging**: Fault events, isolation actions, alerts
- **Status Queries**: Current fence state, zone health
- **Analytics**: Historical trends, incident reporting
- **Real-time Updates**: WebSocket for live dashboard

**Technology Stack**: Node.js + Express + MongoDB + WebSocket

**Current Status** 🟡 **IN PROGRESS**: Schema finalized, API skeleton ready, integration pending

---

## Quick Start

### Prerequisites
- **Node.js**: v18+ (with npm or yarn)
- **MongoDB**: Local instance (v4.4+) or MongoDB Atlas cloud
- **Environment**: Windows, macOS, or Linux

### Local Setup

```bash
# 1. Clone and navigate to backend
cd backend

# 2. Install dependencies
npm install

# 3. Create environment file
cp .env.example .env

# 4. Edit .env with your database URI
# For local MongoDB:
#   MONGODB_URI=mongodb://localhost:27017/fenceguard
# For MongoDB Atlas (cloud):
#   MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/fenceguard

# 5. Start the server
npm start

# Expected output:
# [INFO] Server running on http://localhost:5000
# [INFO] MongoDB connected to fenceguard_db
# [INFO] WebSocket server listening on ws://localhost:5000
```

### Docker Deployment (Optional)
```bash
docker build -t fenceguard-backend .
docker run -p 5000:5000 --env-file .env fenceguard-backend
```

---

## Backend Structure

```
backend/
├─ api/
│  ├─ routes/
│  │  ├─ telemetry.js           # POST /api/telemetry
│  │  ├─ events.js              # GET/POST /api/events
│  │  ├─ status.js              # GET /api/status
│  │  └─ analytics.js           # GET /api/analytics
│  ├─ controllers/
│  │  ├─ telemetryController.js
│  │  ├─ eventController.js
│  │  ├─ statusController.js
│  │  └─ analyticsController.js
│  ├─ models/
│  │  ├─ Telemetry.js           # Sensor readings schema
│  │  ├─ Event.js               # Fault event schema
│  │  └─ Device.js              # Device metadata schema
│  ├─ middleware/
│  │  ├─ auth.js                # API key validation (optional)
│  │  ├─ errorHandler.js        # Global error handling
│  │  └─ logger.js              # Request logging
│  └─ services/
│     ├─ deviceService.js       # Device management
│     ├─ eventService.js        # Event processing
│     └─ notificationService.js # Alert sending (future)
│
├─ database/
│  ├─ seeds/                    # Initial seed data
│  ├─ migrations/               # Schema version upgrades
│  └─ indexes.js                # Index creation for performance
│
├─ config/
│  ├─ database.js               # MongoDB connection config
│  ├─ websocket.js              # WebSocket setup
│  └─ env.js                    # Environment loader
│
├─ tests/
│  ├─ unit/
│  │  └─ telemetryController.test.js
│  └─ integration/
│     └─ api.test.js
│
├─ .env.example                 # Environment template
├─ app.js                       # Express app initialization
├─ server.js                    # Entry point (HTTP + WebSocket)
├─ package.json
└─ README.md
```

---

## API Endpoints

### 1. Telemetry Ingestion

**Endpoint**: `POST /api/telemetry`

**Purpose**: ESP32 sends real-time sensor data

**Request Headers**:
```
Content-Type: application/json
Device-ID: ESP32_001 (optional header for device identification)
```

**Request Body** (JSON):
```json
{
  "timestamp": "2026-08-17T14:23:45Z",
  "device_id": "ESP32_001",
  "zone1_voltage_v": 1.48,
  "zone2_voltage_v": 3.30,
  "zone3_voltage_v": 1.29,
  "zone1_status": "NORMAL",
  "zone2_status": "OPEN_CUT",
  "zone3_status": "NORMAL",
  "bus_voltage_v": 3.276,
  "current_ma": 88.20,
  "power_mw": 294.00,
  "condition": "OPEN_CUT",
  "fault_zone": "ZONE2",
  "severity": "ALERT",
  "confidence": 0.98,
  "data_quality": "MEASURED"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Telemetry received and stored",
  "telemetry_id": "507f1f77bcf86cd799439011"
}
```

**Status Codes**:
- `200 OK`: Successfully stored
- `400 Bad Request`: Missing required fields
- `500 Internal Error`: Database error

**Backend Processing**:
1. Validate telemetry schema
2. Store in `telemetry` collection
3. If `severity = ALERT or CRITICAL`: Create event record
4. Broadcast to all WebSocket clients (dashboard)
5. Return acknowledgment

---

### 2. Event Logging & Retrieval

**Endpoint**: `GET /api/events`

**Purpose**: Retrieve historical fault events

**Query Parameters**:
```
?startDate=2026-08-17          # ISO date
&endDate=2026-08-18            # ISO date
&device_id=ESP32_001           # Device filter
&zone=ZONE1                    # Zone filter (ZONE1, ZONE2, ZONE3)
&condition=OPEN_CUT            # Condition filter (NORMAL, OPEN_CUT, SHORT, MULTI_FAULT)
&severity=ALERT                # Severity filter (ALERT, CRITICAL)
&limit=50                      # Max results (default: 50)
&skip=0                        # Pagination offset
```

**Response**:
```json
{
  "success": true,
  "count": 5,
  "events": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "timestamp": "2026-08-17T14:23:45Z",
      "device_id": "ESP32_001",
      "condition": "OPEN_CUT",
      "fault_zone": "ZONE2",
      "severity": "ALERT",
      "zone1_voltage_v": 1.48,
      "zone2_voltage_v": 3.30,
      "zone3_voltage_v": 1.29,
      "bus_voltage_v": 3.276,
      "current_ma": 88.20,
      "power_mw": 294.00,
      "confidence": 0.98,
      "action_taken": "ALERT_SENT",
      "resolution": null,
      "resolved_at": null
    }
    // ... more events
  ]
}
```

**Endpoint**: `POST /api/events`

**Purpose**: Manually log critical events

**Request Body**:
```json
{
  "device_id": "ESP32_001",
  "condition": "CRITICAL",
  "fault_zone": "ZONE1",
  "severity": "CRITICAL",
  "action_taken": "RELAY_CUT",
  "notes": "Manual isolation triggered"
}
```

**Response**:
```json
{
  "success": true,
  "event_id": "507f1f77bcf86cd799439012"
}
```

---

### 3. Status Query

**Endpoint**: `GET /api/status`

**Purpose**: Get current system state

**Response**:
```json
{
  "success": true,
  "device_id": "ESP32_001",
  "last_heartbeat": "2026-08-17T14:25:30Z",
  "uptime_seconds": 86400,
  "overall_status": "ALERT",
  "zones": [
    {
      "zone_id": "ZONE1",
      "status": "NORMAL",
      "voltage": 1.48,
      "last_change": "2026-08-17T14:23:00Z"
    },
    {
      "zone_id": "ZONE2",
      "status": "OPEN_CUT",
      "voltage": 3.30,
      "last_change": "2026-08-17T14:23:45Z"
    },
    {
      "zone_id": "ZONE3",
      "status": "NORMAL",
      "voltage": 1.29,
      "last_change": "2026-08-17T14:23:00Z"
    }
  ],
  "bus_voltage_v": 3.276,
  "current_ma": 88.20,
  "power_mw": 294.00,
  "relay_status": "ON",
  "led_status": "YELLOW"
}
```

---

### 4. Analytics

**Endpoint**: `GET /api/analytics`

**Purpose**: Historical trends and statistics

**Query Parameters**:
```
?device_id=ESP32_001
&interval=1h              # 1h, 1d, 1w (hourly, daily, weekly)
&days=7                   # Last 7 days
```

**Response**:
```json
{
  "success": true,
  "analytics": {
    "total_events": 42,
    "critical_events": 3,
    "avg_uptime_percent": 98.5,
    "incident_rate": "1.2 per day",
    "most_faulted_zone": "ZONE2",
    "trends": [
      {
        "timestamp": "2026-08-17T00:00:00Z",
        "event_count": 5,
        "avg_current_ma": 95,
        "avg_voltage_v": 3.2,
        "faults": 2
      }
      // ... more time periods
    ]
  }
}
```

---

## Database Schema

### Telemetry Collection

```javascript
{
  _id: ObjectId,                    // MongoDB auto-generated
  timestamp: ISODate,               // When measurement was taken
  device_id: String,                // "ESP32_001"
  
  // Zone Electrical Data
  zone1_voltage_v: Number,          // 0–3.5V
  zone2_voltage_v: Number,          // 0–3.5V
  zone3_voltage_v: Number,          // 0–3.5V
  zone1_status: String,             // "NORMAL" | "OPEN_CUT" | "SHORT"
  zone2_status: String,
  zone3_status: String,
  
  // INA219 Power Sensor
  bus_voltage_v: Number,            // 3.0–3.4V typical
  current_ma: Number,               // 60–130 mA typical
  power_mw: Number,                 // 200–440 mW typical
  
  // Classification & Quality
  condition: String,                // "NORMAL" | "OPEN_CUT" | "SHORT" | "MULTI_FAULT"
  fault_zone: String,               // "NONE" | "ZONE1" | "ZONE2" | "ZONE3" | "ZONE1_ZONE2"
  severity: String,                 // "NORMAL" | "ALERT" | "CRITICAL"
  confidence: Number,               // 0.0–1.0
  data_quality: String,             // "MEASURED" | "IMPUTED_BUS_VOLTAGE"
  
  // Optional Fields
  physical_tamper: Boolean,         // Future: physical tamper detected
  tamper_score: Number,             // Future: 0–1 confidence score
  
  // Metadata
  createdAt: ISODate,
  updatedAt: ISODate
}

// Indexes for performance
db.telemetry.createIndex({ device_id: 1, timestamp: -1 });
db.telemetry.createIndex({ condition: 1, timestamp: -1 });
db.telemetry.createIndex({ timestamp: -1 }, { expireAfterSeconds: 2592000 }); // 30-day TTL
```

### Event Collection

```javascript
{
  _id: ObjectId,
  timestamp: ISODate,               // When event occurred
  device_id: String,                // "ESP32_001"
  
  // Event Details
  condition: String,                // "OPEN_CUT" | "SHORT" | "MULTI_FAULT"
  fault_zone: String,               // Affected zone(s)
  severity: String,                 // "ALERT" | "CRITICAL"
  confidence: Number,               // 0.0–1.0
  
  // Related Measurements
  zone1_voltage_v: Number,
  zone2_voltage_v: Number,
  zone3_voltage_v: Number,
  bus_voltage_v: Number,
  current_ma: Number,
  power_mw: Number,
  
  // Action Taken
  action_taken: String,             // "NONE" | "ALERT_SENT" | "RELAY_CUT"
  relay_status: String,             // "ON" | "OFF"
  
  // Resolution
  resolution: String,               // Operator notes
  resolved_at: ISODate,             // When operator resolved
  resolution_method: String,        // "AUTO" | "MANUAL" | "HARDWARE_RESET"
  
  // Metadata
  createdAt: ISODate
}

// Indexes
db.events.createIndex({ device_id: 1, timestamp: -1 });
db.events.createIndex({ severity: 1 });
db.events.createIndex({ timestamp: -1 }, { expireAfterSeconds: 7776000 }); // 90-day TTL
```

### Device Collection

```javascript
{
  _id: ObjectId,
  device_id: String,                // "ESP32_001" (unique)
  name: String,                     // "Perimeter Fence A"
  location: String,                 // "North pasture"
  
  // Configuration
  zones: [
    { zone_id: "ZONE1", name: "North section", eol_ohms: 470 },
    { zone_id: "ZONE2", name: "West section", eol_ohms: 470 },
    { zone_id: "ZONE3", name: "South section", eol_ohms: 470 }
  ],
  
  // Firmware & Hardware
  firmware_version: String,         // "1.0"
  hardware_version: String,         // "1.0-ESP32"
  last_heartbeat: ISODate,
  
  // Alerts
  alert_email: String,
  alert_phone: String,              // SMS notifications
  
  // Status
  status: String,                   // "ACTIVE" | "INACTIVE" | "ERROR"
  
  // Metadata
  createdAt: ISODate,
  updatedAt: ISODate
}

db.devices.createIndex({ device_id: 1 }, { unique: true });
```

---

## WebSocket Real-Time Updates

**Connection**: `ws://localhost:5000`

**Events Emitted**:

### Event: `telemetry_update`
Sent whenever new sensor data arrives
```json
{
  "type": "telemetry_update",
  "data": {
    "device_id": "ESP32_001",
    "zones": [
      { "zone_id": "ZONE1", "status": "NORMAL", "voltage": 1.48 },
      { "zone_id": "ZONE2", "status": "OPEN_CUT", "voltage": 3.30 },
      { "zone_id": "ZONE3", "status": "NORMAL", "voltage": 1.29 }
    ],
    "bus_voltage_v": 3.276,
    "current_ma": 88.20,
    "power_mw": 294.00,
    "timestamp": "2026-08-17T14:23:45Z"
  }
}
```

### Event: `event_alert`
Sent when critical event occurs
```json
{
  "type": "event_alert",
  "severity": "CRITICAL",
  "data": {
    "condition": "OPEN_CUT",
    "fault_zone": "ZONE2",
    "action_taken": "RELAY_CUT",
    "timestamp": "2026-08-17T14:23:45Z"
  }
}
```

### Event: `device_status`
Sent on device status change
```json
{
  "type": "device_status",
  "device_id": "ESP32_001",
  "status": "ALERT",
  "relay_status": "OFF"
}
```

---

## Environment Configuration

**File**: `.env`

```env
# Server Configuration
PORT=5000
NODE_ENV=development
HOST=0.0.0.0

# MongoDB
MONGODB_URI=mongodb://localhost:27017/fenceguard
MONGODB_POOL_SIZE=10
MONGODB_TIMEOUT=5000

# API Security (optional, basic auth)
API_KEY_ENABLED=false
API_KEY=your_api_key_here

# CORS
CORS_ORIGIN=*

# Logging
LOG_LEVEL=info
LOG_FORMAT=combined

# Telemetry
TELEMETRY_RETENTION_DAYS=30
EVENTS_RETENTION_DAYS=90

# Notifications (future)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL_FROM=fenceguard@example.com
```

---

## Starting the Backend

```bash
# Development mode (with hot reload)
npm run dev

# Production mode
npm start

# With logging
npm start -- --log-level debug
```

**Expected Startup Output**:
```
[INFO] FENCEGUARD-X Backend v1.0
[INFO] MongoDB connection pool initialized
[INFO] Express server listening on http://0.0.0.0:5000
[INFO] WebSocket server ready on ws://0.0.0.0:5000
[INFO] Event indexes created
[INFO] Telemetry indexes created
[INFO] System ready for telemetry ingestion
```

---

## Integration Checklist

- [ ] MongoDB running (local or Atlas)
- [ ] `.env` file configured with MongoDB URI
- [ ] Node.js dependencies installed (`npm install`)
- [ ] Server starts without errors (`npm start`)
- [ ] API responds to test requests (`curl http://localhost:5000/health`)
- [ ] WebSocket connection test (client connects successfully)
- [ ] POST `/api/telemetry` stores data correctly
- [ ] GET `/api/events` retrieves stored events
- [ ] Dashboard WebSocket receives live updates
- [ ] Database retention policies active (TTL indexes)

---

## Performance Considerations

| Metric | Target | Strategy |
|--------|--------|----------|
| Telemetry latency | <100ms | Async processing, indexing |
| Event query latency | <500ms | Database indexes, pagination |
| Concurrent clients | 100+ | WebSocket scaling |
| Data retention | 30d telemetry, 90d events | MongoDB TTL indexes |
| Storage size | ~500MB/year (typical) | Compression, archival |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MongoDB connection refused | Check MongoDB running, URI correct |
| Port 5000 already in use | `lsof -i :5000` to find process, or change PORT in .env |
| WebSocket connection fails | Check firewall, ensure backend running on same host |
| Telemetry not storing | Check MongoDB permissions, schema validation |
| Dashboard not updating | Check WebSocket connection, browser console errors |

---

**Last Updated**: 17 August 2026  
**Status**: 🟡 Schema ready, API skeleton in progress  
**Next Milestone**: Full API integration by 18-AUG
LOG_LEVEL=debug
```

## API Endpoints

### 1. Event Logging

#### POST `/api/v1/events` - Log Event from ESP32
```bash
curl -X POST http://localhost:5000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "sensorId": "ESP32-001",
    "timestamp": "2026-08-14T14:32:45Z",
    "eventType": "critical",
    "current": 3.15,
    "voltage": 350,
    "anomalyScore": 0.92,
    "action": "relay_cut"
  }'

# Response:
{
  "_id": "64f8a1c9d42e1234567890ab",
  "sensorId": "ESP32-001",
  "eventType": "critical",
  "createdAt": "2026-08-14T14:32:45Z"
}
```

#### GET `/api/v1/events` - Retrieve Events
```bash
# All events (paginated)
curl http://localhost:5000/api/v1/events

# Filter by sensor
curl http://localhost:5000/api/v1/events?sensorId=ESP32-001

# Filter by date range
curl "http://localhost:5000/api/v1/events?startDate=2026-08-14&endDate=2026-08-15"

# Filter by event type
curl http://localhost:5000/api/v1/events?eventType=critical

# Response:
{
  "data": [
    {
      "_id": "...",
      "sensorId": "ESP32-001",
      "eventType": "critical",
      "current": 3.15,
      "voltage": 350,
      "anomalyScore": 0.92,
      "timestamp": "2026-08-14T14:32:45Z"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 145
  }
}
```

#### GET `/api/v1/events/search` - Advanced Search
```bash
curl "http://localhost:5000/api/v1/events/search?query=tamper&sensorId=ESP32-001"

# Response: Matching events
```

### 2. Fence Status

#### GET `/api/v1/fence/status` - Current Status
```bash
curl http://localhost:5000/api/v1/fence/status

# Response:
{
  "sensorId": "ESP32-001",
  "status": "critical",
  "current": 3.15,
  "voltage": 350,
  "temperature": 28.5,
  "lastUpdate": "2026-08-14T14:32:45Z",
  "relayState": "off",
  "nextCheckIn": "2026-08-14T14:32:55Z"
}
```

### 3. Analytics

#### GET `/api/v1/analytics/dashboard` - Dashboard Metrics
```bash
curl http://localhost:5000/api/v1/analytics/dashboard?timeRange=24h

# Response:
{
  "totalEvents": 145,
  "criticalCount": 5,
  "alertCount": 18,
  "uptime": 0.98,
  "avgResponseTime": "45ms",
  "currentTrend": "stable"
}
```

#### GET `/api/v1/analytics/timeseries` - Historical Data
```bash
curl "http://localhost:5000/api/v1/analytics/timeseries?metric=current&interval=hourly&days=7"

# Response: Array of time-series points
[
  { "timestamp": "2026-08-08T00:00:00Z", "value": 1.23 },
  { "timestamp": "2026-08-08T01:00:00Z", "value": 1.25 },
  ...
]
```

### 4. Relay Control

#### POST `/api/v1/relay/reset` - Manual Reset
```bash
curl -X POST http://localhost:5000/api/v1/relay/reset \
  -H "Content-Type: application/json" \
  -d '{
    "sensorId": "ESP32-001",
    "reason": "manual_inspection_complete"
  }'

# Response:
{
  "success": true,
  "message": "Relay restore command sent to ESP32-001",
  "resetTime": "2026-08-14T14:32:50Z"
}
```

## Database Schema

### Event Collection
```javascript
db.events.insertOne({
  _id: ObjectId(...),
  sensorId: "ESP32-001",
  timestamp: ISODate("2026-08-14T14:32:45Z"),
  eventType: "critical",          // "normal", "alert", "critical"
  current: 3.15,                  // Amperes
  voltage: 350,                   // Volts
  temperature: 28.5,              // Celsius
  anomalyScore: 0.92,             // 0.0-1.0
  mlClassification: "CRITICAL",   // Model output
  action: "relay_cut",            // "none", "relay_cut", "notify"
  metadata: {
    firmwareVersion: "1.0.0",
    modelVersion: "2",
    rssi: -65                      // WiFi signal (dBm)
  },
  createdAt: ISODate("2026-08-14T14:32:45Z")
});

// Indexes for performance
db.events.createIndex({ sensorId: 1, timestamp: -1 });
db.events.createIndex({ eventType: 1 });
db.events.createIndex({ timestamp: -1 });
```

### Sensor Configuration
```javascript
db.sensors.insertOne({
  _id: ObjectId(...),
  sensorId: "ESP32-001",
  location: "North Perimeter",
  thresholds: {
    alertCurrent: 2.5,            // Amperes
    criticalCurrent: 3.0,
    minVoltage: 200,              // Volts
    maxVoltage: 400
  },
  status: "active",
  lastHeartbeat: ISODate("2026-08-14T14:32:45Z"),
  createdAt: ISODate("2026-08-14T00:00:00Z")
});
```

## MQTT Integration

### Subscribe to Events
```javascript
// In mqttService.js
mqttClient.subscribe('fence/events', (err) => {
  if (err) console.error('Failed to subscribe:', err);
  else console.log('Subscribed to fence/events');
});

mqttClient.on('message', (topic, payload) => {
  const event = JSON.parse(payload);
  
  // Save to MongoDB
  Event.create(event);
  
  // Broadcast to dashboard (WebSocket)
  io.emit('event:new', event);
  
  // Send notification if critical
  if (event.eventType === 'critical') {
    notificationService.sendAlert(event);
  }
});
```

### Publish Commands
```javascript
// Send reset command to ESP32
mqttClient.publish('fence/commands', JSON.stringify({
  command: 'relay_reset',
  sensorId: 'ESP32-001'
}));
```

## WebSocket Real-Time Updates

### Connect from Dashboard
```javascript
const socket = io('http://localhost:5000');

// Listen for new events
socket.on('event:new', (event) => {
  console.log('New event:', event);
  updateDashboard(event);
});

// Listen for status changes
socket.on('status:update', (status) => {
  updateFenceStatus(status);
});
```

### Broadcast from Backend
```javascript
// When event received
io.emit('event:new', event);
io.emit('status:update', currentStatus);
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid sensor ID",
    "details": {
      "field": "sensorId",
      "value": "invalid"
    }
  }
}
```

### Common Errors
| Code | Status | Meaning |
|------|--------|---------|
| INVALID_REQUEST | 400 | Missing or malformed data |
| UNAUTHORIZED | 401 | Missing/invalid JWT token |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Duplicate sensor ID |
| SERVER_ERROR | 500 | Internal server error |

## Authentication

### JWT Token
```bash
# Include in all requests
Authorization: Bearer <jwt_token>

# Token contains:
{
  "sensorId": "ESP32-001",
  "iat": 1692018765,
  "exp": 1692623565
}
```

## Testing

### Unit Tests
```bash
npm run test

# Output:
# PASS api/controllers/eventController.test.js
#   POST /api/v1/events
#     ✓ logs event successfully
#     ✓ rejects malformed data
#   GET /api/v1/events
#     ✓ returns events paginated
```

### Integration Tests
```bash
npm run test:integration

# Tests full request → database → response flow
```

### Manual Testing with Postman/Curl
```bash
# Create event
curl -X POST http://localhost:5000/api/v1/events \
  -H "Content-Type: application/json" \
  -d @test_event.json

# Get events
curl http://localhost:5000/api/v1/events
```

## Performance Monitoring

### Response Times
```bash
# Check average latency
npm run metrics

# Output:
# POST /api/v1/events: avg 45ms, p99 120ms
# GET /api/v1/events: avg 80ms, p99 250ms
```

### Database Indexes
```javascript
// Ensure indexes are created for common queries
db.events.createIndex({ sensorId: 1, timestamp: -1 });
db.events.createIndex({ eventType: 1 });
db.events.createIndex({ timestamp: -1 });
```

## Deployment

### Development
```bash
npm start                # Runs with nodemon (auto-reload)
```

### Production
```bash
NODE_ENV=production npm start

# Or use PM2 (process manager)
pm2 start server.js -i max
pm2 logs
```

## Next Steps

1. [Setup Dashboard](../dashboard/README.md)
2. [Configure Firmware](../firmware/README.md)
3. [Run Integration Tests](../integration-tests/)

---

**Contact**: Alok Kumar (Backend Lead)
**Last Updated**: 14 August 2026
