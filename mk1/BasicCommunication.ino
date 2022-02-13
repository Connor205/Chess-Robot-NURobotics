#include <Stepper.h>

// Standard Arduino Program

const String moveCommand = "move";
const int STEPS_PER_MM = 200;
const int stepsPerRevolution = 90;
Stepper xlStepper(STEPS_PER_MM, 2, 3, 4, 5);
Stepper xrStepper(STEPS_PER_MM, 6, 7, 8, 9);
Stepper yStepper(STEPS_PER_MM, 6, 7, 8, 9);

String input1;
String input2;

void setup()
{
    Serial.begin(9600);
    Serial.println("Hello World!");
    xrStepper.setSpeed(100);
    xlStepper.setSpeed(100);
    yStepper.setSpeed(100);
}

void loop()
{
    if (Serial.available() > 0) {
        input1 = Serial.readStringUntil('\n');
        input2 = Serial.readStringUntil('\n');
        Serial.println("ACK:" + input1);
        Serial.println("ACK:" + input2);

        if (input1 == moveCommand) {
            xlStepper.move(input2.toInt());
            xrStepper.move(input2.toInt());
            yStepper.move(input2.toInt());
        }
    }
}

int getSteps(double distance) { return distance * STEPS_PER_MM; }

int move(int file, int rank)
{
    // Move Y Axis
    yStepper.step(getSteps(rank));
    // Move X Axis
    xrStepper.step(getSteps(file));
}