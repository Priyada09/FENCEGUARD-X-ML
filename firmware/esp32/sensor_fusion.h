/*
  sensor_fusion.h - Preliminary Rule-Based Multi-Sensor Fusion Layer
  
  Evaluates motion dynamics and electrical integrity to produce three distinct states:
  - motion_state      (e.g., NORMAL_STATIONARY, LIGHT_VIBRATION, PHYSICAL_TAMPER)
  - electrical_state  (e.g., NORMAL, ELECTRICAL_FAULT)
  - fusion_state      (e.g., NORMAL, ELECTRICAL_FAULT, PHYSICAL_TAMPER, BREACH)
  
  PRELIMINARY BASELINE NOTICE:
  This rule-based fusion is an interpretable baseline for real-time edge response
  prior to offline ML model training and deployment. It does NOT represent the final
  trained AI/ML model.
*/

#ifndef FENCEGUARD_SENSOR_FUSION_H
#define FENCEGUARD_SENSOR_FUSION_H

#include "config.h"
#include "zone_adc.h"
#include "mpu6050_fusion.h"

// System Output States
enum SystemFusionState {
  FUSION_STATE_NORMAL,
  FUSION_STATE_ELECTRICAL_FAULT,
  FUSION_STATE_PHYSICAL_TAMPER,
  FUSION_STATE_BREACH
};

inline const char* fusionStateToString(SystemFusionState state) {
  switch (state) {
    case FUSION_STATE_ELECTRICAL_FAULT: return "ELECTRICAL_FAULT";
    case FUSION_STATE_PHYSICAL_TAMPER:  return "PHYSICAL_TAMPER";
    case FUSION_STATE_BREACH:           return "BREACH";
    case FUSION_STATE_NORMAL:
    default:                            return "NORMAL";
  }
}

class SensorFusionEngine {
private:
  int motion_persistence_counter;

public:
  SensorFusionEngine() : motion_persistence_counter(0) {}

  // Determine physical motion state based on MPU6050 features & baseline delta
  const char* evaluateMotionState(const MotionFeatures& features) {
    if (features.delta_accel > DELTA_ACCEL_TAMPER_THRESH || features.delta_gyro > DELTA_GYRO_TAMPER_THRESH) {
      motion_persistence_counter++;
      return "PHYSICAL_TAMPER";
    } else if (features.delta_accel > DELTA_ACCEL_LIGHT_THRESH || features.delta_gyro > DELTA_GYRO_LIGHT_THRESH) {
      return "LIGHT_VIBRATION";
    } else {
      motion_persistence_counter = max(0, motion_persistence_counter - 1);
      return "NORMAL_STATIONARY";
    }
  }

  // Determine overall electrical state across the 3 monitored fence zones
  const char* evaluateElectricalState(ElectricalZoneState z1, ElectricalZoneState z2, ElectricalZoneState z3) {
    if (z1 != ZONE_STATE_NORMAL || z2 != ZONE_STATE_NORMAL || z3 != ZONE_STATE_NORMAL) {
      return "ELECTRICAL_FAULT";
    }
    return "NORMAL";
  }

  // Preliminary Rule-Based Multi-Sensor Fusion Decision Engine
  SystemFusionState evaluateFusion(ElectricalZoneState z1, 
                                   ElectricalZoneState z2, 
                                   ElectricalZoneState z3,
                                   const MotionFeatures& motion) {
    
    bool has_electrical_fault = (z1 != ZONE_STATE_NORMAL || z2 != ZONE_STATE_NORMAL || z3 != ZONE_STATE_NORMAL);
    bool has_physical_motion  = (motion.delta_accel > DELTA_ACCEL_TAMPER_THRESH || motion.delta_gyro > DELTA_GYRO_TAMPER_THRESH);
    
    // Preliminary Rule 1: Electrical fault + Physical motion simultaneously => BREACH
    if (has_electrical_fault && has_physical_motion) {
      return FUSION_STATE_BREACH;
    }
    
    // Preliminary Rule 2: Electrical fault only => ELECTRICAL_FAULT
    if (has_electrical_fault) {
      return FUSION_STATE_ELECTRICAL_FAULT;
    }
    
    // Preliminary Rule 3: Physical motion exceeding tamper threshold => PHYSICAL_TAMPER
    if (has_physical_motion) {
      return FUSION_STATE_PHYSICAL_TAMPER;
    }
    
    // Preliminary Rule 4: All normal => NORMAL
    return FUSION_STATE_NORMAL;
  }
};

#endif // FENCEGUARD_SENSOR_FUSION_H
