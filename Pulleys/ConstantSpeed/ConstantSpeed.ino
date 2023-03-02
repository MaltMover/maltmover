#define IN1 14
#define IN2 12
#define IN3 13
#define IN4 15
#include <AccelStepper.h>

const int stepsPerRevolution = 200;  

AccelStepper stepper(AccelStepper::FULL4WIRE, IN1, IN2, IN3, IN4);

void setup()
{  
   stepper.setMaxSpeed(1000);
   stepper.setSpeed(50);	
}

void loop()
{  
   stepper.runSpeed();
}
