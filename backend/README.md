# Backend README

## Overview
FENCEGUARD-X backend provides REST APIs for event logging, fence status queries, and analytics. Built with Node.js, Express, and MongoDB.

## Quick Start

### Prerequisites
- Node.js 18+
- MongoDB (local or Atlas cloud)
- npm or yarn package manager
- Git

### Setup
```bash
# Clone backend
cd backend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and MQTT broker

# Start server
npm start

# Server runs on http://localhost:5000
```

## Backend Structure

```
backend/
├─ api/
│  ├─ routes/
│  │  ├─ events.js              # Event logging
│  │  ├─ status.js              # Fence status
│  │  └─ analytics.js           # Historical data
│  ├─ controllers/
│  │  ├─ eventController.js
│  │  ├─ statusController.js
│  │  └─ analyticsController.js
│  ├─ models/
│  │  ├─ Event.js               # Event schema
│  │  └─ Sensor.js              # Sensor config
│  ├─ middleware/
│  │  ├─ auth.js                # JWT validation
│  │  ├─ errorHandler.js        # Error handling
│  │  └─ logger.js              # Request logging
│  └─ services/
│     ├─ mqttService.js         # MQTT listener
│     └─ notificationService.js # Alerts
│
├─ database/
│  ├─ seeds/                    # Initial data
│  └─ migrations/               # Schema updates
│
├─ config/
│  ├─ database.js               # MongoDB config
│  ├─ mqtt.js                   # MQTT broker config
│  └─ env.js                    # Environment variables
│
├─ tests/
│  ├─ unit/
│  └─ integration/
│
├─ .env.example
├─ app.js                       # Express app
├─ server.js                    # Entry point
├─ package.json
└─ README.md
```

## Environment Configuration

Create `.env`:
```env
# Server
PORT=5000
NODE_ENV=development

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/fenceguard
DB_NAME=fenceguard_db

# MQTT
MQTT_BROKER=mqtt://broker.mosquitto.org
MQTT_PORT=1883
MQTT_TOPIC=fence/events

# Authentication
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRE=7d

# CORS
CORS_ORIGIN=http://localhost:3000

# Logging
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
