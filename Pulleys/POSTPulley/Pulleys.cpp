#include "Arduino.h"
#include <AccelStepper.h>
#include <math.h>
#include "Config.h"
#include "Globals.h"

// Runs pulleys until the distance to go is 0 steps
void run_pulley() {
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    yield(); // Yields so is not blocking other functions
  }
}
