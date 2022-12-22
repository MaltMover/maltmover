void revertConfig(double currentLength, double* mem_preparedLength, double* mem_preparedTime) {
  // Runs if recieves "run": false. 
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