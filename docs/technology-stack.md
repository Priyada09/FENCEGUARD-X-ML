# Technology Stack

## Hardware

### Microcontroller
- **ESP32 (Dual-Core)**
  - CPU: 2× Xtensa 32-bit @ 240 MHz
  - RAM: 520 KB SRAM
  - Flash: 4 MB (OTA updates supported)
  - WiFi: 802.11 b/g/n (2.4 GHz)
  - Bluetooth: 4.2 (BLE)
  - GPIO: 36 programmable pins
  - ADC: 12-bit, 18 channels (1MSPS)
  - I2C: 2 controllers
  - UART: 3 controllers
  - SPI: 4 controllers
  - Watchdog Timer: Yes
  - Power: 80-160mW (active), 10µW (deep sleep)

### Sensors

| Sensor | Purpose | Interface | Accuracy | Power |
|--------|---------|-----------|----------|-------|
| **INA219** | Current measurement | I2C | ±0.5% | 1mW |
| **Voltage Divider** | Fence voltage | ADC | ±1% | <1mW |
| **DS18B20** | Temperature | 1-Wire | ±0.5°C | 5mW |
| **Reed Switch** | Tamper detection | GPIO | Digital | 0mW |

### Actuators & Output

| Device | Purpose | Power | Control |
|--------|---------|-------|---------|
| **Relay Module** | Power isolation | 5V, 1A coil | GPIO (HIGH=OFF) |
| **Passive Buzzer** | Audio alarm | 5V, 20mA | GPIO PWM |
| **LED Array** | Status indicator | 5V, 20mA each | GPIO |

### Power Management
- Input: 5V USB or external power supply
- Regulators: 3.3V linear regulator (LDO)
- Battery backup: Optional 18650 Li-ion (3.7V)
- Estimated runtime: 30+ days (WiFi disabled)

---

## Firmware

### Development Environment
```
Framework: Arduino IDE + ESP-IDF
Language: C/C++
OS: FreeRTOS (real-time kernel)
Toolchain: xtensa-esp32-elf-gcc (v11.2)
```

### Key Libraries
```
│
├─ Hardware Drivers
│  ├─ Wire.h (I2C for INA219)
│  ├─ OneWire.h (DS18B20 temperature)
│  └─ GPIO interrupts (tamper detection)
│
├─ Connectivity
│  ├─ WiFi.h (WiFi stack)
│  ├─ PubSubClient.h (MQTT client)
│  └─ HTTPClient.h (REST fallback)
│
├─ Machine Learning
│  └─ TensorFlow Lite Micro (quantized model)
│
├─ Storage
│  ├─ Preferences.h (EEPROM access)
│  └─ SPIFFS (file system for ML model)
│
└─ Utilities
   ├─ ArduinoJson.h (JSON serialization)
   ├─ time.h (NTP time sync)
   └─ FreeRTOS (task scheduling)
```

### Task Structure (FreeRTOS)
```
xTaskCreate(sensorReadTask, "Sensor", 2048, NULL, 2, NULL);
xTaskCreate(filterTask, "Filter", 2048, NULL, 2, NULL);
xTaskCreate(mlTask, "ML", 4096, NULL, 3, NULL);
xTaskCreate(relayControlTask, "Relay", 1024, NULL, 3, NULL);
xTaskCreate(wifiTask, "WiFi", 2048, NULL, 1, NULL);
xTaskCreate(mqttTask, "MQTT", 2048, NULL, 1, NULL);
```

---

## Machine Learning

### Model Training Pipeline
```
Python 3.9+

Libraries:
├─ pandas (data manipulation)
├─ numpy (numerical computation)
├─ scikit-learn (model training)
├─ tensorflow (alternative: deep learning)
├─ matplotlib / seaborn (visualization)
└─ jupyter (interactive development)
```

### Model Architecture

