/*
  main.cpp - FENCEGUARD-X ESP32 Main Firmware
  
  Modular ESP32 Firmware Entry Point for Safe 3-Zone Laboratory Prototype.
  
  SAFETY NOTICE:
  This firmware is strictly designed for a SAFE LOW-VOLTAGE 3-ZONE prototype.
  Do NOT connect or use this firmware with a real high-voltage electric fence energizer.
  
  Monitors:
  - 3-Zone Electrical Integrity (GPIO 34, 35, 32)
  - INA219 Power & Current Sensor (I2C Address 0x40)
  - MPU6050 6-DOF IMU Motion Sensor (I2C Address 0x68)
*/

#include <Arduino.h>
#include <Wire.h>
#include "config.h"
#include "zone_adc.h"
#include "ina219_sensor.h"
#include "mpu6050_fusion.h"
#include "sensor_fusion.h"
#include "telemetry.h"

// Global Hardware & Engine Instances
INA219Sensor ina219;
MPU6050Fusion mpu6050(MPU6050_I2C_ADDR);
SensorFusionEngine fusion_engine;
TelemetryFormatter telemetry;

unsigned long last_telemetry_time = 0;

void setup() {
  // 1. Initialize Serial Communication
  Serial.begin(SERIAL_BAUD_RATE);
  delay(1000);
  
  Serial.println();
  Serial.println("==================================================");
  Serial.println(" FENCEGUARD-X MODULAR ESP32 FIRMWARE STARTUP");
  Serial.println(" SAFE LOW-VOLTAGE 3-ZONE PROTOTYPE");
  Serial.println("==================================================");

  // 2. Initialize Hardware I2C Bus (SDA: GPIO 21, SCL: GPIO 22)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  
  // 3. Initialize Zone ADC Inputs
  initZoneADC();
  Serial.println("[HW INIT] Zone ADC Pins (GPIO34, GPIO35, GPIO32) Initialized.");

  // 4. Initialize INA219 Sensor
  if (ina219.begin()) {
    Serial.println("[HW INIT] INA219 Power Sensor (0x40) Initialized.");
  } else {
    Serial.println("[HW WARNING] INA219 Power Sensor NOT FOUND! Proceeding with raw 0V stream.");
  }

  // 5. Initialize MPU6050 Sensor & Calibrate Stationary Baseline
  if (mpu6050.begin()) {
    Serial.println("[HW INIT] MPU6050 6-DOF IMU (0x68) Initialized.");
    Serial.println("[CALIB] Measuring stationary baseline offsets...");
    if (mpu6050.calibrateBaseline(CALIBRATION_SAMPLES)) {
      const BaselineCalibration& base = mpu6050.getBaseline();
      Serial.print("[CALIB SUCCESS] Baseline Accel Mag: "); Serial.print(base.mean_accel_mag, 1);
      Serial.print(" | Baseline Gyro Mag: "); Serial.println(base.mean_gyro_mag, 1);
    } else {
      Serial.println("[CALIB WARNING] Baseline calibration incomplete; using defaults.");
    }
  } else {
    Serial.println("[HW WARNING] MPU6050 IMU NOT FOUND! Motion telemetry will be zero.");
  }

  // 6. Print CSV Telemetry Header
  telemetry.printCSVHeader();
  last_telemetry_time = millis();
}

void loop() {
  // Non-blocking sampling timer using millis()
  unsigned long current_time = millis();
  if (current_time - last_telemetry_time < TELEMETRY_INTERVAL_MS) {
    return;
  }
  last_telemetry_time = current_time;

  // Step 1: Read all 3 Zone Voltages & Classify Zone States
  float z1_v = readZone1();
  float z2_v = readZone2();
  float z3_v = readZone3();

  ElectricalZoneState z1_state = classifyZoneVoltage(z1_v);
  ElectricalZoneState z2_state = classifyZoneVoltage(z2_v);
  ElectricalZoneState z3_state = classifyZoneVoltage(z3_v);

  // Step 2: Read INA219 Power Metrics (Preserving raw loose connection 0V readings)
  float bus_v = ina219.getBusVoltage_V();
  float current_ma = ina219.getCurrent_mA();
  float power_mw = ina219.getPower_mW();

  // Step 3: Read MPU6050 & Calculate Derived Motion Features
  if (mpu6050.isInitialized()) {
    mpu6050.readRawData();
    mpu6050.updateFeatures();
  }

  const MPU6050RawData& raw_mpu = mpu6050.getRawData();
  const MotionFeatures& features = mpu6050.getFeatures();

  // Step 4 & 5: Determine Motion State, Electrical State, and Run Fusion Decision Engine
  const char* motion_state = fusion_engine.evaluateMotionState(features);
  const char* electrical_state = fusion_engine.evaluateElectricalState(z1_state, z2_state, z3_state);
  
  SystemFusionState fusion = fusion_engine.evaluateFusion(z1_state, z2_state, z3_state, features);
  const char* fusion_state_str = fusionStateToString(fusion);

  // Step 6: Output Structured CSV Telemetry Row
  telemetry.printCSVRow(current_time,
                        z1_v, z2_v, z3_v,
                        bus_v, current_ma, power_mw,
                        raw_mpu, features,
                        motion_state, electrical_state, fusion_state_str);
}
