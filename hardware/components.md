# Hardware Components & Specifications

## Overview
This document details the hardware components, circuit design, and integration guidelines for the FENCEGUARD-X system.

## Sensors

### INA219 Current Sensor
- **Measurement Range**: ±3.2A (at factory calibration)
- **Resolution**: 0.1mA steps
- **Accuracy**: ±0.5% at calibration
- **Interface**: I2C (0x40-0x4F addressable)
- **Voltage Supply**: 3.3V-5V

### Voltage Divider (Resistive)
- **Input**: Fence voltage (0-400V DC)
- **Output**: 0-3.3V (ADC range)
- **Resistors**: 100kΩ + 1kΩ (100:1 ratio)
- **Accuracy**: ±1% (with 1% tolerance resistors)

### Temperature Sensor (DS18B20)
- **Range**: -55°C to +125°C
- **Accuracy**: ±0.5°C
- **Interface**: 1-Wire protocol
- **Resolution**: 12-bit (0.0625°C)

### Tamper Sensor (Reed Switch)
- **Type**: Magnetic reed switch
- **Pull-in**: ~30 mT
- **Release**: ~20 mT
- **Response Time**: <1ms
- **Interface**: GPIO interrupt

## Actuators

### 5V Relay Module
- **Type**: SPDT (Single-Pole Double-Throw)
- **Coil Voltage**: 5V DC
- **Contact Rating**: 10A @ 250V AC / 10A @ 30V DC
- **Response Time**: ~10ms
- **Isolation**: 2kV dielectric
- **Driver**: 2N2222 NPN transistor

### Passive Buzzer
- **Frequency**: 2.5kHz
- **Voltage**: 5V DC
- **Current**: 20-30mA
- **Control**: GPIO PWM (variable pitch)

### Status LEDs
- **Red**: Critical/Alert state
- **Green**: Normal/OK state
- **Yellow**: Warning/Monitoring state
- **Voltage**: 3.3V-5V (with current-limiting resistor 220Ω)
- **Current**: 15-20mA per LED

## Enclosure & Environmental

- **Type**: IP65-rated plastic enclosure (waterproof)
- **Dimensions**: 150mm × 100mm × 50mm
- **Material**: ABS/Polycarbonate
- **Temperature Rating**: -20°C to +60°C
- **Humidity**: 0-95% non-condensing

## Assembly Notes

- All sensor modules come pre-assembled
- Solder connections should be cold-soldered for reliability
- Use heat-shrink tubing for insulation
- Apply silicone sealant at cable entry points
- Deploy in weatherproof enclosure

---

**Related Files:**
- [Bill of Materials (BOM)](BOM.md)
- [System Architecture](system-architecture.md)
