#include "core_esp8266_features.h"
#include <Stepper.h>
#include <math.h>

const double stepsPrRev = 2047; 
const double revsPrDM = 2; 

Stepper PulleyStepper(stepsPrRev, 14, 13, 12, 15);

void runPulleys(double preparedLength, double preparedTime, double* mem_currentLength) {
  double lenToMove = preparedLength - *mem_currentLength;
  
  

  double revAmount = revsPrDM * lenToMove;
  double stepAmount = revAmount * stepsPrRev;
  double speed = (abs(revAmount) / abs(preparedTime)) * 60;



  PulleyStepper.setSpeed(round(speed));

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
    if (stepAmount > 0) {
      PulleyStepper.step(1);
    } else if (stepAmount < 0) {
      PulleyStepper.step(-1);
    } else {
      break;
    }     

    if (i % 25 == 0) {
      yield();
      delay(1);
    }
  }
  
  

  *mem_currentLength = preparedLength;
  //delay(preparedTime * 1000);
  return;
}
