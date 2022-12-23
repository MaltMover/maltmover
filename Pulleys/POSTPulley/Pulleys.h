#include "core_esp8266_features.h"
#include <Stepper.h>

const double stepsPrRev = 2047; 
const double revsPrDM = 2; 

Stepper PulleyStepper(stepsPrRev, 14, 13, 12, 15);

void runPulleys(double preparedLength, double preparedTime, double* mem_currentLength) {
  double lenToMove = preparedLength - *mem_currentLength;
  
  PulleyStepper.setSpeed(10);

  double revAmount = revsPrDM * lenToMove;
  double stepAmount = revAmount * stepsPrRev;

  Serial.print("current length: ");
  Serial.println(*mem_currentLength);
  Serial.print("len to move: ");
  Serial.println(lenToMove);
  Serial.print("preparedLength to move: ");
  Serial.println(preparedLength);
  Serial.print("steps to move: ");
  Serial.println(stepAmount);
  Serial.println();

  for (int i = 0; i < stepAmount; i++) {
    PulleyStepper.step(1);
    if (i % 25 == 0) {
      yield();
      delay(1);
    }
  }

  *mem_currentLength = preparedLength;
  //delay(preparedTime * 1000);
  return;
}
