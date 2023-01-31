#include <AccelStepper.h>
#include "Arduino.h"
#include "ArduinoJson.h"

void revert_config(AccelStepper pulley_stepper) {
  pulley_stepper.setAcceleration(50);
  Serial.println("Reverted config to original state \n");
}

void set_config(AccelStepper pulley_stepper, DynamicJsonDocument doc) {
  // TODO: Calculate these numbers
  double acceleration = doc["acceleration"];
  double speed = doc["speed"];
  double length = doc["length"];

  pulley_stepper.setAcceleration(acceleration);
  pulley_stepper.moveTo(length);
  pulley_stepper.setSpeed(speed);
}