#include <AccelStepper.h>
#include "Arduino.h"
#include "Config.h"
#include "Globals.h"

#define CALISPEED 40

// Uses analog pin to read which button is pressed
int getButtonNum(int analogVal){
  if (analogVal >= 1020){
    return 0;
  }
  else if (analogVal >= 130){
    return 1;
  }
  else if (analogVal >= 80){
    return 2;
  }
  else{
    return 3;
  }
}

// Check is button actually was pressed, and not just an unstable signal
int getButtonSafe(int pinNum){
  int buttonNum = getButtonNum(analogRead(pinNum));
  Serial.print("Button: ");
  Serial.println(buttonNum);
  if (buttonNum == 0){
    return 0;
  }
  delay(300);  // Wait because unstable signal
  if (getButtonNum(analogRead(pinNum)) == buttonNum){
    // Make sure same button is still pressed
    return buttonNum;
  }
  return 0;
}

// Overloads prev function, compares with "prevNum"
int getButtonSafe(int pinNum, int prevNum){
  int buttonNum = getButtonNum(analogRead(pinNum));
  if (buttonNum == 0){
    return 0;
  }
  if (buttonNum == prevNum){
    return buttonNum;
  }
  delay(300);  // Wait because unstable signal
  if (getButtonNum(analogRead(pinNum)) == buttonNum){
    // Make sure same button is still pressed
    return buttonNum;
  }
  return 0;
}

// Uses hall effect sensor to calibrate
// Part of it is not used, as hall effect is not stable
void finalCalibrate(){
  /*
  bool hallValue = !digitalRead(HALLEFFECT);  // Inverted output
  stepper.setSpeed(-CALISPEED);
  digitalWrite(RUNNINGLED, HIGH);
  digitalWrite(WIFILED, HIGH);
  while (!hallValue){
    stepper.runSpeed();
    hallValue = !digitalRead(HALLEFFECT);  // Inverted output
    yield();
    delayMicroseconds(100);
  }
  // Move by the offset
  stepper.move(LENGTH_OFFSET);
  stepper.setAcceleration(100);
  stepper.runToPosition();
  */

  digitalWrite(RUNNINGLED, LOW);
  digitalWrite(WIFILED, LOW);
  digitalWrite(CONFIGLED, LOW);
  stepper.setCurrentPosition(0);  // Set current position as 0
}

// Function to initially calibrate pulleys
void calibratePulley() {
  int buttonNum = 0;
  while (1){
    buttonNum = getButtonSafe(A0, buttonNum);  // Read buttons from A0
    switch (buttonNum){
      case 0:
        digitalWrite(RUNNINGLED, LOW);
        digitalWrite(WIFILED, LOW);
        break;
      case 1: // Makes length of the pulley shorter
        stepper.setSpeed(-CALISPEED);
        stepper.runSpeed();
        digitalWrite(RUNNINGLED, HIGH);  // Top led
        digitalWrite(WIFILED, LOW);
        break;
      case 2: // Moves to "finalCalibrate()" when manual calibration is done
        digitalWrite(RUNNINGLED, LOW);
        digitalWrite(WIFILED, LOW);
        delay(50);  // Make sure it was not a mistake
        if (getButtonSafe(A0) != 2){
          break;
        }
        finalCalibrate();
        return;  // Exit calibration
        break;       
      case 3: // Makes length of the pulley longer
        stepper.setSpeed(CALISPEED);
        stepper.runSpeed();
        digitalWrite(WIFILED, HIGH); // Bottom LED
        digitalWrite(RUNNINGLED, LOW);
        break;
    }
    delay(1);  // Delay for stability
    yield();   // Yields so other functions (webserver and other) can run
    bool hallValue = !digitalRead(HALLEFFECT);  // Inverted output
    digitalWrite(CONFIGLED, hallValue); // Show hall-effect value
  }
  return;
}
