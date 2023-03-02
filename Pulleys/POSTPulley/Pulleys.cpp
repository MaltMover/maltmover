#include "Arduino.h"
#include <AccelStepper.h>
#include <math.h>
#include "Config.h"
#include "Globals.h"


void run_pulley() {
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    yield();
  }
}
