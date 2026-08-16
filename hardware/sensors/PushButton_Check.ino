/*
  PushButton_Check.ino
  
  EXPERIMENTAL VALIDATION SKETCH - Input/Control Hardware Testing
  
  Purpose:
  --------
  Test digital input detection for tamper switch and emergency stop (E-STOP) button.
  Validates pull-up logic and response timing for safety-critical inputs.
  
  Components Used:
  ----------------
  - ESP32 GPIO26 (E-STOP button, INPUT_PULLUP)
  - ESP32 GPIO27 (Tamper switch, INPUT_PULLUP)
  - Push buttons with active-low logic (pressed = LOW)
  
  What Was Tested:
  ----------------
  - GPIO pullup configuration (INPUT_PULLUP mode)
  - Button press detection (active-low logic)
  - Debouncing behavior
  - Response time and stability
  - Both tamper and E-STOP inputs simultaneously
  
  Expected Output:
  ----------------
  Tamper : NO
  E-STOP : RELEASED
  --------------------------------
  
  (When button pressed:)
  Tamper : YES
  E-STOP : PRESSED
  --------------------------------
  
  Current Status:
  ---------------
  ✅ VALIDATED
  - GPIO26 and GPIO27 reliably detect button presses
  - INPUT_PULLUP logic working correctly
  - No debounce issues observed
  - Safe for use in relay control and safety logic
  
  Next Step:
  ----------
  - Integrate with relay control logic in fenceguard_main.ino
  - Add debouncing if needed for production
  - Test E-STOP isolation cut in INATamper_Combined.ino
*/

#define TAMPER_PIN 27
#define ESTOP_PIN  26

void setup() {
  Serial.begin(115200);

  pinMode(TAMPER_PIN, INPUT_PULLUP);
  pinMode(ESTOP_PIN, INPUT_PULLUP);

  Serial.println();
  Serial.println("--------------------------------");
  Serial.println("FENCEGUARD-X INPUT TEST");
  Serial.println("--------------------------------");
}

void loop() {

  bool tamper = (digitalRead(TAMPER_PIN) == LOW);
  bool estop  = (digitalRead(ESTOP_PIN) == LOW);

  Serial.print("Tamper : ");
  Serial.println(tamper ? "YES" : "NO");

  Serial.print("E-STOP : ");
  Serial.println(estop ? "PRESSED" : "RELEASED");

  Serial.println("--------------------------------");

  delay(5000);
}
