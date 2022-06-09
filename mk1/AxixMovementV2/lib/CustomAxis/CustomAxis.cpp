#include <Arduino.h>
#include <CustomAxis.h>
#include <Utils.h>

void CustomAxis::init()
{
    // Lets grab some of the inital values we care about
    current = 0;
    target = 0;
    cSpeed = 500;
    cDelay = getDelayFromSpeed(cSpeed);
    previousChangeTime = micros();
    currentlyOn = false;

    for (int i = 0; i < numMotors; i++) {
        // Lets set up the pins for the motors
        pinMode(stepPins[i], OUTPUT);
        pinMode(dirPins[i], OUTPUT);
    }
    if (limitSwitchPin != -1) {
        pinMode(limitSwitchPin, INPUT_PULLUP);
    }
    writeInfo("Created " + name + " with " + String(numMotors) + " motors");
    delay(500);
}

bool* CustomAxis::getDirections() { return forwardDirections; }

int CustomAxis::getNumMotors() { return numMotors; }

void CustomAxis::setSpeed(long s)
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
    currentDirection = dir;
    writeInfo("Set direction of " + name + " to " + String(dir));
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
    writeInfo("Moving " + name + " from " + String(current) + " to " + String(targetStep));
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

long CustomAxis::linearSpeedCurve(long currentStep, long totalSteps)
{
    int diffFromMiddle = abs(currentStep - totalSteps / 2);
    double minSpeed = 500.0;
    double maxSpeed = 4000.0;
    return maxSpeed - (((maxSpeed - minSpeed) / (totalSteps / 2)) * diffFromMiddle);
}

long CustomAxis::trapazoidalSpeedCurve(long currentStep, long totalSteps)
{
    int diffFromMiddle = abs(currentStep - totalSteps / 2);
    double minSpeed = 500.0;
    double maxSpeed = 8000.0;
    long slopedSpeed = 2 * maxSpeed - (((2 * maxSpeed - minSpeed) / (totalSteps / 2)) * diffFromMiddle);
    return min(slopedSpeed, maxSpeed);
}

void CustomAxis::moveToAccel(int targetStep)
{
    if (targetStep < 0) {
        writeError("Target step cannot be less than 0");
        return;
    }
    writeInfo("Moving " + name + " from " + String(current) + " to " + String(targetStep) + " with acceleration");
    // Here we want to do the same thing as move, but we want to accelerate and decelerate the axis over the number
    // of steps This involves turning our percentage completion into a speed Then turning that speed into a delay
    // timing

    // We can go ahead and set the direction of the motors
    if (current > targetStep) {
        setDirection(true);
    } else {
        setDirection(false);
    }

    long stepsToMake = abs(targetStep - current);
    for (long i = 0; i < stepsToMake; i++) {
        long s = trapazoidalSpeedCurve(i, stepsToMake);
        // writeInfo(String(s));
        setSpeed(s);
        stepAllMotors();
    };
    current = targetStep;
    writeInfo("Moved " + name + " to " + String(current));
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
    while (checkLimitSwitch() == 1) {
        stepAllMotors();
        steps++;
    }
    // Then we can go ahead and move our motor a few steps before we set the 0 position, this means that we will not be
    // hitting the limit switch ever again unless we calibrate.

    setDirection(!limitSwitchDirection);
    while (checkLimitSwitch() == 0) {
        stepAllMotors();
    }
    writeInfo("Calibrated " + name + ", moved " + String(steps));
    return steps;
}

void CustomAxis::update()
{
    if (current == target) {
        return;
    }
    // So this function will get called many times per second, we want to trigger steps based on the speed
    // We can keep track of the current time of the program and the last time we did a step, notably we should not have
    // any delays here
    int stepsMoved = abs(current - previous);
    int totalSteps = abs(target - previous);
    // We can go ahead and assume that the current speed is updated, then every time we finish a step we will go ahead
    // and update it
    long currentTime = micros();
    long timeSinceLastStep = currentTime - previousChangeTime;
    if (timeSinceLastStep > cDelay) {
        currentlyOn = !currentlyOn;
        writeAllMotors(currentlyOn);
        previousChangeTime = currentTime;
        long s = trapazoidalSpeedCurve(stepsMoved, totalSteps);
        setSpeed(s);
        if (!currentlyOn) // only incrementing steps on the off cycle
        {
            if (current < target) { // Then we can check which direction we are going
                current++;
            } else {
                current--;
            }
        }
    }
}

void CustomAxis::setTarget(int targetStep)
{
    // TODO:: This should probably work, but as for right now it is not needed
    if (current != target) {
        writeError("Set Target of " + name + " failed, already moving");
        return;
    }
    if (targetStep < 0) {
        writeError("Set Target of " + name + " failed, target cannot be less than 0");
        return;
    }
    // Changing previous to the current
    previous = current;
    target = targetStep;
    // Lets also set the direction here
    if (current > target) {
        setDirection(false);
    } else {
        setDirection(true);
    }
    writeInfo("Set target of " + name + " to " + String(target));
}

void CustomAxis::setRelativeMM(int mm)
{
    if (current != target) {
        writeError("Set Relative of " + name + " failed, already moving");
        return;
    }
    // Changing previous to the current
    previous = current;
    long numSteps = convertMMToSteps(mm);
    target = current + numSteps;
    // Lets also set the direction here
    if (current > target) {
        setDirection(false);
    } else {
        setDirection(true);
    }
    writeInfo("Set relative of " + name + " to " + String(target));
}

bool CustomAxis::isMoving() { return (current != target); }

bool CustomAxis::waitToStop()
{
    if (current == target) {
        return true;
    }
    while (current != target) {
        update();
    }
    return true;
}
