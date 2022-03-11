#include <Utils.h>
#include <Arduino.h>
int getDelayFromSpeed(int s)
{
    // Here we are converting ticks per second into a delay timing
    double period = 1.0 / s;
    return period * 1000000;
}

void writeMessage(String type, String message) {
    Serial.print(type);
    Serial.print(": ");
    Serial.println(message);
}

void writeInfo(String message) {
    writeMessage("INFO", message);
}

void writeError(String message) {
    writeMessage("ERROR", message);
}

void writeDebug(String message) {
    writeMessage("DEBUG", message);
}

void waitForSerialInput()
{
    while (Serial.available() == 0) {
        delay(10);
    }
}