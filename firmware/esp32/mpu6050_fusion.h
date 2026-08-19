/*
  mpu6050_fusion.h - MPU6050 6-DOF IMU Acquisition & Motion Feature Extraction
  
  Reads raw 16-bit accelerometer (AX, AY, AZ) and gyroscope (GX, GY, GZ) readings via I2C (0x68).
  Computes motion magnitudes, temporal deltas, and maintains startup baseline calibration.
  
  DESIGN PRINCIPLE:
  Does NOT use a single arbitrary magnitude threshold as the final tamper detector.
  Provides multi-axis temporal features for downstream rule-based and ML fusion.
*/

#ifndef FENCEGUARD_MPU6050_FUSION_H
#define FENCEGUARD_MPU6050_FUSION_H

#include <Wire.h>
#include <math.h>
#include "config.h"

// MPU6050 Register Addresses
#define MPU6050_REG_PWR_MGMT_1 0x6B
#define MPU6050_REG_ACCEL_XOUT_H 0x3B

struct MPU6050RawData {
  int16_t ax;
  int16_t ay;
  int16_t az;
  int16_t gx;
  int16_t gy;
  int16_t gz;
};

struct MotionFeatures {
  float accel_mag;   // Magnitude of raw 3D acceleration vector
  float gyro_mag;    // Magnitude of raw 3D angular velocity vector
  float delta_accel; // Absolute difference in accel magnitude from previous sample
  float delta_gyro;  // Absolute difference in gyro magnitude from previous sample
};

struct BaselineCalibration {
  float mean_ax;
  float mean_ay;
  float mean_az;
  float mean_accel_mag;
  float mean_gyro_mag;
  bool calibrated;
};

class MPU6050Fusion {
private:
  uint8_t i2c_addr;
  bool initialized;
  
  MPU6050RawData current_raw;
  MotionFeatures current_features;
  BaselineCalibration baseline;
  
  float prev_accel_mag;
  float prev_gyro_mag;
  
  // Rolling history for temporal persistence analysis
  float accel_history[MOTION_WINDOW_SIZE];
  float gyro_history[MOTION_WINDOW_SIZE];
  int window_index;

public:
  MPU6050Fusion(uint8_t addr = MPU6050_I2C_ADDR)
    : i2c_addr(addr), initialized(false), prev_accel_mag(0.0f), prev_gyro_mag(0.0f), window_index(0) {
    current_raw = {0, 0, 0, 0, 0, 0};
    current_features = {0.0f, 0.0f, 0.0f, 0.0f};
    baseline = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, false};
    
    for (int i = 0; i < MOTION_WINDOW_SIZE; i++) {
      accel_history[i] = 0.0f;
      gyro_history[i] = 0.0f;
    }
  }

  // Initialize MPU6050 over I2C by waking device from sleep mode
  bool begin() {
    Wire.beginTransmission(i2c_addr);
    Wire.write(MPU6050_REG_PWR_MGMT_1);
    Wire.write(0x00); // Wake up MPU6050
    uint8_t err = Wire.endTransmission();
    
    initialized = (err == 0);
    return initialized;
  }

  bool isInitialized() const {
    return initialized;
  }

  // Read 14 bytes starting at ACCEL_XOUT_H (AX, AY, AZ, Temp, GX, GY, GZ)
  bool readRawData() {
    if (!initialized) return false;
    
    Wire.beginTransmission(i2c_addr);
    Wire.write(MPU6050_REG_ACCEL_XOUT_H);
    if (Wire.endTransmission(false) != 0) return false;
    
    if (Wire.requestFrom((int)i2c_addr, 14, (int)true) != 14) return false;
    
    current_raw.ax = (Wire.read() << 8) | Wire.read();
    current_raw.ay = (Wire.read() << 8) | Wire.read();
    current_raw.az = (Wire.read() << 8) | Wire.read();
    
    // Skip internal temperature sensor reading (2 bytes)
    Wire.read(); Wire.read();
    
    current_raw.gx = (Wire.read() << 8) | Wire.read();
    current_raw.gy = (Wire.read() << 8) | Wire.read();
    current_raw.gz = (Wire.read() << 8) | Wire.read();
    
    return true;
  }

  // Perform startup baseline calibration while prototype is stationary
  bool calibrateBaseline(int samples = CALIBRATION_SAMPLES) {
    if (!initialized) return false;
    
    double sum_ax = 0, sum_ay = 0, sum_az = 0;
    double sum_accel_mag = 0, sum_gyro_mag = 0;
    int valid_samples = 0;

    for (int i = 0; i < samples; i++) {
      if (readRawData()) {
        float mag_a = sqrtf((float)current_raw.ax * current_raw.ax +
                            (float)current_raw.ay * current_raw.ay +
                            (float)current_raw.az * current_raw.az);
        float mag_g = sqrtf((float)current_raw.gx * current_raw.gx +
                            (float)current_raw.gy * current_raw.gy +
                            (float)current_raw.gz * current_raw.gz);
        
        sum_ax += current_raw.ax;
        sum_ay += current_raw.ay;
        sum_az += current_raw.az;
        sum_accel_mag += mag_a;
        sum_gyro_mag += mag_g;
        valid_samples++;
      }
      delay(20);
    }

    if (valid_samples > 0) {
      baseline.mean_ax = sum_ax / valid_samples;
      baseline.mean_ay = sum_ay / valid_samples;
      baseline.mean_az = sum_az / valid_samples;
      baseline.mean_accel_mag = sum_accel_mag / valid_samples;
      baseline.mean_gyro_mag = sum_gyro_mag / valid_samples;
      baseline.calibrated = true;
      
      prev_accel_mag = baseline.mean_accel_mag;
      prev_gyro_mag = baseline.mean_gyro_mag;
      return true;
    }
    
    return false;
  }

  // Process current raw sample, calculate derived motion features, and update window
  void updateFeatures() {
    current_features.accel_mag = sqrtf((float)current_raw.ax * current_raw.ax +
                                       (float)current_raw.ay * current_raw.ay +
                                       (float)current_raw.az * current_raw.az);
                                       
    current_features.gyro_mag = sqrtf((float)current_raw.gx * current_raw.gx +
                                      (float)current_raw.gy * current_raw.gy +
                                      (float)current_raw.gz * current_raw.gz);

    current_features.delta_accel = fabsf(current_features.accel_mag - prev_accel_mag);
    current_features.delta_gyro  = fabsf(current_features.gyro_mag - prev_gyro_mag);

    // Update rolling history
    accel_history[window_index] = current_features.accel_mag;
    gyro_history[window_index]  = current_features.gyro_mag;
    window_index = (window_index + 1) % MOTION_WINDOW_SIZE;

    // Update previous sample trackers
    prev_accel_mag = current_features.accel_mag;
    prev_gyro_mag  = current_features.gyro_mag;
  }

  // Getters
  const MPU6050RawData& getRawData() const { return current_raw; }
  const MotionFeatures& getFeatures() const { return current_features; }
  const BaselineCalibration& getBaseline() const { return baseline; }
};

#endif // FENCEGUARD_MPU6050_FUSION_H
