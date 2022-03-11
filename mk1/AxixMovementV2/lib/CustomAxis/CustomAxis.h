#pragma once
#include <Arduino.h>

class CustomAxis {
private:
    int* stepPins;
    int* dirPins;
    bool* forwardDirections;
    int numMotors;
    bool currentDirection;
    int current;
    int target;
    int mSpeed; // max speed in ticks per second
    int cSpeed;
    int cDelay;
    String name;
    int limitSwitchPin;
    bool limitSwitchDirection;

public:
    CustomAxis(int stepPins_[], int dirPins_[], bool forwardDirections_[], String name_)
    {
        stepPins = stepPins_;
        dirPins = dirPins_;
        forwardDirections = forwardDirections_;
        name = name_;
        limitSwitchPin = -1;
        limitSwitchDirection = false;
    }

    CustomAxis(int stepPins_[], int dirPins_[], bool forwardDirections_[], String name_, int limitSwitchPin_,
        bool limitSwitchDirection_)
    {
        stepPins = stepPins_;
        dirPins = dirPins_;
        forwardDirections = forwardDirections_;
        name = name_;
        limitSwitchPin = limitSwitchPin_;
        limitSwitchDirection = limitSwitchDirection_;
    }

    void init();

    bool* getDirections();

    int getNumMotors();

    void setSpeed(int s);

    int getSpeed();
    int getDelay();
    String getName();

    // Sets the direction based on a boolean, if the boolean is true, the motor will move forward, if false, it will
    // move backward
    void setDirection(bool dir);

    void writeAllMotors(bool high);

    void stepAllMotors();

    void moveTo(int targetStep);

    int getQuadraticSpeedCurve(int currentStep, int totalSteps);

    int linearSpeedCurve(int currentStep, int totalSteps);

    void moveToAccel(int targetStep);

    int checkLimitSwitch();

    int calibrateAxis();
};