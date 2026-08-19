/*
  config.h - FENCEGUARD-X Modular ESP32 Firmware Configuration
  
  SAFETY NOTICE:
  This configuration is strictly for a SAFE LOW-VOLTAGE 3-ZONE laboratory prototype.
  Do NOT connect or use this hardware/firmware with real high-voltage electric fences.
*/

#ifndef FENCEGUARD_CONFIG_H
#define FENCEGUARD_CONFIG_H

#include <Arduino.h>

// ==========================================
// HARDWARE PIN ALLOCATIONS
// ==========================================
// Zone ADC Input Pins (12-bit ADC)
#define ZONE1_ADC_PIN 34
#define ZONE2_ADC_PIN 35
#define ZONE3_ADC_PIN 32

// I2C Peripheral Pins
#define I2C_SDA_PIN 21
#define I2C_SCL_PIN 22

// Actuator & Indicator Pins
#define RELAY_CONTROL_PIN 23  // Safety isolation relay control
#define BUZZER_PIN        14  // Audible alert buzzer
#define LED_RED_PIN       25  // Critical / Alert LED
#define LED_GREEN_PIN     26  // Normal / OK LED
#define LED_YELLOW_PIN    27  // Warning / Motion LED

// ==========================================
// I2C DEVICE ADDRESSES
// ==========================================
#define INA219_I2C_ADDR  0x40  // INA219 Current/Voltage sensor
#define MPU6050_I2C_ADDR 0x68  // MPU6050 6-DOF IMU sensor

// ==========================================
// ADC & VOLTAGE CONVERSION PARAMETERS
// ==========================================
#define ADC_MAX_RAW      4095.0f // 12-bit ADC (0 - 4095)
#define ADC_REF_VOLTAGE  3.3f    // ESP32 ADC reference voltage (Volts)

// Electrical Zone Classification Thresholds (Volts)
// Voltage < 0.5V  => SHORT
// Voltage > 2.5V  => OPEN/CUT
// 0.5V <= V <= 2.5V => NORMAL
#define ZONE_SHORT_THRESHOLD_V 0.5f
#define ZONE_OPEN_THRESHOLD_V  2.5f

// ==========================================
// SYSTEM TIMING & SAMPLING
// ==========================================
#define SERIAL_BAUD_RATE      115200
#define TELEMETRY_INTERVAL_MS 500    // Sampling and telemetry output rate (millis based)
#define CALIBRATION_SAMPLES   50     // Number of samples for stationary baseline calibration

// ==========================================
// CONFIGURABLE MOTION PARAMETERS (MPU6050)
// ==========================================
// NOTE: These parameters are configurable initial heuristics for baseline motion classification.
// They are NOT scientifically validated universal tamper thresholds. Final classification belongs
// to the ML pipeline trained on experimental telemetry.
#define MOTION_WINDOW_SIZE       5     // Rolling temporal window size (samples)
#define DELTA_ACCEL_LIGHT_THRESH 500.0f  // Raw LSB delta threshold for light motion
#define DELTA_ACCEL_TAMPER_THRESH 1800.0f // Raw LSB delta threshold for physical tamper motion
#define DELTA_GYRO_LIGHT_THRESH  300.0f  // Raw LSB delta threshold for light gyro motion
#define DELTA_GYRO_TAMPER_THRESH  1000.0f // Raw LSB delta threshold for strong gyro motion

#endif // FENCEGUARD_CONFIG_H
