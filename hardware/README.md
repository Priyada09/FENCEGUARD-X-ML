# Hardware README

## Overview
FENCEGUARD-X hardware consists of ESP32 microcontroller, current sensors (INA219), voltage monitoring, tamper detection, and relay-based isolation.

## Quick Start
1. Assemble components on breadboard (see [BOM](../docs/BOM.md))
2. Flash firmware (see [firmware/README.md](../firmware/README.md))
3. Run safety tests (see [testing/](testing/))
4. Deploy in weatherproof enclosure

## Folders

- **circuit/** - Schematic diagrams (KiCad/Fritzing)
- **schematics/** - Detailed circuit diagrams
- **testing/** - Hardware validation procedures
- **components.md** - Component specifications

## Key Components

| Component | Purpose | Interface |
|-----------|---------|-----------|
| ESP32 | Main controller | GPIO, I2C, ADC, SPI |
| INA219 | Current measurement | I2C |
| Voltage Divider | Fence voltage | ADC |
| Relay Module | Power isolation | GPIO, 5V coil |
| Buzzer | Audio alert | GPIO PWM |

## Safety First

⚠️ **Warning**: High-voltage fence circuits. Follow electrical safety protocols during assembly and testing.

- Use insulated tools
- Test all connections with multimeter before powering
- Never work with fence connected to power
- Wear safety gloves during assembly

## Next Steps

1. [Review System Architecture](../docs/system-architecture.md)
2. [Set up Firmware](../firmware/README.md)
3. [Run Hardware Tests](testing/)

---

**Contact**: Anup (IoT & Automation Lead)
