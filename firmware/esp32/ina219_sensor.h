/*
  ina219_sensor.h - INA219 Power & Voltage Sensor Interface
  
  Reads bus voltage, shunt current, and power over I2C (address 0x40).
  
  DATA INTEGRITY REQUIREMENT:
  Reports direct empirical readings from the INA219 hardware without synthetic
  imputation or silent modification. If a loose connection causes a 0.000V bus reading,
  the true reading is passed to telemetry to preserve raw experimental integrity.
*/

#ifndef FENCEGUARD_INA219_SENSOR_H
#define FENCEGUARD_INA219_SENSOR_H

#include <Wire.h>
#include <Adafruit_INA219.h>
#include "config.h"

class INA219Sensor {
private:
  Adafruit_INA219 ina219;
  bool initialized;

public:
  INA219Sensor() : ina219(INA219_I2C_ADDR), initialized(false) {}

  // Initialize INA219 hardware on specified I2C address
  bool begin() {
    initialized = ina219.begin();
    return initialized;
  }

  bool isInitialized() const {
    return initialized;
  }

  // Get raw bus voltage (Volts). Preserves hardware zero readings.
  float getBusVoltage_V() {
    if (!initialized) return 0.0f;
    return ina219.getBusVoltage_V();
  }

  // Get current draw in mA.
  float getCurrent_mA() {
    if (!initialized) return 0.0f;
    return ina219.getCurrent_mA();
  }

  // Get power dissipation in mW.
  float getPower_mW() {
    if (!initialized) return 0.0f;
    return ina219.getPower_mW();
  }
};

#endif // FENCEGUARD_INA219_SENSOR_H
