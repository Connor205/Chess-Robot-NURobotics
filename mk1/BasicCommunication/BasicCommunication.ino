#include <AccelStepper.h>

// Standard Arduino Program

const String moveCommand = "move";
const int stepsPerRevolution = 90;
const double diameter = 12.0;
const double radius = diameter / 2.0;
const double pi = 3.1415925635;
const double circumfrence = pi * diameter;
const double mmPerStep = circumfrence / stepsPerRevolution;

#define stepperlxS 1
#define stepperlxD 2
AccelStepper stepperlx(AccelStepper::DRIVER, stepperlxS, stepperlxD);
#define stepperrxS 3
#define stepperrxD 4
AccelStepper stepperrx(AccelStepper::DRIVER, stepperrxS, stepperrxD);
#define stepperyS 5
#define stepperyD 6
AccelStepper steppery(AccelStepper::DRIVER, stepperyS, stepperyD);
#define stepperzS 7
#define stepperzD 8
AccelStepper stepperz(AccelStepper::DRIVER, stepperzS, stepperzD);

String input1;
String input2;

// Moves the x axis towards the front of the robot and the y axis away from the y axis motor (left to right)
int moveXYMM(int xMM, int yMM)
{
  stepperlx.moveTo(xMM / mmPerStep);
  stepperrx.moveTo(xMM / mmPerStep);
  steppery.moveTo(yMM / mmPerStep);
  while (stepperlx.distanceToGo() != 0 || stepperrx.distanceToGo() != 0 || steppery.distanceToGo() != 0) {
    stepperlx.run();
    stepperrx.run();
    steppery.run();
    Serial.println("x_pos:" + String(stepperlx.currentPosition()));
    Serial.println("y_pos:" + String(steppery.currentPosition()));
    delay(10);
  }
}

int getNextIntFromSerial()
{
  String s = Serial.readStringUntil('\n');
  return s.toInt();
}

void executeMoveCommand()
{
  digitalWrite(LED_BUILTIN, HIGH);
  int xMM = getNextIntFromSerial();
  int yMM = getNextIntFromSerial();
  moveXYMM(xMM, yMM);
  digitalWrite(LED_BUILTIN, LOW);

}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10000);
}

void loop()
{
  input1 = Serial.readStringUntil('\n');

  if (input1 == moveCommand) {
    Serial.println("Info:Performing Move Command");
    Serial.println("state:moving");
    executeMoveCommand();
  }

  Serial.println("state:ready");
  delay(100);
}
