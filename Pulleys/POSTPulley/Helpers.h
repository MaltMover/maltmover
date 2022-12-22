void revertConfig(double currentLength, double* mem_preparedLength, double* mem_preparedTime) {
  // Runs if recieves "run": false. 
  *mem_preparedLength = currentLength;
  *mem_preparedTime = -1;

  Serial.println("Reverted config to original state \n");

}