#include <Arduino.h>
#include <CustomAxis.h>
#include <Utils.h>

void CustomAxis::init()
{
    // Lets grab some of the inital values we care about
    current = 0;
    target = 0;
    mSpeed = 4000;
    cSpeed = 2000;
    cDelay = getDelayFromSpeed(cSpeed);
    numMotors = sizeof(stepPins) / sizeof(int) + 1;

    for (int i = 0; i < numMotors; i++) {
        // Lets set up the pins for the motors
        pinMode(stepPins[i], OUTPUT);
        pinMode(dirPins[i], OUTPUT);
    }
    if (limitSwitchPin != -1) {
        pinMode(limitSwitchPin, INPUT);
    }
    writeInfo("Created " + name + " with " + String(numMotors) + " motors");
}

bool* CustomAxis::getDirections() { return forwardDirections; }

int CustomAxis::getNumMotors() { return numMotors; }

void CustomAxis::setSpeed(int s)
{
    // Speed is given in steps per second
    cSpeed = s;
    cDelay = getDelayFromSpeed(s);
}

int CustomAxis::getSpeed() { return cSpeed; }
int CustomAxis::getDelay() { return cDelay; }
String CustomAxis::getName() { return name; }

// Sets the direction based on a boolean, if the boolean is true, the motor will move forward, if false, it will
// move backward
void CustomAxis::setDirection(bool dir)
{
    if (dir) {
        for (int i = 0; i < numMotors; i++) {
            if (forwardDirections[i]) {
                digitalWrite(dirPins[i], HIGH);
            } else {
                digitalWrite(dirPins[i], LOW);
            }
        }
    } else {
        for (int i = 0; i < numMotors; i++) {
            if (forwardDirections[i]) {
                digitalWrite(dirPins[i], LOW);
            } else {
                digitalWrite(dirPins[i], HIGH);
            }
        }
    }
    currentDirection = !currentDirection;
}

void CustomAxis::writeAllMotors(bool high)
{
    for (int i = 0; i < numMotors; i++) {
        if (high) {
            digitalWrite(stepPins[i], HIGH);
        } else {
            digitalWrite(stepPins[i], LOW);
        }
    }
}

void CustomAxis::stepAllMotors()
{
    writeAllMotors(true);
    delayMicroseconds(cDelay);
    writeAllMotors(false);
    delayMicroseconds(cDelay);
}

void CustomAxis::moveTo(int targetStep)
{
    if (targetStep < 0) {
        writeError("Target step cannot be less than 0");
        return;
    }
    writeInfo("Moving " + name + " from " + String(current) + "to " + String(targetStep));
    // We can go ahead and set the direction of the motors
    if (current > targetStep) {
        setDirection(false);
    } else {
        setDirection(true);
    }

    int stepsToMake = abs(targetStep - current);
    for (int i = 0; i < stepsToMake; i++) {
        stepAllMotors();
    };
    current = targetStep;
    writeInfo("Moved " + name + " to " + String(current));
}

int CustomAxis::getQuadraticSpeedCurve(int currentStep, int totalSteps)
{
    // Lets start with a simple quadratic expression
    // minSpeed at 0, minSpeed at totalSteps and maxSpeed at currentStep
    int minSpeed = 400;
    // Serial.println(mSpeed - ((4 * (mSpeed - minSpeed)) / (totalSteps ^ 2) * (currentStep - (totalSteps / 2)) ^
    // 2));
    return mSpeed - ((4 * (mSpeed - minSpeed)) / (totalSteps ^ 2) * (currentStep - (totalSteps / 2)) ^ 2);
}

int CustomAxis::linearSpeedCurve(int currentStep, int totalSteps)
{
    int diffFromMiddle = abs(currentStep - totalSteps / 2);
    double currentStepDouble = currentStep;
    double minSpeed = 800.0;
    return mSpeed - ((mSpeed - minSpeed) / (totalSteps / 2) * diffFromMiddle);
}

void CustomAxis::moveToAccel(int targetStep)
{
    // Here we want to do the same thing as move, but we want to accelerate and decelerate the axis over the number
    // of steps This involves turning our percentage completion into a speed Then turning that speed into a delay
    // timing

    // We can go ahead and set the direction of the motors
    if (current > targetStep) {
        setDirection(false);
    } else {
        setDirection(true);
    }

    int stepsToMake = abs(targetStep - current);
    for (int i = 0; i < stepsToMake; i++) {
        setSpeed(linearSpeedCurve(i, stepsToMake));
        stepAllMotors();
    };
    current = targetStep;
}

int CustomAxis::checkLimitSwitch()
{
    if (limitSwitchPin == -1) {
        return -1;
    }
    return digitalRead(limitSwitchPin);
}

int CustomAxis::calibrateAxis()
{

    // Check if limit pin is -1, if so return
    if (limitSwitchPin == -1) {
        return -1;
    }
    // Moves slowly toward the limit switch until the limit switch is triggered
    // Returns the number of steps it took to reach the limit switch
    int steps = 0;
    setDirection(limitSwitchDirection);
    while (checkLimitSwitch() == 0) {
        stepAllMotors();
        steps++;
    }
    // Then we can go ahead and move our motor a few steps before we set the 0 position, this means that we will not be
    // hitting the limit switch ever again unless we calibrate.

    setDirection(!limitSwitchDirection);
    for (int i = 0; i < 10, i++) {
        stepAllMotors();
        steps++;
    }
    writeInfo("Calibrated " + name + ", moved " + String(steps));
    return steps;
}
