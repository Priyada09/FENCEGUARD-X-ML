# Bill of Materials (BOM)

## Summary
| Category | Cost |
|----------|------|
| Microcontroller & Sensors | $120-150 |
| Relays & Actuators | $50-60 |
| Power & Cabling | $30-40 |
| Enclosure & Miscellaneous | $40-50 |
| **Total (per node)** | **$240-300** |

---

## Detailed Components

### Microcontroller & Development Board

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| ESP32 DevKit V1 | 1 | $8-10 | $8-10 | Dual-core, WiFi, BLE |
| **Subtotal** | | | **$8-10** | |

### Current & Voltage Sensing

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| INA219 Current Sensor Module | 1 | $3-5 | $3-5 | I2C interface, ±3.2A |
| Resistor 10kΩ (for voltage divider) | 2 | $0.05 | $0.10 | ±1% tolerance |
| Capacitor 100nF (filtering) | 3 | $0.10 | $0.30 | Ceramic, bypass |
| **Subtotal** | | | **$3.40-5.40** | |

### Temperature & Tamper Sensing

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| DS18B20 Temperature Sensor | 1 | $1-2 | $1-2 | 1-Wire protocol |
| Reed Switch (magnetic) | 1 | $0.50-1 | $0.50-1 | Tamper detection |
| Mounting magnet | 1 | $0.50 | $0.50 | For reed switch test |
| **Subtotal** | | | **$2-3.50** | |

### Relay & Power Control

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| 5V Relay Module (SPDT) | 1 | $3-4 | $3-4 | Isolation control |
| 2N2222 Transistor | 1 | $0.30 | $0.30 | Relay driver |
| 1N4007 Diode | 1 | $0.10 | $0.10 | Reverse protection |
| Resistor 10kΩ (base) | 1 | $0.05 | $0.05 | Base resistor |
| **Subtotal** | | | **$3.45-4.45** | |

### Output Devices

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| Passive Buzzer (5V) | 1 | $1-2 | $1-2 | Audio alarm |
| LED (Red) | 2 | $0.10 | $0.20 | Status indicators |
| LED (Green) | 1 | $0.10 | $0.10 | Status indicators |
| LED (Yellow) | 1 | $0.10 | $0.10 | Status indicators |
| Resistor 220Ω (LED) | 4 | $0.05 | $0.20 | Current limiting |
| LED Holders | 4 | $0.20 | $0.80 | Mounting |
| **Subtotal** | | | **$2.40-3.40** | |

### Power Supply & Regulation

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| USB 5V Power Supply (2A) | 1 | $5-7 | $5-7 | Input power |
| AMS1117-3.3V Regulator | 1 | $0.30 | $0.30 | 3.3V for ESP32 |
| Electrolytic Capacitor 10µF | 2 | $0.10 | $0.20 | Supply filtering |
| Micro USB Cable | 1 | $1 | $1 | Connection |
| **Subtotal** | | | **$6.50-8.50** | |

### Connectivity & Networking

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| WiFi (built into ESP32) | - | Included | Included | 802.11 b/g/n |
| Antenna (PCB or external) | 1 | $0-2 | $0-2 | Signal boost (optional) |
| **Subtotal** | | | **$0-2** | |

### Passive Components

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| Resistor Pack (assorted) | 1 | $2 | $2 | 100-piece pack |
| Capacitor Pack (assorted) | 1 | $2 | $2 | 50-piece pack |
| **Subtotal** | | | **$4** | |

### Cabling & Connectors

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| Jumper wires (40-piece) | 2 | $1-2 | $2-4 | Prototyping |
| Screw terminal (2-way) | 5 | $0.50 | $2.50 | Fence connection |
| Anderson PowerPole connectors | 2 | $1 | $2 | High-current connection |
| Insulated wire (22 AWG, 10m) | 1 | $3 | $3 | Cabling |
| **Subtotal** | | | **$9.50-11.50** | |

### Enclosure & Mechanical

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| Plastic project box (150×100×50mm) | 1 | $5-8 | $5-8 | Waterproof container |
| DIN rail clips | 1 | $1 | $1 | Panel mounting |
| Rubber grommet (cable entry) | 2 | $0.50 | $1 | Weatherproofing |
| Silica gel desiccant | 1 | $1 | $1 | Moisture absorption |
| Label tape & markers | - | $1 | $1 | Documentation |
| **Subtotal** | | | **$9-12** | |

### Printed Circuit Board (PCB) - Optional

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| Custom PCB (small run) | 1 | $20-50 | $20-50 | Professional vs breadboard |
| OR: Breadboard | 1 | $2 | $2 | Rapid prototyping |
| **Subtotal** | | | **$2-50** | |

### Testing & Debugging Equipment

| Item | Quantity | Unit Cost | Total | Notes |
|------|----------|-----------|-------|-------|
| Digital Multimeter | 1 | $10-20 | $10-20 | Voltage/current testing |
| USB FTDI Programmer | 1 | $5-10 | $5-10 | Serial debugging |
| Logic Analyzer (optional) | 1 | $15-30 | $0 | In BOM (shared) |
| **Subtotal** | | | **Shared** | |

---

## Procurement Strategy

### Recommended Vendors

| Component | Vendor | Lead Time |
|-----------|--------|-----------|
| ESP32, Sensors | AliExpress / Banggood | 2-3 weeks |
| Transistors, Diodes, Resistors | Local electronics shop | Same day |
| Relay Module | Amazon India | 1-2 days |
| Enclosure, Cabling | Local hardware store | Same day |
| INA219 Module | TechyGeek / Arduino India | 1-2 days |

### Cost Optimization
```
Option A: DIY Prototyping (Breadboard)
├─ Cost: $200-250 per unit
├─ Time: Slower assembly
└─ Best for: Development/testing

Option B: Soldered Prototype (Custom PCB)
├─ Cost: $280-350 per node
├─ Time: Faster assembly (batch)
└─ Best for: Field deployment

Option C: Professional Manufacturing (SMD)
├─ Cost: $150-200 per node (100+ units)
├─ Time: Mass production
└─ Best for: Commercial scale
```

---

## Alternative Components

### Current Sensor Alternatives
| Component | Range | Cost | Pros | Cons |
|-----------|-------|------|------|------|
| INA219 (chosen) | ±3.2A | $3-5 | Accurate, I2C | Fixed range |
| ACS712-5 | ±5A | $4-6 | Hall effect | Voltage output |
| Rogowski coil | Up to 200A | $20+ | Non-intrusive | Expensive |

### Microcontroller Alternatives
| Component | Cost | Pros | Cons |
|-----------|------|------|------|
| ESP32 (chosen) | $8-10 | Dual-core, WiFi, BLE | Moderate power |
| Arduino MKR WiFi | $30+ | Official support | Expensive, limited |
| Raspberry Pi Pico W | $6-8 | Cheap | No native WiFi (module needed) |

---

## Assembly Time Estimate

| Stage | Time | Notes |
|-------|------|-------|
| Component selection | 30 min | Research, ordering |
| Breadboard assembly | 1-2 hours | Solderless prototype |
| Soldering (if PCB) | 1-2 hours | Professional: 15 min |
| Firmware flashing | 15 min | Arduino IDE |
| Testing & calibration | 1-2 hours | Sensor validation |
| **Total** | **4-7 hours** | Per unit |

---

## Long-Term Supply Chain

For production at scale:
- Establish vendor agreements for bulk discounts
- Maintain safety stock (3-month supply)
- Diversify suppliers (risk mitigation)
- Plan for component obsolescence (design flexibility)

