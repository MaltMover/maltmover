#include "Arduino.h"
#include <AccelStepper.h>
#include <math.h>
#include "Config.h"
#include "Globals.h"


void run_pulleys() {
  Serial.println(stepper.acceleration());
  Serial.println(stepper.speed());
  Serial.println(stepper.targetPosition());
  stepper.runToPosition();
}