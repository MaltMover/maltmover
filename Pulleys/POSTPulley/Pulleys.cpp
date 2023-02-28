#include "Arduino.h"
#include <AccelStepper.h>
#include <math.h>
#include "Config.h"
#include "Globals.h"


void run_pulleys() {
  stepper.runToPosition();
}