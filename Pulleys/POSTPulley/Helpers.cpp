#include <AccelStepper.h>
#include "Arduino.h"
#include "ArduinoJson.h"
#include "Globals.h"

void revert_config() {
  stepper.setAcceleration(50);
  Serial.println("Reverted config to original state \n");
}

void set_config(DynamicJsonDocument doc) {
  // TODO: Calculate these numbers
  double acceleration = doc["acceleration"];
  double speed = doc["speed"];
  double length = doc["length"];

  stepper.setAcceleration(acceleration);
  stepper.moveTo(length);
  stepper.setSpeed(speed);
}