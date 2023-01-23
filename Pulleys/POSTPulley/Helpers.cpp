#include "Arduino.h"
#include "ArduinoJson.h"



StaticJsonDocument<512> setQuadraticConfig(DynamicJsonDocument doc) {
  StaticJsonDocument<512> quadConfig;
  quadConfig["time"] = doc["time"];
  quadConfig["a"] = doc["a"];
  quadConfig["b"] = doc["b"];
  quadConfig["c"] = doc["c"];
  return quadConfig;

}

void revertConfig(double currentLength, double* mem_preparedLength, double* mem_preparedTime) {
  // Runs if receives "run": false.
  *mem_preparedLength = currentLength;
  *mem_preparedTime = -1;

  Serial.println("Reverted config to original state \n");

}

void setConfig(double length, double time, double* mem_preparedLength, double* mem_preparedTime){

  *mem_preparedLength = length;
  *mem_preparedTime = time;

  Serial.print("Prepared length: ");
  Serial.println(*mem_preparedLength);
  Serial.print("Prepared time: ");
  Serial.println(*mem_preparedTime);
  Serial.println();

}