**Option A: Random Forest (Recommended for SIH)**
- Type: Ensemble (100 trees)
- Inputs: [I_rms, I_peak, I_variance, V_level, dI/dt, T_ambient]
- Outputs: [NORMAL, ANOMALY, CRITICAL]
- Size: ~500 KB (fits ESP32)
- Inference: ~40ms

**Option B: Neural Network (Optional)**
- Type: Dense NN (3 hidden layers)
- Layers: Input(6) → Dense(32) → Dense(16) → Dense(3)
- Framework: TensorFlow Lite Micro
- Quantization: INT8 (4-byte model)
- Size: ~200 KB
- Inference: ~30ms

### Dataset Preparation
```
├─ Normal operation samples (80%)
├─ Tamper events (10%)
├─ Anomaly cases (10%)
└─ Edge cases (synthetic augmentation)

Total samples: 10,000+
Train/Test split: 80/20
Cross-validation: 5-fold
```

### Model Conversion
```
TensorFlow (HDF5)
    ↓ tflite_converter
TFLite (.tflite)
    ↓ hexdump + embedd
.h header (byte array)
    ↓ include in firmware
ESP32 binary
```

---

## Backend

### Framework & Runtime
```
Node.js 18+ (LTS)
Express.js 4.18+ (HTTP server)
Runtime: v18.12.0+ with ES6 support
```

### Dependencies
```json
{
  "express": "^4.18.0",
  "mongoose": "^7.0.0",
  "mqtt": "^5.0.0",
  "dotenv": "^16.0.0",
  "cors": "^2.8.5",
  "compression": "^1.7.4",
  "socket.io": "^4.5.4",
  "joi": "^17.9.0",
  "bcryptjs": "^2.4.3",
  "jsonwebtoken": "^9.0.0"
}
```

### Architecture
```
backend/
├─ api/
│  ├─ routes/
│  │  ├─ events.js (event logging)
│  │  ├─ status.js (fence status)
│  │  └─ analytics.js (historical analysis)
│  ├─ controllers/
│  │  ├─ eventController.js
│  │  ├─ statusController.js
│  │  └─ analyticsController.js
│  ├─ models/
│  │  ├─ Event.js (MongoDB schema)
│  │  └─ Sensor.js (sensor configuration)
│  ├─ middleware/
│  │  ├─ auth.js (JWT validation)
│  │  └─ errorHandler.js
│  └─ services/
│     ├─ mqttService.js (subscribe to events)
│     └─ notificationService.js (email/SMS)
│
├─ database/
│  ├─ seeds/ (initial data)
│  └─ migrations/ (schema updates)
│
├─ config/
│  ├─ database.js (MongoDB connection)
│  ├─ mqtt.js (broker config)
│  └─ env.js (environment variables)
│
├─ app.js (Express app setup)
└─ server.js (entry point)
```

### Database Schema

**Event Collection**
```javascript
{
  _id: ObjectId,
  sensorId: String,       // "ESP32-001"
  timestamp: Date,
  eventType: String,      // "normal"|"alert"|"critical"
  current: Number,        // Amperes
  voltage: Number,        // Volts
  temperature: Number,    // Celsius
  anomalyScore: Number,   // 0.0-1.0
  mlClassification: String, // Model output
  action: String,         // "none"|"relay_cut"|"notify"
  metadata: {
    firmwareVersion: String,
    modelVersion: String,
    rssi: Number          // WiFi signal strength
  }
}
```

### API Endpoints

```
POST   /api/v1/events              # Log event from ESP32
GET    /api/v1/events              # Get events (paginated)
GET    /api/v1/events/search       # Search events
GET    /api/v1/fence/status        # Current status
GET    /api/v1/analytics/dashboard # Dashboard metrics
POST   /api/v1/relay/reset         # Manual relay restore
```

---

## Dashboard

### Frontend Framework
```
React 18+ (UI library)
Vite 4+ (build tool, faster than CRA)
Node.js 18+
```

