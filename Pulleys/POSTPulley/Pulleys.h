#include "core_esp8266_features.h"
void runPulleys(double preparedLength, double preparedTime, double* mem_currentLength) {
  *mem_currentLength = preparedLength;
  delay(preparedTime * 1000);
  return;
}
