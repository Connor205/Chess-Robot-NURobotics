#include <Arduino.h>
int getDelayFromSpeed(int s);

void writeMessage(String type, String message);

void writeInfo(String message);

void writeError(String message);

void writeDebug(String message);

void waitForSerialInput();