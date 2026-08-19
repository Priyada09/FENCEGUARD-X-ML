/*
  telemetry.h - Structured CSV & Diagnostic Serial Output Module
  
  Formats and transmits multi-sensor telemetry over Serial.
  
  CSV TELEMETRY SCHEMA (21 fields):
  timestamp_ms,zone1_voltage,zone2_voltage,zone3_voltage,bus_voltage,current_ma,power_mw,
  ax,ay,az,gx,gy,gz,accel_mag,gyro_mag,delta_accel,delta_gyro,
  motion_state,electrical_state,fusion_state
*/

#ifndef FENCEGUARD_TELEMETRY_H
#define FENCEGUARD_TELEMETRY_H

#include <Arduino.h>
#include "config.h"
#include "zone_adc.h"
#include "mpu6050_fusion.h"
#include "sensor_fusion.h"

class TelemetryFormatter {
private:
  bool header_printed;

public:
  TelemetryFormatter() : header_printed(false) {}

  // Print standardized CSV Header row for data logging
  void printCSVHeader() {
    Serial.println("timestamp_ms,zone1_voltage,zone2_voltage,zone3_voltage,bus_voltage,current_ma,power_mw,ax,ay,az,gx,gy,gz,accel_mag,gyro_mag,delta_accel,delta_gyro,motion_state,electrical_state,fusion_state");
    header_printed = true;
  }

  // Output one structured CSV telemetry row
  void printCSVRow(unsigned long timestamp_ms,
                   float z1_v, float z2_v, float z3_v,
                   float bus_v, float current_ma, float power_mw,
                   const MPU6050RawData& raw,
                   const MotionFeatures& features,
                   const char* motion_state,
                   const char* electrical_state,
                   const char* fusion_state) {
    
    if (!header_printed) {
      printCSVHeader();
    }

    Serial.print(timestamp_ms); Serial.print(",");
    Serial.print(z1_v, 3); Serial.print(",");
    Serial.print(z2_v, 3); Serial.print(",");
    Serial.print(z3_v, 3); Serial.print(",");
    Serial.print(bus_v, 3); Serial.print(",");
    Serial.print(current_ma, 2); Serial.print(",");
    Serial.print(power_mw, 2); Serial.print(",");
    Serial.print(raw.ax); Serial.print(",");
    Serial.print(raw.ay); Serial.print(",");
    Serial.print(raw.az); Serial.print(",");
    Serial.print(raw.gx); Serial.print(",");
    Serial.print(raw.gy); Serial.print(",");
    Serial.print(raw.gz); Serial.print(",");
    Serial.print(features.accel_mag, 2); Serial.print(",");
    Serial.print(features.gyro_mag, 2); Serial.print(",");
    Serial.print(features.delta_accel, 2); Serial.print(",");
    Serial.print(features.delta_gyro, 2); Serial.print(",");
    Serial.print(motion_state); Serial.print(",");
    Serial.print(electrical_state); Serial.print(",");
    Serial.println(fusion_state);
  }

  // Print human-readable diagnostic block for debugging
  void printDiagnosticBlock(unsigned long timestamp_ms,
                            float z1_v, float z2_v, float z3_v,
                            float bus_v, float current_ma, float power_mw,
                            const MotionFeatures& features,
                            const char* motion_state,
                            const char* electrical_state,
                            const char* fusion_state) {
    Serial.println("==================================================");
    Serial.print(" [FENCEGUARD-X TELEMETRY] Time: "); Serial.print(timestamp_ms); Serial.println(" ms");
    Serial.println("--------------------------------------------------");
    Serial.print(" Zone 1: "); Serial.print(z1_v, 2); Serial.print("V ("); Serial.print(classifyZone(z1_v)); Serial.println(")");
    Serial.print(" Zone 2: "); Serial.print(z2_v, 2); Serial.print("V ("); Serial.print(classifyZone(z2_v)); Serial.println(")");
    Serial.print(" Zone 3: "); Serial.print(z3_v, 2); Serial.print("V ("); Serial.print(classifyZone(z3_v)); Serial.println(")");
    Serial.print(" INA219: "); Serial.print(bus_v, 3); Serial.print("V | "); Serial.print(current_ma, 1); Serial.print("mA | "); Serial.print(power_mw, 1); Serial.println("mW");
    Serial.print(" Motion: AccelMag="); Serial.print(features.accel_mag, 1); Serial.print(" dA="); Serial.print(features.delta_accel, 1);
    Serial.print(" | GyroMag="); Serial.print(features.gyro_mag, 1); Serial.print(" dG="); Serial.println(features.delta_gyro, 1);
    Serial.println("--------------------------------------------------");
    Serial.print(" Motion State:     "); Serial.println(motion_state);
    Serial.print(" Electrical State: "); Serial.println(electrical_state);
    Serial.print(" FUSION STATE:     "); Serial.println(fusion_state);
    Serial.println("==================================================");
  }
};

#endif // FENCEGUARD_TELEMETRY_H
