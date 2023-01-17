#include "Arduino.h"
#include <Stepper.h>
#include "Config.h"

void calibrate() {
  // add code to calibrate length of wire
  //delay(5000);
  Stepper CalibrateStepper(stepsPrRev, IN1, IN3, IN2, IN4);
  CalibrateStepper.setSpeed(12);
  CalibrateStepper.step(1000);
  return;
}