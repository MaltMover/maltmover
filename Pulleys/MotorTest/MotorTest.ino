#define IN1 14
#define IN2 12
#define IN3 13
#define IN4 15
#include <AccelStepper.h>

const int stepsPerRevolution = 200;  

AccelStepper stepper(AccelStepper::FULL4WIRE, IN1, IN2, IN3, IN4);

void setup() {
  stepper.setMaxSpeed(500);
  stepper.setSpeed(400);
  stepper.setAcceleration(100);
  Serial.begin(9600);
}

void loop() {
 
  stepper.moveTo(1000);
  run_pulleys();

  delay(5000);

  stepper.moveTo(0);
  run_pulleys();
  delay(5000);
 
}

void run_pulleys() {
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    yield();
  }
}
