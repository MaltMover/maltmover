#include <AccelStepper.h>
#include "Arduino.h"
#include "ArduinoJson.h"
#include "Globals.h"
#include "Config.h"

void revert_config() {
  stepper.setAcceleration(50);
  stepper.moveTo(stepper.currentPosition());
}

void set_config(DynamicJsonDocument doc) {
  double new_acceleration = (double) doc["acceleration"] * steps_pr_dm;
  double new_speed = (double) doc["speed"] * steps_pr_dm;
  double new_length = (double) doc["length"] * steps_pr_dm;

  stepper.setAcceleration(new_acceleration);
  stepper.setSpeed(new_speed);
  stepper.moveTo(new_length);
}
