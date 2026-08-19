/*
  zone_adc.h - 3-Zone Electrical Voltage Acquisition & Classification
  
  Provides independent ADC reading and threshold-based classification for Zone 1,
  Zone 2, and Zone 3 of the FENCEGUARD-X safe low-voltage prototype.
*/

#ifndef FENCEGUARD_ZONE_ADC_H
#define FENCEGUARD_ZONE_ADC_H

#include "config.h"

// Electrical Zone Classification States
enum ElectricalZoneState {
  ZONE_STATE_NORMAL,
  ZONE_STATE_OPEN_CUT,
  ZONE_STATE_SHORT
};

// Helper: Convert state enum to human-readable string
inline const char* electricalZoneStateToString(ElectricalZoneState state) {
  switch (state) {
    case ZONE_STATE_SHORT:    return "SHORT";
    case ZONE_STATE_OPEN_CUT: return "OPEN/CUT";
    case ZONE_STATE_NORMAL:   
    default:                  return "NORMAL";
  }
}

// Classify a single zone voltage reading based on proven threshold logic
inline ElectricalZoneState classifyZoneVoltage(float voltage) {
  if (voltage < ZONE_SHORT_THRESHOLD_V) {
    return ZONE_STATE_SHORT;
  } else if (voltage > ZONE_OPEN_THRESHOLD_V) {
    return ZONE_STATE_OPEN_CUT;
  } else {
    return ZONE_STATE_NORMAL;
  }
}

// String wrapper for classification matching existing sketch outputs
inline const char* classifyZone(float voltage) {
  return electricalZoneStateToString(classifyZoneVoltage(voltage));
}

// Initialize ADC configuration on ESP32
inline void initZoneADC() {
  analogReadResolution(12);
  pinMode(ZONE1_ADC_PIN, INPUT);
  pinMode(ZONE2_ADC_PIN, INPUT);
  pinMode(ZONE3_ADC_PIN, INPUT);
}

// Read raw ADC and calculate voltage for Zone 1 (GPIO 34)
inline float readZone1() {
  int raw = analogRead(ZONE1_ADC_PIN);
  return (raw / ADC_MAX_RAW) * ADC_REF_VOLTAGE;
}

// Read raw ADC and calculate voltage for Zone 2 (GPIO 35)
inline float readZone2() {
  int raw = analogRead(ZONE2_ADC_PIN);
  return (raw / ADC_MAX_RAW) * ADC_REF_VOLTAGE;
}

// Read raw ADC and calculate voltage for Zone 3 (GPIO 32)
inline float readZone3() {
  int raw = analogRead(ZONE3_ADC_PIN);
  return (raw / ADC_MAX_RAW) * ADC_REF_VOLTAGE;
}

#endif // FENCEGUARD_ZONE_ADC_H