### Key Libraries
```
├─ React Router (page navigation)
├─ Redux Toolkit (state management)
├─ Socket.io Client (real-time updates)
├─ Chart.js + react-chartjs-2 (graphs)
├─ Material-UI / Tailwind (styling)
├─ Axios (HTTP client)
├─ React Query (data fetching)
└─ React Toastify (notifications)
```

### Project Structure
```
dashboard/
├─ src/
│  ├─ components/
│  │  ├─ FenceStatus.jsx (main status)
│  │  ├─ EventLog.jsx (history)
│  │  ├─ Analytics.jsx (graphs)
│  │  └─ AlertPanel.jsx (notifications)
│  ├─ pages/
│  │  ├─ Dashboard.jsx
│  │  ├─ Analytics.jsx
│  │  └─ Settings.jsx
│  ├─ redux/
│  │  ├─ slices/ (state)
│  │  └─ store.js
│  ├─ services/
│  │  ├─ api.js (axios instance)
│  │  └─ websocket.js (Socket.io)
│  ├─ styles/
│  │  └─ tailwind.css
│  └─ App.jsx (root component)
├─ public/
└─ package.json
```

### Real-Time Updates
```
WebSocket (Socket.io) for live updates:
├─ fence:status (every second)
├─ event:new (on alert)
└─ connection:status (server health)
```

---

## Development Tools

### Version Control
```
Git (local)
GitHub (remote repository)
```

### CI/CD (Optional)
```
GitHub Actions for:
├─ Firmware compilation check
├─ Backend tests
├─ Dashboard build
└─ Auto-deploy to staging
```

### Testing
```
Backend:
├─ Jest (unit tests)
├─ Supertest (API tests)
└─ MongoDB Memory Server (test DB)

Frontend:
├─ Vitest (unit tests)
├─ React Testing Library (component tests)
└─ Cypress (E2E tests)

Firmware:
├─ PlatformIO Unit Testing
└─ Emulation (qemu)
```

### Monitoring & Logging
```
Backend:
├─ Winston (logging)
├─ Morgan (HTTP logging)
└─ Datadog/CloudWatch (optional)

Frontend:
├─ Sentry (error tracking)
└─ Google Analytics (usage)

Firmware:
├─ Serial logging (USB debug)
└─ MQTT debug topics
```

---

## Security Stack

### Authentication
```
├─ JWT (stateless API auth)
├─ bcrypt (password hashing)
└─ CORS (cross-origin control)
```

### Communication Security
```
├─ TLS 1.2+ (MQTT over TLS)
├─ HTTPS (API endpoints)
└─ JSON Web Tokens (API auth)
```

### Data Protection
```
├─ Mongoose schema validation
├─ Input sanitization (Joi)
└─ Rate limiting (express-rate-limit)
```

---

## Deployment Stack

### Backend Hosting
```
Option 1: Railway.app (recommended for SIH)
Option 2: AWS EC2 + RDS
Option 3: DigitalOcean + Managed DB
Option 4: Vercel Serverless (REST only)
```

### Database
```
MongoDB Atlas (cloud)
├─ Free tier: 512 MB storage
├─ Scalable to production
└─ Built-in backups
```

### Dashboard Hosting
```
Option 1: Vercel (React deployment)
Option 2: Netlify (similar)
Option 3: GitHub Pages (static)
```

### Firmware Distribution
```
├─ GitHub Releases (binary downloads)
├─ OTA updates (Over-The-Air)
└─ MQTT firmware command (update trigger)
```

---

## Development Timeline (Tech Stack)

| Week | Hardware | Firmware | ML | Backend | Dashboard |
|------|----------|----------|----|---------| ---|
| 1-2 | Sensor setup | Skeleton | Dataset | API skeleton | Mock UI |
| 3-4 | Circuit test | I2C drivers | Train model | Event API | Real data |
| 5-6 | Relay integration | Model inference | Evaluate | DB schema | Analytics |
| 7-8 | Safety testing | Full system | Deployment | Auth/security | Real-time |
| 9 | Final integration | All subsystems integrated + tested |
| 10 | Presentation & final demo |

