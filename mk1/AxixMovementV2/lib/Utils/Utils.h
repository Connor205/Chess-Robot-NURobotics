#include <Arduino.h>
long getDelayFromSpeed(long s);

void writeMessage(String type, String message);

void writeInfo(String message);

void writeError(String message);

void writeDebug(String message);

void writeState(String state);

void waitForSerialInput();
long convertMMToSteps(long mm);