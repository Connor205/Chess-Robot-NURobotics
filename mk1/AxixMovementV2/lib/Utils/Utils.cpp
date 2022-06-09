#include <Arduino.h>
#include <Utils.h>
long getDelayFromSpeed(long s)
{
    // Here we are converting ticks per second into a delay timing
    // ticks / second *
    // writeInfo(String(s));
    long microseconds = 1000000 / s;
    // writeInfo(String(microseconds));
    // writeDebug("Speed: " + String(microseconds) + " Delay");
    return microseconds;
}

void writeMessage(String type, String message)
{
    Serial.print(type);
    Serial.print(":");
    Serial.println(message);
}

void writeInfo(String message) { writeMessage("INFO", message); }

void writeError(String message) { writeMessage("ERROR", message); }

void writeDebug(String message) { writeMessage("DEBUG", message); }
void writeState(String state) { writeMessage("STATE", state); }

void waitForSerialInput()
{
    while (Serial.available() == 0) {
        delay(50);
    }
}

int diameter = 12;
int radius = diameter / 2;
int circumference = diameter * 3.14159265;
int stepsPerRevolution = 400;
float mmPerStep = circumference / stepsPerRevolution;
float stepsPerMM = stepsPerRevolution / circumference;

long convertMMToSteps(long mm) { return mm * stepsPerMM; }