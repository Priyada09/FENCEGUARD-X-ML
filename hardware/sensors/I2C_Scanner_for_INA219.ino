/*
  I2C_Scanner_for_INA219.ino
  
  EXPERIMENTAL VALIDATION SKETCH - I2C/Sensor Discovery
  
  Purpose:
  --------
  Scan I2C bus to locate connected devices (especially INA219 power sensor).
  Validates I2C communication channel before running integrated tests.
  
  Components Used:
  ----------------
  - ESP32 I2C pins: GPIO21 (SDA), GPIO22 (SCL)
  - INA219 I2C sensor (expected at 0x40)
  - Optional: Other I2C devices on the bus
  
  What Was Tested:
  ----------------
  - I2C bus initialization and scanning
  - INA219 presence detection at standard address 0x40
  - Multiple device detection (if applicable)
  - I2C communication reliability
  
  Expected Output:
  ----------------
  Scanning I2C bus...
  I2C device found at address 0x40
  I2C scan complete.
  
  Current Status:
  ---------------
  ✅ VALIDATED
  - INA219 reliably detected at 0x40
  - I2C communication confirmed
  
  Next Step:
  ----------
  - Use Load_Detection.ino to validate power measurements
  - Proceed to CSVforZoneData.ino for integrated testing
*/

#include <Wire.h>

void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22);

  Serial.println();
  Serial.println("--------------------------------");
  Serial.println("FenceGuard-X I2C Scanner");
  Serial.println("--------------------------------");
}

void loop() {

  byte error;
  int devices = 0;

  Serial.println("Scanning I2C bus...");

  for (byte address = 1; address < 127; address++) {

    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");

      if (address < 16) {
        Serial.print("0");
      }

      Serial.println(address, HEX);

      devices++;
    }
  }

  if (devices == 0) {
    Serial.println("No I2C devices found.");
  } else {
    Serial.println("I2C scan complete.");
  }

  Serial.println("--------------------------------");
  delay(2000);
}
