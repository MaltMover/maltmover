#include <AccelStepper.h>
#include "Arduino.h"
#include "ArduinoJson.h"
#include "Globals.h"
#include "Config.h"

// Overrides the set values with defaults
void revert_config() {
  stepper.setAcceleration(50);
  stepper.setSpeed(50);
  stepper.setMaxSpeed(50);
  stepper.moveTo(stepper.currentPosition());
}

void set_config(DynamicJsonDocument doc, double steps_pr_dm) {
  // Multiplies received values with steps_pr_dm, so it is steps instead of dm
  double new_acceleration = (double) doc["acceleration"] * steps_pr_dm;
  double new_speed = (double) doc["speed"] * steps_pr_dm;
  double new_length = (double) doc["length"] * steps_pr_dm;

  // Applies new values
  stepper.setAcceleration(new_acceleration);
  stepper.setMaxSpeed(new_speed);
  stepper.moveTo(new_length);
}
