#include <AccelStepper.h>
#include "Arduino.h"
#include "ArduinoJson.h"
#include "Globals.h"
#include "Config.h"

void revert_config() {
  stepper.setAcceleration(50);
}

void set_config(DynamicJsonDocument doc) {
  double acceleration = (double) doc["acceleration"];
  double speed = (double) doc["speed"];
  double length = (double) doc["length"] * steps_pr_dm;

  stepper.setAcceleration(acceleration);
  stepper.setSpeed(speed);
  stepper.moveTo(length);
}