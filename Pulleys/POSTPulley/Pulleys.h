#include "core_esp8266_features.h"
#include <Stepper.h>
#include <math.h>

const double stepsPrRev = 2047; 
const double revsPrDM = 2; 

Stepper PulleyStepper(stepsPrRev, 14, 13, 12, 15);

void runPulleys(double preparedLength, double preparedTime, double* mem_currentLength) {
  double lenToMove = preparedLength - *mem_currentLength;

  if (lenToMove == 0){
    return;
  }

  double revAmount = revsPrDM * lenToMove;
  double stepAmount = revAmount * stepsPrRev;
  double speed = (abs(revAmount) / abs(preparedTime)) * 60;

  PulleyStepper.setSpeed(round(speed));

  int rotDirection = 1;

  if (stepAmount > 0) {
      rotDirection = 1;
    } else if (stepAmount < 0) {
      rotDirection = -1;
    } else {
      return;
  }  

  Serial.print("current length: ");
  Serial.println(*mem_currentLength);
  Serial.print("len to move: ");
  Serial.println(lenToMove);
  Serial.print("preparedLength to move: ");
  Serial.println(preparedLength);
  Serial.print("steps to move: ");
  Serial.println(stepAmount);
  Serial.println();
  
  for (int i = 0; i < abs(stepAmount); i++) {
    PulleyStepper.step(rotDirection);

    if (i % 25 == 0) {
      yield();
    }
  }
  
  *mem_currentLength = preparedLength;
  return;
}
