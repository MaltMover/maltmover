// Stepper pinout
#define IN1 14
#define IN2 12
#define IN3 13
#define IN4 15

// Offset from where the hall-effect triggers (in steps) (in steps)
#define LENGTH_OFFSET -45

// Stepper properties
const double steps_pr_dm = 128;

// Define LED's
#define WIFILED 5  // D1
#define CONFIGLED 4  // D2
#define RUNNINGLED 0 // D3

// Hall-effect sensor
#define HALLEFFECT 16  // D0
